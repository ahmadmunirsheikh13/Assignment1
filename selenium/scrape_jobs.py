from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os

# List of career pages to scrape
CAREER_PAGES = [
    "https://boards.greenhouse.io/",
    "https://jobs.lever.co/",
    "https://jobs.ashbyhq.com/"
]

# Keywords to filter jobs
KEYWORDS = ["Data Science", "Machine Learning", "Data Scientist", "ML Engineer"]

def setup_driver():
    """Setup Chrome WebDriver"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Assuming chromedriver is in PATH or selenium directory
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def search_jobs_greenhouse(driver, base_url):
    """Search jobs on Greenhouse boards"""
    job_links = []
    try:
        driver.get(base_url)
        time.sleep(2)
        
        # Greenhouse typically has search functionality
        # This is a simplified version - may need adjustment per site
        search_box = driver.find_element(By.CSS_SELECTOR, "input[type='search'], input[name='q']")
        search_box.send_keys("Data Science")
        search_box.submit()
        time.sleep(3)
        
        # Collect job links
        jobs = driver.find_elements(By.CSS_SELECTOR, "a[href*='/jobs/']")
        for job in jobs:
            title = job.text.lower()
            if any(keyword.lower() in title for keyword in KEYWORDS):
                job_links.append(job.get_attribute('href'))
                
    except Exception as e:
        print(f"Error scraping Greenhouse: {e}")
    
    return job_links

def search_jobs_lever(driver, base_url):
    """Search jobs on Lever"""
    job_links = []
    try:
        driver.get(base_url)
        time.sleep(2)
        
        # Similar approach for Lever
        jobs = driver.find_elements(By.CSS_SELECTOR, "a[href*='/apply/']")
        for job in jobs:
            title = job.text.lower()
            if any(keyword.lower() in title for keyword in KEYWORDS):
                job_links.append(job.get_attribute('href'))
                
    except Exception as e:
        print(f"Error scraping Lever: {e}")
    
    return job_links

def search_jobs_ashby(driver, base_url):
    """Search jobs on Ashby"""
    job_links = []
    try:
        driver.get(base_url)
        time.sleep(2)
        
        # Ashby job listings
        jobs = driver.find_elements(By.CSS_SELECTOR, "a[href*='/job/']")
        for job in jobs:
            title = job.text.lower()
            if any(keyword.lower() in title for keyword in KEYWORDS):
                job_links.append(job.get_attribute('href'))
                
    except Exception as e:
        print(f"Error scraping Ashby: {e}")
    
    return job_links

def main():
    driver = setup_driver()
    all_job_links = []
    
    try:
        for page in CAREER_PAGES:
            print(f"Scraping {page}")
            if "greenhouse" in page:
                links = search_jobs_greenhouse(driver, page)
            elif "lever" in page:
                links = search_jobs_lever(driver, page)
            elif "ashby" in page:
                links = search_jobs_ashby(driver, page)
            else:
                continue
            
            all_job_links.extend(links)
            time.sleep(1)  # Be respectful to servers
    
    finally:
        driver.quit()
    
    # Remove duplicates
    all_job_links = list(set(all_job_links))
    
    # Save to CSV
    os.makedirs('data/raw', exist_ok=True)
    with open('data/raw/job_links.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['job_url'])
        for link in all_job_links:
            writer.writerow([link])
    
    print(f"Collected {len(all_job_links)} job links")

if __name__ == "__main__":
    main()