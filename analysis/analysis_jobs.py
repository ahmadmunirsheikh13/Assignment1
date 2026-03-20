"""
Job Market Analysis Script
Analyzes job listings data and generates insights and visualizations.

Author: Ahmad Munir Sheikh
Date: March 2026
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from collections import Counter
from datetime import datetime

# Configure plotting
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def load_data(csv_path):
    """Load job data from CSV"""
    if not os.path.exists(csv_path):
        print(f"❌ Error: File not found at {csv_path}")
        return None
    
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded {len(df)} job records")
    return df


def analyze_skills(df):
    """Analyze required skills"""
    print("\n" + "="*80)
    print("🔧 SKILL DEMAND ANALYSIS")
    print("="*80)
    
    # Extract and count skills
    skills_list = []
    for skills_str in df['required_skills'].fillna(''):
        if isinstance(skills_str, str) and skills_str.strip():
            skills = [s.strip().lower() for s in skills_str.split(',')]
            skills_list.extend([s for s in skills if s])
    
    skill_counts = Counter(skills_list)
    top_skills = skill_counts.most_common(20)
    
    print("\nTop 20 Most Demanded Skills:")
    print("-" * 40)
    for i, (skill, count) in enumerate(top_skills, 1):
        print(f"{i:2}. {skill.title():<25} {count:4} jobs ({count/len(df)*100:5.1f}%)")
    
    return top_skills


def analyze_locations(df):
    """Analyze geographic distribution"""
    print("\n" + "="*80)
    print("📍 GEOGRAPHIC DISTRIBUTION")
    print("="*80)
    
    location_counts = df['location'].fillna('Not specified').value_counts().head(15)
    
    print("\nTop 15 Cities with Most Job Openings:")
    print("-" * 40)
    for i, (location, count) in enumerate(location_counts.items(), 1):
        percentage = (count / len(df)) * 100
        bar = "█" * int(percentage / 2)
        print(f"{i:2}. {location:<25} {count:4} jobs {bar:<20} {percentage:5.1f}%")
    
    return location_counts


def analyze_companies(df):
    """Analyze top hiring companies"""
    print("\n" + "="*80)
    print("🏢 TOP HIRING COMPANIES")
    print("="*80)
    
    company_counts = df['company_name'].fillna('Unknown').value_counts().head(20)
    
    print("\nTop 20 Companies Posting Most Jobs:")
    print("-" * 40)
    for i, (company, count) in enumerate(company_counts.items(), 1):
        print(f"{i:2}. {company:<35} {count:3} jobs")
    
    return company_counts


def analyze_experience_levels(df):
    """Analyze internship vs. senior positions"""
    print("\n" + "="*80)
    print("🎓 EXPERIENCE LEVEL ANALYSIS")
    print("="*80)
    
    # Categorize based on keywords
    df['is_internship'] = (
        df['job_title'].str.contains('intern', case=False, na=False) |
        df['employment_type'].str.contains('intern', case=False, na=False)
    )
    
    df['is_entry'] = (
        df['job_title'].str.contains('entry|junior|associate', case=False, na=False) |
        df['job_description'].str.contains('entry|junior|associate|0-2 years|no experience required', case=False, na=False)
    )
    
    df['is_senior'] = (
        df['job_title'].str.contains('senior|lead|principal|staff', case=False, na=False)
    )
    
    internships = df['is_internship'].sum()
    entry_level = df['is_entry'].sum()
    senior = df['is_senior'].sum()
    mid_level = len(df) - internships - entry_level - senior
    
    print("\nExperience Level Breakdown:")
    print("-" * 40)
    print(f"  Internship/Graduate Roles:  {internships:4} ({internships/len(df)*100:5.1f}%)")
    print(f"  Entry-Level (0-2 years):    {entry_level:4} ({entry_level/len(df)*100:5.1f}%)")
    print(f"  Mid-Level (2-5+ years):     {mid_level:4} ({mid_level/len(df)*100:5.1f}%)")
    print(f"  Senior/Lead Roles:          {senior:4} ({senior/len(df)*100:5.1f}%)")
    
    return {
        'internship': int(internships),
        'entry': int(entry_level),
        'mid': int(mid_level),
        'senior': int(senior)
    }


def analyze_job_titles(df):
    """Analyze most common job titles"""
    print("\n" + "="*80)
    print("💼 JOB TITLE ANALYSIS")
    print("="*80)
    
    # Extract job title keywords
    title_keywords = []
    common_titles = [
        'Software Engineer', 'Data Scientist', 'Data Analyst', 'Data Engineer',
        'Product Manager', 'QA Engineer', 'DevOps Engineer', 'Machine Learning',
        'Backend', 'Frontend', 'Full-Stack', 'Business Analyst', 'Manager',
        'Architect', 'Associate', 'Intern', 'Specialist'
    ]
    
    for title in df['job_title'].fillna(''):
        for keyword in common_titles:
            if keyword.lower() in str(title).lower():
                title_keywords.append(keyword)
                break
    
    title_counts = Counter(title_keywords)
    top_titles = title_counts.most_common(15)
    
    print("\nMost Common Job Title Categories:")
    print("-" * 40)
    for i, (title, count) in enumerate(top_titles, 1):
        percentage = (count / len(df)) * 100
        print(f"{i:2}. {title:<30} {count:4} jobs ({percentage:5.1f}%)")
    
    return top_titles


def analyze_employment_type(df):
    """Analyze employment types"""
    print("\n" + "="*80)
    print("⏰ EMPLOYMENT TYPE DISTRIBUTION")
    print("="*80)
    
    emp_type_counts = df['employment_type'].fillna('Not specified').value_counts()
    
    print("\nEmployment Type Breakdown:")
    print("-" * 40)
    for emp_type, count in emp_type_counts.items():
        percentage = (count / len(df)) * 100
        bar = "█" * int(percentage / 3)
        print(f"  {emp_type:<25} {count:4} jobs {bar:<20} {percentage:5.1f}%")
    
    return emp_type_counts


def create_visualizations(df, top_skills, top_locations, experience_levels):
    """Create and save visualizations"""
    print("\n" + "="*80)
    print("📊 GENERATING VISUALIZATIONS")
    print("="*80)
    
    # Create output directory
    charts_dir = "analysis/charts"
    os.makedirs(charts_dir, exist_ok=True)
    
    # 1. Top Skills Bar Chart
    try:
        plt.figure(figsize=(14, 8))
        skills, counts = zip(*top_skills)
        plt.barh(skills, counts, color='steelblue')
        plt.xlabel('Number of Job Postings', fontsize=12, fontweight='bold')
        plt.title('Top 20 Most Demanded Skills', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        chart_path = os.path.join(charts_dir, '01_top_skills.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved: {chart_path}")
        plt.close()
    except Exception as e:
        print(f"  ⚠️ Error creating skills chart: {e}")
    
    # 2. Top Cities Bar Chart
    try:
        plt.figure(figsize=(14, 8))
        top_locations.head(15).plot(kind='barh', color='coral')
        plt.xlabel('Number of Job Postings', fontsize=12, fontweight='bold')
        plt.title('Top 15 Cities with Most Job Openings', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        chart_path = os.path.join(charts_dir, '02_top_cities.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved: {chart_path}")
        plt.close()
    except Exception as e:
        print(f"  ⚠️ Error creating cities chart: {e}")
    
    # 3. Experience Level Pie Chart
    try:
        plt.figure(figsize=(10, 8))
        labels = ['Internship', 'Entry-Level', 'Mid-Level', 'Senior']
        sizes = [
            experience_levels['internship'],
            experience_levels['entry'],
            experience_levels['mid'],
            experience_levels['senior']
        ]
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Job Distribution by Experience Level', fontsize=14, fontweight='bold')
        plt.tight_layout()
        chart_path = os.path.join(charts_dir, '03_experience_distribution.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved: {chart_path}")
        plt.close()
    except Exception as e:
        print(f"  ⚠️ Error creating experience chart: {e}")
    
    # 4. Top Companies Bar Chart
    try:
        plt.figure(figsize=(14, 8))
        df['company_name'].fillna('Unknown').value_counts().head(15).plot(kind='barh', color='lightgreen')
        plt.xlabel('Number of Job Postings', fontsize=12, fontweight='bold')
        plt.title('Top 15 Companies with Most Job Openings', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        chart_path = os.path.join(charts_dir, '04_top_companies.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved: {chart_path}")
        plt.close()
    except Exception as e:
        print(f"  ⚠️ Error creating companies chart: {e}")


def generate_report(df, top_skills, top_locations, experience_levels, top_titles, emp_types):
    """Generate markdown report"""
    print("\n" + "="*80)
    print("📄 GENERATING REPORT")
    print("="*80)
    
    report = f"""# Job Market Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This analysis includes **{len(df)} job listings** collected from Greenhouse, Lever, and Ashby job boards. The report provides insights into skill demand, geographic distribution, companies, and experience level requirements.

