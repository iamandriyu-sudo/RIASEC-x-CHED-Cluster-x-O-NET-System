import pandas as pd

from logic.riasec_scoring import compute_riasec_scores
from logic.dominance_logic import get_dominant_types
from logic.decision_tree import ched_decision_tree
from logic.occupation_retrieval import load_occupations, filter_occupations

items = pd.read_csv("data/questionnaire_items.csv")

responses = pd.DataFrame({
    "item_id": list(range(1, 25)),
    "response_value": [4]*24
})

scores = compute_riasec_scores(responses, items)
dominant, secondary = get_dominant_types(scores)

clusters = ched_decision_tree(dominant, secondary)

occupations = load_occupations(dominant)
occupations = filter_occupations(occupations, secondary)

print("RIASEC Scores:", scores)
print("Dominant:", dominant, "Secondary:", secondary)
print("Recommended CHED Clusters:", clusters)
print("Sample Occupations:")
print(occupations[['Occupation']].head())

