import streamlit as st

st.title("Dataset Assistant")

st.markdown(
    """
### What is this?

An agent that can write and run its own Python (pandas/matplotlib) to answer
questions about a dataset. The dataset is heavily focused on a typical CRM
support ticket situation, because I work with this kind of data regularly.
The dataset is from Kaggle it is a PUBLICALLY available dataset, I always
strive for data privacy and security so I will only ever use publically
available datasets.

Card journeys: a couple of pre-built questions (e.g. "which agents have the
lowest CSAT scores") run a fixed, hardcoded pandas query, and the LLM's only
job is to narrate the resulting table in plain English.

Ask your own question: type anything about the dataset, and this time the LLM
writes its own Python, which runs in a sandboxed executor (restricted builtins,
no filesystem or network access, 30 second timeout) and the result gets fed
back to it. It can call the tool multiple times in a row if it needs to refine
its answer.

### What is the dataset?

eCommerce Customer Service Satisfaction by ddosad on Kaggle: one month of
customer support tickets for a fictional platform, with category/sub-category,
customer remarks, agent details, item price, and CSAT score. Per Kaggle, the
underlying data is fabricated with the Faker library, so nothing here is real
customer information.


Link is here: https://www.kaggle.com/datasets/ddosad/ecommerce-customer-service-satisfaction

*Note* i did make one change to the dataset, I added a text label mapping column for CSAT_Score column so that:
1 = Very Unsatisfied, 2 = Unsatisfied, 3 = Neutral, 4 = Satisfied, 5 = Very Satisfied.


### What is the eval page?

There's a separate eval.py page that runs a set of test questions, easy through
to harder ones, comparing the LLM's answer against the correct answer computed
directly in pandas. This is still a work in progress and I plan to keep adding
harder questions to it.

### Where do I want to go with this?

If successful

- Not just prebuilt journeys but journeys that are automatically derived and suggested BASED on a dataset loaded
- Prebuilt questions with further SUB GENERATED questions
- Date sliders
"""
)

st.divider()

if st.button("Let's start", type="primary", key="start_button"):
    st.switch_page("pages/dashboard.py")
