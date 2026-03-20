import pandas as pd

if __name__ == '__main__':
    csv_path = '../data/final/jobs.csv'
    df = pd.read_csv(csv_path)

    # Normalize text fields
    df['required_skills'] = df['required_skills'].fillna('').astype(str)
    df['location'] = df['location'].fillna('Unknown').astype(str)
    df['job_title'] = df['job_title'].fillna('').astype(str)

    # Top skills in demand
    skill_series = df['required_skills'].str.lower().str.split(',').explode().str.strip().replace('', pd.NA).dropna()
    top_skills = skill_series.value_counts().head(20)

    # Top hiring locations
    top_locations = df['location'].str.strip().replace('', 'Unknown').value_counts().head(20)

    # Entry-level roles (keywords in title/description)
    df['entry_level'] = df['job_title'].str.lower().fillna('').str.contains('entry|junior|associate') | \
                       df['job_description'].str.lower().fillna('').str.contains('entry|junior|associate')
    entry_level_count = int(df['entry_level'].sum())

    print('Top skills in demand:')
    print(top_skills)
    print('\nTop hiring locations:')
    print(top_locations)
    print(f'\nEntry-level role count: {entry_level_count}')
