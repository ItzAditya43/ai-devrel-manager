import streamlit as st
from run_pipeline import analyze_repository

st.set_page_config(page_title="DevRel AI Assistant", layout="centered")

# ---------- CSS Styling ----------
st.markdown("""
<style>
html, body, [data-testid="stApp"] {
    background-color: #0d1117;
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
}

h1 {
    font-size: 2.8rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
    text-align: center;
}

p.subtitle {
    font-size: 1.15rem;
    color: #c9d1d9;
    margin-bottom: 2rem;
    text-align: center;
}

.stTextInput > div > input {
    background-color: rgba(255,255,255,0.08) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    padding: 0.9rem 1.2rem;
    font-size: 1rem;
    border-radius: 10px;
    text-align: center;
}

.stButton > button {
    background: rgba(255,255,255,0.1);
    color: white;
    font-weight: 600;
    padding: 0.8rem 1.6rem;
    font-size: 1rem;
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 10px;
    margin-top: 1.2rem;
    transition: all 0.3s ease;
    width: 100%;
}

.stButton > button:hover {
    background: rgba(255,255,255,0.2);
    border-color: white;
    color: #ffffff;
}

/* Purpose cards */
.purpose-section {
    margin-top: 5rem;
    text-align: center;
}

.purpose-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 2rem;
    margin-top: 2rem;
}

.purpose-card {
    flex: 1 1 300px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.1);
    padding: 1.8rem;
    color: white;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    min-height: 180px;
    max-width: 360px;
}

.purpose-title {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 0.7rem;
    color: #ffffff;
}

.purpose-desc {
    font-size: 1rem;
    color: #c9d1d9;
}
</style>
""", unsafe_allow_html=True)

# ---------- Hero Section ----------
st.markdown("<h1>DevRel AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Let AI analyze GitHub issues and suggest high-impact DevRel actions</p>", unsafe_allow_html=True)

repo_input = st.text_input("Enter GitHub repo (e.g. owner/repo)", value="langchain-ai/langchain", label_visibility="collapsed")

if st.button("🚀 Run Analysis"):
    with st.spinner("Analyzing repository..."):
        try:
            analyze_repository(repo_input)
            st.success("✅ Analysis complete! Redirecting to dashboard...")
            st.switch_page("app.py")
        except Exception as e:
            st.error(f"❌ Analysis failed: {e}")

# ---------- Purpose Section ----------
st.markdown('<div class="purpose-section">', unsafe_allow_html=True)
st.markdown("<h2 style='margin-bottom: 1rem;'>What this app can do for you</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="purpose-grid">
    <div class="purpose-card">
        <div class="purpose-title">📊 Understand GitHub Issues</div>
        <div class="purpose-desc">Classify issues using local LLaMA to detect bugs, feedback, or community queries.</div>
    </div>
    <div class="purpose-card">
        <div class="purpose-title">🌐 Web Context with Tavily</div>
        <div class="purpose-desc">Adds helpful snippets from the web to boost understanding and response quality.</div>
    </div>
    <div class="purpose-card">
        <div class="purpose-title">💡 DevRel Suggestions</div>
        <div class="purpose-desc">Get clear suggestions: tutorials, blog posts, discussions — all from the LLM agent.</div>
    </div>
    <div class="purpose-card">
        <div class="purpose-title">📈 Visual Dashboards</div>
        <div class="purpose-desc">Explore insights visually, filter by labels, compare trends and export reports.</div>
    </div>
</div>
</div>
""", unsafe_allow_html=True)
