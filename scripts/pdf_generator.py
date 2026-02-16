from fpdf import FPDF
import os

def create_pdf_report(text):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # --- FIX: Special characters handle karne ke liye ---
        # Ye line text ko clean karegi taaki PDF crash na ho
        clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
        
        # Title
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(200, 10, txt="AI Employee: Daily Executive Briefing", ln=True, align='C')
        pdf.ln(10)
        
        # Body
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=clean_text)
        
        # Save path
        output_dir = "Briefings"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        output_path = os.path.join(output_dir, "Final_Report.pdf")
        pdf.output(output_path)
        print(f"📄 PDF Report Generated at: {output_path}")
        
    except Exception as e:
        print(f"❌ PDF Error: {e}")

if __name__ == "__main__":
    create_pdf_report("Test briefing with special chars: — ")