## Key Findings

### 📊 Overview
- **Total Jobs Analyzed:** {len(df)}
- **Unique Companies:** {df['company_name'].nunique()}
- **Job Locations:** {df['location'].nunique()} different locations
- **Skill Categories:** {len([s for s, _ in top_skills])} identified

### 🔧 Top 10 Most Demanded Skills
"""
    
    for i, (skill, count) in enumerate(top_skills[:10], 1):
        percentage = (count / len(df)) * 100
        report += f"\n{i}. **{skill.title()}** - {count} jobs ({percentage:.1f}%)"
    
    report += f"""

### 📍 Top 5 Hiring Locations
"""
    
    for i, (location, count) in enumerate(top_locations.head(5).items(), 1):
        percentage = (count / len(df)) * 100
        report += f"\n{i}. **{location}** - {count} jobs ({percentage:.1f}%)"
    
    report += f"""

### 🏢 Top Hiring Companies
"""
    
    top_companies = df['company_name'].fillna('Unknown').value_counts().head(5)
    for i, (company, count) in enumerate(top_companies.items(), 1):
        report += f"\n{i}. **{company}** - {count} jobs"
    
    report += f"""

### 🎓 Experience Level Distribution
- **Internship/Graduate:** {experience_levels['internship']} jobs ({experience_levels['internship']/len(df)*100:.1f}%)
- **Entry-Level (0-2 yrs):** {experience_levels['entry']} jobs ({experience_levels['entry']/len(df)*100:.1f}%)
- **Mid-Level (2-5+ yrs):** {experience_levels['mid']} jobs ({experience_levels['mid']/len(df)*100:.1f}%)
- **Senior/Lead:** {experience_levels['senior']} jobs ({experience_levels['senior']/len(df)*100:.1f}%)

