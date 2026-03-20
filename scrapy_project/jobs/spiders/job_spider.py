import scrapy
import csv
import os
from jobs.items import JobItem

class JobSpider(scrapy.Spider):
    name = 'job_spider'
    
    def start_requests(self):
        # Read job URLs from CSV - use relative path from project root
        print("\n" + "="*60)
        print("Starting Job Spider - Reading job URLs from CSV...")
        print("="*60)
        
        # Construct path relative to repository root
        csv_path = os.path.join(os.path.dirname(__file__), '../../../data/raw/job_links.csv')
        csv_path = os.path.abspath(csv_path)
        
        print(f"CSV Path: {csv_path}")
        
        if not os.path.exists(csv_path):
            print(f"ERROR: CSV file not found at {csv_path}")
            return
        
        urls = []
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'job_url' in row and row['job_url'].strip():
                        urls.append(row['job_url'].strip())
            
            print(f"✓ Found {len(urls)} URLs in CSV")
            
            for idx, url in enumerate(urls, 1):
                print(f"  [{idx}] Queuing: {url}")
                yield scrapy.Request(url=url, callback=self.parse_job, errback=self.error_handler)
        except Exception as e:
            print(f"ERROR reading CSV: {e}")
    
    def error_handler(self, failure):
        """Handle request errors"""
        print(f"ERROR: Failed to fetch {failure.request.url}: {failure.value}")
    
    def parse_job(self, response):
        """Parse job posting and extract all field information"""
        print(f"\n>>> Processing URL: {response.url}")
        
        item = JobItem()
        item['job_url'] = response.url
        
        # Extract job title from page title (works for most job boards)
        title = response.css('title::text').get()
        if title:
            # Clean up title - remove company name prefix
            title = title.strip()
            if ' - ' in title:
                parts = title.split(' - ')
                if len(parts) >= 2:
                    # Usually format is "Company - Job Title" or "Job Title - Company"
                    item['job_title'] = parts[1] if len(parts[1]) > len(parts[0]) else parts[0]
                    item['company_name'] = parts[0] if len(parts[1]) > len(parts[0]) else parts[1]
                else:
                    item['job_title'] = title
            else:
                item['job_title'] = title
        else:
            item['job_title'] = 'Unknown Title'
        
        # If company not extracted from title, try other selectors
        if not item.get('company_name'):
            company_selectors = [
                'meta[property="og:site_name"]::attr(content)',
                '.company::text',
                '.employer::text',
                '[data-company]::text'
            ]
            item['company_name'] = self.extract_first_text(response, company_selectors) or 'Unknown Company'
        
        # Location - try various selectors
        location_selectors = [
            '.location::text',
            '.job-location::text',
            '.workplace::text',
            '[data-location]::text'
        ]
        item['location'] = self.extract_first_text(response, location_selectors) or 'Not specified'
        
        # Department - try various selectors
        dept_selectors = [
            '.department::text',
            '.team::text',
            '.group::text',
            '[data-department]::text'
        ]
        item['department'] = self.extract_first_text(response, dept_selectors) or 'Not specified'
        
        # Employment type
        type_selectors = [
            '.employment-type::text',
            '.job-type::text',
            '.commitment::text',
            '[data-employment-type]::text'
        ]
        item['employment_type'] = self.extract_first_text(response, type_selectors) or 'Full-time'
        
        # Posted date
        date_selectors = [
            '.posted-date::text',
            'time::attr(datetime)',
            '.date::text',
            '[data-date]::text'
        ]
        item['posted_date'] = self.extract_first_text(response, date_selectors) or 'Not specified'
        
        # Job description - try to extract from various containers
        desc_selectors = [
            '.job-description',
            '.description',
            '.job-detail',
            '.posting-description',
            '.content'
        ]
        item['job_description'] = self.extract_description(response, desc_selectors) or 'Description not available'
        
        # Required skills - look for lists or specific sections
        skill_selectors = [
            '.skills li::text',
            '.requirements li::text',
            '.qualifications li::text',
            '[data-skills] li::text'
        ]
        skills = []
        for selector in skill_selectors:
            skills.extend(response.css(selector).getall())

        parsed_skills = self.parse_skills_from_description(item['job_description'])
        if parsed_skills:
            skills.extend(parsed_skills)

        # Normalize and unique skills
        skills = [s.strip() for s in skills if s and s.strip()]
        item['required_skills'] = ', '.join(sorted(set(skills))) if skills else 'Not specified'

        # Experience
        exp_selectors = [
            '.experience::text',
            '.experience-level::text',
            '[data-experience]::text'
        ]
        item['experience'] = self.extract_first_text(response, exp_selectors) or 'Not specified'
        
        # Salary
        salary_selectors = [
            '.salary::text',
            '.compensation::text',
            '[data-salary]::text'
        ]
        item['salary'] = self.extract_first_text(response, salary_selectors) or 'Not specified'
        
        # FILTER: Only yield jobs related to "Data Science" or "Machine Learning"
        job_title_lower = item['job_title'].lower()
        job_desc_lower = item['job_description'].lower()
        skills_lower = item['required_skills'].lower()
        
        keywords = ['data science', 'machine learning', 'ml', 'data scientist', 'ml engineer']
        is_relevant = any(keyword in job_title_lower or keyword in job_desc_lower or keyword in skills_lower 
                         for keyword in keywords)
        
        if is_relevant:
            print(f"  ✓ Title: {item['job_title']}")
            print(f"  ✓ Company: {item['company_name']}")
            print(f"  ✓ Relevant job detected and will be saved")
            yield item
        else:
            print(f"  ✗ Filtered out: {item['job_title']} (not Data Science/ML related)")
    
    def extract_first_text(self, response, selectors):
        """Extract text from first matching selector"""
        for selector in selectors:
            text = response.css(selector).get()
            if text:
                return text.strip()
        return ''
    
    def extract_description(self, response, selectors):
        """Extract and clean job description"""
        desc_text = ''
        for selector in selectors:
            desc_parts = response.css(f'{selector} p::text').getall()
            if desc_parts:
                desc_text = ' '.join(desc_parts).strip()
                break
            # Fallback to direct text
            desc = response.css(f'{selector}::text').get()
            if desc:
                desc_text = desc.strip()
                break
        return desc_text

    def parse_skills_from_description(self, description):
        """Parse required skills based on keywords in the job description"""
        if not description:
            return []

        keywords = [
            'python', 'sql', 'r', 'tensorflow', 'pytorch', 'scikit-learn', 'keras',
            'spark', 'hadoop', 'airflow', 'docker', 'kubernetes', 'pandas', 'numpy',
            'matplotlib', 'seaborn', 'nlp', 'computer vision', 'aws', 'gcp', 'azure'
        ]

        found = set()
        desc_lower = description.lower()
        for key in keywords:
            if key in desc_lower:
                found.add(key)

        return list(found)

        return ''