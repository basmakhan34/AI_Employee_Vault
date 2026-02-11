import streamlit as st
import os
import json
import sys

# Adding the scripts folder to the system path for easier imports
sys.path.append(os.path.join(os.getcwd(), 'scripts'))

try:
    from scripts.master_assistant import run_all
except ImportError:
    from master_assistant import run_all

# Page Configuration
st.set_page_config(page_title="AI-Employee Dashboard", page_icon="🤖", layout="wide")

# --- FUNCTION TO HANDLE SECRETS ---
def setup_credentials():
    """Restores token files from Streamlit Secrets for cloud execution."""
    try:
        if "GOOGLE_TOKEN_JSON" in st.secrets:
            with open("token.json", "w") as f:
                f.write(st.secrets["GOOGLE_TOKEN_JSON"])
        
        if "GOOGLE_GMAIL_TOKEN_JSON" in st.secrets:
            with open("token_gmail.json", "w") as f:
                f.write(st.secrets["GOOGLE_GMAIL_TOKEN_JSON"])
        return True
    except Exception as e:
        st.error(f"Credentials Error: {e}")
        return False

# --- UI DESIGN ---
st.title("🤖 AI-Employee: Gold Tier Dashboard")
st.markdown("---")

# Sidebar for System Monitoring
with st.sidebar:
    st.header("⚙️ System Status")
    st.success("Bronze Tier: Active")
    st.success("Silver Tier: Active")
    st.success("Gold Tier: Active")
    st.divider()
    st.info("Powered by Groq & Llama 3")

# Main Action Area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🚀 Operational Control")
    st.write("Click the button below to trigger the autonomous workflow (Email Sync, Calendar Scan, Financial Analysis, and PDF Generation).")
    
    if st.button("▶️ Execute AI Workflow", use_container_width=True):
        with st.spinner("AI is working... Please wait..."):
            if setup_credentials():
                try:
                    # Running your main logic
                    run_all()
                    st.balloons()
                    st.success("✅ Workflow Completed! Check Discord and Download Report below.")
                except Exception as e:
                    st.error(f"Execution failed: {e}")
            else:
                st.warning("Could not find API tokens in Secrets.")

with col2:
    st.subheader("📥 Latest Outputs")
    # Check for PDF
    pdf_path = "Briefings/Final_Report.pdf"
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
        st.write("No report generated yet. Run the workflow first!")

# Display Briefing Preview if MD exists
st.markdown("---")
report_md = "Briefings/Daily_Report.md"
if os.path.exists(report_md):
    st.subheader("📝 Live Intelligence Preview")
    with open(report_md, "r") as f:
        st.info(f.read())
