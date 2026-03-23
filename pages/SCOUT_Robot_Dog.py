import streamlit as st
from PIL import Image
from streamlit_image_comparison import image_comparison
from modules.nav import Navbar

# Page Config
st.set_page_config(page_title="SCOUT Robot Dog", layout="wide")

Navbar()

# --- HEADER SECTION ---
col1head, col2head = st.columns([4, 1])
with col1head:
    st.title("SCOUT Robot Dog Inventory Localization System")

with col2head:
    st.page_link("streamlit_app.py", label="Home 🏠")

# --- PROJECT:  ---

col1main1, col2main1 = st.columns([1, 2])

with col1main1:
    st.write("**Tech Stack:**")
    st.code("Hardware: Unitree Go2 EDU, Jetson Orin Nano,\nVulcan UHF RFID Scanner, Unitree 4D LiDAR\nSoftware: Python, Unitree ROS SDK")
    ## Link to Paper

    st.button("[SCOUT Paper](https://www.sciencedirect.com/science/article/pii/S2213846325002081)")

    scout_photo = Image.open("assets/scout.jpeg")
    st.image(scout_photo, caption="SCOUT Inventory Localization System")



with col2main1:
    st.markdown("""
    ### HEADLINE
    This project demonstrates
    
    **Key Engineering Achievements:**
    * **ACH 1:** DESC 1
    * **ACH 2:** DESC 2
    * **ACH 3:** DESC 3
    * **ACH 4:** DESC 4
    """)
    
    # Demo Video
    image_comparison(
        img1="assets/scout1.jpeg",
        img2="assets/scout2.jpeg",
        label1="Old System",
        label2="New System"
    )

# --- SKILLS & RESEARCH ---
st.divider()
st.header("Skills Used in Project")
st.write("- **Hardware:** ")
st.write("- **Software:** ")