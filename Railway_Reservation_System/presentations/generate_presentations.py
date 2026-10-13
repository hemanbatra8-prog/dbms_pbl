"""
PowerPoint Presentations Generator Script.
Generates three distinct, editable, academically rigorous PowerPoint presentations:
1. Review_1_Requirements_and_ER_Design.pptx (11 slides)
2. Review_2_Normalization_and_SQL_Implementation.pptx (12 slides)
3. Review_3_Final_Implementation_and_Demo.pptx (12 slides)
"""
import os
import sys
from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = Path(__file__).resolve().parent.parent
PRES_DIR = BASE_DIR / 'presentations'
SCREENSHOTS_DIR = BASE_DIR / 'docs' / 'screenshots'
WOXSEN_LOGO_PATH = SCREENSHOTS_DIR / 'woxsen_logo.png'

# Colors
C_NAVY_DARK = RGBColor(10, 27, 46)     # #0A1B2E
C_NAVY_PRIMARY = RGBColor(15, 43, 72)  # #0F2B48
C_NAVY_LIGHT = RGBColor(26, 66, 110)   # #1A426E
C_GOLD = RGBColor(230, 161, 23)        # #E6A117
C_SLATE_BG = RGBColor(248, 250, 252)   # #F8FAFC
C_CARD_BG = RGBColor(255, 255, 255)    # #FFFFFF
C_TEXT_DARK = RGBColor(30, 41, 59)     # #1E293B
C_TEXT_MUTED = RGBColor(100, 116, 139) # #64748B
C_SUCCESS = RGBColor(16, 185, 129)     # #10B981
C_DANGER = RGBColor(239, 68, 68)       # #EF4444
C_BORDER = RGBColor(203, 213, 225)     # #CBD5E1

def create_base_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs

def set_slide_background(slide, color=C_SLATE_BG):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_header(slide, title_text, category_text, review_text="REVIEW 1 (WEEK 7)"):
    # Header container
    header_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.15))
    header_box.fill.solid()
    header_box.fill.fore_color.rgb = C_NAVY_DARK
    header_box.line.color.rgb = C_GOLD
    header_box.line.width = Pt(2.5)

    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.8)
    tf.margin_top = Inches(0.18)

    p_cat = tf.paragraphs[0]
    p_cat.text = f"{category_text.upper()} | {review_text}"
    p_cat.font.name = 'Arial'
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = C_GOLD

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = 'Arial'
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)

def add_footer(slide, review_tag="Review 1"):
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.4))
    tf = footer_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"Railway Ticket Reservation and Journey Management System | {review_tag} | B.Tech CSE DBMS Project"
    p.font.name = 'Arial'
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_TEXT_MUTED

def add_card(slide, left, top, width, height, title=None, border_color=C_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = C_CARD_BG
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)

    if title:
        header_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.55))
        header_card.fill.solid()
        header_card.fill.fore_color.rgb = C_NAVY_PRIMARY
        header_card.line.color.rgb = border_color
        tf = header_card.text_frame
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.12)
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = 'Arial'
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
    return card

def add_speaker_note(slide, note_text):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = note_text

