tools = [
    {
        "type": "function",
        "function": {
            "name": "code_interpreter",
            "strict": True,
            "description": "Executes Python code and returns stdout/stderr. Supports plotting with plt and sns; call save_plot() to save and register a chart.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Python code to execute.",
                    }
                },
                "required": ["code"],
                "additionalProperties": False,
            },
        },
    }
]
