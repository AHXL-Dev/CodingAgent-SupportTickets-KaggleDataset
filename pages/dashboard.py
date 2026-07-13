import json
import os

import streamlit as st

from cards import (
    CARD1_QUESTION,
    CARD2_QUESTION,
    build_narration_prompt,
    card1_lowest_csat_agents,
    card2_most_complaints_by_category,
)
from main import run_agent_turn, MODEL_NAME
from shared import load_data,is_limit_reached,increment_counter,current_count,DAILY_LIMIT
from system_prompt import build_system_prompt

df = load_data()

# The following is CSS code, for:
# the input text box on the first page. We are referring to the CSS element 'input' AND the continue exploration after a card is clicked or a comment is asked
# There are two things here
# # linear_gradient for the whole textarea within the textbox and border with another colour
# # We also make the text inside this box a different colour as well
# # I KNOW IT DOESNT LOOK GOOD, GO AHEAD AND CHANGE IT IF YOU WANT :)
#

st.markdown(
    """
    <style>
    .st-key-explore_input input,
    .st-key-continue_input textarea {
        background: linear-gradient(to bottom, #eaf4ff 0%, #7fbfff 100%);
        border: 1px solid #4d9bdb;
        color: #07203a;
    }
    </style>
    """,
    unsafe_allow_html=True,  # Given we are hardcoding CSS.. there is no unsafe HTML so have to set this to true otherwise it doesnt render. LLM is not generating this stuff so it should be ok
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": build_system_prompt(df)}]

st.title("Analysis of Customer Ticket Dataset")
st.caption(f"Model: {MODEL_NAME}. Requests today: {current_count()}/{DAILY_LIMIT}")
with st.expander("Preview dataset", expanded=False):
    st.caption(f"{len(df):,} rows · {len(df.columns)} columns")
    st.dataframe(df.head(10), width="stretch")

st.space("medium")

for message in st.session_state.messages:
    role = message["role"]
    if role == "tool":
        try:
            result = json.loads(message["content"]).get("result")
        except (json.JSONDecodeError, TypeError):
            result = None
        if result and result.get("plots"):
            with st.chat_message("assistant"):
                for path in result["plots"]:
                    if os.path.exists(path):
                        st.image(path)
    elif role in ("user", "assistant") and message.get("content"):
        with st.chat_message(role):
            st.markdown(message["content"])

if len(st.session_state.messages) == 1:
    st.subheader("What would you like to explore?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button(CARD1_QUESTION, use_container_width=True):
            if is_limit_reached():
                st.warning("This demo has reached its daily request limit. Please check back tomorrow.")
                st.stop()
            with st.spinner("Analysing... please wait"):
                table = card1_lowest_csat_agents(df)
                prompt = build_narration_prompt(CARD1_QUESTION, table)
                answer, updated_history = run_agent_turn(
                    prompt, st.session_state.messages, df
                )
            increment_counter()
            st.session_state.messages = updated_history
            st.rerun()

    with col2:
        if st.button(CARD2_QUESTION, use_container_width=True):
            if is_limit_reached():
                st.warning("This demo has reached its daily request limit. Please check back tomorrow.")
                st.stop()
            with st.spinner("Analysing... please wait"):
                table = card2_most_complaints_by_category(df)
                prompt = build_narration_prompt(CARD2_QUESTION, table)
                answer, updated_history = run_agent_turn(
                    prompt, st.session_state.messages, df
                )
            increment_counter()
            st.session_state.messages = updated_history
            st.rerun()

    st.space("medium")
    st.divider()
    st.caption("Or explore the dataset yourself!")

    free_text = st.text_input(
        "Ask a question about the dataset...", key="explore_input"
    )
    if st.button("Ask", key="explore_submit") and free_text:
        if is_limit_reached():
            st.warning("This demo has reached its daily request limit. Please check back tomorrow.")
            st.stop()
        with st.chat_message("user"):
            st.markdown(free_text)

        previous_message_count = len(st.session_state.messages)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer, updated_history = run_agent_turn(
                    free_text, st.session_state.messages, df
                )
            for message in updated_history[previous_message_count:]:
                if message["role"] != "tool":
                    continue
                try:
                    result = json.loads(message["content"]).get("result")
                except (json.JSONDecodeError, TypeError):
                    result = None
                if result and result.get("plots"):
                    for path in result["plots"]:
                        if os.path.exists(path):
                            st.image(path)
            st.markdown(answer)
        increment_counter()
        st.session_state.messages = updated_history
        st.rerun()

else:
    st.markdown("##### Want to dive further? Ask away!")
    with st.container():
        prompt = st.chat_input("Explore this journey further...", key="continue_input")

    if prompt:
        if is_limit_reached():
            st.warning("This demo has reached its daily request limit. Please check back tomorrow.")
            st.stop()
        with st.chat_message("user"):
            st.markdown(prompt)
        previous_message_count = len(st.session_state.messages)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer, updated_history = run_agent_turn(
                    prompt, st.session_state.messages, df
                )
            for message in updated_history[previous_message_count:]:
                if message["role"] != "tool":
                    continue
                try:
                    result = json.loads(message["content"]).get("result")
                except (json.JSONDecodeError, TypeError):
                    result = None
                if result and result.get("plots"):
                    for path in result["plots"]:
                        if os.path.exists(path):
                            st.image(path)
            st.markdown(answer)
        increment_counter()
        st.session_state.messages = updated_history
        st.rerun()

    if st.button("↩ Back to explore"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()
