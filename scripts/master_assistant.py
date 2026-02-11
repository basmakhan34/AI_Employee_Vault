import os
import time
import requests
from groq import Groq
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import streamlit as st 

# --- IMPORTING YOUR OTHER MODULES ---
# Make sure these files exist in the same folder or 'scripts' folder
try:
    from scripts.financial_watcher import analyze_finances
    from scripts.pdf_generator import create_pdf_report
except ImportError:
    from financial_watcher import analyze_finances
    from pdf_generator import create_pdf_report

# API Key Logic
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        api_key = None

if not api_key:
    # Instead of raising error immediately, we check it in run_all
    pass 

# Configuration
VAULT_PATH = os.getcwd()
# Recommendation: Get webhook from secrets too
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL") or st.secrets.get("DISCORD_WEBHOOK_URL", "YOUR_FALLBACK_URL")

def get_data_with_retry(retries=3, delay=5):
    for i in range(retries):
        try:
            # Check if token files exist before reading
            if not os.path.exists('token_gmail.json') or not os.path.exists('token.json'):
                print("⚠️ Token files not found. Setup might be missing.")
                return [], []
                
            creds_gmail = Credentials.from_authorized_user_file('token_gmail.json')
            creds_cal = Credentials.from_authorized_user_file('token.json')
            gmail = build('gmail', 'v1', credentials=creds_gmail)
            calendar = build('calendar', 'v3', credentials=creds_cal)
            
            messages = gmail.users().messages().list(userId='me', maxResults=3).execute().get('messages', [])
            emails = [gmail.users().messages().get(userId='me', id=m['id']).execute().get('snippet', '') for m in messages]
            events = calendar.events().list(calendarId='primary', maxResults=3, timeMin=time.strftime('%Y-%m-%dT%H:%M:%SZ')).execute().get('items', [])
            meetings = [e.get('summary', 'Untitled Event') for e in events]
            return emails, meetings
        except Exception as e:
            print(f"⚠️ Attempt {i+1} failed: {e}. Retrying...")
            time.sleep(delay)
    return [], []

def run_all():
    try:
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing!")

        client = Groq(api_key=api_key)
        print("\n--- 🤖 AI EMPLOYEE GOLD ENGINE STARTING ---")
        
        # 1. Fetch Google Data
        print("🔄 Step 1: Fetching Gmail & Calendar...")
        emails, meetings = get_data_with_retry()
        
        # 2. Fetch Financial Data (GOLD POWER)
        print("💰 Step 2: Running Financial Analyst...")
        finance_report = analyze_finances()
        
        # 3. Smart Reasoning (Llama 3)
        print("🧠 Step 3: Generating Executive Briefing...")
        prompt = f"""
        Analyze the following data and provide a professional CEO briefing in English:
        
        EMAILS: {emails}
        MEETINGS: {meetings}
        FINANCIAL STATUS: {finance_report}
        
        Format the output with professional Markdown sections: 
        '## Operational Overview', '## Financial Health', and '## Urgent Action Items'.
        Provide a smart commentary on profitability and expense management.
        """
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}], 
            model="llama-3.3-70b-versatile"
        )
        briefing = response.choices[0].message.content
        
        # 4. Save & Document
        briefing_dir = os.path.join(VAULT_PATH, "Briefings")
        os.makedirs(briefing_dir, exist_ok=True)
        
        report_path = os.path.join(briefing_dir, "Daily_Report.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(briefing)
        
        print("📄 Step 4: Creating PDF Report...")
        create_pdf_report(briefing)

        # 5. Discord Alert
        print("🔔 Step 5: Notifying Team via Discord...")
        # Discord limit is 2000 characters
        data = {"content": f"🏆 **GOLD TIER SYSTEM UPDATE** 🏆\n\n{briefing[:1900]}"}
        requests.post(DISCORD_WEBHOOK, json=data)

        print("\n✨ --- ALL SYSTEMS GO: GOLD TIER COMPLETE --- ✨")
        return True

    except Exception as e:
        print(f"❌ Critical Error: {e}")
        raise e

if __name__ == "__main__":
    run_all()
