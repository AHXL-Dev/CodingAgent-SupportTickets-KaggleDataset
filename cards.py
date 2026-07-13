import pandas as pd
from executor import code_interpreter


CARD1_QUESTION = "Which agents have the lowest CSAT rate and how many tickets do they handle?"
CARD2_QUESTION = "Which product category generates the most complaints?"


def card1_lowest_csat_agents(df: pd.DataFrame) -> str:
    code = """
result = (
    df.groupby("Agent_name")["CSAT Score"]
    .agg(
        csat_rate=lambda x: round((x >= 4).sum() / len(x) * 100, 1),
        ticket_count="count"
    )
    .query("ticket_count >= 50")
    .sort_values("csat_rate")
    .head(5)
)
print(result.to_string())
"""
    return code_interpreter(code, df)["stdout"]


def card2_most_complaints_by_category(df: pd.DataFrame) -> str:
    code = """
result = (
    df.groupby("Product_category")["Unique id"]
    .count()
    .sort_values(ascending=False)
    .head(5)
    .rename("ticket_count")
)
print(result.to_string())
"""
    return code_interpreter(code, df)["stdout"]


def build_narration_prompt(question: str, table: str) -> str:
    return (
        f"Question: {question}\n\n"
        f"Data:\n{table}\n\n"
        f"Narrate this result conversationally for a business audience. "
        f"Do not fabricate any numbers — only use what is in the data above."
    )
