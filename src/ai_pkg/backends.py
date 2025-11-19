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
    """Try to extract a JSON object or array from a text blob.

    Returns parsed JSON on success, or None on failure.
    """
    if not text:
        return None
    content = text.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Attempt to extract JSON object or array substrings
    for open_char, close_char in [('{', '}'), ('[', ']')]:
        start = content.find(open_char)
        end = content.rfind(close_char) + 1
        if start != -1 and end > start:
            payload = content[start:end]
            try:
                return json.loads(payload)
            except json.JSONDecodeError:
                logger.debug(f"Failed to parse JSON between {open_char}...{close_char}", exc_info=True)
                return None
    return None


def suggest_with_gemini(goal: str, api_key: str) -> Union[List[str], Dict[str, List[str]]]:
    """Suggest packages using Google Gemini SDK (google-genai) only.

    Returns either a list of package names (legacy) or a dict with keys 'packages' and 'env_steps'.
    If the SDK is not available or the call fails, an empty list is returned.
    """
    prompt_text = (
        "You are an expert Arch Linux package recommender and environment setup assistant. Your output must be a concise, machine-readable JSON object describing two keys:\n"
        "\n"
        "1) \"env_steps\": An ordered list of shell commands for environment creation and setup. This can include creating virtual environments (python -m venv, pipx, conda), setting up Docker containers, enabling and starting system services, or any preparation steps required before package installation. Always provide steps here even if minimal.\n"
        "\n"
        "2) \"packages\": A list of Arch Linux packages to install with pacman (official package names). For AUR packages, prefix with \"aur:\".\n"
        "\n"
        "IMPORTANT:\n"
        "- Respond with ONLY valid JSON. No Markdown, no backticks, no additional text.\n"
        "- Always include the \"env_steps\" key with at least an empty list if no steps are needed.\n"
        "- Commands should be idempotent and use \"--needed\" with pacman to skip already installed packages.\n"
        "\n"
        f"Task: Provide all environment setup steps and packages needed for the following goal:\n"
        f"\"{goal}\"\n"
        "\n"
        "Example response:\n"
        "{\n"
        "  \"env_steps\": [\n"
        "    \"python -m venv .venv\",\n"
        "    \"source .venv/bin/activate\",\n"
        "    \"sudo systemctl enable mongodb\",\n"
        "    \"sudo systemctl start mongodb\"\n"
        "  ],\n"
        "  \"packages\": [\"nodejs\", \"yarn\", \"mongodb\", \"git\"]\n"
        "}\n"
    )

    if genai is None:
        logger.error("google-genai SDK (genai) is not available; suggest_with_gemini requires the SDK")
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
                logger.warning("Gemini client transient error (attempt %d/%d): %s", attempt, max_attempts, e)
                time.sleep(2 ** (attempt - 1))

        # Extract text content safely from likely response shapes
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
            logger.error("Gemini client returned unexpected shape or empty text")
            return []

        parsed = _extract_json_from_text(text)
        if parsed is not None:
            return parsed

        logger.error("Could not extract JSON from Gemini client text")
        return []
    except Exception:
        logger.exception("Gemini client error")
        return []
