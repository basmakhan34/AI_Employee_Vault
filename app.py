import streamlit as st
import os
import json
import sys

# Adding the current directory and scripts folder to path
current_dir = os.getcwd()
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'scripts'))

# --- FIX: Setting GROQ Environment Variable from Secrets ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# Now try importing the master logic
try:
    from scripts.master_assistant import run_all
except ImportError:
    try:
        from master_assistant import run_all
    except ImportError as e:
        st.error(f"Could not import master_assistant: {e}")

# Page Configuration
st.set_page_config(page_title="AI-Employee Dashboard", page_icon="🤖", layout="wide")

# --- FUNCTION TO HANDLE SECRETS ---
def setup_credentials():
    """Restores token files from Streamlit Secrets for cloud execution."""
    try:
        # Restore Calendar Token
        if "GOOGLE_TOKEN_JSON" in st.secrets:
            with open("token.json", "w") as f:
                f.write(st.secrets["GOOGLE_TOKEN_JSON"])
        
        # Restore Gmail Token
        if "GOOGLE_GMAIL_TOKEN_JSON" in st.secrets:
            with open("token_gmail.json", "w") as f:
                f.write(st.secrets["GOOGLE_GMAIL_TOKEN_JSON"])
        
        # Inject Discord Webhook into environment if exists
        if "DISCORD_WEBHOOK_URL" in st.secrets:
            os.environ["DISCORD_WEBHOOK_URL"] = st.secrets["DISCORD_WEBHOOK_URL"]
            
        return True
    except Exception as e:
        st.error(f"Credentials Error: {e}")
        return False

# --- UI DESIGN ---
st.title("🤖 AI-Employee: Gold Tier Dashboard")
st.markdown("Automated Executive Intelligence for Emails, Calendar, and Finances.")
st.markdown("---")

# Sidebar for System Monitoring
with st.sidebar:
    st.header("⚙️ System Status")
    st.success("Bronze Tier: Active")
    st.success("Silver Tier: Active")
    st.success("Gold Tier: Active")
    st.divider()
    st.info("Powered by Groq & Llama 3")
    if st.button("Clear Cache / Refresh"):
        st.rerun()

# Main Action Area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🚀 Operational Control")
    st.write("Click the button below to trigger the autonomous workflow.")
    
    if st.button("▶️ Execute AI Workflow", use_container_width=True):
        if setup_credentials():
            with st.spinner("AI is analyzing data and generating reports..."):
                try:
                    # Execute the master function
                    run_all()
                    st.balloons()
                    st.success("✅ Workflow Completed! Check Discord and Download Report below.")
                except Exception as e:
                    st.error(f"Execution failed: {e}")
        else:
            st.warning("Could not find API tokens in Secrets.")

with col2:
    st.subheader("📥 Latest Outputs")
    # Using absolute paths to avoid confusion
    pdf_path = os.path.join(current_dir, "Briefings", "Final_Report.pdf")
    
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download Daily PDF Briefing",
                data=f,
                file_name="AI_Daily_Briefing.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.write("No PDF report found. Run the workflow first!")

# Display Briefing Preview if MD exists
st.markdown("---")
report_md = os.path.join(current_dir, "Briefings", "Daily_Report.md")
if os.path.exists(report_md):
    st.subheader("📝 Live Intelligence Preview")
    with open(report_md, "r", encoding="utf-8") as f:
        st.info(f.read())
