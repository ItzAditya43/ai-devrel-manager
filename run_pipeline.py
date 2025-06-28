from tools.github_api import fetch_issues
from tools.github_parser import load_issues
from agents.classifier_agent import classify_issue
from agents.devrel_agent import recommend_devrel_action
from tools.tavily_search import search_tavily_snippets
import os, json
import logging
from collections import Counter
import streamlit as st

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Clean up Tavily snippet content
def clean_snippet(text):
    if not text:
        return ""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    lines = [l for l in lines if len(l) > 40 and not l.lower() in ("response_format", "strict: true")]
    cleaned = " ".join(lines)
    return cleaned[:300] + "..." if len(cleaned) > 300 else cleaned

def analyze_repository(repo: str):
    """
    Enhanced repository analysis with better error handling and progress tracking
    """
    if "/" not in repo:
        raise ValueError("Invalid repo format. Use 'owner/repo'.")
    
    logger.info(f"Starting analysis for repository: {repo}")
    
    # Create progress tracking for Streamlit
    if 'st' in globals():
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    try:
        # Step 1: Fetch issues from GitHub
        logger.info("Fetching issues from GitHub...")
        if 'st' in globals():
            status_text.text("📡 Fetching issues from GitHub...")
            progress_bar.progress(10)
        
        issues = fetch_issues(repo)
        logger.info(f"Fetched {len(issues)} issues")
        
        if not issues:
            raise ValueError("No issues found or GitHub API failed")
        
        # Step 2: Save raw issues
        os.makedirs("data", exist_ok=True)
        raw_path = f"data/{repo.replace('/', '_')}_issues.json"
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(issues, f, indent=2)
        
        if 'st' in globals():
            status_text.text("📝 Processing issues...")
            progress_bar.progress(20)
        
        # Step 3: Parse issues
        parsed = load_issues(raw_path)
        enriched = []
        
        total_issues = len(parsed)
        logger.info(f"Processing {total_issues} parsed issues")
        
        # Counters for tracking success/failure
        successful_classifications = 0
        successful_devrel_suggestions = 0
        successful_web_searches = 0
        
        for i, issue in enumerate(parsed):
            logger.info(f"Processing issue #{issue.get('number', i)}: {issue.get('title', 'No title')[:50]}")
            
            # Update progress
            if 'st' in globals():
                progress = 20 + (i / total_issues) * 60  # 20% to 80%
                progress_bar.progress(int(progress))
                status_text.text(f"🤖 Processing issue {i+1}/{total_issues}: {issue.get('title', 'No title')[:40]}...")
            
            # Step 4: Classify issue
            try:
                issue_text = f"{issue.get('title', '')}\n\n{issue.get('body', '')}"
                label = classify_issue(issue_text)
                issue["predicted_label"] = label
                
                if label != "unknown":
                    successful_classifications += 1
                    logger.info(f"Issue #{issue.get('number')} classified as: {label}")
                else:
                    logger.warning(f"Issue #{issue.get('number')} classification failed")
                    
            except Exception as e:
                logger.error(f"Classification failed for issue #{issue.get('number')}: {e}")
                issue["predicted_label"] = "unknown"
            
            # Step 5: Web search with Tavily
            try:
                query = f"{issue.get('title', '')} {issue.get('body', '')[:150]}"
                web_snippets = search_tavily_snippets(query)
                
                # Clean snippets
                for s in web_snippets:
                    s["content"] = clean_snippet(s.get("content", ""))
                
                # Format context for LLM
                tavily_context = "\n\n".join(
                    f"🔹 {s.get('title', 'No title')}\n{s.get('content', '')}\n🔗 {s.get('url', '')}"
                    for s in web_snippets if s.get("content")
                )
                
                issue["web_snippets"] = web_snippets
                issue["web_context"] = tavily_context[:1000]  # Limit context size
                
                if web_snippets:
                    successful_web_searches += 1
                    logger.info(f"Found {len(web_snippets)} web snippets for issue #{issue.get('number')}")
                
            except Exception as e:
                logger.error(f"Tavily search failed for issue #{issue.get('number')}: {e}")
                issue["web_snippets"] = []
                issue["web_context"] = ""
            
            # Step 6: Get DevRel suggestion
            try:
                suggestion = recommend_devrel_action(issue)
                issue["devrel_action"] = suggestion
                
                if suggestion and suggestion != "No suggestion available":
                    successful_devrel_suggestions += 1
                    logger.info(f"DevRel suggestion for issue #{issue.get('number')}: {suggestion[:50]}...")
                else:
                    logger.warning(f"No DevRel suggestion for issue #{issue.get('number')}")
                    
            except Exception as e:
                logger.error(f"DevRel suggestion failed for issue #{issue.get('number')}: {e}")
                issue["devrel_action"] = "No suggestion available"
            
            enriched.append(issue)
        
        # Step 7: Save enriched data
        if 'st' in globals():
            status_text.text("💾 Saving results...")
            progress_bar.progress(90)
        
        final_path = f"data/{repo.replace('/', '_')}_devrel.json"
        with open(final_path, "w", encoding="utf-8") as f:
            json.dump(enriched, f, indent=2)
        
        # Final statistics
        label_counts = Counter([i["predicted_label"] for i in enriched])
        
        results = {
            "total_issues": len(enriched),
            "labels": label_counts,
            "successful_classifications": successful_classifications,
            "successful_devrel_suggestions": successful_devrel_suggestions,
            "successful_web_searches": successful_web_searches,
            "classification_success_rate": (successful_classifications / total_issues) * 100,
            "devrel_success_rate": (successful_devrel_suggestions / total_issues) * 100,
            "web_search_success_rate": (successful_web_searches / total_issues) * 100
        }
        
        logger.info(f"Analysis complete for {repo}:")
        logger.info(f"  - Total issues: {results['total_issues']}")
        logger.info(f"  - Classification success: {results['classification_success_rate']:.1f}%")
        logger.info(f"  - DevRel suggestion success: {results['devrel_success_rate']:.1f}%")
        logger.info(f"  - Web search success: {results['web_search_success_rate']:.1f}%")
        logger.info(f"  - Label distribution: {dict(label_counts)}")
        
        if 'st' in globals():
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            
            # Show summary stats
            st.info(f"""
            **Analysis Summary:**
            - Total issues processed: {results['total_issues']}
            - Classification success rate: {results['classification_success_rate']:.1f}%
            - DevRel suggestions generated: {results['devrel_success_rate']:.1f}%
            - Web context added: {results['web_search_success_rate']:.1f}%
            """)
            
            if results['classification_success_rate'] < 50:
                st.warning("⚠️ Low classification success rate. Check your LLM endpoint!")
            
            if results['devrel_success_rate'] < 30:
                st.warning("⚠️ Low DevRel suggestion rate. LLM might not be responding properly.")
        
        return results
        
    except Exception as e:
        logger.error(f"Repository analysis failed: {e}")
        if 'st' in globals():
            status_text.text("❌ Analysis failed!")
            progress_bar.progress(0)
        raise

# Test function to verify everything is working
def test_pipeline():
    """Test the pipeline with a small repo"""
    test_repo = "octocat/Hello-World"  # Small test repo
    try:
        results = analyze_repository(test_repo)
        print("Pipeline test successful!")
        print(f"Results: {results}")
        return True
    except Exception as e:
        print(f"Pipeline test failed: {e}")
        return False

if __name__ == "__main__":
    test_pipeline()