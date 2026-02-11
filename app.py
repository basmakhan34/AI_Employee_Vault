import streamlit as st
import os
import sys

# Path Setup: Taaki scripts folder ki files mil sakein
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_path = os.path.join(current_dir, "scripts")
sys.path.append(current_dir)
sys.path.append(scripts_path)

# Load Secrets into Environment for Master Assistant
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
if "DISCORD_WEBHOOK_URL" in st.secrets:
    os.environ["DISCORD_WEBHOOK_URL"] = st.secrets["DISCORD_WEBHOOK_URL"]

# Import Master Logic
try:
    from scripts.master_assistant import run_all
except ImportError:
    from master_assistant import run_all

# Page UI
st.set_page_config(page_title="AI-Employee Dashboard", page_icon="🤖", layout="wide")

def setup_cloud_tokens():
    """Secrets se JSON files bana raha hai for Google APIs"""
    try:
        if "GOOGLE_TOKEN_JSON" in st.secrets:
            with open(os.path.join(current_dir, "token.json"), "w") as f:
                f.write(st.secrets["GOOGLE_TOKEN_JSON"])
        if "GOOGLE_GMAIL_TOKEN_JSON" in st.secrets:
            with open(os.path.join(current_dir, "token_gmail.json"), "w") as f:
                f.write(st.secrets["GOOGLE_GMAIL_TOKEN_JSON"])
        return True
    except Exception as e:
        st.error(f"Token Setup Error: {e}")
        return False

st.title("🤖 AI-Employee: Gold Tier Dashboard")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🚀 Control Center")
    if st.button("▶️ Run Autonomous Workflow", use_container_width=True):
        if setup_cloud_tokens():
            with st.spinner("AI is processing Emails, Calendar & Finances..."):
                try:
                    run_all()
                    st.balloons()
                    st.success("✅ Workflow Success! Discord notified.")
                except Exception as e:
                    st.error(f"Workflow Error: {e}")
        else:
            st.error("Missing Google Tokens in Secrets!")

with col2:
    st.subheader("📥 Reports")
    pdf_file = os.path.join(current_dir, "Briefings", "Final_Report.pdf")
    if os.path.exists(pdf_file):
        with open(pdf_file, "rb") as f:
            st.download_button("📄 Download PDF Report", f, "Executive_Briefing.pdf", "application/pdf")
    else:
        st.info("No PDF available yet.")

# Preview Section
st.divider()
md_file = os.path.join(current_dir, "Briefings", "Daily_Report.md")
if os.path.exists(md_file):
    st.subheader("📝 Intelligence Preview")
    with open(md_file, "r") as f:
        st.markdown(f.read())
