import streamlit as st
from PIL import Image
from modules.nav import Navbar

# Page Config
st.set_page_config(page_title="Assembly Line", layout="wide")

Navbar()

# --- HEADER SECTION ---
col1head, col2head = st.columns([10, 1])
with col1head:
    st.title("Innovation Factory Cyber-Physical Assembly Testbed (IFCAT)")

with col2head:
    st.page_link("streamlit_app.py", label="Home 🏠")

# --- PROJECT:  ---

col1main1, col2main1 = st.columns([1, 2])

with col1main1:
    st.write("**Tech Stack:**")
    st.code("IOT: Home Assistant w/ Proxmox VE\nEdge Control: ESP32\nProgramming: ESPHome, Arduino, Python\nDatabase: InfluxDB\nCOMMS: ESPHome TCP API, MQTT\nSensors/Tracking: IMU Telemetry, Load Cells, Computer Vision")
#    with open("assets/assy_line.jpeg", "rb") as file:
#       st.download_button("Download Full Documentation", use_container_width=True, data=file, mime="application/pdf")
    vig_photo = Image.open("assets/assy_line.jpeg")
    #rot_vig_photo = vig_photo.rotate(270, expand=True)
    st.image(vig_photo, caption="One of Six Stations of the Assembly Line Testbed")
    
    # Git Repo Link
    st.markdown("[**View Project on the Innovation Factory Git**](https://git.factory.uga.edu/UGA-Innovation-Factory/ifcat)")

with col2main1:
    st.markdown("""
    ### An Advanced Cyber-Physical Assembly Testbed
    This project demonstrates the design, deployment, and continuous enhancement of IFCAT, a flexible & accessible cyber-physical assembly testbed built for advanced manufacturing research, teaching, and continuous process monitoring.
    
    **Key Engineering Achievements & Advancements:**
    - **Real-Time Part Tracking & Telemetry:** Upgraded stations with instrumented load cell buckets and IMU telemetry to enable high-resolution, real-time tracking of assembly states and operator interactions directly across Home Assistant and InfluxDB.
    - **Time-Series Video Entropy:** Integrated advanced data collection pipelines to support time-series video entropy extraction algorithms (e.g., Permutation and Cross-Entropy) for real-time anomaly detection and operator fingerprinting.
    - **Modular Co-Design Framework:** Developed a co-design framework connecting the physical assembly line with advanced cyber-infrastructure to facilitate continuous monitoring and lean teaching.
    - **Multimodal Sensor Streams:** Seamlessly integrated diverse sensor streams—including video, audio, part inventory levels, environmental conditions, operator hand movement, and physiological data—to comprehensively analyze human assembly activities and human-robot collaboration dynamics.
    - **Accessible Framework:** Built using accessible, flexible, open-source tools to enable replication and extension by the research community, and to facilitate the development of new assembly research methodologies.
    """)
    
    # Artifact Reference
    st.info("💡 **Modular Assembly Artifact (IFCAA):** This testbed operates in tandem with custom-designed modular assembly artifacts equipped with their own onboard telemetry. Check out the dedicated artifact page for more details on its specific hardware integration.")
    
    # Update the target page path string below to match your project's actual filename for the artifact page
    st.page_link("pages/Assembly_Artifact.py", label="View the IFCAA Modular Artifact Page ➔", icon="⚙️")

# --- SKILLS & RESEARCH ---
st.divider()
st.header("Skills Used in Project")
st.write("- **Hardware:** 3D Design & Printing, Analog & Digital Sensor Integration, Instrumented Load Cells, IMU Telemetry, Industrial IoT, Modular Design, Human Factors Research")
st.write("- **Software:** Signal Processing, Time-Series Entropy Algorithms, Computer Vision, Industrial Logic, Python, ESPHome, MQTT, InfluxDB, GitHub, Linux CLI")