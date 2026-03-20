"""
Job Scraper - Selenium Automation Script
Collects job listings from Greenhouse, Lever, and Ashby career pages.

Platforms:
- Greenhouse: boards.greenhouse.io (used by 500+ companies)
- Lever: jobs.lever.co (ATS by Lever Hire)  
- Ashby: jobs.ashbyhq.com (Modern ATS platform)

Author: Ahmad Munir Sheikh
Date: March 2026
"""

import os
import csv
import time
import logging
from typing import Set, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Career pages from real companies using each platform
GREENHOUSE_PAGES = [
    "https://boards.greenhouse.io/google",
    "https://boards.greenhouse.io/meta",
    "https://boards.greenhouse.io/microsoft",
    "https://boards.greenhouse.io/stripe", 
    "https://boards.greenhouse.io/epic",
]

LEVER_PAGES = [
    "https://jobs.lever.co/amazon",
    "https://jobs.lever.co/netflix",
    "https://jobs.lever.co/spotify",
    "https://jobs.lever.co/uber",
    "https://jobs.lever.co/databricks",
]

ASHBY_PAGES = [
    "https://jobs.ashbyhq.com/stripe",
    "https://jobs.ashbyhq.com/shopify",
    "https://jobs.ashbyhq.com/coinbase",
    "https://jobs.ashbyhq.com/retool",
]

def setup_chrome_driver(headless=True):
    """Setup Chrome WebDriver with proper options"""
    options = Options()
    
    if headless:
        options.add_argument("--headless")
    
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(20)
    driver.implicitly_wait(10)
    
    return driver


class GreenhouseJobScraper:
    """Scraper for Greenhouse career boards"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
    
    def scrape(self, url):
        """Scrape jobs from a Greenhouse board"""
        logger.info(f"🌿 Scraping Greenhouse: {url}")
        
        try:
            self.driver.get(url)
            time.sleep(2)
            
            # Get all job postings
            try:
                # Greenhouse typically uses this structure
                job_elements = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, ".opening, .job-post, .job-item, [data-req-id]")
                    )
                )
            except TimeoutException:
                logger.warning(f"  ⚠️ Jobs not loaded after waiting, trying scroll")
                self._scroll_to_bottom()
                job_elements = self.driver.find_elements(By.CSS_SELECTOR, ".opening, .job-post, .job-item, [data-req-id]")
            
            logger.info(f"  Found {len(job_elements)} job elements")
            
            # Extract job URLs
            job_urls = set()
            for element in job_elements:
                try:
                    # Try to find link in element
                    link = element.find_element(By.TAG_NAME, "a")
                    href = link.get_attribute("href")
                    
                    if href and href not in job_urls:
                        # Make absolute URL if not already
                        if not href.startswith("http"):
                            href = "https://boards.greenhouse.io" + href
                        
                        job_urls.add(href)
                        logger.debug(f"  ✓ Collected: {href[:80]}...")
                
                except NoSuchElementException:
                    continue
            
            logger.info(f"  ✅ Collected {len(job_urls)} unique job URLs")
            return list(job_urls)
            
        except Exception as e:
            logger.error(f"  ❌ Error scraping Greenhouse: {str(e)[:100]}")
            return []
    
    def _scroll_to_bottom(self):
        """Scroll to load all jobs"""
        for _ in range(5):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)


class LeverJobScraper:
    """Scraper for Lever job boards"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
    
    def scrape(self, url):
        """Scrape jobs from a Lever board"""
        logger.info(f"🎯 Scraping Lever: {url}")
        
        try:
            self.driver.get(url)
            time.sleep(2)
            
            # Load all jobs by scrolling
            self._scroll_to_bottom()
            
            # Lever uses posting divs or links
            job_elements = self.driver.find_elements(
                By.CSS_SELECTOR, ".posting, .posting-title, .posting-link, [data-job-id]"
            )
            
            logger.info(f"  Found {len(job_elements)} job elements")
            
            job_urls = set()
            for element in job_elements:
                try:
                    # Different approaches for Lever
                    link = element.find_element(By.TAG_NAME, "a")
                    href = link.get_attribute("href")
                    
                    if href and "lever.co" in href:
                        if href not in job_urls:
                            job_urls.add(href)
                            logger.debug(f"  ✓ Collected: {href[:80]}...")
                except:
                    continue
            
            logger.info(f"  ✅ Collected {len(job_urls)} unique job URLs")
            return list(job_urls)
            
        except Exception as e:
            logger.error(f"  ❌ Error scraping Lever: {str(e)[:100]}")
            return []
    
    def _scroll_to_bottom(self):
        """Scroll to load all jobs"""
        for _ in range(5):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)


