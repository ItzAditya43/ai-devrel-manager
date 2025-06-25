# 🚀 DevRel AI Assistant

Let AI analyze GitHub issues and suggest high-impact DevRel actions — powered by local LLMs and real-time web search.

<p align="center">
  <img src="https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?logo=streamlit&logoColor=white" alt="Streamlit Badge"/>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License Badge"/>
  <img src="https://img.shields.io/badge/Status-Project%20Complete-blue" alt="Status Badge"/>
</p>

---

## 🔍 What It Does

DevRel AI Assistant is an intelligent tool that automates Developer Relations workflows by analyzing GitHub issues from any public repository. It provides:

* 🧠 **LLM-based Issue Classification** using local LLaMA3
* 🌐 **Web Context Search** via Tavily snippets
* 💡 **Actionable DevRel Suggestions** from an AI agent
* 📊 **Visual Dashboards** to explore and export insights
* 🧾 **Report Generation** with downloadable summaries

---

## 🖥️ Landing Page Preview

![Landing Page Screenshot](.github/landing_screenshot.png)

---

## ⚙️ How It Works

1. **User Enters a GitHub Repo** (e.g., `langchain-ai/langchain`)
2. Issues are fetched and classified using a local LLaMA model
3. Tavily adds helpful web context to improve understanding
4. A DevRel agent suggests practical actions (like writing docs, starting discussions, improving README)
5. Visual dashboards and reports summarize the results

---

## 💡 Use Cases

* Developer Advocates prioritizing GitHub feedback
* Open Source maintainers planning content or documentation
* DevRel teams wanting data-backed action suggestions
* Anyone managing large GitHub repos

---

## 🚀 Getting Started Locally

1. **Clone the Repo**

   ```bash
   git clone https://github.com/your-username/devrel-ai-assistant.git
   cd devrel-ai-assistant
   ```

2. **Set Up Requirements**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Locally**

   ```bash
   streamlit run main.py
   ```

4. **Make Sure Ollama Is Running with LLaMA3**

   ```bash
   ollama run llama3
   ```

---

## 🌐 Deployment (Streamlit Cloud)

To deploy:

* Move your secrets (like API keys) to `.streamlit/secrets.toml`
* Push the project to GitHub
* Deploy it directly via [Streamlit Community Cloud](https://streamlit.io/cloud)

---

## 📁 Project Structure

```
.
├── main.py                # Landing page (SaaS-style interface)
├── dashboard.py           # Interactive dashboard
├── run_pipeline.py        # Core orchestration logic for processing issues
├── report.py              # Renders downloadable summary tables in dashboard
├── report_generator.py    # Builds structured reports per label/issue
├── agents/
│   ├── classifier_agent.py   # LLaMA-based issue classification
│   ├── devrel_agent.py       # DevRel suggestion generator using LLaMA
├── tools/
│   ├── github_api.py         # GitHub issue fetching utility
│   ├── github_parser.py      # Cleans and parses raw issue data
│   ├── tavily_search.py      # Web search snippet API wrapper
├── data/                  # Stores processed issue datasets (JSON)
├── .streamlit/
│   └── secrets.toml       # API keys for Tavily and other services
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 🛡️ License

This project is licensed under the MIT License.

---

## 🙌 Credits

Built with ❤️ using [Streamlit](https://streamlit.io), [Ollama](https://ollama.com), and [Tavily](https://www.tavily.com).

---
