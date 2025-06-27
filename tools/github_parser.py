import json

def load_issues(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    issues = []
    for issue in data:
        try:
            issues.append({
                "title": issue.get("title") or "",
                "body": issue.get("body") or "",
                "labels": [label.get("name", "") for label in issue.get("labels") or []],
                "number": issue.get("number", "N/A"),
                "created_at": issue.get("created_at", "N/A")
            })
        except Exception as e:
            print(f"[!] Failed to parse issue #{issue.get('number', 'unknown')}: {e}")
            continue  # Skip this issue safely

    return issues
