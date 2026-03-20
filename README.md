# Assignment1: Tools & Techniques for Data Science

This repository contains a web scraping project for collecting and analyzing job listings related to Data Science and Machine Learning from public career pages using Selenium and Scrapy.

## Project Structure

- `selenium/` - Selenium scripts for automating job search and collecting job URLs
- `scrapy_project/` - Scrapy project for crawling job detail pages and extracting structured data
- `data/raw/` - Intermediate files (job links CSV)
- `data/final/` - Final dataset (jobs JSON)
- `analysis/` - Analysis scripts and notebooks
- `docs/` - Documentation and reports

## Requirements

- Python 3.8+
- Selenium
- Scrapy
- Pandas
- Matplotlib
- ChromeDriver (for Selenium)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/AhmadMunirSheikh/Assignment1-clean.git
   cd Assignment1-clean
   ```

2. Install dependencies:
   ```bash
   pip install selenium scrapy pandas matplotlib
   ```

3. Download ChromeDriver and place it in your PATH or selenium directory.

## Usage

1. Run Selenium scraper to collect job URLs:
   ```bash
   python selenium/scrape_jobs.py
   ```

2. Run Scrapy spider to extract job details:
   ```bash
   cd scrapy_project
   scrapy crawl job_spider
   ```

3. Run analysis script:
   ```bash
   python analysis/analyze_jobs.py
   ```

## Results

See `docs/report.md` for detailed analysis results.

## Git Workflow

- `main`: Stable production branch
- `develop`: Integration branch for features
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches
- `release/*`: Release preparation branches

## License

This project is for educational purposes only.