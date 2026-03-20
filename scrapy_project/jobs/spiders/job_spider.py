import scrapy
import csv
import json
from jobs.items import JobItem

class JobSpider(scrapy.Spider):
    name = 'job_spider'
    
    def start_requests(self):
        # Read job URLs from CSV
        with open('../../data/raw/job_links.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield scrapy.Request(url=row['job_url'], callback=self.parse_job)
    
    def parse_job(self, response):
        item = JobItem()
        item['job_url'] = response.url
        
        # Enhanced selectors for different platforms
        # Job title - try multiple selectors
        title_selectors = [
            'h1::text',
            '.job-title::text',
            '.posting-title::text',
            'h1.job-title::text',
            '.job-header h1::text'
        ]
        item['job_title'] = self.extract_first_text(response, title_selectors)
        
        # Company name
        company_selectors = [
            '.company-name::text',
            '.company::text',
            'meta[property="og:site_name"]::attr(content)',
            '.employer::text',
            '.company-info::text'
        ]
        item['company_name'] = self.extract_first_text(response, company_selectors)
        
        # Location
        location_selectors = [
            '.location::text',
            '[data-location]::text',
            '.job-location::text',
            '.location-info::text',
            '.workplace::text'
        ]
        item['location'] = self.extract_first_text(response, location_selectors)
        
        # Department
        dept_selectors = [
            '.department::text',
            '.team::text',
            '.group::text',
            '[data-department]::text'
        ]
        item['department'] = self.extract_first_text(response, dept_selectors)
        
        # Employment type
        type_selectors = [
            '.employment-type::text',
            '[data-employment-type]::text',
            '.job-type::text',
            '.commitment::text'
        ]
        item['employment_type'] = self.extract_first_text(response, type_selectors)
        
        # Posted date
        date_selectors = [
            '.posted-date::text',
            'time::attr(datetime)',
            '.date::text',
            '[data-date]::text'
        ]
        item['posted_date'] = self.extract_first_text(response, date_selectors)
        
        # Job description
        desc_selectors = [
            '.job-description',
            '.description',
            '.job-detail',
            '.posting-description'
        ]
        item['job_description'] = self.extract_description(response, desc_selectors)
        
        # Required skills
        skill_selectors = [
            '.skills li::text',
            '[data-skills] li::text',
            '.requirements li::text',
            '.qualifications li::text'
        ]
        skills = []
        for selector in skill_selectors:
            skills.extend(response.css(selector).getall())
        item['required_skills'] = ', '.join(set(skills))  # Remove duplicates
        
        # Experience (optional)
        exp_selectors = [
            '.experience::text',
            '.experience-level::text',
            '[data-experience]::text'
        ]
        item['experience'] = self.extract_first_text(response, exp_selectors)
        
        # Salary (optional)
        salary_selectors = [
            '.salary::text',
            '.compensation::text',
            '[data-salary]::text'
        ]
        item['salary'] = self.extract_first_text(response, salary_selectors)
        
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