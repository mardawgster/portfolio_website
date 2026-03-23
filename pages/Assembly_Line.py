import streamlit as st
from PIL import Image
from modules.nav import Navbar

# Page Config
st.set_page_config(page_title="Assembly Line", layout="wide")

Navbar()

# --- HEADER SECTION ---
col1head, col2head = st.columns([10, 1])
with col1head:
    st.title("Innovation Factory Cyber-Physical Assembly Testbed")

with col2head:
    st.page_link("streamlit_app.py", label="Home 🏠")

# --- PROJECT:  ---

col1main1, col2main1 = st.columns([1, 2])

with col1main1:
    st.write("**Tech Stack:**")
    st.code("IOT: Home Assistant w/ Proxmox VE\nEdge Control: ESP32\nProgramming: ESPHome, Arduino, Python\nDatabase: InfluxDB\nCOMMS: ESPHome TCP API, MQTT")
    with open("assets/assy_line.jpeg", "rb") as file:
        st.download_button("Download Full Documentation", data=file, mime="application/pdf")
    vig_photo = Image.open("assets/assy_line.jpeg")
    #rot_vig_photo = vig_photo.rotate(270, expand=True)
    st.image(vig_photo, caption="One of Six Stations of the Assembly Line Testbed")



with col2main1:
    st.markdown("""
    ### An Advanced Assembly Research Testbed
    This project demonstrates the design and development of the IF-CPAT, a flexible & accessible cyber-physical assembly testbed for manual assembly research & teaching.
    
    **Key Engineering Achievements:**
    * **Manual Assembly Research:** Built for manual assembly research, with a focus on human-robot collaboration, cybersecurity, multimodal sensing, and data collection for machine learning applications in manufacturing
    * **Dataset Collection:** Designed to collect a large, multimodal dataset of human assembly activities, including video, audio, and sensor data from the assembly line
    * **Accessible Framework:** Built using accessible, flexible, open-source tools to enable replication and extension by the research community
    * **Multimodal Sensor Streams:** Integrated multiple sensor streams, including video, audio, part inventory levels, operator location, environmental conditions, operator hand movement, physiological data, along with actuator feedback, to enable comprehensive analysis of human assembly activities and human-robot collaboration dynamics 
    """)
    
    # Demo Video
    st.video("VIDEO_LINK") 

# --- SKILLS & RESEARCH ---
st.divider()
st.header("Skills Used in Project")
st.write("- **Hardware:** ")
st.write("- **Software:** ")