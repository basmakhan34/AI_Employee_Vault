import os
import pandas as pd

# Path standard set karein
VAULT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def analyze_finances():
    try:
        # Accounting folder ka sahi rasta
        acc_path = os.path.join(VAULT_PATH, "Accounting")
        
        # Folder check karein
        if not os.path.exists(acc_path):
            return "No Accounting folder found."

        all_files = [f for f in os.listdir(acc_path) if f.endswith('.csv')]
        
        if not all_files:
            return "No CSV files found in Accounting folder. Current Status: $0 Profit."

        total_income = 0
        total_expenses = 0

        for file in all_files:
            df = pd.read_csv(os.path.join(acc_path, file))
            # Column names ko clean karein
            df.columns = df.columns.str.strip().str.capitalize()
            
            if 'Amount' in df.columns and 'Type' in df.columns:
                income = df[df['Type'].str.lower() == 'income']['Amount'].sum()
                expense = df[df['Type'].str.lower() == 'expense']['Amount'].sum()
                total_income += income
                total_expenses += expense

        profit = total_income - total_expenses
        return f"Financial Analysis: Total Income: ${total_income}, Total Expenses: ${total_expenses}, Net Profit: ${profit}."

    except Exception as e:
        return f"Error analyzing finances: {str(e)}"

if __name__ == "__main__":
    print(analyze_finances())