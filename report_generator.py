import json
import csv
from collections import Counter

def load_issues(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def export_to_csv(data, path="filtered_issues.csv"):
    keys = ["number", "title", "body", "predicted_label", "devrel_action", "created_at"]
    with open(path, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for item in data:
            writer.writerow({k: item.get(k, "") for k in keys})
    print(f"✅ Exported CSV: {path}")

def export_to_markdown(data, path="filtered_issues.md"):
    with open(path, "w", encoding="utf-8") as f:
        for issue in data:
            f.write(f"### #{issue['number']} - {issue['title']}\n")
            f.write(f"{issue.get('body', '')[:500]}...\n\n")
            f.write(f"**Predicted:** {issue.get('predicted_label')} | **DevRel:** {issue.get('devrel_action', '-')}\n\n")
            f.write("---\n")
    print(f"✅ Exported Markdown: {path}")

def generate_report(data):
    print("\n📊 DevRel Insights Report")
    print("=" * 30)

    print(f"🔹 Total Issues: {len(data)}")

    # Label distribution
    labels = [issue.get("predicted_label", "unknown") for issue in data]
    label_dist = Counter(labels)

    print("\n🧩 Predicted Issue Types:")
    for label, count in label_dist.items():
        print(f"  {label:<14} → {count}")

    # DevRel action distribution
    actions = [issue.get("devrel_action", "None").split(":")[-1].strip().lower() for issue in data]
    action_dist = Counter(actions)

    print("\n🎯 Suggested DevRel Actions:")
    for action, count in action_dist.items():
        print(f"  {action:<40} → {count}")

    print("\n❓ Sample Questions Needing Help:")
    shown = 0
    for issue in data:
        if issue.get("predicted_label") == "question":
            print(f"\n#{issue['number']}: {issue['title']}")
            print(f"> {issue['body'][:160]}...")
            print(f"📌 DevRel Action: {issue.get('devrel_action')}")
            print("-" * 40)
            shown += 1
            if shown >= 3:
                break

    print("\n✅ End of Report\n")
