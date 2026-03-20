import pandas as pd
import matplotlib.pyplot as plt
import os

if __name__ == '__main__':
    csv_path = '../data/final/jobs.csv'
    df = pd.read_csv(csv_path)

    # Normalize text fields
    df['required_skills'] = df['required_skills'].fillna('').astype(str)
    df['location'] = df['location'].fillna('Unknown').astype(str)
    df['job_title'] = df['job_title'].fillna('').astype(str)

    print("="*60)
    print("DATA SCIENCE & MACHINE LEARNING JOBS ANALYSIS REPORT")
    print("="*60)
    print(f"Total jobs analyzed: {len(df)}")
    print()

    # Top skills in demand
    skill_series = df['required_skills'].str.lower().str.split(',').explode().str.strip().replace('', pd.NA).dropna()
    top_skills = skill_series.value_counts().head(20)

    print("🔧 TOP SKILLS IN DEMAND:")
    print("-" * 30)
    for skill, count in top_skills.items():
        print(f"  {skill.title()}: {count} jobs")
    print()

    # Top hiring locations
    top_locations = df['location'].str.strip().replace('', 'Unknown').value_counts().head(20)

    print("📍 TOP HIRING LOCATIONS:")
    print("-" * 30)
    for location, count in top_locations.items():
        print(f"  {location}: {count} jobs")
    print()

    # Entry-level roles (keywords in title/description)
    df['entry_level'] = df['job_title'].str.lower().fillna('').str.contains('entry|junior|associate') | \
                       df['job_description'].str.lower().fillna('').str.contains('entry|junior|associate')
    entry_level_count = int(df['entry_level'].sum())

    print("🎓 ENTRY-LEVEL ANALYSIS:")
    print("-" * 30)
    print(f"  Entry-level roles found: {entry_level_count}")
    print(f"  Senior/Mid-level roles: {len(df) - entry_level_count}")
    print()

    # Job title analysis
    print("💼 JOB TITLE BREAKDOWN:")
    print("-" * 30)
    title_counts = df['job_title'].value_counts().head(10)
    for title, count in title_counts.items():
        print(f"  {title}: {count}")
    print()

    # Company analysis
    print("🏢 COMPANY ANALYSIS:")
    print("-" * 30)
    company_counts = df['company_name'].value_counts()
    for company, count in company_counts.items():
        print(f"  {company}: {count} jobs")
    print()

    # Employment type analysis
    print("⏰ EMPLOYMENT TYPE ANALYSIS:")
    print("-" * 30)
    employment_counts = df['employment_type'].value_counts()
    for emp_type, count in employment_counts.items():
        print(f"  {emp_type}: {count}")
    print()

    print("="*60)
    print("ANALYSIS COMPLETE - REPORT GENERATED")
    print("="*60)
