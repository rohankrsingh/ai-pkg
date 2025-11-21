import json
import logging
import time
from typing import Any, Union, List, Dict

try:
    from google import genai
except Exception:
    genai = None

logger = logging.getLogger(__name__)


def _extract_json_from_text(text: str) -> Any:
    """Extract JSON object or array from text."""
    if not text:
        return None
    content = text.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    for open_char, close_char in [('{', '}'), ('[', ']')]:
        start = content.find(open_char)
        end = content.rfind(close_char) + 1
        if start != -1 and end > start:
            try:
                return json.loads(content[start:end])
            except json.JSONDecodeError:
                logger.debug(f"Failed to parse JSON {open_char}...{close_char}", exc_info=True)
    return None


def suggest_with_gemini(goal: str, api_key: str) -> Union[List[str], Dict[str, List[str]]]:
    """Suggest packages using Google Gemini SDK.

    Returns dict with 'packages' and 'env_steps' keys, or empty list on failure.
    """
    prompt_text = (
        "You are an Arch Linux package and dev environment assistant. Return ONLY valid JSON with two keys:\n"
        "\n"
        "1. \"env_steps\": Shell commands for setup (mkdir, venv, npm/pip install, service config). Use [] for simple installs.\n"
        "2. \"packages\": Arch packages (official names). Prefix AUR with \"aur:\" (e.g., \"aur:google-chrome\").\n"
        "\n"
        "Rules:\n"
        "- JSON only, no markdown/backticks\n"
        "- Empty env_steps for package installs only\n"
        "- Full env_steps for dev environments/projects\n"
        "- Use --needed with pacman\n"
        "\n"
        f"Task: {goal}\n"
        "\n"
        "Examples:\n"
        "\"install vlc git\" → {\"env_steps\": [], \"packages\": [\"vlc\", \"git\"]}\n"
        "\n"
        "\"create django dev\" → {\"env_steps\": [\"mkdir project && cd project\", \"python -m venv .venv\", \"source .venv/bin/activate\", \"pip install django\"], \"packages\": [\"python\", \"python-pip\", \"git\"]}\n"
        "\n"
        "\"create react project named app1 with tailwind\" → {\"env_steps\": [\"npm create vite@latest app1 -- --template react\", \"cd app1\", \"npm install\", \"npm install -D tailwindcss postcss autoprefixer\", \"npx tailwindcss init -p\"], \"packages\": [\"nodejs\", \"npm\", \"git\"]}\n"
    )

    if genai is None:
        logger.error("google-genai SDK not available")
        return []

    try:
        client = genai.Client()
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_text)
                break
            except Exception as e:
                if attempt == max_attempts:
                    raise
                logger.warning("Gemini error (attempt %d/%d): %s", attempt, max_attempts, e)
                time.sleep(2 ** (attempt - 1))

        # Extract text from response
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
                    pass

        if not text:
            logger.error("Gemini returned empty text")
            return []

        parsed = _extract_json_from_text(text)
        if parsed is not None:
            return parsed

        logger.error("Could not extract JSON from Gemini text")
        return []
    except Exception:
        logger.exception("Gemini client error")
        return []
