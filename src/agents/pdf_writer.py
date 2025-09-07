# pdf_writer.py
from fpdf import FPDF
import textwrap
import os

def wrap_text(text, width=90):
    """Wrap text to avoid FPDF horizontal space issues"""
    return "\n".join(textwrap.wrap(text, width))

def write_news_to_pdf(articles, output_file="news_summary.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "=== Today's Briefing ===", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)

    for idx, a in enumerate(articles, start=1):
        category = a.get("category") or "Uncategorized"
        title = a.get("title") or "No Title"
        link = a.get("link") or "No Link"
        original_text = a.get("text") or a.get("description") or a.get("summary") or "[No original text]"
        summary = a.get("summary") or "[No summary]"

        # Category and title
        pdf.set_font("Arial", "B", 12)
        pdf.multi_cell(0, 7, f"[{category}] {title}")
        pdf.ln(1)

        # Original text
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, f"📰 Original:\n{wrap_text(original_text)}")
        pdf.ln(1)

        # Summary with bullet points
        pdf.multi_cell(0, 6, f"📝 Summary:\n{wrap_text(summary)}")
        pdf.ln(1)

        # Link
        pdf.set_text_color(0, 0, 255)
        pdf.multi_cell(0, 6, f"🔗 Link: {wrap_text(link)}")
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    pdf.output(output_file)
    print(f"✅ PDF saved to: {output_file}")
