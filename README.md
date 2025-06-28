# 🚀 DevRel AI Assistant

Let AI analyze GitHub issues and suggest high-impact DevRel actions — powered by TinyLLaMA and real-time web search.

<p align="center">
  <img src="https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?logo=streamlit&logoColor=white" alt="Streamlit Badge"/>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License Badge"/>
  <img src="https://img.shields.io/badge/Status-Project%20Complete-blue" alt="Status Badge"/>
</p>

---

## 🔍 What It Does

**DevRel AI Assistant** is an LLM-powered tool to streamline Developer Relations workflows by analyzing GitHub issues from any public repository. It provides:

- 🧠 **LLM-based Issue Classification** via **TinyLLaMA on Hugging Face Spaces**
- 🌐 **Web Contextual Insights** from Tavily API
- 💡 **Concrete DevRel Suggestions** (under 120 words)
- 📊 **Interactive Dashboard** to explore, filter, and export insights
- 📥 **Downloadable Reports** in JSON, CSV, and Markdown formats

---

## 🖼️ Sample View

> Below: The dashboard showing issue classification, suggestions, and real-time GitHub insights.

![image](https://github.com/user-attachments/assets/e791b37d-4931-4f2e-982a-c76bb7e954ba)
![image](https://github.com/user-attachments/assets/689a6bde-bbde-4124-9624-0f384d26b97b)

---

## ⚙️ How It Works

1. **User Enters a GitHub Repo** (e.g. `langchain-ai/langchain`)
2. GitHub issues are fetched and cleaned
3. **TinyLLaMA API** classifies issues and suggests DevRel actions
4. **Tavily** searches the web and appends useful snippets for context
5. Dashboard shows charts, insights, and DevRel strategy suggestions

---

## 💡 Use Cases

- Developer Relations teams prioritizing GitHub feedback
- OSS maintainers planning documentation or community outreach
- Dev Advocates summarizing user friction points
- Technical PMs managing issue triage at scale

---

## 🚀 Getting Started Locally

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/devrel-ai-assistant.git
cd devrel-ai-assistant
````

### 2. Set Up Environment

```bash
pip install -r requirements.txt
```

### 3. Set Tavily API Key

Add this to your `.env` or `.streamlit/secrets.toml`:

```
TAVILY_API_KEY=your_key_here
```

### 4. Set LLM Endpoint (Optional)

The app uses this endpoint to call TinyLLaMA:

```
OLLAMA_API_URL=https://aditya69690-100-hack.hf.space/api/generate
```

You can set this in your `.env`.

### 5. Launch the App

```bash
streamlit run main.py
```

---

## 🤖 LLM Backend: TinyLLaMA on Hugging Face Spaces

This project uses **TinyLLaMA** hosted via **Hugging Face Spaces** for all LLM tasks.

* ✅ API URL: `https://aditya69690-100-hack.hf.space/api/generate`
* 🔧 Expected JSON payload format:

```json
{
  "model": "tinyllama",
  "prompt": "<your prompt>",
  "stream": false,
  "temperature": 0.7,
  "system": "You are a DevRel assistant or a classification model.",
  "num_predict": 80
}
```

---

## 💡 Prompt Design for TinyLLaMA

Since the model is small, prompts are optimized for brevity and specificity.

Examples:

* **Classifier:**
  `"Classify the GitHub issue below into one of: bug, feature, question, documentation, discussion. Only return the label."`

* **DevRel Suggestion:**
  `"You're a DevRel expert. Suggest one helpful action for this GitHub issue. Respond in 1 sentence."`

---

## ⚠️ Known Issues & Tips

* 🕒 First response from the Space may take 30–60s due to cold start
* 📏 Keep context short (under \~500 tokens) for best performance
* ✅ Retry logic handles empty responses automatically
* ⛓️ If hosting your own Ollama server, just replace `OLLAMA_API_URL`

---

## 📁 Project Structure

```
.
├── main.py                  # Home screen for inputting repos
├── pages/
│   └── dashboard.py         # Interactive dashboard with charts & filters
├── run_pipeline.py          # Core agent pipeline (classification + Tavily + DevRel)
├── report_generator.py      # Generates structured reports per label
├── report.py                # Report rendering helpers
├── agents/
│   ├── classifier_agent.py  # Predicts label from issue using LLM
│   └── devrel_agent.py      # Suggests DevRel actions using LLM
├── tools/
│   ├── github_api.py        # Pulls issues from GitHub API
│   ├── github_parser.py     # Cleans/parses raw issue data
│   └── tavily_search.py     # Adds external context via Tavily API
├── data/                    # Stores processed issue datasets (.json)
├── requirements.txt
├── test.py                  # To test HuggingFace API
├── .env                     # Store Project secrets
└── README.md
```

---

## 🌐 Deploy to Streamlit Cloud

To deploy:

* Move your `TAVILY_API_KEY` and `OLLAMA_API_URL` into `.streamlit/secrets.toml`
* Push to GitHub
* Deploy directly via [Streamlit Cloud](https://streamlit.io/cloud)

---

## 🛡️ License

This project is licensed under the **MIT License**. Use freely, modify proudly.

---

## 🙌 Credits

Built with ❤️ by \[Adi Pandey] using:

* [Streamlit](https://streamlit.io/)
* [TinyLLaMA via Hugging Face Spaces](https://huggingface.co/spaces)
* [Tavily](https://www.tavily.com/)


