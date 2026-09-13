import streamlit as st
import datetime

# Set web page title and icon optimized for mobile views
st.set_page_config(page_title="Crane Inspection", page_icon="🏗️", layout="centered")

st.title("🏗️ Overhead Crane Condition Report")
st.write("Complete the form on your mobile device. Click the button at the bottom to download your completed report.")

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
# ZERO-DEPENDENCY HTML DOCUMENT GENERATION
# ---------------------------------------------------------
def generate_html():
    # Build a clean, styled HTML report string
    rows_html = ""
    for category, content in report_data.items():
        status_color = "#28a745" if content["Status"] == "Pass" else ("#dc3545" if content["Status"] == "Fail" else "#6c757d")
        note_text = content["Notes"] if content["Notes"] else "No defects noted."
        rows_html += f"""
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">{category}</td>
            <td style="padding: 10px; border: 1px solid #ddd; text-align: center; color: white; background-color: {status_color}; font-weight: bold;">{content["Status"]}</td>
            <td style="padding: 10px; border: 1px solid #ddd;">{note_text}</td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Crane Inspection Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 30px; color: #333; line-height: 1.6; }}
            .header {{ text-align: center; margin-bottom: 30px; border-bottom: 3px solid #333; padding-bottom: 10px; }}
            .section {{ margin-bottom: 25px; }}
            .section-title {{ font-size: 18px; font-weight: bold; background: #f4f4f4; padding: 5px 10px; border-left: 5px solid #007bff; margin-bottom: 15px; }}
            .meta-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }}
            .meta-item {{ font-size: 14px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th {{ background-color: #007bff; color: white; padding: 10px; text-align: left; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>OVERHEAD CRANE CONDITION REPORT</h2>
        </div>
        
        <div class="section">
            <div class="section-title">1. Asset & Inspection Information</div>
            <div class="meta-grid">
                <div class="meta-item"><strong>Date of Inspection:</strong> {inspection_date}</div>
                <div class="meta-item"><strong>Inspector Name:</strong> {inspector if inspector else 'N/A'}</div>
                <div class="meta-item"><strong>Overall Operational Status:</strong> {overall_status}</div>
                <div class="meta-item"><strong>Manufacturer:</strong> {manufacturer if manufacturer else 'N/A'}</div>
                <div class="meta-item"><strong>Make / Model:</strong> {make_model if make_model else 'N/A'}</div>
                <div class="meta-item"><strong>Serial Number:</strong> {serial_no if serial_no else 'N/A'}</div>
                <div class="meta-item"><strong>Crane ID / Tag No.:</strong> {crane_id if crane_id else 'N/A'}</div>
                <div class="meta-item"><strong>Capacity (SWL):</strong> {capacity if capacity else 'N/A'}</div>
                <div class="meta-item"><strong>Facility Location:</strong> {location if location else 'N/A'}</div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">2. Component Status Breakdown</div>
            <table>
                <thead>
                    <tr>
                        <th style="width: 35%;">Inspection Category</th>
                        <th style="width: 15%; text-align: center;">Status</th>
                        <th style="width: 50%;">Notes / Deficiencies</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <div class="section">
            <div class="section-title">3. Action Items & Recommendations</div>
            <div style="border: 1px solid #ddd; padding: 15px; background: #fafafa; border-radius: 4px; font-style: italic;">
                {recommendations if recommendations.strip() else 'No corrective actions listed.'}
            </div>
        </div>

        <div style="text-align: center; margin-top: 50px; font-size: 12px; color: #777; font-style: italic;">
            This document serves as an official equipment health log record.
        </div>
    </body>
    </html>
    """
    return html_content

# ---------------------------------------------------------
# MOBILE EXPORT BUTTON (WITH SERIAL NUMBER FILE NAMING)
# ---------------------------------------------------------
st.header("📋 Export Completed Report")

clean_id = "".join(x for x in crane_id if x.isalnum() or x in ('-', '_')).strip()
clean_serial = "".join(x for x in serial_no if x.isalnum() or x in ('-', '_')).strip()

name_parts = ["Inspection"]
if clean_id:
    name_parts.append(clean_id)
if clean_serial:
    name_parts.append(clean_serial)
name_parts.append(str(inspection_date))

mobile_filename = f"{'_'.join(name_parts)}.html"

html_data = generate_html()

st.download_button(
    label="📄 Download Official Report Document",
    data=html_data,
    file_name=mobile_filename,
    mime="text/html",
    use_container_width=True,
    type="primary"
)
