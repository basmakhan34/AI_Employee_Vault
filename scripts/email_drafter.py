import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def draft_replies():
    creds = Credentials.from_authorized_user_file('token_gmail.json')
    service = build('gmail', 'v1', credentials=creds)
    
    # Last 2 emails uthana
    results = service.users().messages().list(userId='me', maxResults=2).execute()
    for msg in results.get('messages', []):
        m = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippet = m['snippet']
        
        # AI se reply likhwana
        reply = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Write a 2-line polite reply to this email: {snippet}"}],
            model="llama-3.3-70b-versatile"
        ).choices[0].message.content
        
        print(f"\n📩 Original: {snippet[:50]}...")
        print(f"✍️ Draft Reply: {reply}")

if __name__ == "__main__":
    draft_replies()