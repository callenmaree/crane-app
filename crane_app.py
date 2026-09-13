import streamlit as st
import datetime

# Set web page title and icon optimized for mobile views
st.set_page_config(page_title="Crane Inspection", page_icon="🏗️", layout="centered")

st.title("🏗️ Overhead Crane Condition Report")
st.write("Complete the form on your mobile device. Click the button at the bottom to download your completed report file.")

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
# MOBILE GENERATION & DOWNLOAD ENGINE
# ---------------------------------------------------------
st.header("📋 Export Completed Report")

# Format the text data cleanly into a string variable
text_content = f"""OVERHEAD CRANE CONDITION REPORT
=====================================
Date of Inspection : {inspection_date}
Inspector Name : {inspector}
Overall Status : {overall_status}

1. ASSET & MANUFACTURING INFORMATION
-------------------------------------
Manufacturer : {manufacturer}
Make / Model : {make_model}
Serial Number : {serial_no}
Crane ID / Tag No. : {crane_id}
Capacity (SWL) : {capacity}
Facility Location : {location}

2. COMPONENT STATUS BREAKDOWN
-------------------------------------\n"""

for category, content in report_data.items():
    text_content += f"[{content['Status']}] {category}\n"
    if content['Notes']:
        text_content += f" Notes: {content['Notes']}\n"
        
text_content += f"""\n3. ACTION ITEMS & RECOMMENDATIONS
-------------------------------------
{recommendations if recommendations.strip() else 'No corrective actions listed.'}

=====================================
End of Record File
"""

# Clean file name format for mobile file organization
clean_id = "".join(x for x in crane_id if x.isalnum() or x in ('-', '_')) if crane_id else "Crane"
mobile_filename = f"Inspection_{clean_id}_{inspection_date}.txt"

# Native mobile download button
st.download_button(
    label="💾 Download Completed Report File",
    data=text_content,
    file_name=mobile_filename,
    mime="text/plain",
    use_container_width=True,
    type="primary"
)
