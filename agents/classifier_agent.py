import os
import time
from dotenv import load_dotenv
import requests

load_dotenv()

def classify_issue(issue_text, model="llama3", retries=3):
    prompt = f"""You are a helpful DevRel assistant. Categorize this GitHub issue into one of:
- bug
- feature
- question
- documentation
- discussion
Respond with the label only (one word).

Issue:
{issue_text}
"""

    for attempt in range(retries):
        try:
            res = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=30  # optional timeout
            )
            res.raise_for_status()  # raises HTTPError if 4xx or 5xx
            return res.json().get("response", "").strip().lower()
        except Exception as e:
            print(f"[Retry {attempt+1}/{retries}] Error: {e}")
            time.sleep(1 + 2 * attempt)  # basic exponential backoff

    return "unknown"
