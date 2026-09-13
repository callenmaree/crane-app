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
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=1, # Center
        spaceAfter=15
    )
    
    section_style = ParagraphStyle(
        'SecTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=10,
        textColor=colors.HexColor("#007bff")
    )
    
    normal_style = styles['Normal']
    bold_style = ParagraphStyle('BoldText', parent=normal_style, fontName='Helvetica-Bold')

    # Document Title
    story.append(Paragraph("OVERHEAD CRANE CONDITION REPORT", title_style))
    story.append(Spacer(1, 10))
    
    # Section 1: Asset Info
    story.append(Paragraph("1. ASSET & INSPECTION INFORMATION", section_style))
    
    meta_data = [
        [Paragraph("<b>Date of Inspection:</b>", normal_style), Paragraph(str(inspection_date), normal_style),
         Paragraph("<b>Inspector Name:</b>", normal_style), Paragraph(inspector if inspector else "N/A", normal_style)],
        [Paragraph("<b>Manufacturer:</b>", normal_style), Paragraph(manufacturer if manufacturer else "N/A", normal_style),
         Paragraph("<b>Make / Model:</b>", normal_style), Paragraph(make_model if make_model else "N/A", normal_style)],
        [Paragraph("<b>Serial Number:</b>", normal_style), Paragraph(serial_no if serial_no else "N/A", normal_style),
         Paragraph("<b>Crane ID / Tag No:</b>", normal_style), Paragraph(crane_id if crane_id else "N/A", normal_style)],
        [Paragraph("<b>Capacity (SWL):</b>", normal_style), Paragraph(capacity if capacity else "N/A", normal_style),
         Paragraph("<b>Facility Location:</b>", normal_style), Paragraph(location if location else "N/A", normal_style)],
        [Paragraph("<b>Overall Status:</b>", normal_style), Paragraph(f"<b>{overall_status.upper()}</b>", normal_style),
         Paragraph("", normal_style), Paragraph("", normal_style)]
    ]
    
    meta_table = Table(meta_data, colWidths=[110, 160, 110, 160])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))
    
    # Section 2: Checklist
    story.append(Paragraph("2. COMPONENT STATUS BREAKDOWN", section_style))
    
    checklist_data = [
        [Paragraph("<b>Inspection Category</b>", normal_style), 
         Paragraph("<b>Status</b>", normal_style), 
         Paragraph("<b>Notes / Deficiencies</b>", normal_style)]
    ]
    
    for category, content in report_data.items():
        status_text = content["Status"]
        note_text = content["Notes"] if content["Notes"] else "No defects noted."
        checklist_data.append([
            Paragraph(category, normal_style),
            Paragraph(status_text, bold_style),
            Paragraph(note_text, normal_style)
        ])
        
    checklist_table = Table(checklist_data, colWidths=[160, 60, 320])
    checklist_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#007bff")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    # Quick fix for headers color inside table paragraphs
    for i in range(3):
        checklist_data[0][i].style.textColor = colors.white
        
    story.append(checklist_table)
    story.append(Spacer(1, 15))
    
    # Section 3: Recommendations
    story.append(Paragraph("3. ACTION ITEMS & RECOMMENDATIONS", section_style))
    rec_text = recommendations if recommendations.strip() else "No corrective actions listed."
    
    rec_table = Table([[Paragraph(rec_text, normal_style)]], colWidths=[540])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fafafa")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(rec_table)
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph("<i>This document serves as an official equipment health log record.</i>", ParagraphStyle('Footer', parent=normal_style, alignment=1, fontSize=9)))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# ---------------------------------------------------------
# MOBILE EXPORT BUTTON (WITH SERIAL NUMBER FILE NAMING)
# ---------------------------------------------------------
st.header("📋 Export Completed PDF")

clean_id = "".join(x for x in crane_id if x.isalnum() or x in ('-', '_')).strip()
clean_serial = "".join(x for x in serial_no if x.isalnum() or x in ('-', '_')).strip()

name_parts = ["Inspection"]
if clean_id:
    name_parts.append(clean_id)
if clean_serial:
    name_parts.append(clean_serial)
name_parts.append(str(inspection_date))

mobile_filename = f"{'_'.join(name_parts)}.pdf"

try:
    pdf_bytes = generate_pdf()
    
    st.download_button(
        label="📄 Download Official PDF Report",
        data=pdf_bytes,
        file_name=mobile_filename,
        mime="application/pdf",
        use_container_width=True,
        type="primary"
    )
except Exception as e:
    st.error(f"Waiting for form entries... Fill out identifying information sections.")
