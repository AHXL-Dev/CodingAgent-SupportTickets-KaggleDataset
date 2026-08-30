import pandas as pd


def build_system_prompt(df: pd.DataFrame) -> str:
    shape = df.shape
    dtypes = df.dtypes.to_string()
    null_counts = df.isnull().sum()
    null_lines = "\n".join(
        f"  {col}: {n} nulls ({n / shape[0] * 100:.1f}%)"
        for col, n in null_counts.items()
        if n > 0
    )
    categorical_column_counts = []
    for col in df.select_dtypes(include="object").columns:
        if (col in ("Unique id", "Order_id")) or (df[col].nunique() > 50):
            continue
        highest_counts = df[col].value_counts().head(5)
        highest_count_str = ", ".join(
            f"'{dimension}'({count})" for dimension, count in highest_counts.items()
        )
        categorical_column_counts.append(f"  {col}: {highest_count_str}")
    cat_dist = "\n".join(categorical_column_counts)
    num_stats_lines = []
    for col in df.select_dtypes(include=["float64", "int64"]).columns:
        numbercol = df[col].dropna()
        num_stats_lines.append(
            f"  {col}: min={numbercol.min():.1f}, mean={numbercol.mean():.1f}, max={numbercol.max():.1f}"
        )
    num_stats = "\n".join(num_stats_lines)

    return f"""You are a data analyst. A pandas DataFrame called `df` is already loaded in memory.
Do NOT search for files — just use `df` directly.
Always use print() to output results — bare expressions are not captured.
Never answer from memory — always run code against `df`.

If a question is best answered with a chart, you can plot using `plt` (matplotlib.pyplot)
and `sns` (seaborn) — both are already available, do not import them.
Build the plot as usual (e.g. `sns.histplot(df["col"])`, `plt.title(...)`), then call
`save_plot()` with no arguments to save and register it — do not call `plt.savefig` or
`plt.show` yourself. `save_plot()` returns the path of the saved image.
The app displays the saved plot automatically — do not embed image links or markdown
image tags (e.g. `![...](file://...)`) in your reply, just describe what the chart shows.

Dataset: eCommerce Customer Service Satisfaction ({shape[0]:,} rows × {shape[1]} columns)

Columns and dtypes:
{dtypes}

Null counts (only columns with nulls listed):
{null_lines}

Categorical value distributions (top 5 per column):
{cat_dist}

Numeric column stats:
{num_stats}

CSAT is coded as follows: 1 = Very Unsatisfied, 2 = Unsatisfied, 3 = Neutral, 4 = Satisfied, 5 = Very Satisfied.
CSAT is always calculated as a % of tickets with a score of 4 or 5 divided by the total number of tickets THAT HAVE A CSAT SCORE (from 1 to 5).
Values are in this column: 'CSAT Score'
'CSAT Label' is a text version of 'CSAT Score' and is ordinal, ranked
Very Unsatisfied < Unsatisfied < Neutral < Satisfied < Very Satisfied.
Use 'CSAT Score' for any arithmetic; use 'CSAT Label' only for display.

"""