# ==============================================================================
# DELIVERABLE A: REVIEW 1 (WEEK 7) - 11 SLIDES
# ==============================================================================
def generate_review_1():
    prs = create_base_presentation()
    blank_layout = prs.slide_layouts[6]

    # SLIDE 1: Title
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_NAVY_DARK)

    # Decorative accent bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(0.2), Inches(4.2))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_GOLD
    bar.line.fill.background()

    if WOXSEN_LOGO_PATH.exists():
        s1.shapes.add_picture(str(WOXSEN_LOGO_PATH), Inches(9.8), Inches(1.3), width=Inches(2.7))

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.4), Inches(8.5), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "WOXSEN UNIVERSITY | SCHOOL OF TECHNOLOGY | DBMS COURSEWORK"
    p0.font.name = 'Arial'
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = C_GOLD

    p1 = tf.add_paragraph()
    p1.text = "Railway Ticket Reservation and\nJourney Management System"
    p1.font.name = 'Arial'
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)

    p2 = tf.add_paragraph()
    p2.text = "REVIEW 1: Problem Identification, Requirements, and Conceptual ER Design"
    p2.font.name = 'Arial'
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_before = Pt(14)

    p3 = tf.add_paragraph()
    p3.text = "Student Name: Heman  |  Roll Number: 25WU0102097  |  Section: AIML Rhinos\nFaculty Mentor: Prof. Sahithi  |  School of Technology, Woxsen University  |  Review 1"
    p3.font.name = 'Arial'
    p3.font.size = Pt(12)
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.space_before = Pt(28)

    add_speaker_note(s1, "Welcome to Review 1 for the Railway Ticket Reservation and Journey Management System. Today we present our problem formulation, stakeholder analysis, core business rules, and conceptual ER modeling.")

    # SLIDE 2: Problem Identification
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Identification in Railway Journey Management", "Project Motivation", "REVIEW 1")
    add_footer(s2, "Review 1")

    # Left Card: The Real Technical Challenge
    add_card(s2, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Core Technical Challenges in Multi-Hop Inventory")
    tb2_left = s2.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(5.2), Inches(4.5))
    tf2_l = tb2_left.text_frame
    tf2_l.word_wrap = True
    points_2l = [
        ("Monolithic vs Interval Seat Allocation", "Airline seats are occupied for the entire flight. In rail transport, a train visits 10+ stations. A seat can be booked from A-B, vacated, and immediately re-booked from B-D by another passenger."),
        ("Overlapping Segment Conflicts", "If Passenger 1 holds A-C, Passenger 2 cannot book B-D on the same seat because segment [B, C) is contested. Naive databases cause either catastrophic double-booking or severe capacity waste."),
        ("Coupling Definition vs Dated Runs", "Storing train definitions with travel dates causes severe redundancy and update anomalies."),
        ("Auditability & Financial Integrity", "Cancellations, refunds, and queue promotions require transactional consistency across multiple tables.")
    ]
    for title, desc in points_2l:
        p_t = tf2_l.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.bold = True
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = C_NAVY_PRIMARY
        p_d = tf2_l.add_paragraph()
        p_d.text = f"  {desc}"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_TEXT_DARK
        p_d.space_after = Pt(8)

    # Right Card: The Solution Approach
    add_card(s2, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Relational Database Solution Approach")
    tb2_right = s2.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.3), Inches(4.5))
    tf2_r = tb2_right.text_frame
    tf2_r.word_wrap = True
    points_2r = [
        ("Segment-Wise Relational Modeling", "Model seats over half-open intervals [origin_seq, dest_seq) in a dedicated journey_segments table."),
        ("Mathematical Overlap Formula", "Enforce s < r_end AND r_start < e across active allocations."),
        ("ACID Transaction Isolation", "Use row-level locking (SELECT ... FOR UPDATE) to serialize competing requests on candidate seats."),
        ("Third Normal Form (3NF) Schema", "Separate stations, routes, trains, dated runs, coaches, seats, passengers, bookings, and payments into 14 distinct relations.")
    ]
    for title, desc in points_2r:
        p_t = tf2_r.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.bold = True
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = C_NAVY_PRIMARY
        p_d = tf2_r.add_paragraph()
        p_d.text = f"  {desc}"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_TEXT_DARK
        p_d.space_after = Pt(8)

    add_speaker_note(s2, "Slide 2 clarifies the core technical problem: unlike simple airline ticketing, rail seats represent ordered intervals. Our relational design allows safe reuse on non-overlapping segments while preventing conflicts.")

    # SLIDE 3: Objectives & Scope
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Project Objectives & Scope Definition", "Scope & Boundary", "REVIEW 1")
    add_footer(s3, "Review 1")

    # 3 Column Cards
    col_w = Inches(3.7)
    add_card(s3, Inches(0.8), Inches(1.4), col_w, Inches(5.4), "1. Relational Database Design")
    tb_c1 = s3.shapes.add_textbox(Inches(0.9), Inches(2.1), col_w - Inches(0.2), Inches(4.5))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    c1_items = [
        "Develop an enterprise schema with 14 normalized relations in 3NF.",
        "Implement primary keys, foreign keys with ON DELETE rules, and domain CHECK constraints.",
        "Ensure entity decoupling: stations, ordered stops, locomotive definitions, and calendar runs.",
        "Use exact monetary DECIMAL(10,2) types to eliminate floating-point rounding errors."
    ]
    for it in c1_items:
        p = tf_c1.add_paragraph()
        p.text = f"✔ {it}"
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(12)

    add_card(s3, Inches(4.8), Inches(1.4), col_w, Inches(5.4), "2. Business Logic & Integrity")
    tb_c2 = s3.shapes.add_textbox(Inches(4.9), Inches(2.1), col_w - Inches(0.2), Inches(4.5))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    c2_items = [
        "Implement half-open interval seat allocation [origin_seq, dest_seq).",
        "Guarantee transaction safety via pessimistic row locking (FOR UPDATE).",
        "Deterministic fare calculation using distance rates and travel class multipliers.",
        "Automated FIFO waitlist queue allocation and promotion upon cancellation."
    ]
    for it in c2_items:
        p = tf_c2.add_paragraph()
        p.text = f"✔ {it}"
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(12)

    add_card(s3, Inches(8.8), Inches(1.4), col_w, Inches(5.4), "3. Project Scope Boundaries")
    tb_c3 = s3.shapes.add_textbox(Inches(8.9), Inches(2.1), col_w - Inches(0.2), Inches(4.5))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    c3_in = ["Full relational schema in MySQL 8.x / SQLite", "Interactive web UI with train search & booking", "12 Advanced SQL reports and analytical queries", "Automated pytest suite covering all integrity rules"]
    c3_out = ["Live external Indian Railway API integration", "Real banking payment gateway (UPI is simulated)", "Hardware ticketing kiosk devices"]
    p_in_hdr = tf_c3.add_paragraph()
    p_in_hdr.text = "INCLUDED IN PROTOTYPE:"
    p_in_hdr.font.bold = True
    p_in_hdr.font.size = Pt(11)
    p_in_hdr.font.color.rgb = C_SUCCESS
    for it in c3_in:
        p = tf_c3.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(10)
        p.space_after = Pt(4)
    p_out_hdr = tf_c3.add_paragraph()
    p_out_hdr.text = "EXCLUDED FROM SCOPE:"
    p_out_hdr.font.bold = True
    p_out_hdr.font.size = Pt(11)
    p_out_hdr.font.color.rgb = C_DANGER
    p_out_hdr.space_before = Pt(8)
    for it in c3_out:
        p = tf_c3.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(10)
        p.space_after = Pt(4)

    add_speaker_note(s3, "Slide 3 defines the project objectives across schema design, transaction logic, and reports, while clearly separating the academic prototype scope from external banking or live GPS integrations.")

    # SLIDE 4: Stakeholders and User Roles
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Stakeholders and System User Roles", "User Modeling", "REVIEW 1")
    add_footer(s4, "Review 1")

    roles = [
        ("Passenger / Traveler", "End-Users", [
            "Search trains between any two stations on selected dates.",
            "Check live seat availability by travel class (CC, 1A, 2A, 3A, SL).",
            "Book tickets with berth preferences and receive 10-digit PNR.",
            "Check PNR status, view ERS slip, and check waitlist position.",
            "Cancel confirmed or waitlisted bookings and claim refund."
        ], Inches(0.8)),
        ("Reservation Operator", "Ticket Counter Staff", [
            "Issue counter tickets on behalf of walk-in passengers.",
            "Lookup passenger profiles and manage ticket cancellations.",
            "Monitor live coach occupancy rates prior to chart preparation.",
            "Verify passenger identification credentials (Aadhaar, Passport)."
        ], Inches(4.8)),
        ("Database Administrator", "System & Schema Admins", [
            "Manage station nodes, train catalog definitions, and route stops.",
            "Configure operational train runs and assign coach compositions.",
            "Maintain tariff rules (base fare, rate/km, reservation fees).",
            "Execute database audits, integrity checks, and SQL reports."
        ], Inches(8.8))
    ]
    for r_title, r_sub, perms, l_pos in roles:
        add_card(s4, l_pos, Inches(1.4), Inches(3.7), Inches(5.4), r_title)
        tb_r = s4.shapes.add_textbox(l_pos + Inches(0.1), Inches(2.1), Inches(3.5), Inches(4.5))
        tf_r = tb_r.text_frame
        tf_r.word_wrap = True
        p_sub = tf_r.paragraphs[0]
        p_sub.text = f"Role Type: {r_sub}"
        p_sub.font.bold = True
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = C_NAVY_LIGHT
        p_sub.space_after = Pt(10)
        for prm in perms:
            p = tf_r.add_paragraph()
            p.text = f"✔ {prm}"
            p.font.size = Pt(10)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(8)

    add_speaker_note(s4, "Slide 4 specifies the stakeholder roles: Passengers who execute bookings and cancellations, Reservation Operators who inspect charts, and Database Administrators who manage trains, routes, and fare policies.")

    # SLIDE 5: Functional & Non-Functional Requirements
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "System Requirements Specification", "Requirements Engineering", "REVIEW 1")
    add_footer(s5, "Review 1")

    add_card(s5, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Functional Requirements (FR)")
    tb_fr = s5.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(5.2), Inches(4.5))
    tf_fr = tb_fr.text_frame
    tf_fr.word_wrap = True
    fr_list = [
        ("FR-01 Train Discovery", "Search trains between origin and destination on a travel date; enforce origin stop sequence < destination stop sequence."),
        ("FR-02 Segment Availability", "Compute real-time free seats per travel class using the interval non-overlap condition."),
        ("FR-03 Ticket Reservation", "Atomic booking generation with unique 10-digit PNR, berth assignment, and payment record."),
        ("FR-04 Waitlist Management", "Automatic placement into a sequenced queue when segment capacity is exhausted."),
        ("FR-05 Cancellation & Refund", "Process voluntary cancellations, apply policy deductions (20%), and execute waitlist promotion."),
        ("FR-06 SQL Reporting", "Execute 12 analytical queries including occupancy, revenue reconciliation, and route demand.")
    ]
    for tag, desc in fr_list:
        p = tf_fr.add_paragraph()
        p.text = f"• {tag}: {desc}"
        p.font.size = Pt(10.5)
        p.space_after = Pt(6)

    add_card(s5, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Non-Functional Requirements (NFR)")
    tb_nfr = s5.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.3), Inches(4.5))
    tf_nfr = tb_nfr.text_frame
    tf_nfr.word_wrap = True
    nfr_list = [
        ("NFR-01 Data Integrity (ACID)", "All updates wrapped in transactions; rollback on any failure; declarative foreign keys and CHECK constraints."),
        ("NFR-02 Concurrency Safety", "Serialize concurrent bookings using InnoDB row-level locking (SELECT ... FOR UPDATE) to eliminate race conditions."),
        ("NFR-03 Financial Precision", "Store monetary amounts strictly as DECIMAL(10,2) to eliminate floating-point rounding errors."),
        ("NFR-04 Performance & Indexing", "B-Tree indexes on PNR, station codes, train numbers, and segment allocation intervals for sub-second responses."),
        ("NFR-05 Usability & Responsiveness", "Intuitive browser interface formatted like an official IRCTC electronic reservation slip.")
    ]
    for tag, desc in nfr_list:
        p = tf_nfr.add_paragraph()
        p.text = f"• {tag}: {desc}"
        p.font.size = Pt(10.5)
        p.space_after = Pt(8)

    add_speaker_note(s5, "Slide 5 establishes formal functional and non-functional requirements, emphasizing ACID transaction safety, exact financial precision using DECIMAL, and responsive indexing.")

    # SLIDE 6: Core Business Rules
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Core Business Rules & Invariants", "Domain Logic & Constraints", "REVIEW 1")
    add_footer(s6, "Review 1")

    add_card(s6, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Formal Business Invariants Enforced by Database & Application")
    tb_br = s6.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.6))
    tf_br = tb_br.text_frame
    tf_br.word_wrap = True

    b_rules = [
        ("BR-1: Train Catalog vs Run Decoupling", "A train represents master route metadata; a train run represents an operational departure on a specific date. Bookings on different dates for the same train number must never conflict."),
        ("BR-2: Route Progression Invariant", "Stations must be sequenced with positive integers (1, 2, 3...). A valid journey requires origin_stop_seq < destination_stop_seq."),
        ("BR-3: Segment Interval Exclusion", "A confirmed reservation allocates a seat over half-open interval [s, e). Two allocations on the same seat overlap iff existing.start < req.end AND req.start < existing.end. Overlapping requests must be rejected."),
        ("BR-4: Non-Overlapping Seat Reuse", "Two distinct passengers may hold the exact same physical seat on the same train run provided their journey intervals are disjoint (e.g., Passenger A on [1, 2) and Passenger B on [2, 4))."),
        ("BR-5: Waitlist Serialization", "Waitlist entries are scoped by (run_id, travel_class) and assigned sequential queue positions (1, 2, 3...) using atomic transactions."),
        ("BR-6: Deterministic Cancellation Policy", "Voluntary cancellation of a confirmed ticket retains 20% cancellation fee and disburses 80% refund. Waitlisted tickets deduct a flat ₹30 clerkage fee."),
        ("BR-7: Atomic Waitlist Promotion", "Cancelling a confirmed seat immediately checks the waitlist queue in FIFO order, promoting the first candidate whose requested interval is satisfied, updating both records in one transaction.")
    ]
    for tag, desc in b_rules:
        p = tf_br.add_paragraph()
        p.text = f"{tag}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_NAVY_PRIMARY
        r = p.add_run()
        r.text = desc
        r.font.bold = False
        r.font.size = Pt(10.5)
        r.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(7)

    add_speaker_note(s6, "Slide 6 defines the testable business rules. Pay special attention to BR-3 and BR-4: the interval overlap rule guarantees that non-overlapping passengers can reuse the same seat while conflicting requests are rejected.")

    # SLIDE 7: Conceptual ER Diagram
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Conceptual Entity-Relationship (ER) Diagram", "Database Design", "REVIEW 1")
    add_footer(s7, "Review 1")

    # Large container for ER Diagram representation
    add_card(s7, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "ER Model Architecture: Entities, Cardinalities & Junctions")
    
    # Diagram layout using boxes
    er_nodes = [
        ("STATION", Inches(1.2), Inches(2.2), Inches(2.2), Inches(1.1), "PK: station_id\nstation_code (UQ)\nstation_name, city"),
        ("ROUTE", Inches(4.2), Inches(2.2), Inches(2.2), Inches(1.1), "PK: route_id\nroute_code (UQ)\nsrc_stn, dst_stn"),
        ("TRAIN", Inches(7.2), Inches(2.2), Inches(2.2), Inches(1.1), "PK: train_id\ntrain_number (UQ)\ntrain_name, route_id"),
        ("TRAIN_RUN", Inches(10.1), Inches(2.2), Inches(2.2), Inches(1.1), "PK: run_id\ntrain_id (FK)\nrun_date (UQ), status"),
        
        ("TRAIN_STOP", Inches(2.7), Inches(3.9), Inches(2.2), Inches(1.1), "PK: stop_id\nroute_id, station_id\nstop_sequence (UQ)"),
        ("COACH", Inches(5.7), Inches(3.9), Inches(2.2), Inches(1.1), "PK: coach_id\ntrain_id, coach_code\ntravel_class, seats"),
        ("SEAT", Inches(8.7), Inches(3.9), Inches(2.2), Inches(1.1), "PK: seat_id\ncoach_id (FK)\nseat_number, berth"),

        ("PASSENGER", Inches(1.2), Inches(5.3), Inches(2.2), Inches(1.1), "PK: passenger_id\nfull_name, age, gender\nemail, id_card"),
        ("BOOKING", Inches(4.2), Inches(5.3), Inches(2.4), Inches(1.1), "PK: booking_id\npnr_number (UQ)\nrun_id, passenger_id\norig_stn, dest_stn, fare"),
        ("JOURNEY_SEGMENT", Inches(7.2), Inches(5.3), Inches(2.4), Inches(1.1), "PK: segment_id\nbooking_id, seat_id, run_id\n[start_seq, end_seq)"),
        ("WAITLIST", Inches(10.1), Inches(5.3), Inches(2.2), Inches(1.1), "PK: waitlist_id\nbooking_id, run_id\nclass, position, status")
    ]
    for name, left, top, w, h, details in er_nodes:
        node_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
        node_box.fill.solid()
        node_box.fill.fore_color.rgb = C_SLATE_BG
        node_box.line.color.rgb = C_NAVY_PRIMARY
        node_box.line.width = Pt(1.5)
        tf_n = node_box.text_frame
        tf_n.word_wrap = True
        tf_n.margin_left = Inches(0.1)
        tf_n.margin_top = Inches(0.08)
        p_name = tf_n.paragraphs[0]
        p_name.text = name
        p_name.font.name = 'Arial'
        p_name.font.size = Pt(11)
        p_name.font.bold = True
        p_name.font.color.rgb = C_NAVY_PRIMARY
        p_det = tf_n.add_paragraph()
        p_det.text = details
        p_det.font.name = 'Arial'
        p_det.font.size = Pt(8.5)
        p_det.font.color.rgb = C_TEXT_DARK

    add_speaker_note(s7, "Slide 7 shows the conceptual ER diagram. Notice how Route and Station connect via Train_Stop to represent ordered intermediate halts, while Booking and Seat connect via Journey_Segment to represent segment-wise inventory allocations.")

    # SLIDE 8: Entity and Relationship Inventory
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Entity Responsibilities and Cardinalities", "Data Dictionary & Relationships", "REVIEW 1")
    add_footer(s8, "Review 1")

    add_card(s8, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Entity Inventory and Cardinality Matrix")
    
    # Table of Entities
    table_shape = s8.shapes.add_table(8, 5, Inches(1.0), Inches(2.1), Inches(11.333), Inches(4.3))
    t = table_shape.table
    t.columns[0].width = Inches(1.8)
    t.columns[1].width = Inches(1.4)
    t.columns[2].width = Inches(3.2)
    t.columns[3].width = Inches(2.2)
    t.columns[4].width = Inches(2.7)

    headers = ["Entity Name", "Type", "Primary Key & Unique Attributes", "Cardinality", "Core Responsibility"]
    for i, h in enumerate(headers):
        cell = t.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = 'Arial'
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    matrix_rows = [
        ("Station", "Master", "PK: station_id | UQ: station_code", "1 : N with Train_Stop", "Physical geographic railway passenger nodes"),
        ("Route", "Master", "PK: route_id | UQ: route_code", "1 : N with Train, Train_Stop", "Track corridors linking source and destination"),
        ("Train", "Master", "PK: train_id | UQ: train_number", "1 : N with Train_Run, Coach", "Static train catalogs (Vande Bharat, Rajdhani)"),
        ("Train_Run", "Operational", "PK: run_id | UQ: (train_id, run_date)", "1 : N with Booking, Segment", "Dated calendar train departures (3NF Decoupling)"),
        ("Coach & Seat", "Inventory", "PK: coach_id, seat_id | UQ: seat_num", "1 : N Coach to Seat", "Rolling stock physical seating units & berth types"),
        ("Passenger", "Profile", "PK: passenger_id | UQ: email", "1 : N with Booking", "Registered traveler identity and contact records"),
        ("Journey_Segment", "Allocation", "PK: segment_id", "M : 1 with Booking, Seat, Run", "Interval seat allocation [start_seq, end_seq)")
    ]
    for row_idx, r_data in enumerate(matrix_rows):
        for col_idx, text in enumerate(r_data):
            cell = t.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD_BG if row_idx % 2 == 0 else C_SLATE_BG
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.name = 'Arial'
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_TEXT_DARK

    add_speaker_note(s8, "Slide 8 details the entity inventory and cardinalities. Every entity has a strictly defined domain responsibility, eliminating multivalued anomalies.")

    # SLIDE 9: Initial Relational Schema
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Initial Relational Schema Notation", "Logical Schema Design", "REVIEW 1")
    add_footer(s9, "Review 1")

    add_card(s9, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Formally Specified Relational Schema (14 Relations)")
    tb_sch = s9.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.6))
    tf_sch = tb_sch.text_frame
    tf_sch.word_wrap = True

    schemas_text = [
        "1. STATIONS (station_id PK, station_code UNIQUE, station_name, city, state)",
        "2. ROUTES (route_id PK, route_code UNIQUE, source_station_id FK, destination_station_id FK, total_distance_km)",
        "3. TRAIN_STOPS (stop_id PK, route_id FK, station_id FK, stop_sequence, distance_from_source_km, arrival_time, departure_time)",
        "4. TRAINS (train_id PK, train_number UNIQUE, train_name, train_type, route_id FK)",
        "5. TRAIN_RUNS (run_id PK, train_id FK, run_date, status) [UNIQUE: train_id, run_date]",
        "6. COACHES (coach_id PK, train_id FK, coach_code, travel_class, total_seats) [UNIQUE: train_id, coach_code]",
        "7. SEATS (seat_id PK, coach_id FK, seat_number, berth_type) [UNIQUE: coach_id, seat_number]",
        "8. PASSENGERS (passenger_id PK, full_name, gender, age, email, phone, id_card_type, id_card_number)",
        "9. FARE_RULES (fare_id PK, train_type, travel_class, base_fare, rate_per_km, reservation_fee) [UNIQUE: train_type, travel_class]",
        "10. BOOKINGS (booking_id PK, pnr_number UNIQUE, run_id FK, passenger_id FK, origin_station_id FK, destination_station_id FK, origin_stop_seq, destination_stop_seq, travel_class, booking_status, total_fare, booked_at)",
        "11. JOURNEY_SEGMENTS (segment_id PK, booking_id FK, seat_id FK, run_id FK, start_stop_seq, end_stop_seq, allocation_status)",
        "12. WAITLISTS (waitlist_id PK, booking_id FK, run_id FK, travel_class, origin_stop_seq, destination_stop_seq, position, waitlist_status, created_at)",
        "13. PAYMENTS (payment_id PK, booking_id FK, amount, payment_method, transaction_reference UNIQUE, payment_status, paid_at)",
        "14. CANCELLATIONS (cancellation_id PK, booking_id FK UNIQUE, cancellation_reason, cancellation_fee, refund_amount, refund_status, cancelled_at)"
    ]
    for sch in schemas_text:
        p = tf_sch.add_paragraph()
        p.text = sch
        p.font.name = 'Consolas' if 'Consolas' in [f.name for f in prs.slide_layouts[0].shapes] else 'Courier New'
        p.font.size = Pt(9.5)
        p.font.bold = True if ('BOOKINGS' in sch or 'JOURNEY_SEGMENTS' in sch) else False
        p.font.color.rgb = C_NAVY_PRIMARY
        p.space_after = Pt(4)

    add_speaker_note(s9, "Slide 9 presents the formal relational schema notation covering all 14 entities. Primary keys, foreign keys, and unique constraints are explicitly mapped.")

    # SLIDE 10: Proposed Architecture
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Proposed Full-Stack System Architecture", "System Architecture", "REVIEW 1")
    add_footer(s10, "Review 1")

    add_card(s10, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Multi-Tier Relational Application Data Flow")
    
    tiers = [
        ("Presentation Layer", "HTML5, CSS3, Bootstrap 5\nJinja2 Server Templates\nResponsive Ticket UI", Inches(1.2)),
        ("Application Layer", "Python 3 & Flask Framework\nBlueprint Route Handlers\nServer-side Validation", Inches(4.1)),
        ("Business Service Layer", "Availability Service [s, e)\nTransaction Booking Engine\nWaitlist Promotion & Refunds", Inches(7.0)),
        ("Persistence Layer", "MySQL 8.x InnoDB RDBMS\nSQLAlchemy ORM + Raw SQL\nACID Locks & 12 Views", Inches(9.9))
    ]
    for t_name, t_desc, l_pos in tiers:
        t_box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l_pos, Inches(2.2), Inches(2.4), Inches(3.8))
        t_box.fill.solid()
        t_box.fill.fore_color.rgb = C_CARD_BG
        t_box.line.color.rgb = C_NAVY_PRIMARY
        t_box.line.width = Pt(2)
        tf_tb = t_box.text_frame
        tf_tb.word_wrap = True
        tf_tb.margin_left = Inches(0.15)
        tf_tb.margin_top = Inches(0.2)
        p_thdr = tf_tb.paragraphs[0]
        p_thdr.text = t_name
        p_thdr.font.name = 'Arial'
        p_thdr.font.size = Pt(13)
        p_thdr.font.bold = True
        p_thdr.font.color.rgb = C_NAVY_PRIMARY
        p_thdr.space_after = Pt(12)
        p_tdet = tf_tb.add_paragraph()
        p_tdet.text = t_desc
        p_tdet.font.name = 'Arial'
        p_tdet.font.size = Pt(10.5)
        p_tdet.font.color.rgb = C_TEXT_DARK

    add_speaker_note(s10, "Slide 10 illustrates our 4-tier system architecture from browser UI to Flask controller, business services, and MySQL InnoDB persistence.")

    # SLIDE 11: Development Plan
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Implementation & Review Roadmap", "Project Planning", "REVIEW 1")
    add_footer(s11, "Review 1")

    add_card(s11, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Three-Stage Milestone Plan (Week 7 to Week 16)")
    tb_pl = s11.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.5))
    tf_pl = tb_pl.text_frame
    tf_pl.word_wrap = True

    milestones = [
        ("Review 1 (Week 7) - Conceptual Design & Requirements [COMPLETED]", "Finalize business rules, stakeholder requirements, ER modeling, entity inventory, and initial relational schema mapping."),
        ("Review 2 (Week 11) - Normalization, DDL & SQL Implementation [NEXT STAGE]", "Derive functional dependencies, prove 3NF normalization, deploy MySQL 8.x schema DDL with InnoDB constraints, seed benchmark records, and execute 12 analytical SQL queries."),
        ("Review 3 (Week 16) - Final Implementation, Testing & Live Demo [FINAL STAGE]", "Connect Flask web frontend with live database, verify segment-wise allocation and automated waitlist promotion, execute 16 automated pytest suites, and deliver final project reports.")
    ]
    for tag, desc in milestones:
        p_m = tf_pl.add_paragraph()
        p_m.text = f"🎯 {tag}"
        p_m.font.name = 'Arial'
        p_m.font.size = Pt(13)
        p_m.font.bold = True
        p_m.font.color.rgb = C_NAVY_PRIMARY
        p_d = tf_pl.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.name = 'Arial'
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = C_TEXT_DARK
        p_d.space_after = Pt(16)

    add_speaker_note(s11, "Slide 11 outlines our 3-stage academic milestone plan leading up to the final working prototype demonstration.")

    prs.save(str(PRES_DIR / 'Review_1_Requirements_and_ER_Design.pptx'))
    print("Review 1 PPTX generated successfully.")

