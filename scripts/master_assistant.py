import os
import time
import requests
from groq import Groq
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Naye Modules Import
from pdf_generator import create_pdf_report
from financial_watcher import analyze_finances 

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
VAULT_PATH = os.getcwd()
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1471144097556332596/QWkBdNnu7XYBpjdPWc_xV2qlE8FNkeVPdvxrvLTRoQi_sH9FFZBpua1RU0huZ-1Ilf4Y"

def get_data_with_retry(retries=3, delay=5):
    for i in range(retries):
        try:
            creds_gmail = Credentials.from_authorized_user_file('token_gmail.json')
            creds_cal = Credentials.from_authorized_user_file('token.json')
            gmail = build('gmail', 'v1', credentials=creds_gmail)
            calendar = build('calendar', 'v3', credentials=creds_cal)
            
            messages = gmail.users().messages().list(userId='me', maxResults=3).execute().get('messages', [])
            emails = [gmail.users().messages().get(userId='me', id=m['id']).execute().get('snippet', '') for m in messages]
            events = calendar.events().list(calendarId='primary', maxResults=3).execute().get('items', [])
            meetings = [e.get('summary', 'Untitled Event') for e in events]
            return emails, meetings
        except Exception as e:
            print(f"⚠️ Attempt {i+1} failed: {e}. Retrying...")
            time.sleep(delay)
    return [], []

def run_all():
    try:
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
        Analyze the following data and provide a professional CEO briefing:
        
        EMAILS: {emails}
        MEETINGS: {meetings}
        FINANCIAL STATUS: {finance_report}
        
        Format the output with sections: 'Operational Overview', 'Financial Health', and 'Urgent Action Items'.
        Make sure to comment on whether the $1415 profit is good or if expenses need cutting.
        """
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}], 
            model="llama-3.3-70b-versatile"
        )
        briefing = response.choices[0].message.content
        
        # 4. Save & Document
        os.makedirs(f"{VAULT_PATH}/Briefings", exist_ok=True)
        with open(f"{VAULT_PATH}/Briefings/Daily_Report.md", "w", encoding="utf-8") as f:
            f.write(briefing)
        
        print("📄 Step 4: Creating PDF Report...")
        create_pdf_report(briefing)

        # 5. Discord Alert
        print("🔔 Step 5: Notifying Team via Discord...")
        data = {"content": f"🏆 **GOLD TIER SYSTEM UPDATE** 🏆\n\n{briefing[:1800]}"}
        requests.post(DISCORD_WEBHOOK, json=data)

        print("\n✨ --- ALL SYSTEMS GO: GOLD TIER COMPLETE --- ✨")

    except Exception as e:
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    run_all()