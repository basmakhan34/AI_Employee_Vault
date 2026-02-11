import os
from pathlib import Path
from groq import Groq
# Hum apni purani calendar script ka function yahan use karenge
from calendar_sync import get_calendar_events 

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def daily_planner():
    try:
        # Step 1: Calendar se events uthana
        print("📅 Reading your schedule...")
        events = get_calendar_events() 
        
        # Step 2: Groq ko batana
        prompt = f"Here is my schedule for today: {events}. Act as my Executive Assistant. Give me a 3-bullet point summary of my day and one piece of advice to stay productive."
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        
        print("\n--- 🤖 YOUR AI ASSISTANT SAYS ---")
        print(chat_completion.choices[0].message.content)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    daily_planner()