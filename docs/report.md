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
[List of most frequently mentioned skills - to be populated after running analysis]

### Top Locations
[Cities/regions with highest job openings - to be populated after running analysis]

### Top Companies
[Companies posting the most roles - to be populated after running analysis]

### Job Types
- Internships: [count - to be populated]
- Junior Positions: [count - to be populated]

### Most Common Job Titles
[List of most common job titles - to be populated after running analysis]

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

[Summary of insights and trends in the Data Science job market - to be populated after analysis]

## Ethical Compliance

- Only scraped public, non-login pages
- Respected robots.txt and implemented delays
- No CAPTCHA bypass or authentication attempted
- All data collection was for educational purposes only