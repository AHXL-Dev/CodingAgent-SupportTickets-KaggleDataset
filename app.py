import streamlit as st

from main import MODEL_NAME

st.set_page_config(page_title="Dataset Assistant")
st.subheader(f"Using model: {MODEL_NAME}")

dashboard_page = st.Page("pages/dashboard.py", title="Dashboard")
eval_page = st.Page("pages/eval.py", title="Eval")

pg = st.navigation([dashboard_page, eval_page])
pg.run()
