import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise EnvironmentError("❌ GITHUB_TOKEN is missing. Please set it in your .env file.")

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def fetch_issues(repo):
    all_issues = []
    page = 1
    per_page = 100

    while True:
        url = f"https://api.github.com/repos/{repo}/issues?page={page}&per_page={per_page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"❌ GitHub API Error {response.status_code}: {response.text}")
            break

        batch = response.json()

        # ❗ Filter out pull requests (they have a 'pull_request' key)
        issues_only = [issue for issue in batch if "pull_request" not in issue]

        if not issues_only:
            break

        all_issues.extend(issues_only)
        if len(batch) < per_page:
            break  # End of pagination

        page += 1

    print(f"✅ Fetched {len(all_issues)} issues from {repo}")
    return all_issues
