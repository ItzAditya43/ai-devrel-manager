import streamlit as st
import json
from collections import Counter
import pandas as pd
import plotly.graph_objects as go
from run_pipeline import analyze_repository

# ---------- Persistent History Storage ----------
HISTORY_FILE = "search_history.json"

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[:5], f)  # Save only the last 5 entries

# --------- Session State Init ---------
if "search_history" not in st.session_state:
    st.session_state.search_history = load_history()

# --------- Utility Functions ---------
def load_issues(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def count_labels(issues, key):
    values = [issue.get(key, "unknown") for issue in issues]
    return Counter(values)

def clean_action(action):
    return action.split(":")[-1].strip().lower()

def render_bar_chart(data_dict, title):
    theme = st.get_option("theme.base")
    is_dark = theme == "dark"
    color = "#3fb950" if is_dark else "#2f81f7"

    fig = go.Figure(
        data=[go.Bar(
            x=list(data_dict.keys()),
            y=list(data_dict.values()),
            marker_color=color
        )]
    )
    fig.update_layout(
        title=title,
        xaxis_title="Labels",
        yaxis_title="Count",
        template="plotly_dark" if is_dark else "plotly_white",
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

# --------- UI Setup ---------
st.set_page_config(page_title="DevRel Insights", layout="wide")

# --- GitHub Dark Theme CSS ---
github_dark_css = """
<style>
    html, body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .github-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 2px rgba(1, 1, 1, 0.1);
    }
    code {
        background-color: #161b22;
        color: #c9d1d9;
        font-size: 0.9rem;
        padding: 2px 6px;
        border-radius: 4px;
    }
    a {
        color: #58a6ff;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    .stButton > button, .stDownloadButton > button {
        background-color: #21262d !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
        padding: 0.4rem 0.75rem !important;
        font-weight: 500;
        transition: 0.2s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #30363d !important;
        border-color: #58a6ff !important;
        color: #58a6ff !important;
    }
    .stTextInput > div > input {
        background-color: #161b22 !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
    }
    .stSelectbox > div > div {
        background-color: #161b22 !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
    }
    .stMarkdown code {
        background-color: #21262d !important;
    }
    [data-testid="collapsedControl"] svg {
        display: inline !important;
    }
    .material-icons, [class^="st-emotion-cache"] [data-testid*="icon"] {
        font-family: 'Material Icons' !important;
    }
    .devrel-tag {
        display: inline-block;
        background-color: #238636;
        color: white;
        font-size: 12px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 2em;
        margin-left: 0.5rem;
    }
</style>
"""
st.markdown(github_dark_css, unsafe_allow_html=True)

# --------- Title ---------
st.title("🤖 DevRel Insights Dashboard")
st.markdown("Powered by your LLM agents")

# --------- Sidebar ---------
st.sidebar.markdown("## 🔎 Analyze a GitHub Repository")
repo_input = st.sidebar.text_input("Enter repo (format: owner/repo)", value="langchain-ai/langchain")

if st.sidebar.button("🚀 Run Analysis"):
    with st.spinner("Analyzing repository..."):
        try:
            analyze_repository(repo_input)
            st.success("✅ Analysis complete! Reloading results...")
            if repo_input not in st.session_state.search_history:
                st.session_state.search_history.insert(0, repo_input)
                st.session_state.search_history = st.session_state.search_history[:5]
                save_history(st.session_state.search_history)
            st.rerun()
        except Exception as e:
            st.error(f"❌ Analysis failed: {e}")

repo_key = repo_input.replace("/", "_")
json_path = f"data/{repo_key}_devrel.json"

st.sidebar.markdown("---")
st.sidebar.markdown("### 🕘 Recent Repositories")
for repo in st.session_state.search_history:
    if st.sidebar.button(f"🔁 {repo}"):
        st.session_state.repo_reload = repo
        st.rerun()

if st.sidebar.button("🧹 Clear History"):
    st.session_state.search_history = []
    save_history([])
    st.experimental_rerun()

# --------- Load Data ---------
try:
    issues = load_issues(json_path)
    st.success(f"Loaded {len(issues)} issues from {repo_input}.")
except FileNotFoundError:
    st.error(f"❌ No processed file found for {repo_input}.\nExpected file: {json_path}.")
    st.stop()

# --------- Label Filtering ---------
unique_labels = sorted(set(issue.get("predicted_label", "unknown") for issue in issues))
selected_label = st.selectbox("🎯 Filter by predicted label:", ["All"] + unique_labels)
filtered_issues = [i for i in issues if i.get("predicted_label") == selected_label] if selected_label != "All" else issues

# --------- Text Search Filter ---------
search_query = st.text_input("🔍 Search issues by title/body text", "")
if search_query:
    filtered_issues = [
        i for i in filtered_issues
        if search_query.lower() in i.get("title", "").lower() or search_query.lower() in i.get("body", "").lower()
    ]
    st.info(f"🔎 Found {len(filtered_issues)} issue(s) matching: {search_query}")

# --------- Charts ---------
st.markdown("### 🔍 Compare Model vs GitHub Labels")
if st.toggle("Show bar charts", value=True):
    st.subheader("📊 Predicted Issue Labels")
    render_bar_chart(count_labels(filtered_issues, "predicted_label"), "Predicted Labels")

    st.subheader("🏷️ GitHub Labels")
    all_labels = [label.lower() for i in filtered_issues for label in i.get("labels", [])]
    render_bar_chart(Counter(all_labels), "GitHub Labels")

# --------- Export Buttons ---------
st.markdown("### 📥 Export Filtered Issues")
st.download_button("📄 Download JSON", json.dumps(filtered_issues, indent=2), file_name="filtered_issues.json")
st.download_button("📝 Download Markdown",
    "\n\n".join(
        f"### #{i['number']} - {i['title']}\n\n{i.get('body', '')[:500]}...\n\n**Predicted:** {i.get('predicted_label')} | **DevRel:** {i.get('devrel_action', '-')}"
        for i in filtered_issues
    ),
    file_name="filtered_issues.md"
)
df = pd.DataFrame(filtered_issues)
st.download_button("📊 Download CSV", df.to_csv(index=False), file_name="filtered_issues.csv")

# --------- DevRel Suggestions ---------
top_actions = Counter(clean_action(i.get("devrel_action", "")) for i in filtered_issues if i.get("devrel_action"))
if top_actions:
    with st.expander("💡 Top DevRel Suggestions (Click to expand)", expanded=True):
        for action, count in top_actions.most_common(5):
            st.markdown(f"- **{action.capitalize()}** &nbsp;({count})")
else:
    st.warning("No DevRel suggestions found.")

# --------- Misclassified Detection ---------
misclassified = [i for i in filtered_issues if i.get("predicted_label") not in [l.lower() for l in i.get("labels", [])]]
if misclassified:
    with st.expander(f"⚠️ {len(misclassified)} Potentially Misclassified Issues", expanded=False):
        show_all = st.checkbox("🔍 Show all", value=False)
        to_show = misclassified if show_all else misclassified[:5]
        for issue in to_show:
            st.markdown(f"**#{issue['number']} — {issue['title']}**")
            st.markdown(f"🔸 _Predicted:_ {issue.get('predicted_label')} | _GitHub:_ {', '.join(issue.get('labels', [])) or 'None'}")
            st.markdown("---")
else:
    st.info("✅ No misclassified issues found.")

# --------- Sample Questions ---------
st.markdown("---")
st.subheader("❓ Sample 'Question' Issues")
q_issues = [i for i in filtered_issues if i.get("predicted_label") == "question"]
if not q_issues:
    st.info("No issues labeled as 'question'.")
else:
  for issue in q_issues[:3]:
    with st.container():
        st.markdown("<div class='github-card'>", unsafe_allow_html=True)
        st.markdown("<div style='display: flex; justify-content: space-between; align-items: center;'>", unsafe_allow_html=True)
        st.markdown(f"<strong>#{issue['number']}</strong> — {issue['title']}", unsafe_allow_html=True)
        st.markdown(
            f"""
            <a href="{issue.get('html_url', '#')}" target="_blank">
                <button style='background-color:#238636; color:white; border:none; padding:4px 10px; border-radius:4px; font-size:12px;'>
                    🌐 View on GitHub
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.code(issue.get("body", "")[:250] + "...", language="markdown")
        st.markdown(f"<span class='devrel-tag'>{issue.get('devrel_action', 'No suggestion')}</span>", unsafe_allow_html=True)
        if (ctx := issue.get("web_context", "").strip()):
            st.markdown("🌐 _Web Context (Tavily Snippets)_:")
            st.markdown(ctx, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --------- Full Viewer ---------
st.markdown("---")
st.subheader("📚 All Issues (Full Details)")
if st.toggle("🔽 Show all issues with full context"):
    for issue in filtered_issues:
        with st.container():
            st.markdown("<div class='github-card'>", unsafe_allow_html=True)
            st.markdown("<div style='display: flex; justify-content: space-between; align-items: center;'>", unsafe_allow_html=True)
            st.markdown(f"<strong>#{issue['number']}</strong> — {issue['title']}", unsafe_allow_html=True)
            st.markdown(
                f"""
                <a href="{issue.get('html_url', '#')}" target="_blank">
                    <button style='background-color:#238636; color:white; border:none; padding:4px 10px; border-radius:4px; font-size:12px;'>
                        🌐 View on GitHub
                    </button>
                </a>
                """,
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)
            st.write(issue.get("body", ""))
            st.markdown(f"🗓️ Created: `{issue.get('created_at', 'N/A')}`")
            st.markdown(f"<span class='devrel-tag'>{issue.get('devrel_action', 'No suggestion')}</span>", unsafe_allow_html=True)
            if (ctx := issue.get("web_context", "").strip()):
                with st.expander("🌐 Web Context (Tavily Snippets)"):
                    st.markdown(ctx, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
# --------- Recent Issues ---------
st.subheader("🆕 Latest 5 Issues")
try:
    recent_issues = sorted(filtered_issues, key=lambda x: x.get("created_at", ""), reverse=True)[:5]
    for issue in recent_issues:
        with st.container():
            st.markdown("<div class='github-card'>", unsafe_allow_html=True)
        st.markdown("<div style='display: flex; justify-content: space-between; align-items: center;'>", unsafe_allow_html=True)
        st.markdown(f"<strong>#{issue['number']}</strong> — {issue['title']}", unsafe_allow_html=True)
        st.markdown(
            f"""
            <a href="{issue.get('html_url', '#')}" target="_blank">
                <button style='background-color:#238636; color:white; border:none; padding:4px 10px; border-radius:4px; font-size:12px;'>
                    🌐 View on GitHub
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.write(issue.get("body", "")[:500] + "...")
        st.markdown(f"<span class='devrel-tag'>{issue.get('devrel_action', 'No suggestion')}</span>", unsafe_allow_html=True)
        if (ctx := issue.get("web_context", "").strip()):
            with st.expander("🌐 Web Context (Tavily Search)"):
                st.markdown(ctx, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
            
except Exception as e:
    st.warning("⚠️ Could not sort by created_at. Make sure your data includes that field in ISO format.")