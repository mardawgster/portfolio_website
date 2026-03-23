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
    st.link_button(url="https://www.sciencedirect.com/science/article/pii/S2213846325002081", use_container_width=True, label="Read Full Paper 📄")

    scout_photo = Image.open("assets/scout.jpeg")
    st.image(scout_photo, caption="SCOUT Inventory Localization System")



with col2main1:
    st.markdown("""
    ### A Flexible Robot Inventory Localization System for Warehouse Environments
    This project demonstrates the design and development of SCOUT, a mobile robot inventory localization system for warehouse environments, utilizing a Unitree Go2 EDU quadruped robot equipped with a Jetson Orin Nano, Vulcan UHF RFID scanner, and Unitree 4D LiDAR.
    
    **Key Engineering Achievements:**
    * **Novel Localization Method:** Developed a novel inventory localization method that fuses LiDAR-based SLAM with RFID signal strength data to achieve accurate inventory localization in dynamic warehouse environments 
    * **Custom Mounting Solution:** Designed and implemented a custom mounting solution for the RFID scanner and LiDAR sensor on the robot chassis, ensuring optimal sensor placement for inventory scanning while maintaining robot mobility and stability
    * **Robust Communication Protocol:** Implemented a robust communication protocol between the robot and the central control system, enabling real-time data exchange and remote monitoring of the inventory localization process
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
st.write("- **Hardware:** Unitree Go2 EDU, Jetson Orin Nano, Vulcan UHF RFID Scanner, Unitree 4D LiDAR")
st.write("- **Software:** Python, Unitree ROS SDK, Vulcan RFID SDK")