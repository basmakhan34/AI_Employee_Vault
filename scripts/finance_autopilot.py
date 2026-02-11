import os
from pathlib import Path
from groq import Groq
from duckduckgo_search import DDGS

# Setup
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
VAULT_PATH = Path("D:/AI_Employee_Vault")

def get_market_news(query):
    print(f"🔍 AI is searching the internet for: {query}")
    with DDGS() as ddgs:
        results = [r['body'] for r in ddgs.text(query, max_results=3)]
        return "\n".join(results)

def generate_smart_briefing():
    try:
        # Step 1: Internal Data (CSV)
        transactions = open(VAULT_PATH / "Accounting/Feb_Transactions.csv").read()
        
        # Step 2: External Data (Internet Search)
        # Hum AI se market trends mangwa rahe hain
        market_info = get_market_news("latest business trends 2026 for small startups")
        
        prompt = f"""
        Analyze these internal transactions: {transactions}
        AND this external market info: {market_info}
        
        Generate a 'CEO Strategy Report'. 
        1. Financial Audit.
        2. Market Opportunity (based on search).
        3. Action Plan.
        """
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        
        report_path = VAULT_PATH / "Briefings/Market_Strategy_Report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(chat_completion.choices[0].message.content)
        
        print(f"🚀 Success! Strategic Report generated at: {report_path}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    generate_smart_briefing()