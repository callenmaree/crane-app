import streamlit as st
import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Set web page title and icon optimized for mobile views
st.set_page_config(page_title="Crane Inspection", page_icon="🏗️", layout="centered")

st.title("🏗️ Overhead Crane Condition Report")
st.write("Complete the form on your mobile device. Click the button at the bottom to download a professional PDF report.")

# ---------------------------------------------------------
# SECTION 1: ASSET & MANUFACTURER INFORMATION
# ---------------------------------------------------------
st.header("1. Asset & Manufacturing Information")

manufacturer = st.text_input("Manufacturer", placeholder="e.g., Demag, Konecranes")
make_model = st.text_input("Make / Model")
serial_no = st.text_input("Serial Number")
crane_id = st.text_input("Crane ID / Tag No.")
capacity = st.text_input("Capacity (Tons / SWL)")
location = st.text_input("Facility Location / Bay")
inspector = st.text_input("Inspector Name")
inspection_date = st.date_input("Inspection Date", datetime.date.today())

status_options = ["Safe to Operate", "Conditional (Monitor)", "Out of Service (Fail)"]
overall_status = st.selectbox("Overall Operational Status", status_options)

st.markdown("---")

# Helper function optimized for single-column mobile view layouts
def mobile_inspection_row(component_name):
    st.subheader(component_name)
    result = st.radio(
        f"Status for {component_name}", 
        ["Pass", "Fail", "N/A"], 
        horizontal=True, 
        key=f"status_{component_name}"
    )
    notes = st.text_input(
        "Notes / Deficiencies", 
        placeholder="Enter deficiencies or notes if any...", 
        key=f"notes_{component_name}"
    )
    st.markdown("---")
    return {"Status": result, "Notes": notes}

# ---------------------------------------------------------
# INSPECTION CATEGORIES
# ---------------------------------------------------------
report_data = {}

st.header("2. General Crane Structure & Components")
st.caption("Main bridge girders, runway beams, end trucks, tracks, bumpers, and welds.")
report_data["General Structure"] = mobile_inspection_row("General Structure")

st.header("3. Electric Hoist & Components")
st.caption("Hoist drum, load chains/ropes, hooks, safety latches, trolley, and limit switches.")
report_data["Electric Hoist"] = mobile_inspection_row("Electric Hoist")

st.header("4. Mechanical Components")
st.caption("Holding brakes, drive/idler wheels, bearings, couplings, sheaves, and open gears.")
report_data["Mechanical Components"] = mobile_inspection_row("Mechanical Components")

st.header("5. Electrical Components")
st.caption("Motors, control panels, switchgear, contactors, pendants/remotes, and emergency stops.")
report_data["Electrical Components"] = mobile_inspection_row("Electrical Components")

st.header("6. Crane Supply System")
st.caption("Main disconnects, conductor rails, festoon systems, energy chains, and grounding.")
report_data["Crane Supply System"] = mobile_inspection_row("Crane Supply System")

# ---------------------------------------------------------
# FINAL RECOMMENDATIONS & ACTION ITEMS
# ---------------------------------------------------------
st.header("7. Recommendations & Action Items")
recommendations = st.text_area(
    "Enter corrective actions, parts required, or follow-up inspection timelines:",
    placeholder="e.g., Schedule immediate replacement for the hoist limit switch."
)

st.markdown("---")

