import streamlit as st
from PIL import Image

# Page Config
st.set_page_config(page_title="Marcus DiBattista | PhD Portfolio", layout="wide")

# --- HEADER SECTION ---
st.title("Marcus DiBattista, PhD Candidate")
st.subheader("Mechanical Engineering @ University of Georgia")
st.write("Specializing in SME-accessible manufacturing technology and IoT integration.")

# --- PROJECT: FRUIT SORTING VIGNETTE ---
st.divider()
st.header("Featured Project: Agricultural Computer Vision Vignette")

col1, col2 = st.columns([1, 2])

with col1:
    st.image("assets/vignette_photo.JPG", caption="The fully integrated sorting station.", width="stretch")
    st.download_button("Download Vignette Documentation", file_name='assets/vignette_docs.pdf')
    st.write("**Tech Stack:**")
    st.code("CV: YOLOv11\nEdge: ESP32\nLogic: Python\nProtocol: MQTT/Mosquitto")

with col2:
    st.markdown("""
    ### Autonomous Quality Detection for SMEs
    This project demonstrates a low-cost, internet-independent computer vision system designed for agricultural sorting[cite: 23, 24, 25]. 
    
    **Key Engineering Achievements:**
    * **Smoothed Label Algorithm:** Developed a rolling-history classification system to eliminate detection "flickering" in moving objects[cite: 226, 227].
    * **Pneumatic Edge-Triggering:** Integrated an IR proximity sensor with "rising edge" logic to ensure millisecond-accurate ejection of defective fruit[cite: 61, 277].
    * **Accessible Architecture:** Built using an **M4 Mac Mini** and **ESP32**, proving that industrial-grade AI can run on inexpensive, open-source hardware.
    """)
    
    # Placeholder for your demo video
    st.video("https://assets.gaa.im/videos/lemon_sorter_demo.webm") 

# --- SKILLS & RESEARCH ---
st.divider()
st.header("Core Competencies")
st.write("- **Hardware:** CNC (Genmitsu), Pneumatics (135 psi), PCB Design")
st.write("- **Software:** Python (OpenCV, Ultralytics), ESPHome, Home Assistant, C++")