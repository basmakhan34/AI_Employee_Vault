import os
from groq import Groq
from pathlib import Path

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
VAULT_PATH = Path("D:/AI_Employee_Vault")

def generate_linkedin_post():
    try:
        # Step 1: Check karein agar koi briefing file hai, warna generic topic use karein
        briefing_path = VAULT_PATH / "Briefings/Market_Strategy_Report.md"
        
        if briefing_path.exists():
            with open(briefing_path, "r", encoding="utf-8") as f:
                context = f.read()
        else:
            # Agar file nahi hai toh ye default topic use karega
            context = "AI Automation and building Digital Employees for business productivity."

        prompt = f"""
        Topic: {context}
        Act as a Business Expert. Write a high-authority LinkedIn post. 
        - Use 3 relevant hashtags.
        - Add an engaging hook at the start.
        - Keep it professional yet conversational.
        """

        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )

        post_content = response.choices[0].message.content
        
        # Step 2: Save the post
        os.makedirs(VAULT_PATH / "Social_Media", exist_ok=True)
        post_file = VAULT_PATH / "Social_Media/LinkedIn_Draft.md"
        
        with open(post_file, "w", encoding="utf-8") as f:
            f.write(post_content)
            
        print(f"📱 LinkedIn Draft Ready at: {post_file}")
        print("\n--- POST PREVIEW ---")
        print(post_content[:200] + "...") # Thora sa preview dikhane ke liye

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    generate_linkedin_post()