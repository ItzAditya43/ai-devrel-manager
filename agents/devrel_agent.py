import requests
import time

def recommend_devrel_action(issue, model="llama3", min_word_count=20):
    title = issue.get("title", "")
    body = issue.get("body", "")
    label = issue.get("predicted_label", "unknown")
    context = issue.get("web_context") or "[No external context found]"

    # 🎯 Refined DevRel LLM Prompt
    prompt = f"""
You are a Developer Relations (DevRel) strategist AI.

Your task: suggest one **concrete and specific** DevRel action that can help improve or resolve the GitHub issue below. This could include writing a guide, improving docs, adding examples, hosting a discussion, or clarifying errors.

Avoid generalizations. Focus on **useful, actionable** improvements. You may use the external context if helpful.

---
Label: {label}

Title:
{title}

Body:
{body}

External Context:
{context}
---

🧠 Respond in **under 120 words**, ideally 3–5 clear sentences. Make it practical, not vague. Do not repeat the issue content. Do not say “No suggestion”.
"""

    def call_llama(prompt_text, attempt):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt_text, "stream": False},
                timeout=45
            )
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            print(f"[LLM Error Attempt {attempt}] {e}")
            print("🧠 Prompt that caused failure:\n", prompt_text[:300], "...\n")
            return ""

    # 🔁 Retry loop
    for attempt in range(2):
        result = call_llama(prompt, attempt + 1)
        if len(result.split()) >= min_word_count and "no suggestion" not in result.lower():
            return result
        time.sleep(1 + 2 * attempt)

    return "No suggestion available"
