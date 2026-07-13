import pandas as pd
import streamlit as st

'''
st.markdown(
    """

<style>
.st-key-explore_input input
{color: #ff0000;}
</style>
""",
    unsafe_allow_html=True,
)
st.text_input("Ask a question", key="explore_input")
'''
df = pd.read_csv("data/Customer_support_data.csv")
shape = df.shape
null_counts = df.isnull().sum()
null_lines = "\n".join(
    f"  {col}: {n} nulls ({n / shape[0] * 100:.1f}%)"
    for col, n in null_counts.items()
    if n > 0
)
categorical_column_counts = []
for col in df.select_dtypes(include="str").columns:
    if (col in ("Unique id", "Order_id")) or (df[col].nunique() > 50):
        continue
    highest_counts = df[col].value_counts().head(5)
    highest_count_str = ", ".join(
        f"'{dimension}'({count})" for dimension, count in highest_counts.items()
    )
    categorical_column_counts.append(f"  {col}: {highest_count_str}")
cat_dist = "\n".join(categorical_column_counts)
print(cat_dist)


import pandas as pd

df = pd.read_csv("data/Customer_support_data.csv")
print("All columns:", df.columns.tolist())
print("\nShape:", df.shape)

# date column details
print("\nSurvey_response_Date samples:", df["Survey_response_Date"].head(5).tolist())
print("Survey_response_Date dtype:", df["Survey_response_Date"].dtype)

# numeric columns
for col in df.select_dtypes(include=["float64", "int64"]).columns:
    print(
        f"\n{col}: min={df[col].min()}, mean={df[col].mean():.2f}, max={df[col].max()}"
    )

import pandas as pd

df = pd.read_csv("data/Customer_support_data.csv")
print("All columns:", df.columns.tolist())
print("\nShape:", df.shape)
for col in df.select_dtypes(include=["float64", "int64"]).columns:
    print(
        f"\n{col}: min={df[col].min()}, mean={df[col].mean():.2f}, max={df[col].max()}"
    )
