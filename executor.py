import io
import os
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeout

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

PLOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "plots")


def code_interpreter(
    code: str,
    df: pd.DataFrame,
    namespace: dict | None = None,
    timeout_seconds: int = 30,
) -> dict:
    stdout_capture = io.StringIO()
    stderr = ""
    exit_code = 0  # Convention for ok, if this goes wrong we change it to 1
    plot_paths: list[str] = []

    def save_plot() -> str:
        os.makedirs(PLOTS_DIR, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.png"
        path = os.path.join(PLOTS_DIR, filename)
        plt.savefig(path, bbox_inches="tight")
        plt.close("all")
        plot_paths.append(path)
        return path

    restricted_builtins = {
        "print": lambda *args, **kwargs: print(*args, **kwargs, file=stdout_capture),
        "range": range,
        "len": len,
        "list": list,
        "dict": dict,
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "enumerate": enumerate,
        "zip": zip,
        "map": map,
        "filter": filter,
        "sorted": sorted,
        "sum": sum,
        "min": min,
        "max": max,
        "abs": abs,
        "round": round,
        "isinstance": isinstance,
        "type": type,
    }

    if namespace is None:
        namespace = {
            "df": df,
            "pd": pd,
            "plt": plt,
            "sns": sns,
            "save_plot": save_plot,
        }
    namespace["__builtins__"] = restricted_builtins

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(lambda: exec(code, namespace))
        try:
            future.result(timeout=timeout_seconds)  # code must complete in 30 seconds
        except FuturesTimeout:
            stderr = "Execution timed out"
            exit_code = 1  # exit with error code 1
        except Exception:
            stderr = traceback.format_exc()  # so i can get the error details
            exit_code = 1

    return {
        "stdout": stdout_capture.getvalue(),
        "stderr": stderr,
        "exit_code": exit_code,
        "result": {"plots": plot_paths} if plot_paths else None,
        "namespace": namespace,
    }
