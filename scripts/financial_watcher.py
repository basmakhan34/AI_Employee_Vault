import csv
import os
from pathlib import Path

def analyze_finances():
    VAULT_PATH = os.getcwd()
    accounting_dir = vault_path / "Accounting"
    
    total_income = 0
    total_expenses = 0
    
    if not accounting_dir.exists():
        return f"❌ Folder not found at: {accounting_dir}"

    files = list(accounting_dir.glob("*.csv"))
    for file_path in files:
        print(f"📖 Reading: {file_path.name}")
        with open(file_path, mode='r', encoding='utf-8-sig') as file: 
            reader = csv.DictReader(file)
            
    
            reader.fieldnames = [field.strip() for field in reader.fieldnames]
            
            for row in reader:
                try:
                    
                    val_str = row.get('Amount') or row.get('amount')
                    if val_str:
                        val = val_str.replace('$', '').replace(',', '').replace('+', '').strip()
                        amount = float(val)

                        if amount > 0:
                            total_income += amount
                        else:
                            total_expenses += abs(amount)
                except Exception as e:
                    print(f"⚠️ Row Error: {e}")

    net_profit = total_income - total_expenses
    status = "📈 Profit" if net_profit > 0 else "📉 Loss"
    
    summary = (
        f"\n--- 💰 FINANCIAL ANALYST REPORT ---\n"
        f"Total Income:   ${total_income:.2f}\n"
        f"Total Expenses: ${total_expenses:.2f}\n"
        f"Net Position:   ${net_profit:.2f} ({status})\n"
        f"----------------------------------"
    )
    return summary

if __name__ == "__main__":
    print(analyze_finances())