### 💼 Most Common Job Titles
"""
    
    for i, (title, count) in enumerate(top_titles[:10], 1):
        percentage = (count / len(df)) * 100
        report += f"\n{i}. **{title}** - {count} jobs ({percentage:.1f}%)"
    
    report += f"""

### ⏰ Employment Type Distribution
"""
    
    for emp_type, count in emp_types.items():
        percentage = (count / len(df)) * 100
        report += f"\n- **{emp_type}** - {count} jobs ({percentage:.1f}%)"
    
    report += """

## Insights & Recommendations

### Skill Development
- The most in-demand skills are diverse, ranging from programming languages to specialized tools
- Focus on foundational skills like Python, SQL, and cloud platforms (AWS/Azure/GCP)

### Geographic Opportunities
- Major tech hubs continue to dominate job opportunities
- Remote work is increasingly common
- Consider relocation if targeting highest concentration of opportunities

### Career Trajectory
- Entry-level roles provide a pathway for career growth
- Choose specialization based on market demand (cloud, ML, DevOps, etc.)

### Company Insights  
- Large tech companies remain major employers
- Startups offer diverse role types and faster growth

## Methodology

**Data Collection:**
- Selenium: Automated job discovery from career pages
- Scrapy: Distributed crawling for job detail extraction
- Platforms: Greenhouse, Lever, Ashby

**Data Processing:**
- Normalization and deduplication
- Skill extraction from job descriptions
- Experience level categorization

---

**Generated:** {datetime.now().strftime('%A, %B %d, %Y at %H:%M:%S')}
"""
    
    # Write report
    report_path = "analysis/analysis_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"  ✓ Report saved to: {report_path}")
    return report


if __name__ == '__main__':
    print("="*80)
    print("📈 JOB MARKET ANALYSIS SYSTEM")
    print("="*80)
    
    # Load data
    csv_path = 'data/final/jobs.csv'
    df = load_data(csv_path)
    
    if df is not None and len(df) > 0:
        # Run analyses
        top_skills = analyze_skills(df)
        top_locations = analyze_locations(df)
        experience_levels = analyze_experience_levels(df)
        top_titles = analyze_job_titles(df)
        top_companies = analyze_companies(df)
        emp_types = analyze_employment_type(df)
        
        # Create visualizations
        create_visualizations(df, top_skills, top_locations, experience_levels)
        
        # Generate report
        generate_report(df, top_skills, top_locations, experience_levels, top_titles, emp_types)
        
        print("\n" + "="*80)
        print("✨ ANALYSIS COMPLETE")
        print("="*80)
        print("  ✓ All visualizations generated")
        print("  ✓ Report generated: analysis/analysis_report.md")
        print("  ✓ Charts saved to: analysis/charts/")
        print("="*80 + "\n")
    else:
        print("❌ No data available for analysis")
