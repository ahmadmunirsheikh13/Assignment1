from selenium.webdriver.common.keys import Keys

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
        # Greenhouse boards have different structures per company
        # Try to find search functionality or just collect all visible jobs
        driver.get(base_url)
        time.sleep(3)
        
        # Look for search input or department filters
        try:
            search_box = driver.find_element(By.CSS_SELECTOR, "input[type='search'], input[name='q'], input[placeholder*='search']")
            search_box.send_keys("Data Science")
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)
        except:
            print("No search box found, collecting all jobs")
        
        # Scroll to load more jobs
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # Collect job links - Greenhouse uses various selectors
        job_selectors = [
            "a[href*='/jobs/']",
            ".job-link",
            ".opening a",
            "[data-jobid] a"
        ]
        
        for selector in job_selectors:
            try:
                jobs = driver.find_elements(By.CSS_SELECTOR, selector)
                for job in jobs[:20]:  # Limit to first 20
                    title = job.text.lower()
                    href = job.get_attribute('href')
                    if href and any(keyword.lower() in title for keyword in KEYWORDS):
                        job_links.append(href)
                if job_links:
                    break
            except:
                continue
                
    except Exception as e:
        print(f"Error scraping Greenhouse: {e}")
    
    return list(set(job_links))  # Remove duplicates

def search_jobs_lever(driver, base_url):
    """Search jobs on Lever"""
    job_links = []
    try:
        driver.get(base_url)
        time.sleep(3)
        
        # Lever sites vary, try to find search or filter
        try:
            search_box = driver.find_element(By.CSS_SELECTOR, "input[type='search'], input[placeholder*='search']")
            search_box.send_keys("Data Science")
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)
        except:
            print("No search box found, collecting all jobs")
        
        # Scroll to load more
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # Lever job selectors
        job_selectors = [
            "a[href*='/apply/']",
            ".job-title a",
            ".posting-title a",
            "[data-job-id] a"
        ]
        
        for selector in job_selectors:
            try:
                jobs = driver.find_elements(By.CSS_SELECTOR, selector)
                for job in jobs[:20]:
                    title = job.text.lower()
                    href = job.get_attribute('href')
                    if href and any(keyword.lower() in title for keyword in KEYWORDS):
                        job_links.append(href)
                if job_links:
                    break
            except:
                continue
                
    except Exception as e:
        print(f"Error scraping Lever: {e}")
    
    return list(set(job_links))

def search_jobs_ashby(driver, base_url):
    """Search jobs on Ashby"""
    job_links = []
    try:
        driver.get(base_url)
        time.sleep(3)
        
        # Ashby has search functionality
        try:
            search_box = driver.find_element(By.CSS_SELECTOR, "input[type='search'], input[placeholder*='search']")
            search_box.send_keys("Data Science")
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)
        except:
            print("No search box found, collecting all jobs")
        
        # Scroll to load more
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # Ashby job selectors
        job_selectors = [
            "a[href*='/job/']",
            ".job-link",
            ".posting a",
            "[data-job] a"
        ]
        
        for selector in job_selectors:
            try:
                jobs = driver.find_elements(By.CSS_SELECTOR, selector)
                for job in jobs[:20]:
                    title = job.text.lower()
                    href = job.get_attribute('href')
                    if href and any(keyword.lower() in title for keyword in KEYWORDS):
                        job_links.append(href)
                if job_links:
                    break
            except:
                continue
                
    except Exception as e:
        print(f"Error scraping Ashby: {e}")
    
    return list(set(job_links))

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