class AshbyJobScraper:
    """Scraper for Ashby job boards"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
    
    def scrape(self, url):
        """Scrape jobs from an Ashby board"""
        logger.info(f"🏢 Scraping Ashby: {url}")
        
        try:
            self.driver.get(url)
            time.sleep(2)
            
            # Load all jobs
            self._scroll_to_bottom()
            
            # Ashby job selectors
            job_elements = self.driver.find_elements(
                By.CSS_SELECTOR, "[data-job], .job-title, .job-posting, .posting"
            )
            
            logger.info(f"  Found {len(job_elements)} job elements")
            
            job_urls = set()
            for element in job_elements:
                try:
                    # Get link from element
                    try:
                        link = element.find_element(By.TAG_NAME, "a")
                        href = link.get_attribute("href")
                    except:
                        # Element might be the link itself
                        href = element.get_attribute("href")
                    
                    if href and "ashby" in href.lower():
                        if href not in job_urls:
                            job_urls.add(href)
                            logger.debug(f"  ✓ Collected: {href[:80]}...")
                except:
                    continue
            
            logger.info(f"  ✅ Collected {len(job_urls)} unique job URLs")
            return list(job_urls)
            
        except Exception as e:
            logger.error(f"  ❌ Error scraping Ashby: {str(e)[:100]}")
            return []
    
    def _scroll_to_bottom(self):
        """Scroll to load all jobs"""
        for _ in range(5):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)


def main():
    """Main execution"""
    logger.info("=" * 80)
    logger.info("🚀 JOB SCRAPING AUTOMATION STARTED")
    logger.info("=" * 80)
    
    driver = setup_chrome_driver(headless=False)
    all_job_links = set()
    
    try:
        # ===== GREENHOUSE SCRAPING =====
        logger.info("\n📍 PHASE 1: GREENHOUSE BOARDS")
        logger.info("-" * 80)
        gh_scraper = GreenhouseJobScraper(driver)
        
        for url in GREENHOUSE_PAGES:
            links = gh_scraper.scrape(url)
            all_job_links.update(links)
            time.sleep(1)  # Polite delay
        
        logger.info(f"Greenhouse subtotal: {len(all_job_links)} unique jobs\n")
        
        # ===== LEVER SCRAPING =====
        logger.info("📍 PHASE 2: LEVER JOB BOARDS")
        logger.info("-" * 80)
        lever_scraper = LeverJobScraper(driver)
        
        for url in LEVER_PAGES:
            links = lever_scraper.scrape(url)
            all_job_links.update(links)
            time.sleep(1)  # Polite delay
        
        logger.info(f"Total after Lever: {len(all_job_links)} unique jobs\n")
        
        # ===== ASHBY SCRAPING =====
        logger.info("📍 PHASE 3: ASHBY JOB BOARDS")
        logger.info("-" * 80)
        ashby_scraper = AshbyJobScraper(driver)
        
        for url in ASHBY_PAGES:
            links = ashby_scraper.scrape(url)
            all_job_links.update(links)
            time.sleep(1)  # Polite delay
        
        logger.info(f"Grand total: {len(all_job_links)} unique jobs\n")
        
    except Exception as e:
        logger.error(f"❌ Fatal error during scraping: {e}")
    finally:
        driver.quit()
        logger.info("Browser closed")
    
    # ===== SAVE RESULTS =====
    logger.info("\n" + "=" * 80)
    logger.info("💾 SAVING RESULTS")
    logger.info("=" * 80)
    
    all_job_links = list(all_job_links)
    
    # Create directory if needed
    os.makedirs("data/raw", exist_ok=True)
    
    # Write to CSV
    csv_path = "data/raw/job_links.csv"
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['job_url'])
            for link in all_job_links:
                writer.writerow([link])
        
        file_size_kb = os.path.getsize(csv_path) / 1024
        logger.info(f"✅ SUCCESS: Saved {len(all_job_links)} job URLs")
        logger.info(f"   File: {csv_path}")
        logger.info(f"   Size: {file_size_kb:.1f} KB")
        
    except Exception as e:
        logger.error(f"❌ Error saving CSV: {e}")
    
    logger.info("\n" + "=" * 80)
    logger.info("✨ SCRAPING COMPLETE")
    logger.info(f"   Unique job URLs: {len(all_job_links)}")
    logger.info(f"   Next: Run Scrapy spider to extract job details")
    logger.info("=" * 80 + "\n")


if __name__ == "__main__":
    main()
