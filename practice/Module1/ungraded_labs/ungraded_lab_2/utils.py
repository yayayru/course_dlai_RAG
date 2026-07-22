import requests
import json
import os
from pathlib import Path
from typing import List, Dict
from together import Together

def _load_dotenv_from_parents():
    """
    Load simple KEY=VALUE pairs from the nearest .env file.
    This keeps the notebook runnable without adding python-dotenv.
    """
    current_dir = Path(__file__).resolve().parent
    for directory in (current_dir, *current_dir.parents):
        env_path = directory / ".env"
        if not env_path.exists():
            continue
        for line in env_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and not os.environ.get(key):
                os.environ[key] = value
        break

def _with_bearer_prefix(api_key):
    if not api_key:
        return ""
    if api_key.lower().startswith("bearer "):
        return api_key
    return f"Bearer {api_key}"

def _without_bearer_prefix(api_key):
    if api_key.lower().startswith("bearer "):
        return api_key[7:].strip()
    return api_key

_load_dotenv_from_parents()

def get_proxy_url():
    """
    Get the proxy URL from environment variable or fall back to Together.ai endpoint.
    Uses TOGETHER_BASE_URL environment variable set in Dockerfile.
    Defaults to https://api.together.xyz/ if not set.
    """
    return os.environ.get('TOGETHER_BASE_URL', 'https://api.together.xyz/')

def get_proxy_headers():
    """
    Get the appropriate headers for API calls based on the platform.
    Returns Authorization header with Together API key if available.
    """
    api_key = get_together_key()
    if not api_key:
        return {}
    return {"Authorization": _with_bearer_prefix(api_key)}

def get_together_key():
    """
    Get the Together API key from environment variables.
    """
    return os.environ.get("TOGETHER_API_KEY", "")

def generate_with_single_input(prompt: str,
                               role: str = 'user',
                               top_p: float = None,
                               temperature: float = None,
                               max_tokens: int = 500,
                               model: str ="Qwen/Qwen3.5-9B",
                               together_api_key = None,
                              **kwargs):

    # Remove None parameters for Together API - don't set to string 'none'
    if top_p is None:
        payload_top_p = None
    else:
        payload_top_p = top_p
    if temperature is None:
        payload_temperature = None
    else:
        payload_temperature = temperature

    payload = {
        "model": model,
        "messages": [{'role': role, 'content': prompt}],
        "max_tokens": max_tokens,
        "reasoning": {"enabled": False},
        **kwargs
    }
    # Only add temperature and top_p if they're not None
    if payload_temperature is not None:
        payload["temperature"] = payload_temperature
    if payload_top_p is not None:
        payload["top_p"] = payload_top_p

    together_api_key = together_api_key or get_together_key()

    if not together_api_key:
        url = os.path.join(get_proxy_url(), 'v1/chat/completions')
        response = requests.post(url, json = payload, headers = get_proxy_headers(), verify=False)
        if not response.ok:
            raise Exception(f"Error while calling LLM: {response.text}")
        try:
            json_dict = json.loads(response.text)
        except Exception as e:
            raise Exception(f"Failed to get correct output from LLM call.\nException: {e}\nResponse: {response.text}")
    else:
        client = Together(api_key = _without_bearer_prefix(together_api_key))
        json_dict = client.chat.completions.create(**payload).model_dump()
        json_dict['choices'][-1]['message']['role'] = json_dict['choices'][-1]['message']['role'].name.lower()
    try:
        output_dict = {'role': json_dict['choices'][-1]['message']['role'], 'content': json_dict['choices'][-1]['message']['content']}
    except Exception as e:
        raise Exception(f"Failed to get correct output dict. Please try again. Error: {e}")
    return output_dict


def generate_with_multiple_input(messages: List[Dict],
                               top_p: float = None,
                               temperature: float = None,
                               max_tokens: int = 500,
                               model: str ="Qwen/Qwen3.5-9B",
                                together_api_key = None,
                                **kwargs):
    # Remove None parameters for Together API
    if top_p is None:
        payload_top_p = None
    else:
        payload_top_p = top_p
    if temperature is None:
        payload_temperature = None
    else:
        payload_temperature = temperature

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "reasoning": {"enabled": False},
        **kwargs
    }
    # Only add temperature and top_p if they're not None
    if payload_temperature is not None:
        payload["temperature"] = payload_temperature
    if payload_top_p is not None:
        payload["top_p"] = payload_top_p

    together_api_key = together_api_key or get_together_key()

    if not together_api_key:
        url = os.path.join(get_proxy_url(), 'v1/chat/completions')
        response = requests.post(url, json = payload, headers = get_proxy_headers(), verify=False)
        if not response.ok:
            raise Exception(f"Error while calling LLM: {response.text}")
        try:
            json_dict = json.loads(response.text)
        except Exception as e:
            raise Exception(f"Failed to get correct output from LLM call.\nException: {e}\nResponse: {response.text}")
    else:
        client = Together(api_key = _without_bearer_prefix(together_api_key))
        json_dict = client.chat.completions.create(**payload).model_dump()
        json_dict['choices'][-1]['message']['role'] = json_dict['choices'][-1]['message']['role'].name.lower()
    try:
        output_dict = {'role': json_dict['choices'][-1]['message']['role'], 'content': json_dict['choices'][-1]['message']['content']}
    except Exception as e:
        raise Exception(f"Failed to get correct output dict. Please try again. Error: {e}")
    return output_dict
