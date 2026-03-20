# Job Market Analysis: Web Scraping & Data Science Project

A comprehensive web scraping and data analysis project that collects job listings from leading Applicant Tracking Systems (Greenhouse, Lever, Ashby) and produces actionable insights about the job market.

## 📋 Project Overview

This project demonstrates full-stack data engineering and analysis:
- **Selenium Automation**: Browser automation to discover job listings from 3 approved sources
- **Scrapy Extraction**: Distributed crawling to extract structured job data
- **Data Analysis**: Pandas-based analytics and visualization
- **Git Workflow**: Professional repository structure with feature branches and PRs

## 📁 Repository Structure

```
Assignment1/
├── selenium/                    # Browser automation scripts
│   └── job_scraper.py          # Main Selenium scraper
├── scrapy_project/             # Scrapy spider project
│   ├── jobs/                   # Spider definitions
│   │   ├── spiders/
│   │   │   └── job_spider.py   # Main job extraction spider
│   │   ├── items.py            # Data models
│   │   ├── pipelines.py        # Data processing pipelines
│   │   └── settings.py         # Scrapy configuration
│   └── scrapy.cfg
├── data/
│   ├── raw/                    # Intermediate files
│   │   └── job_links.csv       # URLs from Selenium phase
│   └── final/                  # Final datasets
│       ├── jobs.csv            # Structured job data
│       └── jobs.json           # Alternative JSON format
├── analysis/                   # Data analysis & insights
│   ├── analysis_jobs.py        # Analysis script
│   └── analysis_report.md     # Summary findings
├── docs/                       # Documentation
│   ├── setup_guide.md         # Detailed setup instructions
│   └── job_sources_selection.txt
├── README.md                   # This file
├── requirements.txt            # Python dependencies
└── .gitignore                 # Git ignore rules
```

## 🎯 Key Features

### Data Collection (Selenium)
- ✅ Automate job search on 3 career platforms
- ✅ Apply location & department filters  
- ✅ Handle pagination and infinite scroll
- ✅ Collect job detail page URLs
- ✅ Export to `job_links.csv`

### Data Extraction (Scrapy)
- ✅ Parse job detail pages
- ✅ Extract 10+ fields (title, company, location, skills, etc.)
- ✅ Normalize and validate data
- ✅ Pipeline for CSV/JSON export
- ✅ Handle errors gracefully

### Data Analysis
- ✅ Top 10 most demanded skills
- ✅ Cities with highest job openings
- ✅ Companies posting most roles
- ✅ Internship vs. senior positions breakdown
- ✅ Job title frequency analysis
- ✅ Visualizations and summary report

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Chrome browser (for Selenium)
- Git (for version control)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ahmadmunirsheikh13/Assignment1.git
   cd Assignment1
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download ChromeDriver**
   - Visit: https://chromedriver.chromium.org/
   - Download matching your Chrome version
   - Place in `selenium/` folder or add to PATH

### Execution Steps

#### Step 1: Collect Job URLs with Selenium
```bash
python selenium/job_scraper.py
```
Output: `data/raw/job_links.csv`

#### Step 2: Extract Job Details with Scrapy
```bash
cd scrapy_project
scrapy crawl job_spider
```
Output: `data/final/jobs.csv`

#### Step 3: Analyze Data
```bash
cd ..
python analysis/analysis_jobs.py
```
Output: Analysis report and visualizations

## 📊 Data Schema

The final `jobs.csv` includes:
| Field | Type | Description |
|-------|------|-------------|
| job_title | str | Position title |
| company_name | str | Employer name |
| location | str | Job location |
| department | str | Department/Team |
| employment_type | str | Full-time / Part-time / Internship |
| posted_date | str | Publication date |
| job_url | str | Direct link to job |
| description | str | Full job description |
| required_skills | str | Comma-separated skills |
| experience_level | str | Entry / Mid / Senior (if available) |

## 🔍 Analysis Outputs

Latest analysis (2026-03-21) across 20 job listings:

### Top In-Demand Skills
1. **Python** - 17 positions
2. **SQL** - 8 positions  
3. **Java** - 7 positions
4. **Go** - 5 positions
5. **Databases** - 5 positions

### Geographic Distribution
- **San Francisco CA**: 8 jobs (40%)
- **Mountain View CA**: 2 jobs
- **Menlo Park CA**: 2 jobs
- **Other locations**: 8 jobs

### Top Hiring Companies
1. **Stripe** - 3 openings
2. **Google, Meta, Netflix** - 2 openings each

### Full Analysis Report
See [docs/analysis_report.md](docs/analysis_report.md) for comprehensive insights.

## 📝 Git Workflow (Professional)

### Branch Strategy
- `main` - Production release versions (tagged)
- `develop` - Integration branch for features
- `feature/*` - Individual feature development

### Example Workflow
```bash
# Start feature
git checkout develop
git fetch origin
git checkout -b feature/selenium-search

# Make commits
git add .
git commit -m "feat: implement job search with location filter"

# Push and create PR
git push origin feature/selenium-search
# Create PR to develop on GitHub: Review → Merge

# Release to main
git checkout main
git merge develop
git tag v1.0.0
git push origin main --tags
```

## 📋 Compliance & Ethics

- ✅ **Polite Scraping**: 2-second delays between requests
- ✅ **robots.txt Compliance**: Respect site crawl rules
- ✅ **Public Data Only**: No authentication bypass or private data
- ✅ **Rate Limiting**: Throttled requests to avoid overload
- ✅ **Attribution**: Sources cited in reports and code comments

## 🔗 Approved Job Platforms

1. **Greenhouse** - Used by 500+ companies
   - careers.greenhouse.io (various sub-domains)
   
2. **Lever** - ATS by Lever Hire
   - jobs.lever.co

3. **Ashby** - Modern ATS platform
   - ashby.jobs

## 📚 Documentation

- [Setup Guide](docs/setup_guide.md) - Detailed environment setup
- [Analysis Report](analysis/analysis_report.md) - Findings and insights
- [Data Sources](docs/job_sources_selection.txt) - Why these platforms

## 👨‍💻 Technologies

- **Selenium** v4.x - Browser automation
- **Scrapy** v2.x - Web scraping framework
- **Pandas** - Data manipulation
- **Matplotlib/Seaborn** - Visualization
- **ChromeDriver** - Chrome automation

## 📄 License

MIT License - See repo for details

## 🤝 Contributing

1. Create feature branch from `develop`
2. Make small, focused commits
3. Push and create pull request
4. Wait for review and merge to `develop`
5. After stable release, merge `develop` to `main`

---

**Last Updated**: March 2026
**Status**: In Development

4. Run analysis script:
   ```bash
   python analysis/analyze_jobs.py
   ```

## Results

See `analysis/analysis_report.txt` and `analysis/business_insights.txt` for detailed analysis results. The final dataset is saved as `data/final/jobs.csv`.

## Git Workflow

- `main`: Stable production branch
- `develop`: Integration branch for features
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches
- `release/*`: Release preparation branches

## License

This project is for educational purposes only.