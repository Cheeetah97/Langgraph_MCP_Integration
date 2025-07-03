import os
from langchain_openai import ChatOpenAI
from functools import lru_cache
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

@lru_cache(maxsize = 10)
def _get_model(
    name: str,
    temp: Optional[float] = None,
    max_tokens: Optional[int] = None,
    fp: Optional[float] = None,
    pp: Optional[float] = None
):

    if name == 'openai':
        kwargs = {
            "model": "gpt-4.1-mini-2025-04-14",
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "max_retries": 2
        }
        if temp is not None:
            kwargs["temperature"] = temp
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens
        if fp is not None:
            kwargs["frequency_penalty"] = fp
        if pp is not None:
            kwargs["presence_penalty"] = pp

        model = ChatOpenAI(**kwargs)
    
    elif name == 'openai-pro':
        kwargs = {
            "model": "o3-mini",
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "max_retries": 2
        }

        model = ChatOpenAI(**kwargs)

    else:
        raise ValueError(f"Unsupported Model Name: {name}")

    return model
