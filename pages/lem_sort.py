import streamlit as st
from PIL import Image

# Page Config
st.set_page_config(page_title="Lemon Sorting Project", layout="wide")

# --- HEADER SECTION ---
col1head, col2head = st.columns([10, 1])
with col1head:
    st.title("Lemon Sorting Project")

with col2head:
    st.page_link("streamlit_app.py", label="Home 🏠")

# --- PROJECT: FRUIT SORTING VIGNETTE ---

col1main1, col2main1 = st.columns([1, 2])

with col1main1:
    st.write("**Tech Stack:**")
    st.code("CV: YOLOv11\nEdge: ESP32 & M4 Mac Mini\nLogic: Python\nCOM Protocol: MQTT/Mosquitto")
    with open("assets/vignette_docs.pdf", "rb") as file:
        st.download_button("Download Full Documentation", data=file, mime="application/pdf")
    vig_photo = Image.open("assets/vignette_photo.jpeg")
    st.image(vig_photo, caption="The fully integrated sorting station.")



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