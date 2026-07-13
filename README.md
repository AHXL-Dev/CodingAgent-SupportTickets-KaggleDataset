# Dataset Analysis Assistant

An agent that can write and run its own Python (pandas/matplotlib) to answer questions about a dataset. The dataset is heavily focused on a typical CRM support ticket situation, because I work with this kind of data regularly. The dataset is from Kaggle it is a PUBLICALLY available dataset, I always strive for data privacy and security so I will only ever use publically available datasets. 

In this app, you either click a pre-built "journey" card or just type your own question and it goes and figures out the answer by actually executing code, not by guessing from memory. I am not letting the LLM do any actual calculations! its all done in python.

** Note ** : Yes I am aware of all the data security issues with doing something like this in a corporate like environment, this is something i am still exploring further. One thing I have done is sandboxed it with only modules that I allow..

This is a prototype. There's plenty I could still add, but this is the extent of it for now.

## What it actually does

There are two ways into a conversation:

- **Card journeys** — a couple of pre-built questions (e.g. "which agents have the lowest CSAT scores") run a fixed, hardcoded pandas query, and the LLM's only job is to narrate the resulting table in plain English.

- **Ask your own question** — type anything about the dataset, and this time the LLM writes its own Python, which runs in a sandboxed executor (restricted builtins, no filesystem or network access, 30 second timeout) and the result gets fed back to it. It can call the tool multiple times in a row if it needs to refine its answer.

I've only allowed pandas,matplotlib and seaborn , and then the other normal inbuilt packages. I have done this deliberately but more could be added if wanted.

## Dataset

[eCommerce Customer Service Satisfaction](https://www.kaggle.com/datasets/ddosad/ecommerce-customer-service-satisfaction) by ddosad on Kaggle — one month of customer support tickets for a fictional platform, with category/sub-category, customer remarks, agent details, item price, and CSAT score. Per Kaggle, the underlying data is fabricated with the Faker library, so nothing here is real customer information.


## Stack

- Python 3.13, dependencies managed with `uv`
- Streamlit for the UI
- pandas / matplotlib / seaborn for the actual analysis
- OpenRouter, via the OpenAI Python SDK with the base URL swapped over

## About the model, and why you might see rate limit messages

This runs on OpenRouter's **free `openai/gpt-oss-20b`** tier. I have tried Deepseek V4 which worked amazingly, and actually GPT-OSS-20b works pretty well as well. I really want to try to test it further though to see if it generates alot of mistakes. 

Two things are worth knowing if you're poking around this publicly:

1. There's a self-imposed daily cap (150 requests/day, shown live in the app as "Requests today: X/150") so a burst of public traffic can't burn through the free quota in one sitting.
2. OpenRouter's free tier has its own throttling on top of that. If you see a message saying the model is rate limited, that's expected behaviour.

In my informal testing pretty much got 95% accuracy (outside of the eval page) 

## Evaluation

There's a separate `eval.py` page that runs a set of test questions, easy through to harder ones, comparing the LLM's answer against the correct answer computed directly in pandas. This is still a work in progress and I plan to keep adding harder questions to it.

## Known limitations / what's next

This is intentionally a small prototype, not a finished product. Things I know are missing or rough:

- Only two pre-built card journeys right now
- Eval question set is still fairly limited
- Everything assumes a single local CSV, no database backing
- I would love to put some date/time sliders especially in the prebuilt part so the user can select a timeframe, even with the prebuilt questions.

If you want to point this at your own data, swap the CSV in `data/` and rewrite the card journeys in `cards.py` to match.
