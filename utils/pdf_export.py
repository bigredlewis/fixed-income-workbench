"""
PDF export utility for AI-generated analysis results.
Uses fpdf2 to create clean, professional PDF reports.
"""

from io import BytesIO
from fpdf import FPDF
from datetime import datetime


class AnalysisPDF(FPDF):
    """Custom PDF class with header/footer branding."""

    def __init__(self, title: str = "Analysis Report", issuer: str = ""):
        super().__init__()
        self.report_title = title
        self.issuer = issuer

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Fixed Income Analyst Workbench", align="L")
        self.cell(0, 8, datetime.now().strftime("%B %d, %Y"), align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(70, 130, 180)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def _clean_text(text: str) -> str:
    """Replace characters that cause encoding issues in fpdf2."""
    replacements = {
        "\u2013": "-",   # en dash
        "\u2014": "--",  # em dash
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2022": "-",   # bullet
        "\u2026": "...", # ellipsis
        "\u00a0": " ",   # non-breaking space
        "\u2192": "->",  # right arrow
        "\u2190": "<-",  # left arrow
        "\u2264": "<=",  # less than or equal
        "\u2265": ">=",  # greater than or equal
        "\u00b1": "+/-", # plus minus
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Encode to latin-1 and replace any remaining unsupported chars
    return text.encode("latin-1", errors="replace").decode("latin-1")


def create_analysis_pdf(
    title: str,
    issuer: str,
    analysis_type: str,
    content: str,
    source_file: str = "",
) -> bytes:
    """Create a PDF from a single AI analysis result.

    Args:
        title: Report title
        issuer: Company/issuer name (optional)
        analysis_type: Type of analysis performed
        content: The AI-generated analysis text (markdown-ish)
        source_file: Name of the source document (optional)

    Returns:
        PDF file as bytes
    """
    pdf = AnalysisPDF(title=title, issuer=issuer)
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, _clean_text(title), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Metadata
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    if issuer:
        pdf.cell(0, 6, f"Issuer: {_clean_text(issuer)}", new_x="LMARGIN", new_y="NEXT")
    if analysis_type:
        pdf.cell(0, 6, f"Analysis Type: {_clean_text(analysis_type)}", new_x="LMARGIN", new_y="NEXT")
    if source_file:
        pdf.cell(0, 6, f"Source: {_clean_text(source_file)}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Divider
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # Content - parse markdown-like formatting
    _render_markdown_content(pdf, content)

    # Output
    return bytes(pdf.output())


def create_multi_analysis_pdf(
    title: str,
    analyses: list,
    issuer: str = "",
) -> bytes:
    """Create a PDF with multiple analysis results.

    Args:
        title: Report title
        analyses: List of dicts with keys: 'file', 'type', 'result'
        issuer: Company/issuer name (optional)

    Returns:
        PDF file as bytes
    """
    pdf = AnalysisPDF(title=title, issuer=issuer)
    pdf.alias_nb_pages()

    for i, analysis in enumerate(analyses):
        pdf.add_page()

        # Section title
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(30, 30, 30)
        section_title = f"{analysis.get('file', 'Analysis')} - {analysis.get('type', 'General')}"
        pdf.cell(0, 10, _clean_text(section_title), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # Metadata
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(6)

        # Content
        _render_markdown_content(pdf, analysis.get("result", ""))

    return bytes(pdf.output())


def _render_markdown_content(pdf: FPDF, content: str):
    """Render markdown-like content to PDF with basic formatting."""
    content = _clean_text(content)
    lines = content.split("\n")

    for line in lines:
        stripped = line.strip()

        if not stripped:
            pdf.ln(3)
            continue

        # Headers
        if stripped.startswith("### "):
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(50, 50, 50)
            pdf.ln(2)
            pdf.cell(0, 7, stripped[4:], new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
            continue

        if stripped.startswith("## "):
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(40, 40, 40)
            pdf.ln(3)
            pdf.cell(0, 8, stripped[3:], new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            continue

        if stripped.startswith("# "):
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(30, 30, 30)
            pdf.ln(4)
            pdf.cell(0, 9, stripped[2:], new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)
            continue

        # Numbered headers like "1. CREDIT PROFILE:" or "**HEADER:**"
        is_section_header = False
        if len(stripped) > 2:
            # Check for "1. TITLE" or "1) TITLE" patterns
            if (stripped[0].isdigit() and stripped[1] in ".)" and stripped[2] == " "):
                header_text = stripped[3:].strip()
                if header_text == header_text.upper() or header_text.startswith("**"):
                    is_section_header = True
            # Check for bold markers
            if stripped.startswith("**") and "**" in stripped[2:]:
                is_section_header = True

        if is_section_header:
            # Remove bold markers
            clean = stripped.replace("**", "")
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(50, 50, 50)
            pdf.ln(3)
            pdf.multi_cell(0, 6, clean)
            pdf.ln(1)
            continue

        # Bullet points
        if stripped.startswith("- ") or stripped.startswith("* "):
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(50, 50, 50)
            bullet_text = stripped[2:]
            # Handle bold within bullets
            bullet_text = bullet_text.replace("**", "")
            # Save x, indent, print, then restore x for next line
            left_margin = pdf.l_margin
            pdf.set_x(left_margin + 6)
            available_width = pdf.w - pdf.r_margin - pdf.get_x()
            pdf.multi_cell(available_width, 5, f"- {bullet_text}")
            continue

        # Regular text
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        # Remove bold markers from regular text
        clean_line = stripped.replace("**", "")
        pdf.multi_cell(0, 5, clean_line)
