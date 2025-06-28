import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_API_URL = "https://aditya69690-100-hack.hf.space/api/chat"

def recommend_devrel_action(issue, model="tinyllama", min_word_count=10):
    title = issue.get("title", "")
    body = issue.get("body", "")
    label = issue.get("predicted_label", "unknown")
    context = issue.get("web_context") or "[No extra context]"

    system_prompt = "You are a Developer Relations (DevRel) assistant. Suggest clear, practical actions to improve GitHub issues."

    user_prompt = f"""
Label: {label}
Title: {title}
Body: {body}
Context: {context}

Suggest one specific, actionable DevRel improvement in 1–2 sentences. Avoid fluff or repeating the issue.
"""

    def call_llm(prompt_text, attempt):
        try:
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt_text}
                    ],
                    "stream": False
                },
                timeout=20
            )
            response.raise_for_status()
            return response.json()["message"]["content"].strip()
        except Exception as e:
            print(f"[LLM Error Attempt {attempt}] {e}")
            return ""

    for attempt in range(2):
        result = call_llm(user_prompt, attempt + 1)
        if result and "no suggestion" not in result.lower() and len(result.split()) >= min_word_count:
            return result
        time.sleep(1 + 2 * attempt)

    return "No suggestion available"
