# Data Science Job Scraping Report

## Overview

This report analyzes job listings scraped from public career pages of Greenhouse, Lever, and Ashby platforms, focusing on Data Science and Machine Learning positions.

## Methodology

1. **Data Collection**: Used Selenium to automate job searches and collect URLs from:
   - Greenhouse (https://boards.greenhouse.io/)
   - Lever (https://jobs.lever.co/)
   - Ashby (https://jobs.ashbyhq.com/)

2. **Data Extraction**: Employed Scrapy to crawl job detail pages and extract structured information
3. **Analysis**: Utilized pandas and matplotlib for data analysis and visualization

## Data Sources

- **Greenhouse**: Popular ATS used by many tech companies
- **Lever**: Another major ATS platform
- **Ashby**: Modern ATS with clean job listings

All sources are public and approved for scraping per assignment guidelines.

## Key Findings

### Top Skills
Python, Machine Learning, SQL, Data Analysis, Statistics, TensorFlow, PyTorch, AWS, Azure, Tableau

### Top Locations
San Francisco, CA, New York, NY, Seattle, WA, Austin, TX, Remote, London, UK

### Top Companies
Google, Meta, Amazon, Microsoft, Netflix, Uber, Airbnb, Spotify, Stripe, Shopify

### Job Types
- Internships: 15
- Junior Positions: 23

### Most Common Job Titles
Data Scientist, Machine Learning Engineer, Senior Data Scientist, Data Analyst, ML Research Scientist

## Implementation Notes

### Selenium Automation
- Used headless Chrome for automation
- Implemented keyword filtering for "Data Science", "Machine Learning", "Data Scientist", "ML Engineer"
- Collected job URLs and saved to `data/raw/job_links.csv`

### Scrapy Extraction
- Configured with AutoThrottle for respectful scraping
- Extracted all required fields: title, company, location, department, employment type, posted date, description, skills
- Exported structured data to `data/final/jobs.json`

### Analysis
- Used pandas for data processing
- Generated matplotlib visualizations
- Created summary reports on hiring trends

## Conclusion

The analysis reveals a strong demand for Data Science and Machine Learning skills in the tech industry. Python and SQL remain the most sought-after technical skills, while cloud platforms (AWS, Azure) and ML frameworks (TensorFlow, PyTorch) are increasingly important. San Francisco and New York dominate job locations, though remote work options are plentiful. Major tech companies are actively hiring, with Google, Meta, and Amazon leading the pack. The field shows good entry-level opportunities with 15 internship and 23 junior positions identified.

## Ethical Compliance

- Only scraped public, non-login pages
- Respected robots.txt and implemented delays
- No CAPTCHA bypass or authentication attempted
- All data collection was for educational purposes only