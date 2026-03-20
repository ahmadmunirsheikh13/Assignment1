import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

# List of career pages to scrape - using real company career pages (expanded for 100+ jobs)
CAREER_PAGES = [
    "https://boards.greenhouse.io/google",
    "https://boards.greenhouse.io/meta",
    "https://boards.greenhouse.io/microsoft",
    "https://boards.greenhouse.io/apple",
    "https://boards.greenhouse.io/amazon",
    "https://boards.greenhouse.io/netflix",
    "https://jobs.lever.co/amazon",
    "https://jobs.lever.co/netflix",
    "https://jobs.lever.co/spotify",
    "https://jobs.lever.co/uber",
    "https://jobs.lever.co/airbnb",
    "https://jobs.ashbyhq.com/stripe",
    "https://jobs.ashbyhq.com/airbnb",
    "https://jobs.ashbyhq.com/coinbase",
    "https://jobs.ashbyhq.com/shopify"
]

# Keywords to filter jobs (expanded for comprehensive collection)
KEYWORDS = [
    "Data Science", "Machine Learning", "Data Scientist", "ML Engineer",
    "Data Analyst", "AI Engineer", "Machine Learning Engineer", "Data Engineer",
    "Research Scientist", "Applied Scientist", "Principal Data Scientist",
    "Senior Data Scientist", "Lead Data Scientist", "Data Science Manager",
    "ML Research", "Deep Learning", "Computer Vision", "NLP", "Natural Language Processing"
]

