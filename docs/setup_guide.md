# Setup Guide: Job Scraping & Analysis Project

## Environment Setup

### Step 1: Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: ChromeDriver Setup
1. Check your Chrome version:
   - Open Chrome → Settings → About Chrome (shows version like 121.x.x)
2. Download matching ChromeDriver:
   - Visit: https://chromedriver.chromium.org/
   - Download the version matching your Chrome
3. Place in one of these locations:
   - `selenium/chromedriver` (recommended)
   - System PATH
   - Or specify full path in script

### Step 4: Verify Installation
```bash
# Test Selenium import
python -c "from selenium import webdriver; print('Selenium OK')"

# Test Scrapy
scrapy --version

# Test Pandas
python -c "import pandas; print('Pandas OK')"
```

## Configuration Files

### Scrapy Settings (`scrapy_project/jobs/settings.py`)
- Set `USER_AGENT` to identify your crawler
- Configure `ROBOTSTXT_OBEY = True` to respect robots.txt
- Set `DOWNLOAD_DELAY = 2` for polite scraping
- Configure output formats (CSV, JSON)

### Environment Variables (Optional)
Create `.env` file for sensitive data:
```
CHROME_DRIVER_PATH=/path/to/chromedriver
PROXY_URL=optional
HEADLESS=True
```

## Execution Flow

### 1️⃣ Selenium Phase
```bash
python selenium/job_scraper.py
```
**Duration**: ~10-15 minutes (depending on search results)
**Output**: `data/raw/job_links.csv` with columns: [job_url, company, listed_date]
**Logs**: Check console for progress

### 2️⃣ Scrapy Phase
```bash
cd scrapy_project
scrapy crawl job_spider --logfile=spider.log
cd ..
```
**Duration**: Varies by number of URLs
**Output**: `data/final/jobs.csv` and `jobs.json`
**Logs**: Check scrapy logs for errors

### 3️⃣ Analysis Phase
```bash
python analysis/analysis_jobs.py
```
**Duration**: < 1 minute
**Output**: 
- Console statistics
- `analysis/analysis_report.md` with findings
- Charts in `analysis/charts/`

## Troubleshooting

### ChromeDriver Version Mismatch
**Error**: `ChromeDriver version mismatch`
**Solution**: 
1. Check Chrome version: `chrome://version/`
2. Download exact matching ChromeDriver
3. Verify path in script

### Connection Timeouts
**Error**: `Connection timeout` or `ConnectionRefusedError`
**Solution**:
1. Check internet connection
2. Verify website is accessible
3. Increase timeout in settings
4. Check if site is blocking automated requests

### Scrapy Empty Results
**Error**: No data in output file
**Solution**:
1. Verify `job_links.csv` is populated
2. Check CSS selectors in spider match page structure
3. Review Scrapy logs: `scrapy crawl job_spider --loglevel=DEBUG`
4. Test selectors manually with developer tools

### Permission Denied
**Error**: `Permission denied` on chromedriver
**Solution** (Linux/Mac):
```bash
chmod +x selenium/chromedriver
```

## Best Practices

### Rate Limiting
- Consistent 2-second delays between requests
- Limits requests to ~30 per minute per domain
- Respectful behavior toward target servers

### Error Handling
- Selenium retries failed element clicks
- Scrapy spider logs errors without stopping
- Missing fields set to empty strings
- Analysis handles missing values gracefully

### Data Quality
- Fields trimmed and normalized
- Duplicates removed by URL
- Dates parsed consistently
- Skills split on common delimiters

### Monitoring
- Console logs all major steps
- File-based logs for detailed debugging
- Progress indicators for long operations
- Summary statistics printed at end

## Common Extension Points

### Add New Job Platform
1. Create new function in `selenium/job_scraper.py`
2. Add selectors for platform's job cards
3. Append URLs to `job_links.csv`

### Modify Data Extracted
1. Edit `scrapy_project/jobs/items.py` to add fields
2. Update spider CSS selectors
3. Modify analysis script to use new fields

### Change Analysis Metrics
1. Edit `analysis/analysis_jobs.py`
2. Add new aggregations/visualizations
3. Update report generation

## Performance Tips

### For Large Scale
- Increase `CONCURRENT_REQUESTS` in Scrapy settings
- Use distributed crawling with Scrapy Cloud
- Cache intermediate results

### For Development
- Use `-a debug=1` argument to limit results
- Test selectors on single URL first
- Use Scrapy shell for selector testing:
  ```bash
  scrapy shell "https://example.com/job"
  ```

## File Size Expectations

- `job_links.csv`: 5-50 KB (~100-1000 jobs)
- `jobs.csv`: 50-500 KB depending on description length
- `analysis_report.md`: ~10-20 KB

---

**Last Updated**: March 2026
**Version**: 1.0
