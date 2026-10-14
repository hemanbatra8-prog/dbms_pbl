"""
Space-Optimized Builder for Official Woxsen University DBMS PBL Report.
Eliminates all unnecessary blank spaces, rogue page breaks, and empty paragraphs.
Generates:
- Railway_Reservation_System/docs/Railway_Ticket_Reservation_DBMS_PBL_Report.docx
- docs/Railway_Ticket_Reservation_DBMS_PBL_Report.docx
- Railway_Ticket_Reservation_DBMS_PBL_Report.docx
- PDF versions via LibreOffice headless export
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / 'docs'
ROOT_DIR = BASE_DIR.parent
ROOT_DOCS_DIR = ROOT_DIR / 'docs'
SCREENSHOTS_DIR = DOCS_DIR / 'screenshots'
TEMPLATE_PATH = DOCS_DIR / 'DBMS_PBL_Report_Template_Final_with_Guidelines.docx'
TARGET_DOCX = DOCS_DIR / 'Railway_Ticket_Reservation_DBMS_PBL_Report.docx'
TARGET_PDF = DOCS_DIR / 'Railway_Ticket_Reservation_DBMS_PBL_Report.pdf'

sys.path.insert(0, str(DOCS_DIR))
from pbl_report_data import (
    PROJECT_TITLE, STUDENT_DETAILS, TOC_DATA, TABLES_LIST, FIGURES_LIST,
    ACRONYMS_DATA, ABSTRACT_TEXT, KEYWORDS_TEXT,
    TABLE_1_HEADERS, TABLE_1_ROWS, TABLE_2_HEADERS, TABLE_2_ROWS,
    TABLE_3_HEADERS, TABLE_3_ROWS, TABLE_4_HEADERS, TABLE_4_ROWS,
    TABLE_5_HEADERS, TABLE_5_ROWS, TABLE_6_HEADERS, TABLE_6_ROWS,
    TABLE_7_HEADERS, TABLE_7_ROWS, TABLE_8_HEADERS, TABLE_8_ROWS,
    TABLE_9_HEADERS, TABLE_9_ROWS, TABLE_10_HEADERS, TABLE_10_ROWS,
    TABLE_11_HEADERS, TABLE_11_ROWS, TABLE_12_HEADERS, TABLE_12_ROWS,
    TABLE_13_HEADERS, TABLE_13_ROWS, TABLE_14_HEADERS, TABLE_14_ROWS,
    TABLE_15_HEADERS, TABLE_15_ROWS, IEEE_REFERENCES
)

FONT_NAME = 'Times New Roman'
FONT_CODE = 'Courier New'
COLOR_TEXT = RGBColor(0, 0, 0)
COLOR_SUCCESS = RGBColor(16, 130, 70)
HEX_HEADER_BG = "EAEFF5"
HEX_ROW_ALT = "F8FAFC"
HEX_WHITE = "FFFFFF"

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=20, bottom=20, left=45, right=45):
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

def format_cell(cell, text, font_name=FONT_NAME, size_pt=8.5, bold=False, italic=False, color_rgb=COLOR_TEXT, align=WD_ALIGN_PARAGRAPH.LEFT, bg_color=None, margins=(20, 20, 45, 45)):
    if bg_color:
        set_cell_background(cell, bg_color)
    set_cell_margins(cell, *margins)
    p = cell.paragraphs[0]
    p.text = ''
    p.alignment = align
    p.paragraph_format.line_spacing = 1.02
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

def populate_table_data(table, headers, rows_data, col_widths=None, base_size_pt=8.5, code_size_pt=8.0, margins=(20, 20, 45, 45)):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    while len(table.rows) > 1:
        tr = table.rows[-1]._tr
        tr.getparent().remove(tr)
        
    hdr_cells = table.rows[0].cells
    while len(hdr_cells) < len(headers):
        table.rows[0]._tr.append(parse_xml(f'<w:tc {nsdecls("w")}><w:p/></w:tc>'))
        hdr_cells = table.rows[0].cells
        
    trPr = table.rows[0]._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    
    for c_idx, h_text in enumerate(headers):
        format_cell(hdr_cells[c_idx], h_text, font_name=FONT_NAME, size_pt=base_size_pt, bold=True, bg_color=HEX_HEADER_BG, margins=margins)
        
    for r_idx, row_vals in enumerate(rows_data):
        row = table.add_row()
        r_trPr = row._tr.get_or_add_trPr()
        for elem in list(r_trPr):
            if 'cantSplit' in elem.tag:
                r_trPr.remove(elem)
                
        bg_col = HEX_ROW_ALT if r_idx % 2 == 1 else HEX_WHITE
        for c_idx, val in enumerate(row_vals):
            is_status = val in ['PASSED', 'ACTIVE', 'CONFIRMED', '3NF', 'COMPLETED', 'Yes']
            color = COLOR_SUCCESS if is_status else COLOR_TEXT
            bold = is_status or (c_idx == 0 and len(row_vals) > 3)
            font_use = FONT_CODE if ('()' in str(val) or 'SELECT' in str(val) or 'CREATE' in str(val) or 'test_' in str(val) or 'TC-' in str(val) or 'FR-' in str(val)) else FONT_NAME
            size_use = code_size_pt if font_use == FONT_CODE else base_size_pt
            format_cell(row.cells[c_idx], str(val), font_name=font_use, size_pt=size_use, bold=bold, color_rgb=color, bg_color=bg_col, margins=margins)
            
    if col_widths:
        for row in table.rows:
            for c_idx, w in enumerate(col_widths):
                if c_idx < len(row.cells):
                    row.cells[c_idx].width = Inches(w)

def add_paragraph_after(target_p, text, font_name=FONT_NAME, size_pt=11.0, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2, space_before=0, line_spacing=1.15):
    new_p = parse_xml(f'<w:p {nsdecls("w")}/>')
    target_p._p.addnext(new_p)
    p = docx.text.paragraph.Paragraph(new_p, target_p._parent)
    p.alignment = align
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    return p

def remove_element(elem):
    parent = elem.getparent()
    if parent is not None:
        parent.remove(elem)

def clean_run_page_breaks(p):
    """Removes rogue <w:br w:type='page'/> inside paragraph runs."""
    for r in p.runs:
        for elem in list(r._r):
            if elem.tag.endswith('br') and elem.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type') == 'page':
                r._r.remove(elem)
            elif elem.tag.endswith('br') and elem.get(f'{{{nsdecls("w")}}}type') == 'page':
                r._r.remove(elem)

def generate_report(toc_data_override=None, tables_list_override=None, figures_list_override=None):
    print(f"Loading template: {TEMPLATE_PATH}")
    doc = docx.Document(str(TEMPLATE_PATH))
    
    # -------------------------------------------------------------------------
    # 1. CLEAN UP GUIDELINES AT THE START
    # -------------------------------------------------------------------------
    elems_to_remove = []
    for elem in doc._body._element:
        if elem.tag.endswith('tbl'):
            break
        elems_to_remove.append(elem)
    for elem in elems_to_remove:
        remove_element(elem)

    # -------------------------------------------------------------------------
    # 2. TITLE PAGE TABLES & DETAILS
    # -------------------------------------------------------------------------
    t1 = doc.tables[1]
    format_cell(t1.rows[0].cells[0], PROJECT_TITLE, font_name=FONT_NAME, size_pt=12.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    
    t2 = doc.tables[2]
    format_cell(t2.rows[0].cells[1], STUDENT_DETAILS["program"], font_name=FONT_NAME, size_pt=9.0, bold=False)
    format_cell(t2.rows[1].cells[1], STUDENT_DETAILS["section"], font_name=FONT_NAME, size_pt=9.0, bold=False)
    format_cell(t2.rows[2].cells[1], STUDENT_DETAILS["faculty"], font_name=FONT_NAME, size_pt=9.0, bold=False)
    format_cell(t2.rows[3].cells[1], STUDENT_DETAILS["date"], font_name=FONT_NAME, size_pt=9.0, bold=False)
    format_cell(t2.rows[4].cells[1], STUDENT_DETAILS["year"], font_name=FONT_NAME, size_pt=9.0, bold=False)
    
    t3 = doc.tables[3]
    format_cell(t3.rows[1].cells[0], STUDENT_DETAILS["roll_no"], font_name=FONT_NAME, size_pt=9.0, bold=True)
    format_cell(t3.rows[1].cells[1], STUDENT_DETAILS["name"], font_name=FONT_NAME, size_pt=9.0, bold=True)
    format_cell(t3.rows[1].cells[2], STUDENT_DETAILS["mobile"], font_name=FONT_NAME, size_pt=9.0, bold=False)
    format_cell(t3.rows[1].cells[3], STUDENT_DETAILS["email"], font_name=FONT_NAME, size_pt=9.0, bold=False)

    # -------------------------------------------------------------------------
    # 3. ACKNOWLEDGEMENT & UNDERTAKING
    # -------------------------------------------------------------------------
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "Name of the Faculty" in p.text:
            p.text = (
                f"I thank my course faculty, {STUDENT_DETAILS['faculty']}, for the continuous guidance, constructive suggestions, "
                "and expert technical mentorship throughout the conceptualization, relational normalization, and full-stack implementation "
                "of this project. Her guidance helped me master the practical application of database concepts including advanced ER modeling, "
                "3NF dependency preservation, pessimistic transaction locking, SQL analytical reports, and relational web development.\n\n"
                f"Submitted by: {STUDENT_DETAILS['name']} (Roll No: {STUDENT_DETAILS['roll_no']}, Section: {STUDENT_DETAILS['section']})."
            )
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.2
            p.paragraph_format.space_after = Pt(2)
            p.runs[0].font.name = FONT_NAME
            p.runs[0].font.size = Pt(11.0)
        elif "[Project Title]" in p.text:
            p.text = p.text.replace("[Project Title]", "Railway Ticket Reservation and Journey Management System Using Relational Database Management Systems")
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.2
            p.paragraph_format.space_after = Pt(2)
            p.runs[0].font.name = FONT_NAME
            p.runs[0].font.size = Pt(11.0)

    # Table 4: Undertaking Signature Table
    t4 = doc.tables[4]
    format_cell(t4.rows[0].cells[4], "Heman\n(Digital Signature)", font_name=FONT_NAME, size_pt=8.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(t4.rows[1].cells[2], STUDENT_DETAILS["date"], font_name=FONT_NAME, size_pt=8.5)
    format_cell(t4.rows[1].cells[4], STUDENT_DETAILS["name"], font_name=FONT_NAME, size_pt=8.5, bold=True)
    format_cell(t4.rows[2].cells[2], STUDENT_DETAILS["place"], font_name=FONT_NAME, size_pt=8.5)
    format_cell(t4.rows[2].cells[4], STUDENT_DETAILS["roll_no"], font_name=FONT_NAME, size_pt=8.5, bold=True)
    format_cell(t4.rows[3].cells[4], "B.Tech CSE (AIML)", font_name=FONT_NAME, size_pt=8.5)

    # -------------------------------------------------------------------------
    # 4. PRELIMINARY LISTS (TOC, TABLES, FIGURES, ACRONYMS)
    # -------------------------------------------------------------------------
    t5 = doc.tables[5]
    populate_table_data(t5, ["Contents", "Page No."], toc_data_override or TOC_DATA, col_widths=[5.5, 1.0], base_size_pt=8.5)
    
    t6 = doc.tables[6]
    populate_table_data(t6, ["Table No.", "Table Title", "Page No."], tables_list_override or TABLES_LIST, col_widths=[1.4, 4.3, 0.8], base_size_pt=8.5)
    
    t7 = doc.tables[7]
    populate_table_data(t7, ["Figure No.", "Figure Title", "Page No."], figures_list_override or FIGURES_LIST, col_widths=[1.4, 4.3, 0.8], base_size_pt=8.5)
    
    t8 = doc.tables[8]
    populate_table_data(t8, ["Acronym", "Expansion"], ACRONYMS_DATA, col_widths=[1.5, 5.0], base_size_pt=8.5)
    
    # Remove Table 9 (Instructional guide table for abstract)
    t9 = doc.tables[9]
    remove_element(t9._tbl)

    # Unify LIST OF TABLES and LIST OF FIGURES on Page 5
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "LIST OF FIGURES" in p.text:
            p.paragraph_format.page_break_before = False
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)

    # -------------------------------------------------------------------------
    # 5. ABSTRACT & KEYWORDS
    # -------------------------------------------------------------------------
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "[Write the final abstract here.]" in p.text:
            p.text = ABSTRACT_TEXT
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.2
            p.paragraph_format.space_after = Pt(3)
            p.runs[0].font.name = FONT_NAME
            p.runs[0].font.size = Pt(11.0)
        elif "Keywords: [Relational Database" in p.text or "Keywords:" in p.text:
            p.text = f"Keywords: {KEYWORDS_TEXT}"
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.2
            p.paragraph_format.space_after = Pt(4)
            p.runs[0].font.name = FONT_NAME
            p.runs[0].font.size = Pt(11.0)
            p.runs[0].font.italic = True

    # -------------------------------------------------------------------------
    # 6. CHAPTER 1: PROBLEM STATEMENT, OBJECTIVES, SCOPE & ERD
    # -------------------------------------------------------------------------
    p_prob_text = (
        "Passenger railway operations face a fundamentally more challenging inventory allocation dilemma than commercial "
        "airlines. In airline reservation systems, seat inventory is allocated monolithically for the entirety of a point-to-point "
        "flight leg. In contrast, railway trains travel through long linear corridors of 10 to 30 intermediate stations. A single physical "
        "berth may be allocated to Passenger A from Station 1 to Station 3, vacated, and immediately re-allocated to Passenger B from "
        "Station 3 to Station 6 without physical conflict. However, naive relational designs that rely on a single boolean 'is_booked' "
        "flag cause catastrophic double-booking across overlapping sub-journeys, or prematurely report trains as 'sold out' despite "
        "ample vacant capacity on unreserved sub-segments.\n\n"
        "Furthermore, high-concurrency ticket booking creates severe database race conditions during peak reservation windows. "
        "When hundreds of concurrent passengers attempt to reserve the final remaining berth on a high-demand train run, uncoordinated "
        "read-modify-write cycles lead to severe overbooking anomalies and transactional deadlocks. Existing manual processes and legacy "
        "flat databases fail to provide mathematical interval validation, transactional concurrency safety, automated FIFO waitlist "
        "promotion, and multi-dimensional operational analytics. This project engineers a mathematically formalized, 3NF-compliant "
        "relational database system powered by MySQL 8.x InnoDB and Python Flask to solve these core operational challenges."
    )
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "[Problem statement - approximately 1 to 2 paragraphs.]" in p.text:
            p.text = p_prob_text
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.2
            p.paragraph_format.space_after = Pt(2)
            p.runs[0].font.name = FONT_NAME
            p.runs[0].font.size = Pt(11.0)

    obj_texts = [
        "1. Design a normalized relational schema up to Third Normal Form (3NF) comprising 14 decoupled relations, eliminating partial and transitive functional dependencies to guarantee zero insertion, update, and deletion anomalies.",
        "2. Formulate and implement a mathematical half-open interval allocation algorithm [start_stop_seq, end_stop_seq) to evaluate segment conflicts dynamically and maximize seat utilization across multi-hop rail corridors.",
        "3. Implement pessimistic row-level locking (SELECT ... FOR UPDATE) and atomic database transactions to guarantee ACID concurrency compliance, preventing overbooking race conditions during simultaneous user checkouts.",
        "4. Develop an automated FIFO waitlist management and queue promotion mechanism that immediately promotes waiting passengers and reallocates vacated berths upon ticket cancellation.",
        "5. Construct a full-stack Python/Flask web application connected to MySQL InnoDB with parameterized query protection, intuitive Electronic Reservation Slip (ERS) generation, and 12 analytical SQL reporting benchmarks."
    ]
    obj_idx = 0
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "[Objective" in p.text:
            if obj_idx < len(obj_texts):
                p.text = obj_texts[obj_idx]
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_after = Pt(2)
                p.runs[0].font.name = FONT_NAME
                p.runs[0].font.size = Pt(10.5)
                obj_idx += 1

    # Table 1: Scope & Assumptions (Table 9)
    populate_table_data(doc.tables[9], TABLE_1_HEADERS, TABLE_1_ROWS, col_widths=[1.8, 4.7], base_size_pt=8.5)
    # Table 2: Proposed Solution Strategy (Table 10)
    populate_table_data(doc.tables[10], TABLE_2_HEADERS, TABLE_2_ROWS, col_widths=[1.8, 4.7], base_size_pt=8.5)
    # Table 3: Functional Requirements (Table 11)
    populate_table_data(doc.tables[11], TABLE_3_HEADERS, TABLE_3_ROWS, col_widths=[1.0, 4.3, 1.2], base_size_pt=8.5)

    # 1.6 ER Diagram: Replace [Insert approved ER diagram here]
    er_path = SCREENSHOTS_DIR / 'er_diagram.png'
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "[Insert approved ER diagram here]" in p.text:
            p.text = ""
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.keep_with_next = True
            if er_path.exists():
                r = p.add_run()
                r.add_picture(str(er_path), width=Inches(4.6))
    
    # Table 4: Entity & Relationship Summary (Table 12)
    populate_table_data(doc.tables[12], TABLE_4_HEADERS, TABLE_4_ROWS, col_widths=[1.7, 2.8, 2.0], base_size_pt=8.0, code_size_pt=7.5, margins=(15, 15, 35, 35))

    # -------------------------------------------------------------------------
    # 7. CHAPTER 2: LOGICAL DATABASE DESIGN & NORMALIZATION
    # -------------------------------------------------------------------------
    populate_table_data(doc.tables[13], TABLE_5_HEADERS, TABLE_5_ROWS, col_widths=[0.6, 1.8, 4.1], base_size_pt=8.5)
    populate_table_data(doc.tables[14], TABLE_6_HEADERS, TABLE_6_ROWS, col_widths=[1.5, 1.4, 1.6, 2.0], base_size_pt=8.0, code_size_pt=7.5)

    # Section 2.3: Functional Dependencies
    fd_text = (
        "The relational design is governed by a rigorous set of minimal functional dependencies across all 14 relations, "
        "ensuring that every non-key attribute is fully functionally dependent on candidate keys:\n\n"
        "1. stations: station_id -> {station_code, station_name, city, state}; station_code -> {station_id, ...}\n"
        "2. routes: route_id -> {route_code, source_station_id, destination_station_id, total_distance_km}\n"
        "3. train_stops: stop_id -> {route_id, station_id, stop_sequence, distance_from_source_km, arrival_time, departure_time}; "
        "{route_id, stop_sequence} -> {stop_id, station_id, ...}\n"
        "4. trains: train_id -> {train_number, train_name, train_type, route_id}; train_number -> {train_id, ...}\n"
        "5. train_runs: run_id -> {train_id, run_date, status}; {train_id, run_date} -> {run_id, status}\n"
        "6. coaches: coach_id -> {train_id, coach_code, travel_class, total_seats}; {train_id, coach_code} -> {coach_id, ...}\n"
        "7. seats: seat_id -> {coach_id, seat_number, berth_type}; {coach_id, seat_number} -> {seat_id, berth_type}\n"
        "8. passengers: passenger_id -> {full_name, gender, age, email, phone, id_card_type, id_card_number}\n"
        "9. fare_rules: fare_id -> {train_type, travel_class, base_fare, rate_per_km, reservation_fee}; {train_type, travel_class} -> {fare_id, ...}\n"
        "10. bookings: booking_id -> {pnr_number, run_id, passenger_id, origin_station_id, destination_station_id, origin_stop_seq, destination_stop_seq, travel_class, booking_status, total_fare, booked_at}\n"
        "11. journey_segments: segment_id -> {booking_id, seat_id, run_id, start_stop_seq, end_stop_seq, allocation_status}\n"
        "12. waitlists: waitlist_id -> {booking_id, run_id, travel_class, origin_stop_seq, destination_stop_seq, position, waitlist_status, created_at}\n"
        "13. payments: payment_id -> {booking_id, amount, payment_method, transaction_reference, payment_status, paid_at}\n"
        "14. cancellations: cancellation_id -> {booking_id, cancellation_reason, cancellation_fee, refund_amount, refund_status, cancelled_at}"
    )
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "[Example format: Key -> non-key attributes" in p.text:
            p.text = fd_text
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(2)
            p.runs[0].font.name = FONT_CODE
            p.runs[0].font.size = Pt(7.5)

    # Table 7: Normalization Status up to 3NF (Table 15)
    populate_table_data(doc.tables[15], TABLE_7_HEADERS, TABLE_7_ROWS, col_widths=[1.5, 0.6, 0.6, 0.6, 0.6, 2.6], base_size_pt=8.5)

    # Section 2.4: Normalization Narrative & BCNF Trade-off
    norm_narrative = (
        "Normalization Walkthrough up to Third Normal Form (3NF):\n\n"
        "• First Normal Form (1NF): All multi-valued attributes and repeating groups were systematically eliminated. In unnormalized "
        "railway manifests, passengers and intermediate station halts are stored as comma-delimited arrays. Decomposing these into dedicated "
        "tables (passengers, train_stops, journey_segments) ensures that every attribute contains only atomic, indivisible domain values.\n\n"
        "• Second Normal Form (2NF): In a composite-key candidate relation such as (coach_id, seat_number), non-prime attributes like "
        "total_seats and travel_class depend solely on coach_id, not on seat_number. Decomposing coaches and seats eliminates partial functional "
        "dependencies, ensuring that every non-prime attribute is fully functionally dependent on the primary key.\n\n"
        "• Third Normal Form (3NF): In naive reservation tables, ticket records store train names, origin city names, and base fare rates. "
        "However, booking_id -> origin_station_id -> city and booking_id -> train_type -> base_fare represent transitive functional dependencies "
        "X -> Y and Y -> Z where Y is not a superkey. Normalizing into stations, routes, and fare_rules eliminates update and deletion anomalies.\n\n"
        "• Boyce-Codd Normal Form (BCNF) vs 3NF Engineering Trade-Off: In relations with overlapping candidate keys such as train_stops where "
        "both {route_id, stop_sequence} and {route_id, station_id} are candidate keys, decomposing strictly to BCNF would fragment the functional "
        "dependency set, requiring cross-table JOIN constraints to validate stop order. Preserving 3NF guarantees dependency preservation "
        "(F = F1 U F2) without requiring costly multi-table locking triggers during high-speed transaction inserts."
    )
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "2.4 Normalization" in p.text:
            add_paragraph_after(p, norm_narrative, size_pt=9.5, space_after=2, line_spacing=1.12)

    # Table 8: Data Dictionary (Table 16)
    populate_table_data(doc.tables[16], TABLE_8_HEADERS, TABLE_8_ROWS, col_widths=[1.2, 1.4, 1.1, 1.4, 1.4], base_size_pt=8.0, code_size_pt=7.5, margins=(15, 15, 35, 35))

    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "2.6 Implementation of Logical Design" in p.text:
            p.paragraph_format.page_break_before = True
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(2)

    # Table 9: Database Implementation Environment (Table 17)
    populate_table_data(doc.tables[17], TABLE_9_HEADERS, TABLE_9_ROWS, col_widths=[2.5, 4.0], base_size_pt=8.0, margins=(15, 15, 35, 35))

    # Section 2.6: DDL & Sample Data Excerpts (Tightly styled)
    ddl_sample_text = (
        "-- Representative DDL Excerpt: Multi-Hop Journey Segments & Concurrency Locks\n"
        "CREATE TABLE journey_segments (\n"
        "    segment_id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    booking_id INT NOT NULL,\n"
        "    seat_id INT NOT NULL,\n"
        "    run_id INT NOT NULL,\n"
        "    start_stop_seq INT NOT NULL,\n"
        "    end_stop_seq INT NOT NULL,\n"
        "    allocation_status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',\n"
        "    CONSTRAINT fk_seg_booking FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE,\n"
        "    CONSTRAINT fk_seg_seat FOREIGN KEY (seat_id) REFERENCES seats(seat_id) ON DELETE RESTRICT,\n"
        "    CONSTRAINT fk_seg_run FOREIGN KEY (run_id) REFERENCES train_runs(run_id) ON DELETE CASCADE,\n"
        "    CONSTRAINT chk_seg_seq_order CHECK (end_stop_seq > start_stop_seq),\n"
        "    INDEX idx_seat_run_alloc (run_id, seat_id, allocation_status)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n\n"
        "-- Representative Sample Insert Record:\n"
        "INSERT INTO stations (station_id, station_code, station_name, city, state)\n"
        "VALUES (1, 'NDLS', 'New Delhi Railway Station', 'New Delhi', 'Delhi'),\n"
        "       (2, 'CNB', 'Kanpur Central', 'Kanpur', 'Uttar Pradesh'),\n"
        "       (3, 'PRYJ', 'Prayagraj Junction', 'Prayagraj', 'Uttar Pradesh'),\n"
        "       (4, 'BSB', 'Varanasi Junction', 'Varanasi', 'Uttar Pradesh');"
    )
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "[Insert representative DDL snippets" in p.text:
            p.text = ddl_sample_text
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(2)
            p.runs[0].font.name = FONT_CODE
            p.runs[0].font.size = Pt(7.5)

    # -------------------------------------------------------------------------
    # 8. CHAPTER 3: APPLICATION DEVELOPMENT & TESTING
    # -------------------------------------------------------------------------
    p_app_overview = (
        "The application layer is implemented as an asynchronous Python Flask web service following the Model-View-Controller (MVC) "
        "architectural pattern. The user interface utilizes responsive HTML5 and Bootstrap 5.3 components, communicating with Flask Blueprint "
        "controllers. Database operations are mediated via SQLAlchemy ORM configured over a production-grade connection pool (10 persistent "
        "connections, 20 burst overflow). To eliminate SQL injection vulnerabilities, all dynamic queries strictly utilize parameterized "
        "bindings. Core reservation operations are encapsulated in serialized transactional boundaries utilizing pessimistic row-level "
        "locking (SELECT ... FOR UPDATE) to guarantee absolute ACID consistency during peak concurrent booking spikes."
    )
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "[Application overview - approximately 1 paragraph.]" in p.text:
            p.text = p_app_overview
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            p.runs[0].font.name = FONT_NAME
            p.runs[0].font.size = Pt(10.5)

    populate_table_data(doc.tables[18], TABLE_10_HEADERS, TABLE_10_ROWS, col_widths=[2.5, 4.0], base_size_pt=8.0, margins=(12, 12, 30, 30))
    populate_table_data(doc.tables[19], TABLE_11_HEADERS, TABLE_11_ROWS, col_widths=[1.5, 1.8, 1.8, 1.4], base_size_pt=7.5, code_size_pt=7.0, margins=(10, 10, 25, 25))
    populate_table_data(doc.tables[20], TABLE_12_HEADERS, TABLE_12_ROWS, col_widths=[1.2, 1.6, 1.5, 2.2], base_size_pt=7.5, code_size_pt=7.0, margins=(10, 10, 25, 25))
    populate_table_data(doc.tables[21], TABLE_13_HEADERS, TABLE_13_ROWS, col_widths=[1.6, 2.3, 2.6], base_size_pt=7.5, code_size_pt=7.0, margins=(10, 10, 25, 25))
    populate_table_data(doc.tables[22], TABLE_14_HEADERS, TABLE_14_ROWS, col_widths=[1.8, 2.2, 2.5], base_size_pt=7.5, code_size_pt=7.0, margins=(10, 10, 25, 25))

    # Section 3.7: Optimized Screenshot Placement
    # Screen width = 3.7 in (height = 2.24 in)
    # Page A: Heading + Figure 2, Figure 3, Figure 4
    # Page B: Figure 5, Figure 6, Figure 7
    # Page C: Section 3.8 + Table 15 + Key Verification Results narrative
    screens = [
        ("dashboard.png", "Figure 2. Executive Analytics and Key Performance Indicator (KPI) Dashboard"),
        ("search_results.png", "Figure 3. Multi-Hop Train Search and Segment Seat Inventory Results"),
        ("booking_ers.png", "Figure 4. Confirmed Electronic Reservation Slip (ERS Ticket Confirmation)"),
        ("waitlist_queue.png", "Figure 5. Live Waitlist Queue and Real-Time Position Tracking"),
    ]
    
    img_placeholders = [p for p in doc.paragraphs if "[Insert application screenshot here]" in p.text]
    for idx, (img_file, caption) in enumerate(screens):
        if idx < len(img_placeholders):
            target_p = img_placeholders[idx]
            target_p.text = ""
            target_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            target_p.paragraph_format.space_before = Pt(2)
            target_p.paragraph_format.space_after = Pt(1)
            target_p.paragraph_format.keep_with_next = True
            img_full = SCREENSHOTS_DIR / img_file
            if img_full.exists():
                r = target_p.add_run()
                r.add_picture(str(img_full), width=Inches(3.7))

    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "Figure 2." in p.text:
            p.text = "Figure 2. Executive Analytics and Key Performance Indicator (KPI) Dashboard"
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
        elif "Figure 3." in p.text:
            p.text = "Figure 3. Multi-Hop Train Search and Segment Seat Inventory Results"
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
        elif "Figure 4." in p.text:
            p.text = "Figure 4. Confirmed Electronic Reservation Slip (ERS Ticket Confirmation)"
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
        elif "Figure 5." in p.text:
            p.text = "Figure 5. Live Waitlist Queue and Real-Time Position Tracking"
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)

    # Insert Figure 6 & 7 before Section 3.8
    p_38 = None
    for p in doc.paragraphs:
        if "3.8 Testing and Results" in p.text:
            p_38 = p
            break
            
    if p_38:
        img_reports = SCREENSHOTS_DIR / 'sql_reports.png'
        if img_reports.exists():
            p_img6 = p_38.insert_paragraph_before()
            p_img6.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img6.paragraph_format.space_before = Pt(2)
            p_img6.paragraph_format.space_after = Pt(1)
            p_img6.paragraph_format.keep_with_next = True
            p_img6.add_run().add_picture(str(img_reports), width=Inches(3.7))
            p_cap6 = p_38.insert_paragraph_before("Figure 6. Executive SQL Analytical Reports Console")
            p_cap6.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap6.paragraph_format.space_before = Pt(1)
            p_cap6.paragraph_format.space_after = Pt(2)
            p_cap6.runs[0].font.name = FONT_NAME
            p_cap6.runs[0].font.size = Pt(9.0)
            p_cap6.runs[0].font.bold = True
            
        img_admin = SCREENSHOTS_DIR / 'schema_admin.png'
        if img_admin.exists():
            p_img7 = p_38.insert_paragraph_before()
            p_img7.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img7.paragraph_format.space_before = Pt(2)
            p_img7.paragraph_format.space_after = Pt(1)
            p_img7.paragraph_format.keep_with_next = True
            p_img7.add_run().add_picture(str(img_admin), width=Inches(3.7))
            p_cap7 = p_38.insert_paragraph_before("Figure 7. Relational Database Schema Explorer and Administrative Inventory Control")
            p_cap7.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap7.paragraph_format.space_before = Pt(1)
            p_cap7.paragraph_format.space_after = Pt(2)
            p_cap7.runs[0].font.name = FONT_NAME
            p_cap7.runs[0].font.size = Pt(9.0)
            p_cap7.runs[0].font.bold = True

    # Find the paragraph for Figure 5's image and set page_break_before = True so Figures 5, 6, 7 start on Page B
    for p in doc.paragraphs:
        if "Figure 5." in p.text:
            prev_p = p._p.getprevious()
            if prev_p is not None:
                prev_par = docx.text.paragraph.Paragraph(prev_p, doc)
                prev_par.paragraph_format.page_break_before = True

    # Set page_break_before = True on Section 3.8 so it starts cleanly on Page C
    if p_38:
        p_38.paragraph_format.page_break_before = True

    # Table 15: Test Cases (Table 23)
    populate_table_data(doc.tables[23], TABLE_15_HEADERS, TABLE_15_ROWS, col_widths=[0.8, 1.5, 1.6, 1.5, 1.4, 0.7], base_size_pt=7.5, code_size_pt=7.0, margins=(15, 15, 30, 30))

    # Section 3.8: Key Results & Observations Narrative
    test_summary_text = (
        "Key Verification Results and Empirical Observations:\n\n"
        "• 100% Automated Test Pass Rate: All 16 automated integration and unit test suites executed with zero failures "
        "(16 passed in 0.41 seconds on macOS Darwin arm64 under pytest 8.4.2).\n"
        "• Mathematical Interval Integrity: Verified that non-overlapping seat allocations [1,2) and [2,4) coexist on the same "
        "physical berth without conflict, while overlapping requests [1,3) and [2,4) are rejected immediately.\n"
        "• Referential & Domain Constraint Enforcement: Verified that negative base fares, passenger ages outside [1, 119], duplicate "
        "train numbers, and invalid foreign keys are strictly blocked at the relational engine level, preventing corrupt data states.\n"
        "• Concurrency & Waitlist Promotion: Confirmed that cancellation of a confirmed seat triggers immediate automated FIFO "
        "promotion of the next waiting candidate, updating booking status to CONFIRMED and reallocating the vacated berth atomically."
    )
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "[Key results and observations.]" in p.text:
            p.text = test_summary_text
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.08
            p.paragraph_format.space_after = Pt(2)
            p.runs[0].font.name = FONT_NAME
            p.runs[0].font.size = Pt(9.5)

    # -------------------------------------------------------------------------
    # 9. CHAPTER 4: CONCLUSION & FUTURE ENHANCEMENTS
    # -------------------------------------------------------------------------
    conclusion_text = (
        "This project successfully designed, formalized, implemented, and verified an end-to-end Railway Ticket Reservation and "
        "Journey Management System engineered around relational database management principles. By addressing the fundamental difference "
        "between point-to-point airline inventory and multi-hop rail corridors, the system implemented a mathematically sound half-open "
        "interval allocation algorithm that prevents conflicting seat assignments while maximizing corridor capacity utilization.\n\n"
        "The relational database schema comprises 14 decoupled relations strictly normalized to Third Normal Form (3NF), successfully "
        "eliminating insertion, update, and deletion anomalies while preserving all functional dependencies. ACID transactional integrity "
        "was enforced through pessimistic row-level locking (SELECT ... FOR UPDATE) and atomic database transactions. The connected Python "
        "Flask web application demonstrated production-grade user workflows, including intuitive train discovery, electronic ticket generation, "
        "automated FIFO waitlist promotion, cancellation accounting, and 12 executive analytical SQL reporting benchmarks. Comprehensive "
        "verification across 16 automated pytest unit and integration test suites confirmed the structural and operational robustness of the design."
    )
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "[Conclusion - approximately 1 to 2 paragraphs.]" in p.text:
            p.text = conclusion_text
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            p.runs[0].font.name = FONT_NAME
            p.runs[0].font.size = Pt(11.0)

    enhancements = [
        "1. Dynamic RAC (Reservation Against Cancellation) Split-Berth Allocation: Implement automated splitting of single physical sleeper berths between two daytime passengers, automatically consolidating berths into full sleepers as cancellations occur.",
        "2. Live Indian Railways IRCTC API & Telemetry Integration: Connect the database to real-time train tracking telemetry and external GPS feeds to dynamically adjust departure schedules and track platform delays.",
        "3. Distributed In-Memory Caching (Redis) & Read Replicas: Implement Redis key-value caching for static route stop lookups and database read replicas to handle extreme peak traffic surges during morning Tatkal booking windows."
    ]
    e_idx = 0
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "[Limitation / Future enhancement" in p.text:
            if e_idx < len(enhancements):
                p.text = enhancements[e_idx]
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_after = Pt(2)
                p.runs[0].font.name = FONT_NAME
                p.runs[0].font.size = Pt(10.5)
                e_idx += 1

    # -------------------------------------------------------------------------
    # 10. CHAPTER 5: REFERENCES (IEEE STYLE - CLEAN NUMBERING)
    # -------------------------------------------------------------------------
    ref_placeholders = [p for p in doc.paragraphs if "[Replace with an actual source cited" in p.text]
    last_p = ref_placeholders[-1] if ref_placeholders else None
    for idx, ref_text in enumerate(IEEE_REFERENCES):
        if idx < len(ref_placeholders):
            target_p = ref_placeholders[idx]
            # Strip automatic list numbering from template
            numPr = target_p._p.xpath('./w:pPr/w:numPr')
            for elem in numPr:
                elem.getparent().remove(elem)
            target_p.text = ref_text
            target_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            target_p.paragraph_format.line_spacing = 1.1
            target_p.paragraph_format.space_after = Pt(2)
            target_p.runs[0].font.name = FONT_NAME
            target_p.runs[0].font.size = Pt(9.0)
        else:
            if last_p is not None:
                new_p = add_paragraph_after(last_p, ref_text, font_name=FONT_NAME, size_pt=9.0, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=2, line_spacing=1.1)
                last_p = new_p

    p_to_del = []
    del_mode = False
    for p in doc.paragraphs:
        txt = p.text.strip()
        if "Use IEEE reference style throughout" in txt or "5.1 IEEE In-Text Citation Guidelines" in txt:
            del_mode = True
        elif "APPENDICES" in txt:
            del_mode = False
        if del_mode:
            p_to_del.append(p)
    for p in p_to_del:
        remove_element(p._p)

    # -------------------------------------------------------------------------
    # 11. CHAPTER 6: APPENDICES (Tightly styled)
    # -------------------------------------------------------------------------
    app_a_text = (
        "The complete relational database schema DDL script, table constraints, indices, relational views, and benchmark SQL "
        "reports are maintained in the following version-controlled repository files:\n\n"
        "• DDL Schema & Table Constraints: Railway_Reservation_System/database/schema.sql (14 relations in 3NF)\n"
        "• Pre-Compiled Relational Views: Railway_Reservation_System/database/views.sql (vw_confirmed_segments, vw_booking_summary, vw_train_occupancy_summary)\n"
        "• Analytical & Operational Reports: Railway_Reservation_System/database/reports.sql (12 benchmark SQL queries)\n"
        "• Database Seeding & Synthetic Data Generator: Railway_Reservation_System/database/seed_data.py"
    )
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "[Database script / file reference]" in p.text:
            p.text = app_a_text
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(2)
            p.runs[0].font.name = FONT_CODE
            p.runs[0].font.size = Pt(8.0)

    app_b_text = (
        "The complete full-stack web application source code is organized into modular Flask blueprints:\n\n"
        "• Main Application Entrypoint: Railway_Reservation_System/run.py\n"
        "• Application Factory & Extensions: Railway_Reservation_System/app/__init__.py, Railway_Reservation_System/app/extensions.py\n"
        "• Relational ORM Models (13 files): Railway_Reservation_System/app/models/*.py\n"
        "• Business Services & Interval Math: Railway_Reservation_System/app/services/availability_service.py\n"
        "• Flask Route Blueprints (8 controllers): Railway_Reservation_System/app/routes/*.py\n"
        "• Responsive Front-End UI Templates (12 Jinja2 files): Railway_Reservation_System/app/templates/*.html\n"
        "• Automated Test Suite (16 pytest suites): Railway_Reservation_System/tests/test_*.py"
    )
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "[Source-code / repository reference]" in p.text:
            p.text = app_b_text
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(2)
            p.runs[0].font.name = FONT_CODE
            p.runs[0].font.size = Pt(8.0)

    app_c_text = (
        "Automated Test Execution Transcript (pytest 8.4.2 | Python 3.9.6 | macOS arm64):\n"
        "============================= test session starts ==============================\n"
        "Railway_Reservation_System/tests/test_availability.py::test_interval_overlap_logic PASSED      [  6%]\n"
        "Railway_Reservation_System/tests/test_availability.py::test_non_overlapping_seat_reuse PASSED   [ 12%]\n"
        "Railway_Reservation_System/tests/test_availability.py::test_conflicting_interval_detection PASSED [ 18%]\n"
        "Railway_Reservation_System/tests/test_availability.py::test_cancelled_allocation_restores_availability PASSED [ 25%]\n"
        "Railway_Reservation_System/tests/test_cancellations.py::test_eligible_cancellation_and_refund_policy PASSED [ 31%]\n"
        "Railway_Reservation_System/tests/test_cancellations.py::test_duplicate_cancellation_rejected PASSED [ 37%]\n"
        "Railway_Reservation_System/tests/test_cancellations.py::test_automated_waitlist_promotion PASSED [ 43%]\n"
        "Railway_Reservation_System/tests/test_integrity.py::test_unique_train_number_constraint PASSED [ 50%]\n"
        "Railway_Reservation_System/tests/test_integrity.py::test_invalid_foreign_key_rejected PASSED    [ 56%]\n"
        "Railway_Reservation_System/tests/test_integrity.py::test_passenger_age_check_constraint PASSED   [ 62%]\n"
        "Railway_Reservation_System/tests/test_integrity.py::test_negative_fare_check_constraint PASSED [ 68%]\n"
        "Railway_Reservation_System/tests/test_integrity.py::test_duplicate_stop_sequence_rejected PASSED [ 75%]\n"
        "Railway_Reservation_System/tests/test_reports.py::test_all_12_reports_execute_successfully PASSED [ 81%]\n"
        "Railway_Reservation_System/tests/test_reservations.py::test_valid_booking_success PASSED       [ 87%]\n"
        "Railway_Reservation_System/tests/test_reservations.py::test_invalid_origin_dest_sequence_fails PASSED [ 93%]\n"
        "Railway_Reservation_System/tests/test_reservations.py::test_train_runs_isolation PASSED        [100%]\n"
        "============================== 16 passed in 0.41s =============================="
    )
    for p in doc.paragraphs:
        clean_run_page_breaks(p)
        if "[Additional supporting material]" in p.text:
            p.text = app_c_text
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(2)
            p.runs[0].font.name = FONT_CODE
            p.runs[0].font.size = Pt(7.5)

    # -------------------------------------------------------------------------
    # 12. REMOVE ALL REMAINING INSTRUCTIONAL PROMPTS AND BLANK PARAGRAPHS
    # -------------------------------------------------------------------------
    instruction_snippets = [
        "use this common structure for all dbms pbl projects",
        "update this list after finalising the report",
        "retain only the acronyms used in the report",
        "this chapter should represent the evidence",
        "describe the current problem, affected users",
        "state 3-5 measurable objectives",
        "explain how the proposed solution will address",
        "insert the approved er diagram",
        "this chapter should document how the approved",
        "list every relation derived from the er model",
        "include primary key, foreign key, unique",
        "list the important functional dependencies",
        "prepare the data dictionary for all tables",
        "mention the dbms used, provide representative",
        "this chapter should show how the approved",
        "briefly explain the users, application purpose",
        "explain how the application prevents invalid",
        "insert the important application screenshots",
        "summarize the key results after the test-case",
        "summarize the problem addressed, database design",
        "mention genuine limitations of the current",
        "attach the complete ddl/dml/query script",
        "provide the source-code folder/repository",
        "include any additional test data, screenshots",
        "write the abstract as one self-contained paragraph",
        "use ieee reference style throughout the report"
    ]
    
    # Controlled major section breaks:
    # Controlled major section breaks:
    # Notice: REFERENCES is unified with CHAPTER 4 on the same page!
    # Notice: CHAPTER 3 flows right after Section 2.6 on the same page!
    major_breaks = [
        "ACKNOWLEDGEMENT",
        "UNDERTAKING",
        "TABLE OF CONTENTS",
        "ABSTRACT",
        "CHAPTER 1",
        "CHAPTER 2",
        "CHAPTER 4",
        "APPENDICES"
    ]

    p_to_remove = []
    for p in doc.paragraphs:
        txt = p.text.strip().lower()
        has_draw = '<w:drawing' in p._p.xml
        
        is_instruction = any(snippet in txt for snippet in instruction_snippets)
        if is_instruction:
            p_to_remove.append(p)
            continue
            
        if not txt and not has_draw:
            p_to_remove.append(p)
            continue
            
        if p.style and ('Heading' in p.style.name or 'Caption' in p.style.name):
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(1)
        elif any(p.text.strip().startswith(prefix) for prefix in ['Table ', 'Figure ']):
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(1)

    for p in p_to_remove:
        remove_element(p._p)

    for p in doc.paragraphs:
        txt = p.text.strip()
        if txt in major_breaks:
            p.paragraph_format.page_break_before = True
        elif txt == "CHAPTER 3":
            p.paragraph_format.page_break_before = False
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(2)
        elif txt == "REFERENCES":
            p.paragraph_format.page_break_before = False
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(2)

    # -------------------------------------------------------------------------
    # 13. SAVE AND EXPORT
    # -------------------------------------------------------------------------
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    ROOT_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    
    doc.save(str(TARGET_DOCX))
    print(f"Report saved to: {TARGET_DOCX}")

def detect_exact_page_numbers(pdf_path):
    import pypdf
    reader = pypdf.PdfReader(str(pdf_path))
    page_map = {}
    
    for idx, page in enumerate(reader.pages):
        p_num = idx + 1
        lines = [l.strip() for l in page.extract_text().splitlines() if l.strip()]
        
        # Front matter
        if any(l == 'TABLE OF CONTENTS' for l in lines):
            page_map['TABLE OF CONTENTS'] = str(p_num)
        if any('LIST OF TABLES' in l for l in lines) and p_num <= 8:
            page_map['LIST OF TABLES'] = str(p_num)
        if any('LIST OF FIGURES' in l for l in lines) and p_num <= 8:
            page_map['LIST OF FIGURES'] = str(p_num)
        if any('LIST OF ACRONYMS' in l for l in lines) and p_num <= 8:
            page_map['LIST OF ACRONYMS'] = str(p_num)
        if any(l == 'ABSTRACT' for l in lines):
            page_map['Abstract'] = str(p_num)
            
        if p_num < 7:
            continue
            
        # Chapter 1
        if any('CHAPTER 1' in l for l in lines):
            page_map['1. PROBLEM STATEMENT, SOLUTION STRATEGY AND ER DIAGRAM'] = str(p_num)
        if any(l.startswith('1.1 Problem Statement') for l in lines):
            page_map['   1.1 Problem Statement'] = str(p_num)
        if any(l.startswith('1.2 Objectives') for l in lines):
            page_map['   1.2 Objectives'] = str(p_num)
        if any(l.startswith('1.3 Scope and Assumptions') for l in lines):
            page_map['   1.3 Scope and Assumptions'] = str(p_num)
        if any(l.startswith('1.4 Proposed Solution Strategy') for l in lines):
            page_map['   1.4 Proposed Solution Strategy'] = str(p_num)
        if any(l.startswith('1.5 Functional Requirements') for l in lines):
            page_map['   1.5 Functional Requirements'] = str(p_num)
        if any(l.startswith('1.6 Entity-Relationship') for l in lines):
            page_map['   1.6 Entity-Relationship Diagram (ERD)'] = str(p_num)
        if any(l.startswith('1.7 Entity and Relationship') for l in lines):
            page_map['   1.7 Entity and Relationship Summary'] = str(p_num)
            
        # Chapter 2
        if any('CHAPTER 2' in l for l in lines):
            page_map['2. LOGICAL DATABASE DESIGN'] = str(p_num)
        if any(l.startswith('2.1 Relational Schema') for l in lines):
            page_map['   2.1 Relational Schema'] = str(p_num)
        if any(l.startswith('2.2 Keys and Integrity') for l in lines):
            page_map['   2.2 Keys and Integrity Constraints'] = str(p_num)
        if any(l.startswith('2.3 Functional Dependencies') for l in lines):
            page_map['   2.3 Functional Dependencies'] = str(p_num)
        if any(l.startswith('2.4 Normalization') for l in lines):
            page_map['   2.4 Normalization up to Third Normal Form (3NF)'] = str(p_num)
        if any(l.startswith('2.5 Data Dictionary') for l in lines):
            page_map['   2.5 Data Dictionary'] = str(p_num)
        if any(l.startswith('2.6 Implementation of Logical') for l in lines):
            page_map['   2.6 Implementation of Logical Design: DDL and Sample Data'] = str(p_num)
            
        # Chapter 3
        if any('CHAPTER 3' in l for l in lines):
            page_map['3. APPLICATION DEVELOPMENT USING LOGICAL DATABASE DESIGN'] = str(p_num)
        if any(l.startswith('3.1 Application Overview') for l in lines):
            page_map['   3.1 Application Overview'] = str(p_num)
        if any(l.startswith('3.2 Development Environment') for l in lines):
            page_map['   3.2 Development Environment and Database Connectivity'] = str(p_num)
        if any(l.startswith('3.3 Application Modules') for l in lines):
            page_map['   3.3 Application Modules and Database Mapping'] = str(p_num)
        if any('Core Business Logic' in l or '3.4 CRUD' in l or '3.4 Core Business' in l for l in lines):
            page_map['   3.4 CRUD Operations'] = str(p_num)
        if any('Views Specification' in l or '3.5 Business Rules' in l or '3.5 Database Views' in l for l in lines):
            page_map['   3.5 Business Rules, Validation and Error Handling'] = str(p_num)
        if any('Validation and Business' in l or '3.6 Reports' in l or '3.6 Validation' in l for l in lines):
            page_map['   3.6 Reports and Database Operations'] = str(p_num)
        if any(l.startswith('3.7 Application Screens') for l in lines):
            page_map['   3.7 Application Screens'] = str(p_num)
        if any(l.startswith('3.8 Testing and Results') for l in lines):
            page_map['   3.8 Testing and Results'] = str(p_num)
            
        # Chapter 4
        if any('CHAPTER 4' in l for l in lines):
            page_map['4. CONCLUSION'] = str(p_num)
        if any(l.startswith('4.1 Limitations') for l in lines):
            page_map['   4.1 Limitations and Future Enhancements'] = str(p_num)
            
        # Chapter 5 & 6
        if any(l == 'REFERENCES' for l in lines):
            page_map['5. REFERENCES'] = str(p_num)
        if any('APPENDICES' in l for l in lines):
            page_map['6. APPENDICES'] = str(p_num)
        if any('APPENDIX A' in l for l in lines):
            page_map['   Appendix A — Complete Database Script'] = str(p_num)
        if any('APPENDIX B' in l for l in lines):
            page_map['   Appendix B — Application Source Code'] = str(p_num)
        if any('APPENDIX C' in l for l in lines):
            page_map['   Appendix C — Additional Test Data and Outputs'] = str(p_num)
            
        # Tables 1-15
        for t_idx in range(1, 16):
            t_key = f'Table {t_idx}'
            if any(l.startswith(f'Table {t_idx}.') for l in lines) and t_key not in page_map:
                page_map[t_key] = str(p_num)
                
        # Figures 1-7
        for f_idx in range(1, 8):
            f_key = f'Figure {f_idx}'
            if any(l.startswith(f'Figure {f_idx}.') for l in lines) and f_key not in page_map:
                page_map[f_key] = str(p_num)
                
    return page_map

def build_with_exact_page_numbers():
    # Pass 1: Build initial optimized docx
    print("--- PASS 1: Generating initial space-optimized docx ---")
    generate_report()
    
    # Export to PDF via LibreOffice
    print("Converting to PDF for page layout detection...")
    subprocess.run([
        '/opt/homebrew/bin/soffice', '--headless', '--convert-to', 'pdf',
        str(TARGET_DOCX), '--outdir', str(DOCS_DIR)
    ], check=True)
    
    # Pass 2: Extract real page numbers from PDF
    print("--- PASS 2: Detecting exact page numbers from PDF ---")
    page_map = detect_exact_page_numbers(TARGET_PDF)
    print(f"Detected {len(page_map)} structural targets in PDF.")
    
    # Build updated TOC, Tables List, Figures List
    new_toc = []
    for item, fallback_p in TOC_DATA:
        p_detected = page_map.get(item, page_map.get(item.strip(), fallback_p))
        new_toc.append((item, p_detected))
        
    new_tables = []
    for tbl, title, fallback_p in TABLES_LIST:
        p_detected = page_map.get(tbl, fallback_p)
        new_tables.append((tbl, title, p_detected))
        
    new_figures = []
    for fig, title, fallback_p in FIGURES_LIST:
        p_detected = page_map.get(fig, fallback_p)
        new_figures.append((fig, title, p_detected))
        
    # Re-run generate_report with exact page numbers
    print("Re-compiling report with 100% synchronized page numbers...")
    generate_report(
        toc_data_override=new_toc,
        tables_list_override=new_tables,
        figures_list_override=new_figures
    )
    
    # Export final PDF
    print("Generating final synchronized PDF...")
    subprocess.run([
        '/opt/homebrew/bin/soffice', '--headless', '--convert-to', 'pdf',
        str(TARGET_DOCX), '--outdir', str(DOCS_DIR)
    ], check=True)
    
    # Copy deliverables to root and docs/
    shutil.copy(str(TARGET_DOCX), str(ROOT_DOCS_DIR / 'Railway_Ticket_Reservation_DBMS_PBL_Report.docx'))
    shutil.copy(str(TARGET_DOCX), str(ROOT_DIR / 'Railway_Ticket_Reservation_DBMS_PBL_Report.docx'))
    shutil.copy(str(TARGET_PDF), str(ROOT_DOCS_DIR / 'Railway_Ticket_Reservation_DBMS_PBL_Report.pdf'))
    shutil.copy(str(TARGET_PDF), str(ROOT_DIR / 'Railway_Ticket_Reservation_DBMS_PBL_Report.pdf'))
    print("All deliverables copied to docs/ and workspace root.")

if __name__ == '__main__':
    build_with_exact_page_numbers()
