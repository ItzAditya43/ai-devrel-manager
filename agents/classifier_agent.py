import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def classify_issue(issue_text, model="llama3", retries=2):
    prompt = f"""You are a helpful DevRel assistant. Categorize this GitHub issue into one of:
- bug
- feature
- question
- documentation
- discussion

Respond with the label only (one word, lowercase).

Issue:
{issue_text}
"""

    def call_llm(prompt_text, attempt):
        try:
            res = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt_text, "stream": False},
                timeout=20
            )
            res.raise_for_status()
            return res.json().get("response", "").strip().split()[0].lower()
        except Exception as e:
            print(f"[Classifier Error Attempt {attempt}] {e}")
            print("📦 Prompt sent:\n", prompt_text[:200])
            return "unknown"

    for attempt in range(retries):
        result = call_llm(prompt, attempt + 1)
        if result in {"bug", "feature", "question", "documentation", "discussion"}:
            return result
        time.sleep(1 + 2 * attempt)

    return "unknown"
