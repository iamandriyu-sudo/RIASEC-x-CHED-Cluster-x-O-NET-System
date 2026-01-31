import pandas as pd

def compute_riasec_scores(responses_df, items_df):
    scores = {'R':0, 'I':0, 'A':0, 'S':0, 'E':0, 'C':0}

    merged = responses_df.merge(items_df, on="item_id")

    for _, row in merged.iterrows():
        scores[row['riasec_type']] += row['response_value']

    return scores