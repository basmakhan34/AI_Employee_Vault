import os
import time
import requests
import sys
from groq import Groq
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# --- FLEXIBLE IMPORTS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    import financial_watcher as fw
    import pdf_generator as pg
except ImportError:
    from scripts import financial_watcher as fw
    from scripts import pdf_generator as pg

# --- API SETUP ---
# Local terminal ke liye key direct ya environment se
api_key = os.getenv("GROQ_API_KEY") or "YOUR_GROQ_API_KEY_HERE" 
client = Groq(api_key=api_key) if api_key else None

# Vault path: Project folder ke root ka rasta
VAULT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- FIXED DISCORD WEBHOOK ---
# Yahan os.getenv hata kar direct URL likhna hai
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1471144097556332596/QWkBdNnu7XYBpjdPWc_xV2qlE8FNkeVPdvxrvLTRoQi_sH9FFZBpua1RU0huZ-1Ilf4Y"

def get_data_with_retry(retries=3, delay=5):
    for i in range(retries):
        try:
            token_path = os.path.join(VAULT_PATH, 'token.json')
            gmail_token_path = os.path.join(VAULT_PATH, 'token_gmail.json')
            
            if not os.path.exists(token_path) or not os.path.exists(gmail_token_path):
                print("⚠️ Tokens missing. Skipping Google data...")
                return ["No Emails found"], ["No Meetings found"]

            creds_gmail = Credentials.from_authorized_user_file(gmail_token_path)
            creds_cal = Credentials.from_authorized_user_file(token_path)
            
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
        
        if not client:
            print("❌ Error: GROQ_API_KEY is not set!")
            return

        # 1. Fetch Google Data
        print("🔄 Step 1: Fetching Gmail & Calendar...")
        emails, meetings = get_data_with_retry()
        
        # 2. Fetch Financial Data
        print("💰 Step 2: Running Financial Analyst...")
        finance_report = fw.analyze_finances()
        
        # 3. Smart Reasoning
        print("🧠 Step 3: Generating Executive Briefing...")
        prompt = f"""
        Analyze the following data and provide a professional CEO briefing:
        EMAILS: {emails}
        MEETINGS: {meetings}
        FINANCIAL STATUS: {finance_report}
        Format the output with sections: 'Operational Overview', 'Financial Health', and 'Urgent Action Items'.
        """
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}], 
            model="llama-3.3-70b-versatile"
        )
        briefing = response.choices[0].message.content
        
        # 4. Save to Obsidian
        briefing_folder = os.path.join(VAULT_PATH, "Briefings")
        os.makedirs(briefing_folder, exist_ok=True)
        report_path = os.path.join(briefing_folder, "Daily_Report.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(briefing)
        
        # 5. Create PDF
        print("📄 Step 4: Creating PDF Report...")
        pg.create_pdf_report(briefing)

        # 6. Discord Alert
        print("🔔 Step 5: Notifying Team via Discord...")
        data = {"content": f"🏆 **GOLD TIER SYSTEM UPDATE** 🏆\n\n{briefing[:1800]}"}
        response = requests.post(DISCORD_WEBHOOK, json=data)
        
        if response.status_code == 204:
            print("✅ Discord message sent!")
        else:
            print(f"⚠️ Discord failed with status: {response.status_code}")

        print("\n✨ --- ALL SYSTEMS GO: GOLD TIER COMPLETE --- ✨")

    except Exception as e:
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    run_all()