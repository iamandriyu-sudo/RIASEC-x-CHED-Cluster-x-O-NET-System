import pandas as pd

def load_occupations(riasec_type):
    file_map = {
        'R': 'data/Realistic.csv',
        'I': 'data/Investigative.csv',
        'A': 'data/Artistic.csv',
        'S': 'data/Social.csv',
        'E': 'data/Enterprising.csv',
        'C': 'data/Conventional.csv'
    }

    df = pd.read_csv(file_map[riasec_type])
    return df

def filter_occupations(df, secondary=None, max_job_zone=4):
    df = df[df['Job Zone'] <= max_job_zone]

    if secondary:
        df = df[df['Interest Code'].str.contains(secondary)]

    return df
