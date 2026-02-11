import requests
import sys

def send_discord_message(message: str):
    """
    Sends a message to a Discord channel using a webhook URL.

    Args:
        message: The string message to send.
    """
    # IMPORTANT: Replace this with your actual Discord Webhook URL
    # You can get this from your Discord server settings -> Integrations -> Webhooks
    WEBHOOK_URL = "https://discord.com/api/webhooks/1471144097556332596/QWkBdNnu7XYBpjdPWc_xV2qlE8FNkeVPdvxrvLTRoQi_sH9FFZBpua1RU0huZ-1Ilf4Y" 

    if WEBHOOK_URL == "[YAHAN APNA URL PASTE KAREIN]":
        print("Error: Please replace '[YAHAN APNA URL PASTE KAREIN]' with your actual Discord Webhook URL in discord_notifier.py")
        sys.exit(1)

    payload = {
        "content": message
    }

    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        print("Message sent to Discord successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Discord: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_message = " ".join(sys.argv[1:])
    else:
        user_message = "Hello from the Python script! This is a test message."
        print("No message provided. Sending a default test message.")
        print("Usage: python discord_notifier.py \"Your custom message here\"")
    
    send_discord_message(user_message)