def setup_driver():
    """Setup Chrome WebDriver"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service("C:/WebDriver/bin/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def search_jobs_greenhouse(driver, base_url):
    """Search jobs on Greenhouse boards"""
    job_links = []
    try:
        driver.get(base_url)
        time.sleep(5)  # Increased wait time

        # Try different search approaches
        try:
            # Look for search input
            search_selectors = [
                "input[type='search']",
                "input[name='q']",
                "input[placeholder*='search']",
                "input[placeholder*='Search']",
                "#search-bar",
                ".search-input"
            ]

            search_box = None
            for selector in search_selectors:
                try:
                    search_box = driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue

            if search_box:
                search_box.clear()
                search_box.send_keys("Data Scientist")
                search_box.send_keys(Keys.RETURN)
                time.sleep(3)
            else:
                print("No search box found, collecting all jobs")

        except Exception as e:
            print(f"Search failed: {e}, collecting all jobs")

        # Scroll multiple times to load more jobs (15-20 times for comprehensive collection)
        for i in range(20):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)  # Shorter wait time for efficiency
            print(f"Scroll {i+1}/20 completed")

        # Collect job links with multiple selectors (comprehensive collection)
        job_selectors = [
            "a[href*='/jobs/']",
            ".job-link",
            ".opening a",
            "[data-jobid] a",
            ".job-title a",
            ".posting-title a",
            ".job a",
            ".position a",
            ".career a[href*='job']",
            ".vacancy a",
            "[data-mapped='true'] a",
            ".job-posting a",
            ".requisition a"
        ]

        all_links = set()
        for selector in job_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    href = elem.get_attribute('href')
                    title = elem.text.lower()
                    if href and any(keyword.lower() in title for keyword in KEYWORDS):
                        all_links.add(href)
                        print(f"✓ Found job: {title[:50]}...")
            except Exception as e:
                print(f"Selector {selector} failed: {e}")
                continue

        job_links = list(all_links)
        print(f"Found {len(job_links)} Data Science/ML jobs on Greenhouse")

    except Exception as e:
        print(f"Error scraping Greenhouse: {e}")

    return job_links

def search_jobs_lever(driver, url):
    """Search jobs on Lever"""
    job_links = []
    try:
        driver.get(url)
        time.sleep(5)
        
        # Lever has different company pages, try to search
        try:
            search_selectors = [
                "input[type='search']",
                "input[placeholder*='search']",
                "input[name='q']"
            ]
            
            search_box = None
            for selector in search_selectors:
                try:
                    search_box = driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if search_box:
                search_box.clear()
                search_box.send_keys("Data Scientist")
                search_box.send_keys(Keys.RETURN)
                time.sleep(3)
            else:
                print("No search box found, collecting all jobs")
        
        except Exception as e:
            print(f"Search failed: {e}, collecting all jobs")
        
        # Scroll to load more (15-20 times for comprehensive collection)
        for i in range(20):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        
        # Lever job selectors (comprehensive collection)
        job_selectors = [
            "a[href*='/apply/']",
            ".job-title a",
            ".posting-title a",
            "[data-job-id] a",
            ".posting a",
            ".lever-job a",
            ".job-listing a",
            ".position a[href*='apply']",
            ".career a[href*='apply']",
            "[data-qa='posting-name'] a"
        ]
        
        all_links = set()
        for selector in job_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    href = elem.get_attribute('href')
                    title = elem.text.lower()
                    if href and any(keyword.lower() in title for keyword in KEYWORDS):
                        all_links.add(href)
            except Exception as e:
                print(f"Selector {selector} failed: {e}")
                continue
        
        job_links = list(all_links)
        print(f"Found {len(job_links)} Data Science/ML jobs on Lever")
        
    except Exception as e:
        print(f"Error scraping Lever: {e}")
    
    return job_links

def search_jobs_ashby(driver, url):
    """Search jobs on Ashby"""
    job_links = []
    try:
        driver.get(url)
        time.sleep(5)
        
        # Ashby has search functionality
        try:
            search_selectors = [
                "input[type='search']",
                "input[placeholder*='search']",
                "input[name='q']"
            ]
            
            search_box = None
            for selector in search_selectors:
                try:
                    search_box = driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if search_box:
                search_box.clear()
                search_box.send_keys("Data Scientist")
                search_box.send_keys(Keys.RETURN)
                time.sleep(3)
            else:
                print("No search box found, collecting all jobs")
        
        except Exception as e:
            print(f"Search failed: {e}, collecting all jobs")
        
        # Scroll to load more (15-20 times for comprehensive collection)
        for i in range(20):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        
        # Ashby job selectors (comprehensive collection)
        job_selectors = [
            "a[href*='/job/']",
            ".job-link",
            ".posting a",
            "[data-job] a",
            ".job-title a",
            ".ashby-job a",
            ".job-post a",
            ".career a[href*='job']",
            "[data-testid*='job'] a",
            ".position-link a"
        ]
        
        all_links = set()
        for selector in job_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    href = elem.get_attribute('href')
                    title = elem.text.lower()
                    if href and any(keyword.lower() in title for keyword in KEYWORDS):
                        all_links.add(href)
            except Exception as e:
                print(f"Selector {selector} failed: {e}")
                continue
        
        job_links = list(all_links)
        print(f"Found {len(job_links)} Data Science/ML jobs on Ashby")
        
    except Exception as e:
        print(f"Error scraping Ashby: {e}")
    
    return job_links

def main():
    driver = setup_driver()
    all_job_links = []
    
    try:
        for page in CAREER_PAGES:
            print(f"\n🔍 Scraping {page}")
            if "greenhouse" in page:
                links = search_jobs_greenhouse(driver, page)
            elif "lever" in page:
                links = search_jobs_lever(driver, page)
            elif "ashby" in page:
                links = search_jobs_ashby(driver, page)
            else:
                continue
            
            all_job_links.extend(links)
            print(f"📊 Total jobs collected so far: {len(all_job_links)}")
            time.sleep(1)  # Shorter delay for efficiency
    
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
    
    print(f"\n✅ SUCCESS: Collected {len(all_job_links)} unique Data Science/ML job links!")
    print("📁 Saved to data/raw/job_links.csv")

if __name__ == "__main__":
    main()