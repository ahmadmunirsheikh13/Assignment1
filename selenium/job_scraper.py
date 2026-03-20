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
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    # Use WebDriverManager to automatically manage ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def search_jobs_greenhouse(driver, url):
    """Search jobs on Greenhouse boards"""
    job_links = []
    try:
        print(f"Visiting Greenhouse page: {url}")
        driver.get(url)
        time.sleep(3)

        # Wait for page to load and try to find job listings
        try:
            # First, let's see what we can find on the page
            print("Looking for job listings...")

            # Try multiple approaches to find jobs
            job_elements = []

            # Method 1: Look for common Greenhouse job selectors
            selectors_to_try = [
                ".job-post, .opening",
                "[data-jobid]",
                ".job-link",
                ".posting",
                ".job-title",
                "a[href*='/jobs/']",
                ".career a",
                ".position"
            ]

            for selector in selectors_to_try:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"Found {len(elements)} elements with selector '{selector}'")
                        job_elements.extend(elements)
                except:
                    continue

            # Method 2: If no jobs found, try scrolling and searching
            if not job_elements:
                print("No jobs found initially, trying search...")
                try:
                    # Look for search box
                    search_box = driver.find_element(By.CSS_SELECTOR, "input[type='search'], input[name='q'], input[placeholder*='search']")
                    search_box.clear()
                    search_box.send_keys("data scientist")
                    search_box.send_keys(Keys.RETURN)
                    time.sleep(3)

                    # Try selectors again after search
                    for selector in selectors_to_try:
                        try:
                            elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            if elements:
                                job_elements.extend(elements)
                        except:
                            continue
                except:
                    print("Search functionality not found")

            # Extract links from found elements
            for elem in job_elements:
                try:
                    # Get link
                    if elem.tag_name == 'a':
                        href = elem.get_attribute('href')
                        title = elem.text.strip()
                    else:
                        # Look for link inside the element
                        link_elem = elem.find_element(By.TAG_NAME, 'a')
                        href = link_elem.get_attribute('href')
                        title = link_elem.text.strip() or elem.text.strip()

                    if href and title:
                        # Check if it's a data science related job
                        title_lower = title.lower()
                        if any(keyword.lower() in title_lower for keyword in KEYWORDS):
                            if href not in job_links:  # Avoid duplicates
                                job_links.append(href)
                                print(f"✓ Found job: {title[:60]}...")

                except Exception as e:
                    continue

            print(f"Total Data Science jobs found on Greenhouse: {len(job_links)}")

        except Exception as e:
            print(f"Error during job search: {e}")

    except Exception as e:
        print(f"Error scraping Greenhouse: {e}")

    return job_links

def search_jobs_lever(driver, url):
    """Search jobs on Lever"""
    job_links = []
    try:
        print(f"Visiting Lever page: {url}")
        driver.get(url)
        time.sleep(3)

        # Wait for page to load and try to find job listings
        try:
            print("Looking for job listings...")

            # Try multiple approaches to find jobs
            job_elements = []

            # Method 1: Look for common Lever job selectors
            selectors_to_try = [
                ".posting",
                ".posting-title",
                ".job-title",
                "[data-job-id]",
                "a[href*='/apply/']",
                ".lever-job",
                ".position"
            ]

            for selector in selectors_to_try:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"Found {len(elements)} elements with selector '{selector}'")
                        job_elements.extend(elements)
                except:
                    continue

            # Method 2: If no jobs found, try scrolling
            if not job_elements:
                print("No jobs found initially, trying scrolling...")
                for i in range(10):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)

                    # Check for new jobs after scrolling
                    for selector in selectors_to_try:
                        try:
                            elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            if elements:
                                job_elements.extend(elements)
                        except:
                            continue

                    if job_elements:
                        break

            # Extract links from found elements
            for elem in job_elements:
                try:
                    # Get link
                    if elem.tag_name == 'a':
                        href = elem.get_attribute('href')
                        title = elem.text.strip()
                    else:
                        # Look for link inside the element
                        link_elem = elem.find_element(By.TAG_NAME, 'a')
                        href = link_elem.get_attribute('href')
                        title = link_elem.text.strip() or elem.text.strip()

                    if href and title:
                        # Check if it's a data science related job
                        title_lower = title.lower()
                        if any(keyword.lower() in title_lower for keyword in KEYWORDS):
                            if href not in job_links:  # Avoid duplicates
                                job_links.append(href)
                                print(f"✓ Found job: {title[:60]}...")

                except Exception as e:
                    continue

            print(f"Total Data Science jobs found on Lever: {len(job_links)}")

        except Exception as e:
            print(f"Error during job search: {e}")

    except Exception as e:
        print(f"Error scraping Lever: {e}")

    return job_links

def search_jobs_ashby(driver, url):
    """Search jobs on Ashby"""
    job_links = []
    try:
        print(f"Visiting Ashby page: {url}")
        driver.get(url)
        time.sleep(3)

        # Wait for page to load and try to find job listings
        try:
            print("Looking for job listings...")

            # Try multiple approaches to find jobs
            job_elements = []

            # Method 1: Look for common Ashby job selectors
            selectors_to_try = [
                ".job-post",
                ".posting",
                "[data-job]",
                ".job-title",
                "a[href*='/job/']",
                ".ashby-job",
                ".position"
            ]

            for selector in selectors_to_try:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"Found {len(elements)} elements with selector '{selector}'")
                        job_elements.extend(elements)
                except:
                    continue

            # Method 2: If no jobs found, try scrolling
            if not job_elements:
                print("No jobs found initially, trying scrolling...")
                for i in range(10):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)

                    # Check for new jobs after scrolling
                    for selector in selectors_to_try:
                        try:
                            elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            if elements:
                                job_elements.extend(elements)
                        except:
                            continue

                    if job_elements:
                        break

            # Extract links from found elements
            for elem in job_elements:
                try:
                    # Get link
                    if elem.tag_name == 'a':
                        href = elem.get_attribute('href')
                        title = elem.text.strip()
                    else:
                        # Look for link inside the element
                        link_elem = elem.find_element(By.TAG_NAME, 'a')
                        href = link_elem.get_attribute('href')
                        title = link_elem.text.strip() or elem.text.strip()

                    if href and title:
                        # Check if it's a data science related job
                        title_lower = title.lower()
                        if any(keyword.lower() in title_lower for keyword in KEYWORDS):
                            if href not in job_links:  # Avoid duplicates
                                job_links.append(href)
                                print(f"✓ Found job: {title[:60]}...")

                except Exception as e:
                    continue

            print(f"Total Data Science jobs found on Ashby: {len(job_links)}")

        except Exception as e:
            print(f"Error during job search: {e}")

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