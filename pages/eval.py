import pandas as pd
import streamlit as st

from executor import code_interpreter
from main import run_agent_turn, MODEL_NAME
from shared import load_data, is_limit_reached, increment_counter,current_count,DAILY_LIMIT
from system_prompt import build_system_prompt
from tools import tools

df = load_data()


if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": build_system_prompt(df)}]

question_1 = "How many rows in the dataframe?"
question_1_answer = len(df)

question_2 = "What is the average CSAT score?"
question_2_answer = df["CSAT Score"].mean()
question_3 = "What are the top 5 product categories?"
question_3_answer = (
    df.groupby("Product_category")["Unique id"]
    .agg("count")
    .sort_values(ascending=False)
    .head(5)
)
question_4 = "Show me the CSAT % by agent shift ranked highest to lowest."
question_4_answer = (
    df.groupby("Agent Shift")["CSAT Score"]
    .agg(lambda x: (x.isin([4, 5]).sum() / len(x)) * 100)
    .sort_values(ascending=False)
)
question_5 = "What is the average connected handling time for 'Electronic' tickets handled during the morning shift?"

question_5_answer = round(
    df[(df["Product_category"] == "Electronics") & (df["Agent Shift"] == "Morning")][
        "connected_handling_time"
    ].mean(),
    1,
)

question_6 = "Which month had the most tickets submitted?"
question_6_answer = (
    pd.to_datetime(df["Survey_response_Date"], format="%d-%b-%y")
    .dt.to_period("M")
    .value_counts()
    .index[0]
    .strftime("%B %Y")
)


def run_eval_question(key_suffix: str) -> None:
    st.session_state[f"run_eval_{key_suffix}"] = True


def render_eval_row(question: str, expected_answer: str, key_suffix: str) -> None:
    st.button(
        question,
        use_container_width=True,
        on_click=run_eval_question,
        args=(key_suffix,),
    )

    if st.session_state.get(f"run_eval_{key_suffix}"):
        if is_limit_reached():
            st.warning("This demo has reached its daily request limit. Please check back tomorrow.")
            st.stop()
        with st.spinner("Running evaluation..."):
            answer, updated_history = run_agent_turn(
                question, st.session_state.messages, df
            )
            st.session_state[f"eval_answer_{key_suffix}"] = answer
            st.session_state.messages = updated_history
        increment_counter()
        st.session_state[f"run_eval_{key_suffix}"] = False

    if f"eval_answer_{key_suffix}" in st.session_state:
        st.write(st.session_state[f"eval_answer_{key_suffix}"])
        st.write(f"Correct answer is: {expected_answer}")


st.title("How well is our LLM answering queries?")

st.caption(f"Model: {MODEL_NAME}. Requests today: {current_count()}/{DAILY_LIMIT}")
st.subheader("Pick a question to check!")
row1 = st.container()
row2 = st.container()
row3 = st.container()
row4 = st.container()
row5 = st.container()
row6 = st.container()
with row1:
    render_eval_row(question_1, f"{question_1_answer}", "1")

with row2:
    render_eval_row(question_2, f"{question_2_answer:.2f}", "2")
with row3:
    render_eval_row(question_3, f"{question_3_answer.to_dict()}", "3")
with row4:
    render_eval_row(question_4, f"{question_4_answer.to_dict()}", "4")
with row5:
    render_eval_row(question_5, f"{question_5_answer}", "5")
with row6:
    render_eval_row(question_6, f"{question_6_answer}", "6")
