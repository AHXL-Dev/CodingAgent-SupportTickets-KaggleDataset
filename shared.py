import datetime
import json
import pandas as pd
import streamlit as st
DAILY_LIMIT = 150
COUNTER_PATH = "data/counter.json"
def read_counter() -> dict:
    try:
        with open(COUNTER_PATH) as f:
            return json.load(f)
    except (FileNotFoundError,json.JSONDecodeError):
        return {"date": "","count": 0}

def write_counter(data:dict) -> None:
    with open(COUNTER_PATH, "w") as f:
        json.dump(data, f)

def is_limit_reached() -> bool:
    data = read_counter()
    today = datetime.date.today().isoformat()
    if data["date"] != today:
        return False
    return data["count"] >= DAILY_LIMIT

def increment_counter() -> int:
    data = read_counter()
    today = datetime.date.today().isoformat()
    if data["date"] != today:
        data = {"date": today, "count": 0}
    data["count"] += 1
    write_counter(data)
    return data["count"]

def current_count() -> int:
    data = read_counter()
    today = datetime.date.today().isoformat()
    if data["date"] != today:
        return 0
    return data["count"]

@st.cache_resource
def load_data() -> pd.DataFrame:
    return pd.read_csv("data/Customer_support_data.csv")
