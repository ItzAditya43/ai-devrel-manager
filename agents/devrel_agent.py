import requests

def recommend_devrel_action(issue, model="llama3", min_word_count=25):
    title = issue.get("title", "")
    body = issue.get("body", "")
    label = issue.get("predicted_label", "unknown")
    context = issue.get("web_context", "").strip() or "[No external context found]"

    # 🧠 Optimized DevRel Prompt
    prompt = f"""
You are a highly skilled Developer Relations (DevRel) strategist AI.

Analyze the following GitHub issue and provide **one actionable and insightful DevRel recommendation** that can help resolve or improve it. Your response should be **specific, practical, and based on the provided context**, not generic.

Suggestions may include improving docs, adding usage examples, starting community discussions, clarifying error messages, or offering educational content.

---
GitHub Issue Label: {label}

Issue Title:
{title}

Issue Body:
{body}

External Context (Search Snippets):
{context}

---
✅ Please reply with a single, well-structured recommendation in **4–5 clear sentences**. Keep it under **120 words**. Avoid bullet points, repetition, vague terms, or generic responses.
"""

    def call_llama(prompt_text):
        try:
            res = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt_text, "stream": False},
                timeout=45
            )
            return res.json().get("response", "").strip()
        except Exception as e:
            print(f"[!] DevRel LLM call failed: {e}")
            return "No suggestion available"

    # 🔁 First attempt
    response = call_llama(prompt)

    # 📏 Retry if too short or unhelpful
    if len(response.split()) < min_word_count or "no suggestion" in response.lower():
        print("[!] Short or unhelpful DevRel response detected. Retrying...")
        response = call_llama(prompt)

    return response