# ---------------------------------------------------------
# REPORTLAB PDF GENERATION ENGINE
# ---------------------------------------------------------
def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#FFFFFF"),
        alignment=1,
    )
    
    section_style = ParagraphStyle(
        'SecTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        spaceBefore=15,
        spaceAfter=8,
        textColor=colors.HexColor("#0F1117")
    )
    
    text_normal = ParagraphStyle('TextNorm', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#333333"))
    text_bold = ParagraphStyle('TextBold', parent=text_normal, fontName='Helvetica-Bold')
    
    status_hdr_style = ParagraphStyle('HdrTxt', parent=text_normal, fontName='Helvetica-Bold', textColor=colors.HexColor("#FFFFFF"), alignment=1)
    pass_style = ParagraphStyle('PassTxt', parent=text_normal, fontName='Helvetica-Bold', textColor=colors.HexColor("#1E7E34"), alignment=1)
    fail_style = ParagraphStyle('FailTxt', parent=text_normal, fontName='Helvetica-Bold', textColor=colors.HexColor("#BD2130"), alignment=1)
    na_style = ParagraphStyle('NaTxt', parent=text_normal, fontName='Helvetica-Bold', textColor=colors.HexColor("#545B62"), alignment=1)

    # Header Card
    header_table = Table([[Paragraph("🏗️ OVERHEAD CRANE CONDITION REPORT", title_style)]], colWidths=[540])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0E1117")), 
        ('PADDING', (0,0), (-1,-1), 14),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))
    
    # Asset Info
    story.append(Paragraph("1. Asset & Manufacturing Information", section_style))
    meta_rows = [
        [Paragraph("Manufacturer", text_bold), Paragraph(manufacturer if manufacturer else "—", text_normal),
         Paragraph("Date of Inspection", text_bold), Paragraph(str(inspection_date), text_normal)],
        [Paragraph("Make / Model", text_bold), Paragraph(make_model if make_model else "—", text_normal),
         Paragraph("Inspector Name", text_bold), Paragraph(inspector if inspector else "—", text_normal)],
        [Paragraph("Serial Number", text_bold), Paragraph(serial_no if serial_no else "—", text_normal),
         Paragraph("Crane ID / Tag No.", text_bold), Paragraph(crane_id if crane_id else "—", text_normal)],
        [Paragraph("Capacity (SWL)", text_bold), Paragraph(capacity if capacity else "—", text_normal),
         Paragraph("Facility Location", text_bold), Paragraph(location if location else "—", text_normal)],
        [Paragraph("Overall Status", text_bold), Paragraph(f"<b>{overall_status.upper()}</b>", text_bold),
         Paragraph("", text_normal), Paragraph("", text_normal)]
    ]
    
    meta_table = Table(meta_rows, colWidths=[135, 135, 135, 135])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9FA")), 
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E0E0E0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))
    
    # Checklist Matrix
    story.append(Paragraph("2. Component Status Breakdown", section_style))
    table_data = [
        [Paragraph("Inspection Category", status_hdr_style), 
         Paragraph("Status", status_hdr_style), 
         Paragraph("Notes / Deficiencies", status_hdr_style)]
    ]
    
    row_styles = []
    idx = 1
    for category, content in report_data.items():
        status_val = content["Status"]
        note_val = content["Notes"] if content["Notes"] else "No defects noted."
        
        if status_val == "Pass":
            status_p = Paragraph("PASS", pass_style)
            bg_color = colors.HexColor("#D4EDDA")
        elif status_val == "Fail":
            status_p = Paragraph("FAIL", fail_style)
            bg_color = colors.HexColor("#F8D7DA")
        else:
            status_p = Paragraph("N/A", na_style)
            bg_color = colors.HexColor("#E2E3E5")
            
        table_data.append([
            Paragraph(category, text_bold),
            status_p,
            Paragraph(note_val, text_normal)
        ])
        row_styles.append(('BACKGROUND', (1, idx), (1, idx), bg_color))
        idx += 1
        
    checklist_table = Table(table_data, colWidths=[160, 80, 300])
    base_styles = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#262730")), 
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D3D3D3")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]
    base_styles.extend(row_styles)
    checklist_table.setStyle(TableStyle(base_styles))
    story.append(checklist_table)
    story.append(Spacer(1, 10))
    
    # Recommendations Box
    story.append(Paragraph("3. Recommendations & Action Items", section_style))
    rec_text = recommendations if recommendations.strip() else "No specific corrective actions or recommendations noted."
    
    rec_table = Table([[Paragraph(rec_text, text_normal)]], colWidths=[540])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFF3CD")), 
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#FFEBAA")),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(rec_table)
    
    # Bottom Disclaimer
    story.append(Spacer(1, 25))
