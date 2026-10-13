"""
Build Official Woxsen University DBMS PBL Report.
Source Template: Railway_Reservation_System/docs/DBMS_PBL_Report_Template_Final_with_Guidelines.docx
Target Output:
- Railway_Reservation_System/docs/Railway_Ticket_Reservation_DBMS_PBL_Report.docx
- docs/Railway_Ticket_Reservation_DBMS_PBL_Report.docx
"""
import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / 'docs'
ROOT_DOCS_DIR = BASE_DIR.parent / 'docs'
SCREENSHOTS_DIR = DOCS_DIR / 'screenshots'
TEMPLATE_PATH = DOCS_DIR / 'DBMS_PBL_Report_Template_Final_with_Guidelines.docx'
TARGET_DOCX = DOCS_DIR / 'Railway_Ticket_Reservation_DBMS_PBL_Report.docx'

# Styling constants per Woxsen guidelines
FONT_NAME = 'Times New Roman'
FONT_CODE = 'Courier New'
COLOR_TEXT = RGBColor(0, 0, 0)
COLOR_MUTED = RGBColor(80, 80, 80)
COLOR_SUCCESS = RGBColor(16, 130, 70)
HEX_HEADER_BG = "EAEFF5"
HEX_ROW_ALT = "F8FAFC"
HEX_WHITE = "FFFFFF"

def set_cell_background(cell, hex_color):
    """Sets background shading of a docx table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    """Sets internal cell margins in twips."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def format_cell(cell, text, font_name=FONT_NAME, size_pt=10, bold=False, italic=False, color_rgb=COLOR_TEXT, align=WD_ALIGN_PARAGRAPH.LEFT, bg_color=None):
    if bg_color:
        set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
    p = cell.paragraphs[0]
    p.text = ''
    p.alignment = align
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    if color_rgb:
        run.font.color.rgb = color_rgb
    return p

def populate_table_data(table, headers, rows_data, col_widths=None):
    """Clears existing rows and repopulates with formatted headers and data rows."""
    # Clear all existing rows except the first (which will become header)
    while len(table.rows) > 1:
        tr = table.rows[-1]._tr
        tr.getparent().remove(tr)
    
    # Ensure header row has right number of columns
    hdr_cells = table.rows[0].cells
    while len(hdr_cells) < len(headers):
        table.rows[0]._tr.append(parse_xml(f'<w:tc {nsdecls("w")}><w:p/></w:tc>'))
        hdr_cells = table.rows[0].cells
        
    for c_idx, h_text in enumerate(headers):
        format_cell(hdr_cells[c_idx], h_text, font_name=FONT_NAME, size_pt=10, bold=True, bg_color=HEX_HEADER_BG)
        
    # Add data rows
    for r_idx, row_vals in enumerate(rows_data):
        row = table.add_row()
        bg_col = HEX_ROW_ALT if r_idx % 2 == 1 else HEX_WHITE
        for c_idx, val in enumerate(row_vals):
            is_status = val in ['PASSED', 'ACTIVE', 'CONFIRMED', '3NF', 'COMPLETED']
            color = COLOR_SUCCESS if is_status else COLOR_TEXT
            bold = is_status or (c_idx == 0 and len(row_vals) > 3)
            font_use = FONT_CODE if ('()' in str(val) or 'SELECT' in str(val) or 'CREATE' in str(val) or 'test_' in str(val) or 'FD_' in str(val)) else FONT_NAME
            size_use = 9.5 if font_use == FONT_CODE else 10
            format_cell(row.cells[c_idx], str(val), font_name=font_use, size_pt=size_use, bold=bold, color_rgb=color, bg_color=bg_col)
            
    # Apply column widths if provided
    if col_widths:
        for row in table.rows:
            for c_idx, w in enumerate(col_widths):
                if c_idx < len(row.cells):
                    row.cells[c_idx].width = Inches(w)

print("Helper functions defined.")
