import streamlit as st
import pandas as pd

from logic.riasec_scoring import compute_riasec_scores
from logic.dominance_logic import get_dominant_types
from logic.decision_tree import ched_decision_tree
from logic.occupation_retrieval import load_occupations, filter_occupations

st.set_page_config(page_title="RIASEC–CHED Career Guidance", layout="centered")

st.title("RIASEC–CHED Career Guidance System")

if "page" not in st.session_state:
    st.session_state.page = "questionnaire"

def questionnaire_page():
    st.header("Career Interest Questionnaire")

    st.write(
        "Please answer the following statements honestly. "
        "There are no right or wrong answers."
    )

    items = pd.read_csv("data/questionnaire_items.csv")

    responses = {}

    for _, row in items.iterrows():
        responses[row["item_id"]] = st.radio(
            row["item_text"],
            options=[1, 2, 3, 4, 5],
            horizontal=True,
            key=f"q_{row['item_id']}"
        )

    if st.button("Submit Questionnaire"):
        st.session_state.responses = responses
        st.session_state.page = "results"

def results_page():
    st.header("Your Career Guidance Results")

    items = pd.read_csv("data/questionnaire_items.csv")

    responses_df = pd.DataFrame({
        "item_id": list(st.session_state.responses.keys()),
        "response_value": list(st.session_state.responses.values())
    })

    scores = compute_riasec_scores(responses_df, items)
    dominant, secondary = get_dominant_types(scores)
    clusters = ched_decision_tree(dominant, secondary)

    occupations = load_occupations(dominant)
    occupations = filter_occupations(occupations, secondary)

    st.subheader("RIASEC Interest Profile")

    score_df = pd.DataFrame.from_dict(scores, orient="index", columns=["Score"])
    st.bar_chart(score_df)

    st.write(f"**Dominant Interest Type:** {dominant}")
    st.write(f"**Secondary Interest Type:** {secondary}")

