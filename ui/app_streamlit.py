import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from logic.riasec_scoring import compute_riasec_scores
from logic.dominance_logic import get_dominant_types
from logic.decision_tree import ched_decision_tree
from logic.occupation_retrieval import load_occupations, filter_occupations


# -----------------------------
# PAGE CONFIG & SESSION STATE
# -----------------------------
st.set_page_config(
    page_title="RIASEC–CHED Career Guidance",
    layout="centered"
)

st.title("RIASEC–CHED Career Guidance System")

# IMPORTANT: initialize page state ONCE
if "page" not in st.session_state:
    st.session_state.page = "questionnaire"

if "responses" not in st.session_state:
    st.session_state.responses = {}


# -----------------------------
# QUESTIONNAIRE PAGE
# -----------------------------
def questionnaire_page():
    st.header("Career Interest Questionnaire")

    st.write(
        "Please answer all statements honestly using the scale below."
    )

    items = pd.read_csv("data/questionnaire_items.csv")

    with st.container(height=500):
        for _, row in items.iterrows():
            st.session_state.responses[row["item_id"]] = st.radio(
                row["item_text"],
                options=[1, 2, 3, 4, 5],
                key=f"q_{row['item_id']}"
            )

    st.markdown("---")

    if st.button("Submit Questionnaire"):
        st.session_state.page = "results"
        st.rerun()


# -----------------------------
# RESULTS PAGE
# -----------------------------
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

    st.write(f"*Dominant Interest Type:* {dominant}")
    st.write(f"*Secondary Interest Type:* {secondary}")

    st.subheader("Recommended CHED Priority Program Clusters")
    for cluster in clusters:
        st.success(cluster)

    st.subheader("Related Occupations (O*NET)")
    if not occupations.empty:
        st.dataframe(
            occupations[["Occupation", "Job Zone", "Interest Code"]].head(10)
        )
    else:
        st.warning("No matching occupations found.")

    st.markdown("---")

    if st.button("Go Back to Questionnaire"):
        st.session_state.page = "questionnaire"
        st.rerun()


# -----------------------------
# PAGE ROUTER (THIS WAS MISSING / BROKEN)
# -----------------------------
if st.session_state.page == "questionnaire":
    questionnaire_page()

elif st.session_state.page == "results":
    results_page()