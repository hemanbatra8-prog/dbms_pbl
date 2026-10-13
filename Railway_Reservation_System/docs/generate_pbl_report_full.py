"""
Complete Builder for Official Woxsen University DBMS PBL Report.
Reads: Railway_Reservation_System/docs/DBMS_PBL_Report_Template_Final_with_Guidelines.docx
Outputs:
- Railway_Reservation_System/docs/Railway_Ticket_Reservation_DBMS_PBL_Report.docx
- docs/Railway_Ticket_Reservation_DBMS_PBL_Report.docx
"""
import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / 'docs'
ROOT_DOCS_DIR = BASE_DIR.parent / 'docs'
SCREENSHOTS_DIR = DOCS_DIR / 'screenshots'
TEMPLATE_PATH = DOCS_DIR / 'DBMS_PBL_Report_Template_Final_with_Guidelines.docx'
TARGET_DOCX = DOCS_DIR / 'Railway_Ticket_Reservation_DBMS_PBL_Report.docx'

print("Script template ready.")
