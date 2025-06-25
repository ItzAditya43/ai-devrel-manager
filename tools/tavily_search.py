import os
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_tavily_snippets(query, max_results=3):
    try:
        results = tavily.search(query=query, search_depth="advanced")
        return [
            {
                "title": r.get("title", "Untitled"),
                "url": r.get("url", ""),
                "content": r.get("content", "").strip()
            }
            for r in results.get("results", [])[:max_results]
        ]
    except Exception as e:
        print(f"[!] Tavily search failed: {e}")
        return []
