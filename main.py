import json
import os
import re

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI,RateLimitError
from executor import code_interpreter
from tools import tools

load_dotenv()
api_key = os.getenv("OPENROUTER")
MODEL_NAME = "openai/gpt-oss-20b:free"
client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

LOCAL_IMAGE_LINK_RE = re.compile(r"!\[[^\]]*\]\(file://[^)]*\)")


def strip_local_image_links(content: str) -> str:
    return LOCAL_IMAGE_LINK_RE.sub("", content).strip()


def run_agent_turn(
    user_message: str, history: list, df: pd.DataFrame
) -> tuple[str, list]:
    history.append({"role": "user", "content": user_message})
    execution_result = None
    namespace = None
    bad_args_retries = 0
    MAX_BAD_ARGS_RETRIES = 6

    while True:
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=history,
                tools=tools,
                extra_headers={"x-or-beta-structured-outputs-2025-11-13": "true"},
            )
        except RateLimitError:
            return (
                "The model is currently rate limited — please try again in a minute.",
                history,
            )
        message = response.choices[0].message
        print(f"[message] {message}")
        history.append(message.model_dump(exclude_none=True))

        if not message.tool_calls:
            if message.content:
                print(message.content)
                return strip_local_image_links(message.content), history
            elif execution_result:
                return execution_result["stdout"], history
            else:
                return (
                    "[no response]",
                    history,
                )

        for tool_call in message.tool_calls:
            try:
                args = json.loads(tool_call.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            # I had to add this later because GPT OSS which is a weaker model had to retry and i had not really allowed for that in my code.
            if "code" not in args:
                bad_args_retries += 1
                if bad_args_retries > MAX_BAD_ARGS_RETRIES:
                    return (
                        "The model failed to call the tool correctly after several attempts. Please rephrase your question.",
                        history,
                    )
                history.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(
                            {
                                "error": "no code provided, please retry with valid arguments"
                            }
                        ),
                    }
                )
                continue

            execution_result = code_interpreter(args["code"], df, namespace=namespace)
            namespace = execution_result.pop("namespace")
            print(f"[tool result] {execution_result}")
            history.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(execution_result),
                }
            )
