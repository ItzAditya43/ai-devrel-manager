import json

def load_issues(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    issues = []
    for issue in data:
        issues.append({
            "title": issue.get("title"),
            "body": issue.get("body", ""),
            "labels": [label["name"] for label in issue.get("labels", [])],
            "number": issue.get("number"),
            "created_at": issue.get("created_at", "N/A")
        })
    return issues
