import scrapy
import csv
import json
from jobs.items import JobItem

class JobSpider(scrapy.Spider):
    name = 'job_spider'
    
    def start_requests(self):
        # Read job URLs from CSV
        print("Starting to read job URLs from CSV...")
        with open('../data/raw/job_links.csv', 'r') as f:
            reader = csv.DictReader(f)
            urls = []
            for row in reader:
                urls.append(row['job_url'])
            print(f"Found {len(urls)} URLs in CSV")
            for url in urls[:3]:  # Print first 3 URLs
                print(f"URL: {url}")
                yield scrapy.Request(url=url, callback=self.parse_job)
    
    def parse_job(self, response):
        print(f"Processing URL: {response.url}")
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
        
        print(f"Extracted title: {item['job_title']}")
        
        # If company not extracted from title, try other selectors
        if not item.get('company_name'):
            company_selectors = [
                'meta[property="og:site_name"]::attr(content)',
                '.company::text',
                '.employer::text'
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
        item['required_skills'] = ', '.join(set(skills)) if skills else 'Not specified'
        
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
        
        print(f"Final item: title={item['job_title']}, company={item['company_name']}")
        yield item
    
    def extract_first_text(self, response, selectors):
        """Extract text from first matching selector"""
        for selector in selectors:
            text = response.css(selector).get()
            if text:
                return text.strip()
        return ''
    
    def extract_description(self, response, selectors):
        """Extract and clean job description"""
        for selector in selectors:
            desc_parts = response.css(f'{selector} p::text').getall()
            if desc_parts:
                return ' '.join(desc_parts).strip()
            # Fallback to direct text
            desc = response.css(f'{selector}::text').get()
            if desc:
                return desc.strip()
        return ''