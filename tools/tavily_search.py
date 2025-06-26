import os
import requests

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise EnvironmentError("❌ TAVILY_API_KEY is missing. Set it in .env or secrets.toml.")

def search_tavily_snippets(query, max_results=1):
    url = "https://api.tavily.com/search"
    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "search_depth": "advanced",
        "max_results": max_results,
        "include_answer": False
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        return [
            {
                "title": r.get("title", "Untitled"),
                "url": r.get("url", ""),
                "content": r.get("content", "").strip()
            }
            for r in data.get("results", [])[:max_results]
        ]
    except Exception as e:
        print(f"[!] Tavily search failed: {e}")
        return []