# ==============================================================================
# DELIVERABLE B: REVIEW 2 (WEEK 11) - 12 SLIDES
# ==============================================================================
def generate_review_2():
    prs = create_base_presentation()
    blank_layout = prs.slide_layouts[6]

    # Slide 1: Title
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_NAVY_DARK)
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(0.2), Inches(4.2))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_GOLD
    bar.line.fill.background()

    if WOXSEN_LOGO_PATH.exists():
        s1.shapes.add_picture(str(WOXSEN_LOGO_PATH), Inches(9.8), Inches(1.3), width=Inches(2.7))

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.4), Inches(8.5), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = "WOXSEN UNIVERSITY | SCHOOL OF TECHNOLOGY | DBMS COURSEWORK"
    p0.font.bold = True
    p0.font.size = Pt(13)
    p0.font.color.rgb = C_GOLD
    p1 = tf.add_paragraph()
    p1.text = "Railway Ticket Reservation and\nJourney Management System"
    p1.font.bold = True
    p1.font.size = Pt(32)
    p1.font.color.rgb = RGBColor(255, 255, 255)
    p2 = tf.add_paragraph()
    p2.text = "REVIEW 2: Normalization, DDL Constraints, and SQL Query Implementation"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_before = Pt(14)
    p3 = tf.add_paragraph()
    p3.text = "Student Name: Heman  |  Roll Number: 25WU0102097  |  Section: AIML Rhinos\nFaculty Mentor: Prof. Sahithi  |  School of Technology, Woxsen University  |  Week 11"
    p3.font.size = Pt(12)
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.space_before = Pt(28)
    add_speaker_note(s1, "Welcome to Review 2. We present our 3NF normalization proofs, functional dependency analysis, MySQL DDL schema, and executed SQL query reports.")

    # Slide 2: Final Relational Schema
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Refined and Implemented Relational Schema", "Database Architecture", "REVIEW 2")
    add_footer(s2, "Review 2")
    add_card(s2, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "14 Production-Ready Relational Tables")
    tb2 = s2.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tables_summary = [
        ("stations", "PK: station_id | UNIQUE: station_code", "Physical railway stations"),
        ("routes", "PK: route_id | UNIQUE: route_code | FK: source_stn, dest_stn", "Track corridors and total distance"),
        ("train_stops", "PK: stop_id | FK: route_id, station_id | UNIQUE: (route_id, stop_seq)", "Ordered station stops and arrival/departure times"),
        ("trains", "PK: train_id | UNIQUE: train_number | FK: route_id", "Locomotive catalog (Vande Bharat, Rajdhani)"),
        ("train_runs", "PK: run_id | FK: train_id | UNIQUE: (train_id, run_date)", "Operational calendar dates decoupled from trains"),
        ("coaches & seats", "PK: coach_id, seat_id | UNIQUE: (coach_id, seat_number)", "Physical carriages and seat berth units"),
        ("passengers", "PK: passenger_id | UNIQUE: email | CHECK: age BETWEEN 1 AND 119", "Decoupled traveler identity records"),
        ("bookings", "PK: booking_id | UNIQUE: pnr_number | FK: run_id, passenger_id", "Transactional booking records with fare and status"),
        ("journey_segments", "PK: segment_id | FK: booking_id, seat_id, run_id", "Half-open seat intervals [start_seq, end_seq)"),
        ("waitlists", "PK: waitlist_id | FK: booking_id, run_id", "FIFO queue positions for exhausted segments"),
        ("payments & cancels", "PK: payment_id, cancellation_id | UNIQUE: txn_ref, booking_id", "Audited payment and refund ledgers")
    ]
    for tbl, keys, desc in tables_summary:
        p = tf2.add_paragraph()
        p.text = f"• {tbl.upper()}: "
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_NAVY_PRIMARY
        r = p.add_run()
        r.text = f"{keys} — {desc}"
        r.font.bold = False
        r.font.size = Pt(10)
        p.space_after = Pt(4)
    add_speaker_note(s2, "Slide 2 recaps the implemented schema. Primary, foreign, and unique constraints are fully defined across all 14 tables.")

    # Slide 3: Functional Dependencies
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Formal Functional Dependency (FD) Analysis", "Relational Theory", "REVIEW 2")
    add_footer(s3, "Review 2")
    add_card(s3, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Minimal Candidate Keys and Functional Dependencies")
    tb3 = s3.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.6))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    fds = [
        ("stations: CK = {station_id}, {station_code}", "station_id -> {station_code, station_name, city, state}\nstation_code -> {station_id, station_name, city, state}"),
        ("trains: CK = {train_id}, {train_number}", "train_id -> {train_number, train_name, train_type, route_id}\ntrain_number -> {train_id, train_name, train_type, route_id}"),
        ("train_runs: CK = {run_id}, {train_id, run_date}", "run_id -> {train_id, run_date, status}\n{train_id, run_date} -> {run_id, status}"),
        ("train_stops: CK = {stop_id}, {route_id, stop_seq}", "stop_id -> {route_id, station_id, stop_seq, distance, arrival, dep}\n{route_id, stop_seq} -> {stop_id, station_id, distance, arrival, dep}"),
        ("passengers: CK = {passenger_id}, {email}", "passenger_id -> {full_name, gender, age, email, phone, id_card_type, id_card_num}"),
        ("bookings: CK = {booking_id}, {pnr_number}", "pnr_number -> {booking_id, run_id, passenger_id, orig_stn, dest_stn, status, fare}")
    ]
    for ck, fd_txt in fds:
        p = tf3.add_paragraph()
        p.text = f"✔ {ck}:"
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_NAVY_PRIMARY
        p_d = tf3.add_paragraph()
        p_d.text = f"   {fd_txt}"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = C_TEXT_DARK
        p_d.space_after = Pt(6)
    add_speaker_note(s3, "Slide 3 presents the formal functional dependencies. Every non-key attribute is determined by candidate keys.")

    # Slide 4: Normalization (1NF, 2NF, 3NF)
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Step-by-Step Normalization to Third Normal Form", "Normalization Proof", "REVIEW 2")
    add_footer(s4, "Review 2")

    col_w = Inches(3.7)
    add_card(s4, Inches(0.8), Inches(1.4), col_w, Inches(5.4), "1NF: Atomic Attributes")
    tb4_1 = s4.shapes.add_textbox(Inches(0.9), Inches(2.1), col_w - Inches(0.2), Inches(4.5))
    tf4_1 = tb4_1.text_frame
    tf4_1.word_wrap = True
    p = tf4_1.paragraphs[0]
    p.text = "Problem in UNF:\nSpreadsheet contains repeating groups and multivalued stop lists (e.g. 'NDLS, CNB, PRYJ').\n\nDecomposition:\n• Decompose stops into discrete tuples: train_stops(stop_id, route_id, station_id, stop_sequence).\n• Remove multivalued passenger lists.\n• Every cell contains strictly atomic scalar values."
    p.font.size = Pt(10.5)

    add_card(s4, Inches(4.8), Inches(1.4), col_w, Inches(5.4), "2NF: No Partial Dependencies")
    tb4_2 = s4.shapes.add_textbox(Inches(4.9), Inches(2.1), col_w - Inches(0.2), Inches(4.5))
    tf4_2 = tb4_2.text_frame
    tf4_2.word_wrap = True
    p = tf4_2.paragraphs[0]
    p.text = "Problem in 1NF:\nIn composite key {train_id, run_date}, train_name depends solely on train_id, violating 2NF.\n\nDecomposition:\n• Isolate trains(train_id, train_name, train_type) from dated train_runs(run_id, train_id, run_date).\n• Isolate coaches and seats.\n• Isolate passenger profile attributes from bookings."
    p.font.size = Pt(10.5)

    add_card(s4, Inches(8.8), Inches(1.4), col_w, Inches(5.4), "3NF: No Transitive Dependencies")
    tb4_3 = s4.shapes.add_textbox(Inches(8.9), Inches(2.1), col_w - Inches(0.2), Inches(4.5))
    tf4_3 = tb4_3.text_frame
    tf4_3.word_wrap = True
    p = tf4_3.paragraphs[0]
    p.text = "Problem in 2NF:\nIn bookings, booking_id -> cancellation_id -> {refund_amt, fee}. Non-prime attributes depend transitively on cancellation_id.\n\nDecomposition:\n• Extract cancellations into dedicated table.\n• Extract payments into dedicated table.\n• Extract fare_rules into separate pricing catalog."
    p.font.size = Pt(10.5)

    add_speaker_note(s4, "Slide 4 proves the normalization progression from UNF to 1NF (atomicity), 2NF (eliminating partial dependencies), and 3NF (eliminating transitive dependencies).")

    # Slide 5: Data Dictionary Summary
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Relational Data Dictionary Summary", "Schema Specifications", "REVIEW 2")
    add_footer(s5, "Review 2")
    add_card(s5, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Core Entity Column Constraints & Types")
    t_shape5 = s5.shapes.add_table(8, 6, Inches(1.0), Inches(2.1), Inches(11.333), Inches(4.3))
    t5 = t_shape5.table
    t5.columns[0].width = Inches(1.8)
    t5.columns[1].width = Inches(1.8)
    t5.columns[2].width = Inches(1.4)
    t5.columns[3].width = Inches(1.0)
    t5.columns[4].width = Inches(2.5)
    t5.columns[5].width = Inches(2.8)
    h5 = ["Table", "Column", "Type", "Null?", "Key / Constraints", "Description"]
    for i, h in enumerate(h5):
        cell = t5.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(255, 255, 255)
    d5_rows = [
        ("stations", "station_code", "VARCHAR(10)", "No", "UNIQUE, INDEX", "IRCTC station identifier (e.g. NDLS)"),
        ("train_stops", "stop_sequence", "INT", "No", "CHECK (> 0), UQ(route, seq)", "Ordered sequence position"),
        ("train_runs", "run_date", "DATE", "No", "UQ(train_id, run_date)", "Scheduled operational date"),
        ("passengers", "age", "INT", "No", "CHECK (age > 0 AND age < 120)", "Passenger legal age"),
        ("bookings", "total_fare", "DECIMAL(10,2)", "No", "CHECK (total_fare >= 0)", "Exact ticket purchase price"),
        ("journey_segments", "allocation_status", "VARCHAR(20)", "No", "DEFAULT 'ACTIVE', INDEX", "'ACTIVE' or 'CANCELLED'"),
        ("cancellations", "refund_amount", "DECIMAL(10,2)", "No", "CHECK (refund_amount >= 0)", "Refund processed to passenger")
    ]
    for r_idx, r_data in enumerate(d5_rows):
        for c_idx, val in enumerate(r_data):
            cell = t5.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD_BG if r_idx % 2 == 0 else C_SLATE_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_TEXT_DARK
    add_speaker_note(s5, "Slide 5 summarizes the data dictionary with precise data types and declarative constraints.")

    # Slide 6: DDL and Constraints
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "MySQL DDL and Declarative Integrity Constraints", "Physical Database Design", "REVIEW 2")
    add_footer(s6, "Review 2")
    add_card(s6, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Production MySQL 8.x DDL Code Extracts")
    tb6 = s6.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.6))
    tf6 = tb6.text_frame
    tf6.word_wrap = True
    ddl_snippets = [
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
        "    CONSTRAINT chk_seg_seq_order CHECK (end_stop_seq > start_stop_seq),\n"
        "    INDEX idx_seat_run_alloc (run_id, seat_id, allocation_status)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;",
        "CREATE TABLE waitlists (\n"
        "    waitlist_id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    booking_id INT NOT NULL,\n"
        "    run_id INT NOT NULL,\n"
        "    travel_class VARCHAR(10) NOT NULL,\n"
        "    position INT NOT NULL,\n"
        "    waitlist_status VARCHAR(20) NOT NULL DEFAULT 'WAITING',\n"
        "    CONSTRAINT chk_wl_pos_positive CHECK (position > 0),\n"
        "    INDEX idx_wl_queue (run_id, travel_class, position)\n"
        ") ENGINE=InnoDB;"
    ]
    for snip in ddl_snippets:
        p = tf6.add_paragraph()
        p.text = snip
        p.font.name = 'Courier New'
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_NAVY_PRIMARY
        p.space_after = Pt(8)
    add_speaker_note(s6, "Slide 6 shows actual DDL statements demonstrating foreign keys, composite indexes, and check constraints on InnoDB tables.")

    # Slide 7: Segment-Wise Seat Allocation Logic
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Segment-Wise Seat Availability and Overlap Algorithm", "Core Allocation Logic", "REVIEW 2")
    add_footer(s7, "Review 2")

    add_card(s7, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "The Half-Open Interval Formula [s, e)")
    tb7_l = s7.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(5.2), Inches(4.5))
    tf7_l = tb7_l.text_frame
    tf7_l.word_wrap = True
    p = tf7_l.paragraphs[0]
    p.text = "Interval Overlap Condition:\nFor existing allocation [s, e) and requested interval [r_start, r_end):\n\nOVERLAP = (s < r_end) AND (r_start < e)\n\nRelational SQL Implementation:\nSELECT seat_id FROM journey_segments\nWHERE run_id = :run_id \n  AND allocation_status = 'ACTIVE'\n  AND start_stop_seq < :req_end\n  AND :req_start < end_stop_seq;\n\nAny seat returned by this query is currently occupied over the requested segment."
    p.font.size = Pt(11)

    add_card(s7, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Empirical Seat Reuse Demonstration")
    tb7_r = s7.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.3), Inches(4.5))
    tf7_r = tb7_r.text_frame
    tf7_r.word_wrap = True
    p = tf7_r.paragraphs[0]
    p.text = "Route: NDLS(1) -> CNB(2) -> PRYJ(3) -> BSB(4)\n\nCase 1: Valid Non-Overlapping Reuse (Seat C1-1)\n• Passenger 1 books NDLS -> CNB: [1, 2)\n• Passenger 2 books CNB -> BSB: [2, 4)\nOverlap Test: 1 < 4 (True) AND 2 < 2 (False) => NO CONFLICT!\nBoth confirmed simultaneously on Seat C1-1!\n\nCase 2: Conflicting Request Blocked\n• Passenger 3 requests NDLS -> BSB: [1, 4)\nOverlap Test with [1, 2): 1 < 4 (True) AND 1 < 2 (True) => CONFLICT!\nSeat C1-1 is blocked."
    p.font.size = Pt(11)

    add_speaker_note(s7, "Slide 7 explains the mathematical interval overlap formula and shows our benchmark proof: Passenger 1 and 2 sharing Seat C1-1 on disjoint segments.")

    # Slide 8: Waitlist, Cancellation, Refunds, Promotion
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Waitlist Queue & Atomic Promotion Workflow", "Queue & Refund Policy", "REVIEW 2")
    add_footer(s8, "Review 2")
    add_card(s8, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Deterministic Cancellation & Promotion Pipeline")
    tb8 = s8.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.6))
    tf8 = tb8.text_frame
    tf8.word_wrap = True
    wl_steps = [
        ("1. Queue Serialization", "When a travel class is exhausted for an interval, bookings are placed into waitlists with position = MAX(position) + 1. Scoped strictly by (run_id, travel_class)."),
        ("2. Cancellation & Deterministic Refund", "Cancellation of confirmed ticket applies a 20% fee deduction (retained) and 80% refund. The journey_segments record transitions to CANCELLED."),
        ("3. Re-verification of Waitlist Candidates", "Waiting entries are retrieved in FIFO order (position ASC). The candidate's exact [origin, dest) interval is re-checked against all coach seats."),
        ("4. Atomic Promotion Execution", "If an eligible seat is found, a new JourneySegment is created, candidate booking becomes CONFIRMED, and waitlist status becomes PROMOTED within the same database transaction.")
    ]
    for tag, desc in wl_steps:
        p = tf8.add_paragraph()
        p.text = f"✔ {tag}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_NAVY_PRIMARY
        r = p.add_run()
        r.text = desc
        r.font.bold = False
        r.font.size = Pt(10.5)
        p.space_after = Pt(10)
    add_speaker_note(s8, "Slide 8 details the waitlist queue management, cancellation fee policy, and the atomic promotion subroutine.")

    # Slide 9: SQL Query Demonstrations
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "SQL Implementation: Joins, Nested Queries & Views", "SQL Query Engineering", "REVIEW 2")
    add_footer(s9, "Review 2")
    add_card(s9, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Executed SQL Query Extracts")
    tb9 = s9.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.6))
    tf9 = tb9.text_frame
    tf9.word_wrap = True
    sql_snips = [
        "-- 1. COACH OCCUPANCY WITH MULTI-TABLE JOINS & AGGREGATION\n"
        "SELECT c.coach_code, c.travel_class, COUNT(DISTINCT js.segment_id) AS occupied,\n"
        "       ROUND(COUNT(DISTINCT js.segment_id) * 100.0 / c.total_seats, 2) AS occupancy_pct\n"
        "FROM coaches c JOIN seats s ON c.coach_id = s.coach_id\n"
        "LEFT JOIN journey_segments js ON s.seat_id = js.seat_id AND js.allocation_status = 'ACTIVE'\n"
        "GROUP BY c.coach_id, c.coach_code, c.travel_class, c.total_seats;",
        "-- 2. FINANCIAL RECONCILIATION AUDIT (SCALAR NESTED SUBQUERIES)\n"
        "SELECT \n"
        "    (SELECT SUM(total_fare) FROM bookings) AS gross_booked_fare,\n"
        "    (SELECT SUM(amount) FROM payments WHERE payment_status = 'COMPLETED') AS net_collected,\n"
        "    (SELECT SUM(refund_amount) FROM cancellations) AS total_refunded;"
    ]
    for sn in sql_snips:
        p = tf9.add_paragraph()
        p.text = sn
        p.font.name = 'Courier New'
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_NAVY_PRIMARY
        p.space_after = Pt(10)
    add_speaker_note(s9, "Slide 9 highlights actual executed SQL queries showing multi-table joins, GROUP BY, aggregations, and scalar subqueries.")

    # Slide 10: 12 Benchmark Reports Summary
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "12 Executed Benchmark SQL Reports", "Analytical Reports", "REVIEW 2")
    add_footer(s10, "Review 2")
    add_card(s10, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Comprehensive SQL Reporting Catalog")
    tb10 = s10.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.6))
    tf10 = tb10.text_frame
    tf10.word_wrap = True
    rep_list = [
        "1. Segment-Wise Seat Availability by Train & Class", "2. Passenger Booking History & Detailed Itinerary",
        "3. Active Waitlist Queue Priority & Position", "4. Coach Occupancy Percentage Ratio",
        "5. Route Demand & Passenger Volume Analysis", "6. Cancellation Counts, Fees & Refund Disbursed",
        "7. Complete Journey Timetable & Station Stops", "8. Revenue Grouped by Train and Travel Class",
        "9. Financial Reconciliation Audit (Fares vs Refunds)", "10. Status Distribution (Confirmed vs WL vs Cancel)",
        "11. Train Stop Timetable & Distance Analysis", "12. High-Value Frequent Passengers (Nested Query)"
    ]
    for i in range(0, 12, 2):
        p = tf10.add_paragraph()
        p.text = f"• {rep_list[i]:<55} • {rep_list[i+1]}"
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(10)
    add_speaker_note(s10, "Slide 10 inventories the 12 operational reports executed by the system and available in the web reporting dashboard.")

    # Slide 11: Prototype Progress & Test Evidence
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Database Prototype and Automated Test Evidence", "Verification & Progress", "REVIEW 2")
    add_footer(s11, "Review 2")
    add_card(s11, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Actual Execution Evidence (16 Passed Tests in 0.36s)")
    tb11 = s11.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.6))
    tf11 = tb11.text_frame
    tf11.word_wrap = True
    p = tf11.paragraphs[0]
    p.text = "Automated Test Suite Output (pytest 8.4.2):\n"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_NAVY_PRIMARY

    test_log_txt = (
        "Railway_Reservation_System/tests/test_availability.py::test_interval_overlap_logic PASSED [  6%]\n"
        "Railway_Reservation_System/tests/test_availability.py::test_non_overlapping_seat_reuse PASSED [ 12%]\n"
        "Railway_Reservation_System/tests/test_availability.py::test_conflicting_interval_detection PASSED [ 18%]\n"
        "Railway_Reservation_System/tests/test_cancellations.py::test_eligible_cancellation_and_refund_policy PASSED [ 31%]\n"
        "Railway_Reservation_System/tests/test_cancellations.py::test_automated_waitlist_promotion PASSED [ 43%]\n"
        "Railway_Reservation_System/tests/test_integrity.py::test_unique_train_number_constraint PASSED [ 50%]\n"
        "Railway_Reservation_System/tests/test_integrity.py::test_passenger_age_check_constraint PASSED [ 62%]\n"
        "Railway_Reservation_System/tests/test_reports.py::test_all_12_reports_execute_successfully PASSED [ 81%]\n"
        "Railway_Reservation_System/tests/test_reservations.py::test_valid_booking_success PASSED [ 87%]\n"
        "============================== 16 passed in 0.36s =============================="
    )
    p_log = tf11.add_paragraph()
    p_log.text = test_log_txt
    p_log.font.name = 'Courier New'
    p_log.font.size = Pt(9.5)
    p_log.font.color.rgb = C_SUCCESS
    p_log.space_before = Pt(6)

    add_speaker_note(s11, "Slide 11 shows real automated testing evidence: 16 pytest test cases passing in 0.36 seconds with zero warnings or errors.")

    # Slide 12: Review 3 Roadmap
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Milestone Review 3 Objectives & Roadmap", "Next Steps", "REVIEW 2")
    add_footer(s12, "Review 2")
    add_card(s12, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Final Review 3 Deliverable Goals")
    tb12 = s12.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.5))
    tf12 = tb12.text_frame
    tf12.word_wrap = True
    r3_goals = [
        ("Complete End-to-End Browser UI", "Deploy intuitive dashboard, interactive train search, booking wizard, and ERS ticket slip views."),
        ("Concurrency & Stress Verification", "Verify transaction boundaries and row locking under multi-user simulated requests."),
        ("Comprehensive Academic Project Report", "Compile full 23-section project report with relational schema, data dictionary, and viva prep."),
        ("Live Demonstration Sequence", "Deliver repeatable 5-8 minute live demonstration script showcasing seat reuse and waitlist promotion.")
    ]
    for tag, desc in r3_goals:
        p = tf12.add_paragraph()
        p.text = f"🎯 {tag}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = C_NAVY_PRIMARY
        r = p.add_run()
        r.text = desc
        r.font.bold = False
        r.font.size = Pt(11)
        p.space_after = Pt(14)
    add_speaker_note(s12, "Slide 12 concludes Review 2 with our roadmap toward the final Review 3 demonstration.")

    prs.save(str(PRES_DIR / 'Review_2_Normalization_and_SQL_Implementation.pptx'))
    print("Review 2 PPTX generated successfully.")

