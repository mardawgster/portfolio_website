import streamlit as st
from PIL import Image

# Page Config
st.set_page_config(page_title="Marcus DiBattista | PhD Portfolio", layout="wide")

# --- HEADER SECTION ---
col1head, col2head = st.columns([4, 1])
with col1head:
    st.title("Marcus DiBattista, PhD Candidate")
    st.subheader("Mechanical Engineering @ University of Georgia")
    st.write("Specializing in SME-accessible manufacturing technology and IoT integration.")
with col2head:
    st.image("assets/Headshot.png", width=150)

# --- PROJECT: FRUIT SORTING VIGNETTE ---
st.divider()
st.header("Featured Project: Agricultural Computer Vision Vignette")

col1main1, col2main1 = st.columns([1, 2])

with col1main1:
    st.write("**Tech Stack:**")
    st.code("CV: YOLOv11\nEdge: ESP32 & M4 Mac Mini\nLogic: Python\nCOM Protocol: MQTT/Mosquitto")
    with open("assets/vignette_docs.pdf", "rb") as file:
        st.download_button("Download Vignette Documentation", data=file, mime="application/pdf")
    vig_photo = Image.open("assets/vignette_photo.JPG")
    rot_vig_photo = vig_photo.rotate(270, expand=True)
    st.image(rot_vig_photo, caption="The fully integrated sorting station.")



with col2main1:
    st.markdown("""
    ### Autonomous Quality Detection for SMEs
    This project demonstrates a low-cost, robust, internet-independent computer vision system designed for automated agricultural sorting. 
    
    **Key Engineering Achievements:**
    * **Smoothed Label Algorithm:** Developed a rolling-history classification system to eliminate detection "flickering" and rotation compensation in moving objects.
    * **Pneumatic Edge-Triggering:** Integrated an IR proximity sensor with "rising edge" logic to ensure millisecond-accurate ejection of defective fruit.
    * **Accessible Architecture:** Built using an **M4 Mac Mini** and **ESP32**, proving that industrial-grade AI can run on inexpensive, open hardware.
    * **Open-Source Software:** Runs an open-source YOLO V11 model and trained on real data showing the accessibility of the technology.
    """)
    
    # Demo Video
    st.video("https://assets.gaa.im/videos/lemon_sorter_demo.webm") 

# --- SKILLS & RESEARCH ---
st.divider()
st.header("Core Competencies")
st.write("- **Hardware:** CNC (Genmitsu), Pneumatics (135 psi), PCB Design")
st.write("- **Software:** Python (OpenCV, Ultralytics), ESPHome, Home Assistant, C++")