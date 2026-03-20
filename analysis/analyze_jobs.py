import pandas as pd
import matplotlib.pyplot as plt
import json
from collections import Counter
import re

def load_jobs_data():
    """Load jobs data from JSON file"""
    with open('data/final/jobs.json', 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

def analyze_skills(df):
    """Analyze top skills"""
    all_skills = []
    for skills in df['required_skills'].dropna():
        skills_list = [s.strip() for s in skills.split(',') if s.strip()]
        all_skills.extend(skills_list)
    
    skill_counts = Counter(all_skills)
    return skill_counts.most_common(10)

def analyze_locations(df):
    """Analyze top locations"""
    locations = df['location'].dropna()
    location_counts = Counter(locations)
    return location_counts.most_common(10)

def analyze_companies(df):
    """Analyze top companies"""
    companies = df['company_name'].dropna()
    company_counts = Counter(companies)
    return company_counts.most_common(10)

def analyze_job_types(df):
    """Analyze job types (internships, junior positions)"""
    titles = df['job_title'].dropna().str.lower()
    
    internships = titles.str.contains('intern').sum()
    junior = titles.str.contains('junior|entry').sum()
    
    return {
        'internships': internships,
        'junior_positions': junior
    }

def analyze_job_titles(df):
    """Analyze most common job titles"""
    titles = df['job_title'].dropna()
    title_counts = Counter(titles)
    return title_counts.most_common(10)

def create_visualizations(df):
    """Create visualizations"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Top skills
    skills = analyze_skills(df)
    if skills:
        skills_df = pd.DataFrame(skills, columns=['Skill', 'Count'])
        skills_df.plot(kind='bar', x='Skill', y='Count', ax=axes[0,0])
        axes[0,0].set_title('Top Skills')
        axes[0,0].tick_params(axis='x', rotation=45)
    
    # Top locations
    locations = analyze_locations(df)
    if locations:
        loc_df = pd.DataFrame(locations, columns=['Location', 'Count'])
        loc_df.plot(kind='bar', x='Location', y='Count', ax=axes[0,1])
        axes[0,1].set_title('Top Locations')
        axes[0,1].tick_params(axis='x', rotation=45)
    
    # Top companies
    companies = analyze_companies(df)
    if companies:
        comp_df = pd.DataFrame(companies, columns=['Company', 'Count'])
        comp_df.plot(kind='bar', x='Company', y='Count', ax=axes[1,0])
        axes[1,0].set_title('Top Companies')
        axes[1,0].tick_params(axis='x', rotation=45)
    
    # Job titles
    titles = analyze_job_titles(df)
    if titles:
        title_df = pd.DataFrame(titles, columns=['Title', 'Count'])
        title_df.plot(kind='bar', x='Title', y='Count', ax=axes[1,1])
        axes[1,1].set_title('Most Common Job Titles')
        axes[1,1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('docs/job_analysis.png')
    plt.show()

def generate_report(df):
    """Generate analysis report"""
    report = "# Job Analysis Report\n\n"
    
    # Top skills
    skills = analyze_skills(df)
    report += "## Top Skills\n"
    for skill, count in skills:
        report += f"- {skill}: {count}\n"
    report += "\n"
    
    # Top locations
    locations = analyze_locations(df)
    report += "## Top Locations\n"
    for loc, count in locations:
        report += f"- {loc}: {count}\n"
    report += "\n"
    
    # Top companies
    companies = analyze_companies(df)
    report += "## Top Companies\n"
    for comp, count in companies:
        report += f"- {comp}: {count}\n"
    report += "\n"
    
    # Job types
    job_types = analyze_job_types(df)
    report += "## Job Types\n"
    report += f"- Internships: {job_types['internships']}\n"
    report += f"- Junior Positions: {job_types['junior_positions']}\n"
    report += "\n"
    
    # Job titles
    titles = analyze_job_titles(df)
    report += "## Most Common Job Titles\n"
    for title, count in titles:
        report += f"- {title}: {count}\n"
    
    with open('docs/analysis_report.md', 'w') as f:
        f.write(report)

def main():
    try:
        df = load_jobs_data()
        print(f"Loaded {len(df)} job listings")
        
        # Generate visualizations
        create_visualizations(df)
        
        # Generate text report
        generate_report(df)
        
        print("Analysis complete. Check docs/ for results.")
        
    except FileNotFoundError:
        print("Jobs data not found. Run Scrapy spider first.")

if __name__ == "__main__":
    main()