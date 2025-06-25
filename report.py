from report_generator import load_issues, generate_report, export_to_csv, export_to_markdown

filename = "data/langchain-ai_langchain_devrel.json"  # adjust as needed
issues = load_issues(filename)

generate_report(issues)
export_to_csv(issues)
export_to_markdown(issues)
