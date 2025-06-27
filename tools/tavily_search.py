import os
import requests

# 🔁 Toggle to enable/disable Tavily search
USE_TAVILY = True

if not USE_TAVILY:
    def search_tavily_snippets(query, max_results=1):
        print("[Tavily] Skipped search (USE_TAVILY=False)")
        return []

else:
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
            response = requests.post(url, json=payload, headers=headers, timeout=20)
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            cleaned = []
            for r in results[:max_results]:
                title = r.get("title", "Untitled")
                url = r.get("url", "")
                content = (r.get("content") or "").strip()
                cleaned.append({
                    "title": title,
                    "url": url,
                    "content": content
                })

            print(f"[Tavily] Found {len(cleaned)} result(s) for: {query[:50]}...")
            return cleaned

        except Exception as e:
            print(f"[!] Tavily search failed: {e}")
            return []
