import streamlit as st
from PIL import Image
from modules.nav import Navbar

# Page Config
st.set_page_config(page_title="Manual Assembly Artifact", layout="wide")

Navbar()

# --- HEADER SECTION ---
col1head, col2head = st.columns([4, 1])
with col1head:
    st.title("Modular Cyber-Physical Assembly Artifact")

# --- PROJECT:  ---

col1main1, col2main1 = st.columns([1, 2])

with col1main1:
    st.write("**Tech Stack:**")
    st.code("""
    • ESPHome / C++
    • Home Assistant
    • MQTT Protocol
    • 3D CAD & FDM Printing
    """)
    
    # Update FILE_PATH to your actual PDF documentation path
#    with open("assets/Artifact_Documentation.pdf", "rb") as file:
#        st.download_button("Download Full Documentation", data=file, mime="application/pdf")
    
    # Update FILE_PATH to your actual image path
    vig_photo = Image.open("assets/artifact.png") 
    rot_vig_photo = vig_photo.rotate(270, expand=True)
    st.image(rot_vig_photo, caption="20mm T-slot Assembly Artifact with M5StickC Edge Node")

with col2main1:
    st.markdown("""
    ### Re-engineering Assembly Operations for Smart Manufacturing Research
    This project replaces a discontinued, proprietary commercial oscillating tool with a fully open, rigorously designed cyber-physical assembly artifact. Built as a standardized data generation node for a smart manufacturing testbed, this artifact resolves the mechanical degradation and closed-ecosystem limitations of traditional tools. It serves as a highly modular, untethered IoT node capable of streaming multi-modal telemetry—functioning simultaneously as an ergonomic assembly workpiece, a quality-control data generator, and an active surface for cyber-physical security simulations.
    
    **Key Engineering Achievements:**
    - **Extreme Modularity & Replicability:** Designed using a 20mm T-slot extruded aluminum frame, metric hardware, and standardized 3D-printable components, ensuring infinite assembly/disassembly cycles without mechanical failure. 
    - **Integrated Mechatronics & Edge Compute:** Features a custom two-pulley system (drive and encoder) monitored by an IR photointerrupter, directly wired to an onboard, battery-powered M5StickC Plus 2 (ESP32) microcontroller.
    - **Real-Time Telemetry & Digital Twin:** Utilizes ESPHome to process sensor data locally, publishing RPM metrics and live 3D orientation (via internal gyroscope/accelerometer) over MQTT directly to a central Home Assistant dashboard.
    - **Multi-Functional Experimental Utility:** Incorporates ergonomic fixturing handles for manual human-factors research while intentionally exposing network surfaces to allow researchers to inject and study simulated cyber-attacks.
    """)
    
    # Update VIDEO_LINK to your actual YouTube or hosted video URL
    st.video("https://www.youtube.com/watch?v=YOUR_VIDEO_ID") 

# --- SKILLS & RESEARCH ---
st.divider()
st.header("Skills Used in Project")
st.write("- **Hardware:** ESP32 Microcontrollers (M5Stack), IR Photointerrupter Sensors, 20mm Extruded Aluminum, Multi-axis IMUs, Bambu Lab FDM 3D Printing, First-Principles Mechatronics")
st.write("- **Software:** ESPHome, Home Assistant, MQTT Broker Configuration, IoT Network Topologies, Digital Twin Dashboarding, Open-Source Data Infrastructure")