# ==============================================================================
# DELIVERABLE C: REVIEW 3 (WEEK 16) - 12 SLIDES
# ==============================================================================
def generate_review_3():
    prs = create_base_presentation()
    blank_layout = prs.slide_layouts[6]

    # Slide 1: Title
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_NAVY_DARK)
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(0.2), Inches(4.2))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_GOLD
    bar.line.fill.background()

    if WOXSEN_LOGO_PATH.exists():
        s1.shapes.add_picture(str(WOXSEN_LOGO_PATH), Inches(9.8), Inches(1.3), width=Inches(2.7))

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.4), Inches(8.5), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = "WOXSEN UNIVERSITY | SCHOOL OF TECHNOLOGY | DBMS FINAL REVIEW"
    p0.font.bold = True
    p0.font.size = Pt(13)
    p0.font.color.rgb = C_GOLD
    p1 = tf.add_paragraph()
    p1.text = "Railway Ticket Reservation and\nJourney Management System"
    p1.font.bold = True
    p1.font.size = Pt(32)
    p1.font.color.rgb = RGBColor(255, 255, 255)
    p2 = tf.add_paragraph()
    p2.text = "REVIEW 3: Final System Implementation, Verification, and Live Demonstration"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_before = Pt(14)
    p3 = tf.add_paragraph()
    p3.text = "Student Name: Heman  |  Roll Number: 25WU0102097  |  Section: AIML Rhinos\nFaculty Mentor: Prof. Sahithi  |  School of Technology, Woxsen University  |  Week 16"
    p3.font.size = Pt(12)
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.space_before = Pt(28)
    add_speaker_note(s1, "Welcome to the final Review 3 presentation. Today we demonstrate the completed, fully functional Railway Ticket Reservation and Journey Management System, showcasing our verified relational database, working UI, and automated tests.")

    # Slide 2: Final Architecture
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Final System Architecture and Technology Stack", "System Architecture", "REVIEW 3")
    add_footer(s2, "Review 3")
    add_card(s2, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Production Multi-Tier Implementation Flow")
    tiers = [
        ("Web Frontend", "Bootstrap 5 & HTML5\nResponsive Navbar & Alerts\nERS Ticket Slips\nJavaScript Auto-loader", Inches(1.2)),
        ("Application Core", "Python 3.9 & Flask\n8 Modular Blueprints\nForm Validations\nCustom Jinja2 Filters", Inches(4.1)),
        ("Business Engine", "Availability Service [s, e)\nTransaction Safe Booking\nPessimistic Row Locks\nAtomic WL Promotion", Inches(7.0)),
        ("Database Tier", "MySQL 8.x InnoDB Engine\n14 Relations in 3NF\n4 Relational Views\n12 SQL Benchmark Reports", Inches(9.9))
    ]
    for t_name, t_desc, l_pos in tiers:
        t_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l_pos, Inches(2.2), Inches(2.4), Inches(3.8))
        t_box.fill.solid()
        t_box.fill.fore_color.rgb = C_CARD_BG
        t_box.line.color.rgb = C_NAVY_PRIMARY
        t_box.line.width = Pt(2)
        tf_tb = t_box.text_frame
        tf_tb.word_wrap = True
        tf_tb.margin_left = Inches(0.15)
        tf_tb.margin_top = Inches(0.2)
        p_thdr = tf_tb.paragraphs[0]
        p_thdr.text = t_name
        p_thdr.font.name = 'Arial'
        p_thdr.font.size = Pt(13)
        p_thdr.font.bold = True
        p_thdr.font.color.rgb = C_NAVY_PRIMARY
        p_thdr.space_after = Pt(12)
        p_tdet = tf_tb.add_paragraph()
        p_tdet.text = t_desc
        p_tdet.font.name = 'Arial'
        p_tdet.font.size = Pt(10.5)
        p_tdet.font.color.rgb = C_TEXT_DARK
    add_speaker_note(s2, "Slide 2 outlines the completed architecture linking HTML5/Bootstrap 5 frontend to Flask controllers, business services, and MySQL InnoDB persistence.")

    # Slide 3: Final ER Diagram & Schema
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Implemented ER Diagram and Database Design", "Database Design", "REVIEW 3")
    add_footer(s3, "Review 3")
    add_card(s3, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Fully Consistent 14-Table 3NF Relational Schema")
    tb3 = s3.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.6))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    er_highlights = [
        ("Identical Schema Consistency", "The implemented database schema strictly matches the ER design from Review 1 and normalization proofs from Review 2 without discrepancies."),
        ("Entity Separation", "Stations, Routes, Ordered Stops, Locomotive Definitions, Dated Runs, Rolling Stock Coaches, and Individual Seat Units are completely decoupled."),
        ("Transactional Integrity", "Bookings, Journey_Segments, Waitlists, Payments, and Cancellations maintain complete auditability through foreign keys and composite unique constraints."),
        ("Monetary Precision", "All currency columns use DECIMAL(10,2) eliminating binary floating-point rounding errors.")
    ]
    for tag, desc in er_highlights:
        p = tf3.add_paragraph()
        p.text = f"✔ {tag}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_NAVY_PRIMARY
        r = p.add_run()
        r.text = desc
        r.font.bold = False
        r.font.size = Pt(10.5)
        p.space_after = Pt(10)
    add_speaker_note(s3, "Slide 3 confirms total structural consistency across all 3 reviews without changing table names or dropping constraints.")

    # Slide 4: Application Modules
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Completed Application Modules Overview", "Module Inventory", "REVIEW 3")
    add_footer(s4, "Review 3")
    add_card(s4, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Implemented Software Modules (100% Complete)")
    tb4 = s4.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.6))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    mods = [
        ("Dashboard Module (/)", "Live database KPI summary cards: total trains, passengers, bookings, waitlists, revenue."),
        ("Train Search & Timetable (/search)", "Origin/destination route matching, stop timetable ordering, live segment seat availability."),
        ("Passenger Profile Module (/passengers)", "Passenger registration with age domain check (1-119) and government ID validation."),
        ("Reservation & ERS Module (/book, /booking/<pnr>)", "Atomic booking, berth allocation, PNR generation, payment simulation, and printable ERS slip."),
        ("Cancellation & Refund Module (/cancel)", "PNR lookup, refund preview (20% fee deduction), and automated waitlist promotion trigger."),
        ("Waitlist Registry (/waitlist)", "Live FIFO queue position tracking across runs and travel classes."),
        ("SQL Reports Hub (/reports)", "Interactive execution of all 12 benchmark SQL reports with dynamic data tables.")
    ]
    for tag, desc in mods:
        p = tf4.add_paragraph()
        p.text = f"• {tag}: "
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_NAVY_PRIMARY
        r = p.add_run()
        r.text = desc
        r.font.bold = False
        r.font.size = Pt(10)
        p.space_after = Pt(5)
    add_speaker_note(s4, "Slide 4 summarizes the 7 completed software modules running in the live application.")

    # Slide 5: Train Search & Live Availability (Screenshot Embedded)
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Train Search and Live Segment-Wise Availability", "Live System Demonstration", "REVIEW 3")
    add_footer(s5, "Review 3")
    add_card(s5, Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.4), "Operational Feature Explanation")
    tb5 = s5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.4), Inches(4.5))
    tf5 = tb5.text_frame
    tf5.word_wrap = True
    p = tf5.paragraphs[0]
    p.text = (
        "• User selects Origin (NDLS), Destination (BSB), and Travel Date (2026-10-14).\n\n"
        "• Relational query validates route progression (Stop 1 precedes Stop 4).\n\n"
        "• Segment availability algorithm tests interval overlap across all physical seats in CC and 1A coaches.\n\n"
        "• Live status cards display remaining free seats or active waitlist positions with calculated fares."
    )
    p.font.size = Pt(11)
    
    # Embed screenshot on right
    img_search = SCREENSHOTS_DIR / "search_results.png"
    if img_search.exists():
        s5.shapes.add_picture(str(img_search), Inches(6.8), Inches(1.4), width=Inches(5.7))

    add_speaker_note(s5, "Slide 5 demonstrates our live Train Search module with an actual application screenshot showing Vande Bharat Express availability on NDLS-BSB.")

    # Slide 6: Reservation & Seat Allocation (Screenshot Embedded)
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Confirmed Reservation and Seat Allocation", "Live System Demonstration", "REVIEW 3")
    add_footer(s6, "Review 3")
    add_card(s6, Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.4), "Electronic Reservation Slip (ERS) Workflow")
    tb6 = s6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.4), Inches(4.5))
    tf6 = tb6.text_frame
    tf6.word_wrap = True
    p = tf6.paragraphs[0]
    p.text = (
        "• Transaction safety: Row-level lock (FOR UPDATE) acquired during seat assignment.\n\n"
        "• Generates unique 10-digit PNR and binds passenger profile.\n\n"
        "• Inserts active JourneySegment over [1, 2) and records completed Payment.\n\n"
        "• Renders printable Electronic Reservation Slip showing Coach, Seat number, and Berth Type."
    )
    p.font.size = Pt(11)

    img_ers = SCREENSHOTS_DIR / "booking_ers.png"
    if img_ers.exists():
        s6.shapes.add_picture(str(img_ers), Inches(6.8), Inches(1.4), width=Inches(5.7))

    add_speaker_note(s6, "Slide 6 shows the confirmed Electronic Reservation Slip for PNR 2348912341, confirming coach and seat assignment.")

    # Slide 7: Waitlist & Atomic Promotion (Screenshot Embedded)
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Waitlist Queue and Automated Promotion", "Live System Demonstration", "REVIEW 3")
    add_footer(s7, "Review 3")
    add_card(s7, Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.4), "Atomic FIFO Promotion Logic")
    tb7 = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.4), Inches(4.5))
    tf7 = tb7.text_frame
    tf7.word_wrap = True
    p = tf7.paragraphs[0]
    p.text = (
        "• Exhausted Capacity: When class capacity is full, passenger is queued at Position WL #1.\n\n"
        "• Cancellation Trigger: Cancelling a confirmed booking deducts a 20% cancellation fee, refunds 80%, and marks the segment CANCELLED.\n\n"
        "• Atomic Promotion: The system checks the waitlist queue in FIFO order, re-verifies segment availability, assigns the freed seat, and updates status to PROMOTED in one atomic transaction."
    )
    p.font.size = Pt(11)

    img_wl = SCREENSHOTS_DIR / "waitlist_queue.png"
    if img_wl.exists():
        s7.shapes.add_picture(str(img_wl), Inches(6.8), Inches(1.4), width=Inches(5.7))

    add_speaker_note(s7, "Slide 7 shows the live waitlist queue and demonstrates how cancellation atomically promotes eligible candidates.")

    # Slide 8: SQL Reports & CRUD Operations (Screenshot Embedded)
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "SQL Reports Hub and Database-Backed CRUD", "Analytical Reporting", "REVIEW 3")
    add_footer(s8, "Review 3")
    add_card(s8, Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.4), "12 Real-Time Analytical SQL Queries")
    tb8 = s8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.4), Inches(4.5))
    tf8 = tb8.text_frame
    tf8.word_wrap = True
    p = tf8.paragraphs[0]
    p.text = (
        "• Interactive Reports Hub: Select between 12 benchmark SQL reports.\n\n"
        "• Demonstrates Joins, GROUP BY, HAVING, and scalar subqueries.\n\n"
        "• Financial Reconciliation: Audits gross booking value vs payments collected vs refunds disbursed.\n\n"
        "• Coach Occupancy: Computes exact percentage occupancy per physical carriage."
    )
    p.font.size = Pt(11)

    img_rep = SCREENSHOTS_DIR / "sql_reports.png"
    if img_rep.exists():
        s8.shapes.add_picture(str(img_rep), Inches(6.8), Inches(1.4), width=Inches(5.7))

    add_speaker_note(s8, "Slide 8 shows our SQL Reports Hub executing live analytical queries against the database.")

    # Slide 9: Integrity, Transactions, and Performance
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Transaction Boundaries, Locking, and Integrity", "ACID & Concurrency", "REVIEW 3")
    add_footer(s9, "Review 3")
    add_card(s9, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "ACID Enforcement and Concurrency Control")
    tb9 = s9.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.6))
    tf9 = tb9.text_frame
    tf9.word_wrap = True
    acid_points = [
        ("Atomicity", "db.session.begin_nested() ensures that if seat assignment or payment fails, all related insertions roll back cleanly."),
        ("Consistency", "Declarative CHECK constraints (age > 0, fare >= 0, dest > orig) and Foreign Keys maintain valid relational states."),
        ("Isolation & Row Locking", "SELECT ... FOR UPDATE places exclusive row locks on TrainRun / Seat rows, serializing competing reservations and eliminating double-booking race conditions."),
        ("Durability", "InnoDB transaction write-ahead logs (redo_log) guarantee data persistence across sudden server crashes."),
        ("Indexing Performance", "B-Tree indexes on (run_id, seat_id, allocation_status) allow interval overlap checks to execute in sub-millisecond time.")
    ]
    for tag, desc in acid_points:
        p = tf9.add_paragraph()
        p.text = f"✔ {tag}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_NAVY_PRIMARY
        r = p.add_run()
        r.text = desc
        r.font.bold = False
        r.font.size = Pt(10.5)
        p.space_after = Pt(8)
    add_speaker_note(s9, "Slide 9 explains the transaction boundaries, row-level locking strategy, and indexing optimizations guaranteeing ACID safety.")

    # Slide 10: Testing Methodology & Actual Results
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Testing Methodology and Verified Results", "Automated Testing Verification", "REVIEW 3")
    add_footer(s10, "Review 3")
    add_card(s10, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "16 Automated Tests Executed via pytest (100% Pass Rate)")
    
    t_shape10 = s10.shapes.add_table(9, 4, Inches(1.0), Inches(2.1), Inches(11.333), Inches(4.3))
    t10 = t_shape10.table
    t10.columns[0].width = Inches(3.2)
    t10.columns[1].width = Inches(2.5)
    t10.columns[2].width = Inches(4.2)
    t10.columns[3].width = Inches(1.4)
    h10 = ["Test Case", "Category", "Verification Goal", "Result"]
    for i, h in enumerate(h10):
        cell = t10.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(255, 255, 255)
    t10_data = [
        ("test_interval_overlap_logic", "Algorithm", "Mathematical half-open interval overlap evaluation", "PASSED"),
        ("test_non_overlapping_seat_reuse", "Business Logic", "Seat C1-1 concurrently held on [1,2) and [2,4)", "PASSED"),
        ("test_conflicting_interval_detection", "Integrity", "Conflicting request for [1,4) correctly rejected", "PASSED"),
        ("test_cancelled_allocation_restores_availability", "State Machine", "Cancelling segment frees seat for subsequent booking", "PASSED"),
        ("test_eligible_cancellation_and_refund", "Financial Audit", "20% fee deducted; 80% refunded to passenger", "PASSED"),
        ("test_duplicate_cancellation_rejected", "Transactions", "Second cancellation attempt raises ValueError", "PASSED"),
        ("test_automated_waitlist_promotion", "Queue Logic", "Freeing confirmed seat promotes WL candidate atomically", "PASSED"),
        ("test_all_12_reports_execute_successfully", "SQL Analytics", "All 12 benchmark queries execute without errors", "PASSED")
    ]
    for r_idx, r_data in enumerate(t10_data):
        for c_idx, val in enumerate(r_data):
            cell = t10.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD_BG if r_idx % 2 == 0 else C_SLATE_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.bold = True if c_idx == 3 else False
            p.font.color.rgb = C_SUCCESS if val == 'PASSED' else C_TEXT_DARK
    add_speaker_note(s10, "Slide 10 presents genuine test execution evidence: 16 test cases passing in 0.36 seconds covering interval overlaps, cancellations, and integrity constraints.")

    # Slide 11: Limitations and Future Scope
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Limitations and Future Enhancements", "Engineering Evaluation", "REVIEW 3")
    add_footer(s11, "Review 3")
    add_card(s11, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Current Prototype Limitations")
    tb11_l = s11.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(5.2), Inches(4.5))
    tf11_l = tb11_l.text_frame
    tf11_l.word_wrap = True
    p = tf11_l.paragraphs[0]
    p.text = (
        "• Simulated Financial Gateway: Simulated UPI/Card processing without live banking webhooks.\n\n"
        "• Static Timetables: Fixed scheduled departures without real-time GPS locomotive tracking.\n\n"
        "• Single RDBMS Node: Local relational database instance rather than distributed multi-region cluster."
    )
    p.font.size = Pt(11)

    add_card(s11, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Future Scope & Production Scaling")
    tb11_r = s11.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.3), Inches(4.5))
    tf11_r = tb11_r.text_frame
    tf11_r.word_wrap = True
    p = tf11_r.paragraphs[0]
    p.text = (
        "• Real-Time NTES Integration: Live train delay tracking and platform assignment feeds.\n\n"
        "• Redis Inventory Caching: High-throughput memory bitsets to handle massive concurrent Tatkal spikes.\n\n"
        "• Dynamic AI Pricing: Predictive demand modeling adjusting fares and estimating waitlist confirmation probability.\n\n"
        "• Read Replicas: Offloading analytical reporting queries to MySQL read replicas."
    )
    p.font.size = Pt(11)

    add_speaker_note(s11, "Slide 11 addresses real-world engineering constraints and identifies scalable enhancements like Redis caching and live NTES APIs.")

    # Slide 12: Conclusion & Viva Preparation
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Conclusion and Viva Voce Preparation", "Summary & Viva Defense", "REVIEW 3")
    add_footer(s12, "Review 3")
    add_card(s12, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.4), "Key Academic Takeaways & Ready Viva Defenses")
    tb12 = s12.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.6))
    tf12 = tb12.text_frame
    tf12.word_wrap = True
    viva_summary = [
        ("Why is 3NF necessary?", "Decoupling train definitions from dated runs, and passenger profiles from bookings, prevents update and insertion anomalies."),
        ("How is seat reuse solved?", "Half-open intervals [s, e) tested via s < r_end AND r_start < e allow disjoint passenger journeys on the same seat."),
        ("How are race conditions prevented?", "ACID transactions with pessimistic row locking (SELECT ... FOR UPDATE) serialize competing requests."),
        ("Why use DECIMAL?", "Fixed-point DECIMAL(10,2) prevents binary floating-point rounding errors in fares and refunds."),
        ("How are waitlists promoted?", "Automated FIFO queue evaluation re-checks segment availability and promotes candidates atomically.")
    ]
    for q, a in viva_summary:
        p = tf12.add_paragraph()
        p.text = f"Q: {q}"
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_NAVY_PRIMARY
        p_ans = tf12.add_paragraph()
        p_ans.text = f"A: {a}"
        p_ans.font.size = Pt(10)
        p_ans.font.color.rgb = C_TEXT_DARK
        p_ans.space_after = Pt(6)

    add_speaker_note(s12, "Slide 12 concludes the review by summarizing key academic contributions and offering crisp, defensible viva answers.")

    prs.save(str(PRES_DIR / 'Review_3_Final_Implementation_and_Demo.pptx'))
    print("Review 3 PPTX generated successfully.")

if __name__ == '__main__':
    generate_review_1()
    generate_review_2()
    generate_review_3()
