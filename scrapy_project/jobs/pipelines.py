import csv
import os

class JobsPipeline:
    def open_spider(self, spider):
        os.makedirs('../../data/final', exist_ok=True)
        self.file = open('../../data/final/jobs.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        # Write header
        self.writer.writerow([
            'job_title', 'company_name', 'location', 'department', 
            'employment_type', 'posted_date', 'job_url', 'job_description', 
            'required_skills', 'experience', 'salary'
        ])
    
    def close_spider(self, spider):
        self.file.close()
    
    def process_item(self, item, spider):
        print(f"Pipeline processing item: {item['job_title']}")
        self.writer.writerow([
            item.get('job_title', ''),
            item.get('company_name', ''),
            item.get('location', ''),
            item.get('department', ''),
            item.get('employment_type', ''),
            item.get('posted_date', ''),
            item.get('job_url', ''),
            item.get('job_description', ''),
            item.get('required_skills', ''),
            item.get('experience', ''),
            item.get('salary', '')
        ])
        return item