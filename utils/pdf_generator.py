from fpdf import FPDF
import io

class ResumePDF(FPDF):
    def header(self):
        # We don't want a default header on every page for a resume
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def generate_resume_pdf(text_content):
    """
    Parses the AI-generated resume text and formats it into a professional PDF.
    """
    pdf = ResumePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Fonts - Using standard Arial/Helvetica for ATS friendliness
    pdf.set_font("Arial", size=11)
    
    # Pre-process text to break any extremely long words (like URLs or divider links) without spaces
    def break_long_words(text, limit=60):
        return " ".join([w if len(w) <= limit else " ".join([w[i:i+limit] for i in range(0, len(w), limit)]) for w in text.split(" ")])
    
    lines = text_content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(5)
            continue
            
        line = break_long_words(line)
            
        # Bold headers (Lines starting with ** or [ or all caps)
        if (line.startswith("**") and line.endswith("**")) or line.isupper() or line.startswith("["):
            clean_line = line.replace("**", "").replace("[", "").replace("]", "")
            pdf.set_font("Arial", "B", 13)
            pdf.set_text_color(0, 51, 102) # Dark Blue for headers
            pdf.multi_cell(0, 10, clean_line)
            pdf.set_font("Arial", size=11)
            pdf.set_text_color(0, 0, 0) # Back to black
        
        # Bullet points
        elif line.startswith("-") or line.startswith("•") or line.startswith("*"):
            pdf.set_x(15)
            pdf.multi_cell(0, 6, line)
        
        else:
            pdf.multi_cell(0, 6, line)
            
    # Return as bytes
    pdf_output = pdf.output(dest='S')
    return bytes(pdf_output)
