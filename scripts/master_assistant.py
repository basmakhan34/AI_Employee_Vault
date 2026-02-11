import os
import time
import requests
from groq import Groq
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Flexible Imports for PDF and Finance
try:
    import financial_watcher as fw
    import pdf_generator as pg
except ImportError:
    from scripts import financial_watcher as fw
    from scripts import pdf_generator as pg

def get_data_with_retry():
    try:
        # Check tokens
        if not os.path.exists('token_gmail.json') or not os.path.exists('token.json'):
            return ["Missing Tokens"], ["Missing Tokens"]
            
        creds_gmail = Credentials.from_authorized_user_file('token_gmail.json')
        creds_cal = Credentials.from_authorized_user_file('token.json')
        
        gmail = build('gmail', 'v1', credentials=creds_gmail)
        calendar = build('calendar', 'v3', credentials=creds_cal)
        
        # Simple fetch
        msgs = gmail.users().messages().list(userId='me', maxResults=2).execute().get('messages', [])
        emails = [gmail.users().messages().get(userId='me', id=m['id']).execute().get('snippet', '') for m in msgs]
        
        events = calendar.events().list(calendarId='primary', maxResults=2).execute().get('items', [])
        meetings = [e.get('summary', 'Meeting') for e in events]
        
        return emails, meetings
    except Exception as e:
        return [f"Error: {e}"], []

def run_all():
    api_key = os.getenv("GROQ_API_KEY")
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing!")

    client = Groq(api_key=api_key)
    
    # 1. Data Fetch
    emails, meetings = get_data_with_retry()
    
    # 2. Finance Fetch
    finance_status = fw.analyze_finances()
    
    # 3. AI Reasoning
    prompt = f"Summarize for CEO: Emails: {emails}, Meetings: {meetings}, Finance: {finance_status}. Provide 3 action items."
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile"
    )
    briefing = response.choices[0].message.content
    
    # 4. Save & PDF
    os.makedirs("Briefings", exist_ok=True)
    with open("Briefings/Daily_Report.md", "w") as f:
        f.write(briefing)
    
    pg.create_pdf_report(briefing)
    
    # 5. Discord
    if webhook:
        requests.post(webhook, json={"content": f"🚀 **Gold Tier Update:**\n{briefing[:1500]}"})

if __name__ == "__main__":
    run_all()
