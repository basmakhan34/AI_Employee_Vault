import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Ab hum Calendar aur Gmail dono ke scopes mangenge
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_summary():
    creds = None
    if os.path.exists('token_gmail.json'):
        creds = Credentials.from_authorized_user_file('token_gmail.json', SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'D:/AI_Employee_Vault/scripts/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token_gmail.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    
    # Sirf inbox ke last 5 emails uthana
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=5).execute()
    messages = results.get('messages', [])

    print("\n📩 Reading your latest emails...")
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippet = m['snippet']
        print(f"- {snippet[:100]}...")

if __name__ == '__main__':
    get_gmail_summary()