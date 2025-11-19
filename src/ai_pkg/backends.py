import json
import logging
import time
import requests
from typing import Any

try:
    from google import genai
except Exception:
    genai = None

logger = logging.getLogger(__name__)


def _extract_json_from_text(text: str) -> Any:
    """Try to extract a JSON object or array from a text blob.

    Returns parsed JSON on success, or None on failure.
    """
    if not text:
        return None
    content = text.strip()
    # Try to parse whole text first
    try:
        return json.loads(content)
    except Exception:
        pass

    # Find first JSON-like substring (object or array)
    if '{' in content:
        start = content.find('{')
        end = content.rfind('}') + 1
        if end > start:
            payload = content[start:end]
            try:
                return json.loads(payload)
            except Exception:
                logger.debug('Failed to parse JSON object payload', exc_info=True)
                return None
    if '[' in content:
        start = content.find('[')
        end = content.rfind(']') + 1
        if end > start:
            payload = content[start:end]
            try:
                return json.loads(payload)
            except Exception:
                logger.debug('Failed to parse JSON array payload', exc_info=True)
                return None

    return None


def suggest_with_gemini(goal: str, api_key: str):
    """Suggest packages using Google Gemini API via google-genai client if available, otherwise fallback to REST.

    Returns either a list of package names (legacy) or a dict with keys 'packages' and 'env_steps'.
    """
    prompt_text = (
        "You are an Arch Linux package recommender and environment setup assistant. Your job is to produce a concise, machine-readable JSON object describing:\n"
        "  1) any environment creation steps (virtualenvs, venvs, python -m venv, python -m pipx, conda envs, docker commands) as an ordered list of shell commands under the key 'env_steps'.\n"
        "  2) a list of Arch packages (official pacman names) under the key 'packages'. For AUR packages, prefix the name with 'aur:' (for example 'aur:google-chrome').\n"
        "IMPORTANT: Respond with ONLY valid JSON (no markdown, no surrounding backticks). The JSON must be either an object with keys 'packages' and 'env_steps', or simply an array of package names (legacy).\n"
        f"Task: Provide environment steps and packages needed to {goal}\n"
        "Prefer pacman package names and keep commands idempotent. When suggesting pacman install commands, prefer using '--needed' so packages already installed are skipped.\n"
        "Example object response: {\"env_steps\": [\"python -m venv .venv\", \"source .venv/bin/activate\"], \"packages\": [\"python\", \"git\"] }\n"
    )

    # Prefer using google-genai client
    if genai is not None:
        try:
            client = genai.Client()
            # Retry a few times for transient server-side overloads (503).
            max_attempts = 3
            response = None
            for attempt in range(1, max_attempts + 1):
                try:
                    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_text)
                    break
                except Exception as e:
                    # If this was the last attempt, re-raise to be caught by outer except
                    if attempt == max_attempts:
                        raise
                    logger.warning('Gemini client transient error (attempt %d/%d): %s', attempt, max_attempts, e)
                    # exponential backoff
                    time.sleep(2 ** (attempt - 1))
            # Attempt to extract text safely from likely response shapes
            text = None
            try:
                text = response.candidates[0].content.parts[0].text
            except Exception:
                try:
                    text = response.candidates[0].content[0].text
                except Exception:
                    try:
                        text = response.candidates[0].content.text
                    except Exception:
                        text = None
            if not text:
                logger.warning('Gemini client returned unexpected shape; falling back to REST')
            else:
                parsed = _extract_json_from_text(text)
                if parsed is not None:
                    return parsed
                logger.warning('Could not extract JSON from Gemini client text; falling back to REST')
        except Exception:
            logger.exception('Gemini client error; falling back to REST')

    # Fallback REST path
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": prompt_text}]}
        ],
        "generationConfig": {"responseMimeType": "text/plain", "candidateCount": 1, "temperature": 0.1}
    }
    params = {"key": api_key}

    try:
        resp = requests.post(url, headers=headers, params=params, json=data)
        resp.raise_for_status()
        result = resp.json()
        if "error" in result:
            logger.error('Gemini API error: %s', result["error"].get("message", "Unknown error"))
            return []

        # attempt to get text from several shapes
        text = None
        try:
            text = result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            try:
                text = result["candidates"][0]["content"][0]["text"]
            except Exception:
                try:
                    text = result["candidates"][0]["text"]
                except Exception:
                    text = None

        if not text:
            logger.error('Gemini REST response unexpected. Full response: %s', result)
            return []

        parsed = _extract_json_from_text(text)
        if parsed is not None:
            return parsed

        logger.error('Could not extract valid JSON from Gemini response text')
        return []
    except requests.exceptions.RequestException:
        logger.exception('Network error when calling Gemini REST API')
        return []
    except Exception:
        logger.exception('Unexpected error in suggest_with_gemini')
        return []