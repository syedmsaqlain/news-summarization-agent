# pdf_writer.py
from fpdf import FPDF
import re
import os
# First install: pip install reportlab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


def remove_emojis(text: str) -> str:
    """
    Remove all emojis and non-printable characters from text
    """
    if not text:
        return ""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002700-\U000027BF"  # dingbats
        "\U0001F900-\U0001F9FF"  # supplemental symbols & pictographs
        "\U00002600-\U000026FF"  # miscellaneous symbols
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub("", text)

def safe_text(text, max_length=200) -> str:
    """
    Clean text for PDF with aggressive filtering
    """
    if text is None:
        return ""
    
    text = str(text)
    
    # Remove emojis first
    text = remove_emojis(text)
    
    # Remove any non-ASCII characters completely
    text = re.sub(r'[^\x00-\x7F]', '', text)
    
    # Break up extremely long words (common cause of the error)
    text = re.sub(r'(\S{30,})', lambda m: m.group(1)[:30] + ' ' + m.group(1)[30:], text)
    
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Limit overall length
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text

def split_long_text(text, max_line_length=80):
    """
    Split text into lines with maximum length to prevent horizontal overflow
    """
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        if len(' '.join(current_line + [word])) <= max_line_length:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)

def write_pdf_reportlab(articles: list, output_path="demo/news_summary.pdf"):
    """
    Using ReportLab - removes the introductory line from summaries
    """
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    import os
    
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                          leftMargin=0.75*inch, rightMargin=0.75*inch,
                          topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        spaceAfter=6
    )
    
    summary_style = ParagraphStyle(
        'CustomSummary',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        spaceAfter=4,
        leading=12
    )
    
    # Phrases to filter out (case insensitive)
    intro_phrases = [
        "Here's a summary of the article in 3-4 bullet points:",
        "here is a summary of the article",
        "summary of the article",
        "article summary:",
        "bullet points:",
        "key points:"
    ]
    
    for i, article in enumerate(articles, start=1):
        title = safe_text(article.get("title"))
        category = safe_text(article.get("category") or "Uncategorized")
        summary = article.get("summary") or article.get("description") or "No summary"
        link = safe_text(article.get("link"))
        
        # Add to story
        story.append(Paragraph(f"{i}. [{category}] {title}", title_style))
        
        # Process summary - filter out introductory lines
        if summary:
            # Convert to string and handle None
            summary_str = str(summary) if summary else "No summary"
            
            # Split by newlines to preserve the original line breaks
            summary_lines = summary_str.split('\n')
            
            for line in summary_lines:
                line = line.strip()
                if line:
                    # Skip lines that contain introductory phrases
                    line_lower = line.lower()
                    skip_line = any(phrase in line_lower for phrase in intro_phrases)
                    
                    if not skip_line:
                        # Preserve bullet points if they already exist
                        if line.startswith(('•', '-', '*', '→')):
                            story.append(Paragraph(line, summary_style))
                        else:
                            story.append(Paragraph(f"• {line}", summary_style))
        else:
            story.append(Paragraph("• No summary available", summary_style))
        
        if link:
            story.append(Paragraph(f"Link: {link}", styles['Italic']))
        
        story.append(Spacer(1, 0.2*inch))
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.build(story)
    print(f"✅ PDF written with ReportLab: {output_path}")
