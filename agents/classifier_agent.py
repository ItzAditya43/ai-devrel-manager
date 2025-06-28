import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_API_URL = "https://aditya69690-100-hack.hf.space/api/chat"

def classify_issue(issue_text, model="tinyllama", retries=2):
    system_prompt = "You are a GitHub issue classifier. Respond only with one label: bug, feature, question, documentation, or discussion."
    user_prompt = f"""Classify this GitHub issue:
---
{issue_text}
---
Just return the label (one word, lowercase).
"""

    def call_llm(prompt_text, attempt):
        try:
            res = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt_text}
                    ],
                    "stream": False
                },
                timeout=15
            )
            res.raise_for_status()
            return res.json()["message"]["content"].strip().split()[0].lower()
        except Exception as e:
            print(f"[Classifier Error Attempt {attempt}] {e}")
            return "unknown"

    for attempt in range(retries):
        result = call_llm(user_prompt, attempt + 1)
        if result in {"bug", "feature", "question", "documentation", "discussion"}:
            return result
        time.sleep(1 + 2 * attempt)

    return "unknown"
