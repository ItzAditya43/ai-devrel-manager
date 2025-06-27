from tools.github_api import fetch_issues
from tools.github_parser import load_issues
from agents.classifier_agent import classify_issue
from agents.devrel_agent import recommend_devrel_action
from tools.tavily_search import search_tavily_snippets
import os, json
from collections import Counter

# Clean up Tavily snippet content
def clean_snippet(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    lines = [l for l in lines if len(l) > 40 and not l.lower() in ("response_format", "strict: true")]
    cleaned = " ".join(lines)
    return cleaned[:300] + "..." if len(cleaned) > 300 else cleaned

def analyze_repository(repo: str):
    if "/" not in repo:
        raise ValueError("Invalid repo format. Use 'owner/repo'.")

    issues = fetch_issues(repo)
    os.makedirs("data", exist_ok=True)

    raw_path = f"data/{repo.replace('/', '_')}_issues.json"
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(issues, f, indent=2)

    parsed = load_issues(raw_path)
    enriched = []

    for issue in parsed:
        issue_text = issue["title"] + "\n\n" + issue["body"]
        label = classify_issue(issue_text)
        issue["predicted_label"] = label

        try:
            query = f"{issue['title']} {issue['body'][:150]}"
            web_snippets = search_tavily_snippets(query)

            for s in web_snippets:
                s["content"] = clean_snippet(s.get("content", ""))

            # Format: title, content and link for LLM prompt
            tavily_context = "\n\n".join(
                f"🔹 {s['title']}\n{s['content']}\n🔗 {s['url']}"
                for s in web_snippets if s["content"]
            )

        except Exception as e:
            print(f"[!] Tavily failed for issue #{issue['number']}: {e}")
            web_snippets = []
            tavily_context = ""

        issue["web_snippets"] = web_snippets
        issue["web_context"] = tavily_context

        try:
            suggestion = recommend_devrel_action(issue)
        except Exception as e:
            print(f"[!] DevRel suggestion failed for issue #{issue['number']}: {e}")
            suggestion = "no_suggestion"

        issue["devrel_action"] = suggestion
        enriched.append(issue)

    final_path = f"data/{repo.replace('/', '_')}_devrel.json"
    with open(final_path, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2)

    return {
        "total_issues": len(enriched),
        "labels": Counter([i["predicted_label"] for i in enriched])
    }
