# 🤖 AI Employee: Autonomous Business Agent (Gold Tier)

This project is a sophisticated **Autonomous AI Employee** designed to manage daily business operations. It integrates Gmail, Google Calendar, and Financial data into a centralized **Obsidian Dashboard** with real-time **Discord Alerts**.

---

## 🌟 Key Features
- **🧠 Executive Intelligence:** Powered by **Llama-3 (Groq)** to analyze emails, meetings, and finances.
- **💰 Financial Analyst:** Automatically processes CSV files in the `Accounting` folder to calculate Profit/Loss.
- **📅 Workspace Sync:** Fetches real-time data from **Gmail** and **Google Calendar**.
- **📊 Professional Reporting:** Generates a daily **PDF Executive Briefing** and updates an **Obsidian** dashboard.
- **🔔 Instant Notifications:** Sends autonomous updates to the team via **Discord Webhooks**.

---

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **AI Model:** Llama-3.3-70b (via Groq Cloud)
- **Local Dashboard:** Obsidian (with Periodic Notes)
- **APIs:** Google Cloud (Gmail/Calendar), Discord API
- **PDF Engine:** FPDF

---

## 📂 Project Structure
- `scripts/master_assistant.py`: The brain of the agent.
- `scripts/financial_watcher.py`: Handles CSV processing.
- `scripts/pdf_generator.py`: Manages document creation.
- `Briefings/`: Stores Daily Reports in Markdown and PDF.
- `Accounting/`: The landing zone for financial CSVs.

---

## 🚀 How It Works
1. The **Watcher** monitors the `Accounting` folder for new transactions.
2. The **Master Assistant** fetches schedule data from Google APIs.
3. **Llama-3** generates a CEO-level briefing based on all data.
4. The system updates the **Obsidian Vault** and sends a **Discord** alert.

---

## 👤 Author
**Basma Khan** *Built for the AI Employee Hackathon 2026*
