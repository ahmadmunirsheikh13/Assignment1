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
        
        # Extract job details - selectors will vary by platform
        # These are generic selectors, may need customization per site
        
        # Job title
        item['job_title'] = response.css('h1::text').get() or response.css('.job-title::text').get()
        
        # Company name
        item['company_name'] = response.css('.company-name::text').get() or response.css('meta[property="og:site_name"]::attr(content)').get()
        
        # Location
        item['location'] = response.css('.location::text').get() or response.css('[data-location]::text').get()
        
        # Department
        item['department'] = response.css('.department::text').get()
        
        # Employment type
        item['employment_type'] = response.css('.employment-type::text').get() or response.css('[data-employment-type]::text').get()
        
        # Posted date
        item['posted_date'] = response.css('.posted-date::text').get() or response.css('time::attr(datetime)').get()
        
        # Job description
        item['job_description'] = ' '.join(response.css('.job-description p::text').getall()) or response.css('.job-description::text').get()
        
        # Required skills
        skills = response.css('.skills li::text').getall() or response.css('[data-skills] li::text').getall()
        item['required_skills'] = ', '.join(skills)
        
        # Experience (optional)
        item['experience'] = response.css('.experience::text').get()
        
        # Salary (optional)
        item['salary'] = response.css('.salary::text').get()
        
        yield item