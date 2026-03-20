import csv
import os

class JobsPipeline:
    def open_spider(self, spider):
        """Initialize pipeline - create output directory and CSV file with headers"""
        print("\n" + "="*60)
        print("JobsPipeline: Initializing...")
        print("="*60)
        
        # Calculate path relative to project root (scrapy_project directory)
        base_dir = os.path.join(os.path.dirname(__file__), '../../data/final')
        base_dir = os.path.abspath(base_dir)
        
        os.makedirs(base_dir, exist_ok=True)
        self.output_file = os.path.join(base_dir, 'jobs.csv')
        
        print(f"Output directory: {base_dir}")
        print(f"Output file: {self.output_file}")
        
        self.file = open(self.output_file, 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        
        # Write header row
        headers = [
            'job_title', 'company_name', 'location', 'department', 
            'employment_type', 'posted_date', 'job_url', 'job_description', 
            'required_skills', 'experience', 'salary'
        ]
        self.writer.writerow(headers)
        self.file.flush()
        
        print(f"✓ CSV header written")
        print(f"✓ Pipeline ready to process items")
        print("="*60 + "\n")
        
        self.item_count = 0
    
    def close_spider(self, spider):
        """Close the pipeline - finalize CSV file"""
        self.file.close()
        print("\n" + "="*60)
        print(f"JobsPipeline: Closed")
        print(f"✓ Total items saved: {self.item_count}")
        print(f"✓ Output file: {self.output_file}")
        print("="*60 + "\n")
    
    def process_item(self, item, spider):
        """Process each scraped item - write to CSV"""
        self.item_count += 1
        print(f"\n[Item #{self.item_count}] Pipeline processing:")
        print(f"  Title: {item.get('job_title', 'N/A')}")
        print(f"  Company: {item.get('company_name', 'N/A')}")
        print(f"  Location: {item.get('location', 'N/A')}")
        
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
        
        # Flush to ensure data is written immediately
        self.file.flush()
        print(f"  ✓ Written to {self.output_file}")
        
        return item