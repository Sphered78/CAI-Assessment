
import streamlit as st
import pandas as pd

# Load cleaned questions
questions = pd.read_csv("cleaned_questions.csv")

# Define Likert scale options
likert_options = {
    "1 - Never": 1,
    "2 - Rarely": 2,
    "3 - Half the time": 3,
    "4 - Most of the time": 4,
    "5 - Always": 5
}

# Define subdomain mapping based on question ranges
subdomain_mapping = {
    "Negative Interactions": range(1, 11),
    "Disappointments": range(11, 21),
    "Negative Social/Cultural": range(21, 31),
    "Nature of Task/Activity": range(31, 41),
    "Physical Environment": range(41, 51),
    "Medication": range(51, 61),
    "Illness": range(61, 71),
    "Physiological States": range(71, 81),
    "Sleep": range(81, 88),
    "Other Biological": range(88, 94)
}

# Reverse the mapping for lookup
question_to_subdomain = {}
for subdomain, q_range in subdomain_mapping.items():
    for q_num in q_range:
        question_to_subdomain[q_num] = subdomain

# Streamlit app
st.title("Contextual Assessment Inventory (CAI)")

st.markdown("Please complete the following 93 questions. For each, select a Likert scale response and optionally provide additional context.")

responses = []
text_responses = []

with st.form("cai_form"):
    for _, row in questions.iterrows():
        q_num = int(row["Number"])
        q_text = row["Question"]
        st.markdown(f"**Q{q_num}: {q_text}**")
        score = st.radio(f"Select a score for Q{q_num}", list(likert_options.keys()), key=f"score_{q_num}")
        text = st.text_input(f"Optional: Specify for Q{q_num}", key=f"text_{q_num}")
        responses.append((q_num, likert_options[score]))
        text_responses.append((q_num, text))
        st.markdown("---")

    submitted = st.form_submit_button("Submit Assessment")

if submitted:
    st.success("Assessment submitted successfully!")

    # Organize scores by subdomain
    subdomain_scores = {sub: [] for sub in subdomain_mapping}
    for q_num, score in responses:
        sub = question_to_subdomain[q_num]
        subdomain_scores[sub].append(score)

    # Calculate percentage of scores >= 3 per subdomain
    subdomain_percentages = {}
    for sub, scores in subdomain_scores.items():
        if scores:
            high_scores = [s for s in scores if s >= 3]
            percentage = (len(high_scores) / len(scores)) * 100
            subdomain_percentages[sub] = round(percentage, 2)

    # Sort subdomains by concern level
    sorted_subdomains = sorted(subdomain_percentages.items(), key=lambda x: x[1], reverse=True)

    st.header("Summary Report")
    st.markdown("### Subdomain Concern Levels (based on % of scores ≥ 3):")
    for sub, pct in sorted_subdomains:
        st.write(f"- **{sub}**: {pct}%")

    st.markdown("### Optional Text Responses:")
    for q_num, text in text_responses:
        if text.strip():
            st.write(f"**Q{q_num}**: {text}")
