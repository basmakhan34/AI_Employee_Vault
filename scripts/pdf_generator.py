from fpdf import FPDF
import datetime

class AI_Report(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'AI EXECUTIVE EMPLOYEE - DAILY BRIEFING', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf_report(content):
    pdf = AI_Report()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    pdf.cell(200, 10, txt=f"Date: {date_str}", ln=1, align='L')
    pdf.ln(10)
    
    # AI Content ko PDF mein dalna
    pdf.multi_cell(0, 10, txt=content)
    
    report_path = "D:/AI_Employee_Vault/Briefings/Final_Report.pdf"
    pdf.output(report_path)
    print(f"📄 PDF Report Generated at: {report_path}")

if __name__ == "__main__":
    # Test run
    with open("D:/AI_Employee_Vault/Briefings/Daily_Report.md", "r", encoding="utf-8") as f:
        text = f.read()
    create_pdf_report(text)