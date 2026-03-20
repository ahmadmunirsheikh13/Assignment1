"""
Job Scraper - Selenium Automation Script
Collects job listings from major career platforms and ATS systems.

Platforms:
- Greenhouse: boards.greenhouse.io (used by 500+ companies)
- Lever: jobs.lever.co (ATS by Lever Hire)  
- Ashby: jobs.ashbyhq.com (Modern ATS platform)
- Airbnb, Stripe, OpenAI career pages

Author: Ahmad Munir Sheikh
Date: March 2026
"""

import time
import pandas as pd
import logging
from typing import List, Set
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException
)
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Career pages from real companies using each platform
CAREER_URLS = [
    "https://careers.airbnb.com/positions/",
    "https://stripe.com/jobs/search",
    "https://jobs.ashbyhq.com/openai",
    "https://boards.greenhouse.io/stripe",
    "https://jobs.lever.co/spotify",
    "https://jobs.ashbyhq.com/retool",
]

# ----------------------------
# Setup Selenium Driver
# ----------------------------
def get_driver():
    """Setup Chrome WebDriver with proper options"""
    options = Options()
    options.add_argument("--headless")  # run in background
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)
    
    return driver


# ----------------------------
# Scroll Page (for dynamic sites)
# ----------------------------
def scroll_page(driver, times=5):
    """Scroll page to load dynamic content"""
    logger.info(f"  Scrolling page {times} times to load content...")
    for i in range(times):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        except Exception as e:
            logger.warning(f"  Scroll attempt {i+1} failed: {str(e)[:50]}")
            continue


# ----------------------------
# Scrape Job Links
# ----------------------------
def scrape_job_links(driver, url: str) -> List[str]:
    """
    Scrape job links from a career page
    Applies filters for job-related keywords
    """
    try:
        logger.info(f"Getting URL: {url}")
        driver.get(url)
        time.sleep(5)

        # Scroll to load dynamic content
        scroll_page(driver)

        links: Set[str] = set()

        # Find all links on page
        elements = driver.find_elements(By.TAG_NAME, "a")
        logger.info(f"  Found {len(elements)} total links")

        for el in elements:
            try:
                href = el.get_attribute("href")

                if href:
                    href_lower = href.lower()

                    # Filter job-related links
                    if any(keyword in href_lower for keyword in ["job", "position", "career", "opening", "apply"]):
                        links.add(href)
            except StaleElementReferenceException:
                continue
            except Exception as e:
                logger.debug(f"  Error processing element: {str(e)[:30]}")
                continue

        logger.info(f"  ✓ Found {len(links)} job-related links")
        return list(links)

    except TimeoutException:
        logger.error(f"  ✗ Timeout loading page: {url}")
        return []
    except Exception as e:
        logger.error(f"  ✗ Error scraping {url}: {str(e)[:100]}")
        return []


# ----------------------------
# Main Function
# ----------------------------
def main():
    """Main execution function"""
    logger.info("=" * 80)
    logger.info("JOB SCRAPING AUTOMATION STARTED")
    logger.info("=" * 80)
    
    driver = get_driver()
    all_data = []

    try:
        for url in CAREER_URLS:
            logger.info(f"\nScraping: {url}")
            
            job_links = scrape_job_links(driver, url)

            for link in job_links:
                all_data.append({
                    "source_url": url,
                    "job_url": link
                })
            
            time.sleep(2)  # Polite delay between requests

    except Exception as e:
        logger.error(f"Fatal error during scraping: {str(e)}")
    finally:
        driver.quit()
        logger.info("Browser closed")

    # Convert to DataFrame
    logger.info("\n" + "=" * 80)
    logger.info("SAVING RESULTS")
    logger.info("=" * 80)
    
    if all_data:
        df = pd.DataFrame(all_data)
        
        # Save to CSV
        output_path = "data/raw/job_links.csv"
        df.to_csv(output_path, index=False)
        
        logger.info(f"SUCCESS: Saved {len(df)} job links")
        logger.info(f"  File: {output_path}")
        logger.info(f"  Columns: {list(df.columns)}")
        
        # Show summary
        logger.info("\nSummary by Source:")
        for source in df['source_url'].unique():
            count = len(df[df['source_url'] == source])
            logger.info(f"  - {source}: {count} jobs")
    else:
        logger.warning("No job links collected")

    logger.info("\n" + "=" * 80)
    logger.info("SCRAPING COMPLETE")
    logger.info("Next: Run Scrapy spider to extract job details")
    logger.info("=" * 80 + "\n")


# ----------------------------
# Run Script
# ----------------------------
if __name__ == "__main__":
    main()

