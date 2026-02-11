import time
import os
from pathlib import Path

# Path setup
VAULT_PATH = Path("D:/AI_Employee_Vault")
WATCH_FOLDER = VAULT_PATH / "Needs_Action"

def check_for_tasks():
    # Folder check karein
    files = list(WATCH_FOLDER.glob("*.md"))
    
    if files:
        print(f"\n[!] {len(files)} Naye tasks mile hain!")
        for f in files:
            print(f"--- Task File: {f.name} ---")
            with open(f, 'r') as file:
                print("Content:")
                print(file.read())
            print("--------------------------")
        print("\nACTION: Is content ko copy karein aur Gemini chat mein bhejein.")
    else:
        print(".", end="", flush=True)

if __name__ == "__main__":
    print(f"Monitoring folder: {WATCH_FOLDER}")
    print("Naye tasks ka intezar hai (Har 5 seconds)...")
    try:
        while True:
            check_for_tasks()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nWatcher band ho raha hai.")