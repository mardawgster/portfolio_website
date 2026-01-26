import streamlit as st
from PIL import Image

# Page Config
st.set_page_config(page_title="Create Lab Buildout", layout="wide")

# --- HEADER SECTION ---
col1head, col2head = st.columns([4, 1])
with col1head:
    st.title("Create Lab Buildout")

with col2head:
    st.page_link("streamlit_app.py", label="Home 🏠")

# --- PROJECT:  ---

col1main1, col2main1 = st.columns([1, 1])

with col1main1:
    st.write("**Equipment:**")
    st.code("FDM Additive: Bambu Labs H2D, X1C, P1S; Prusa XL, i3\nResin Additive: Formlabs 3L\nSubtractive: Haas Desktop Mill, Bambu Labs H2D Laser Module\nHusky Tool Chest w/ Assorted Hand Tools, Milwaukee Power Tools")
    vig_photo = Image.open("assets/smi_tools.png")
    rot_vig_photo = vig_photo.rotate(270, expand=True)
    st.image(rot_vig_photo, caption="IMAGE CAPTION")



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
    st.video("VIDEO_LINK") 

# --- SKILLS & RESEARCH ---
st.divider()
st.header("Skills Used in Project")
st.write("- **Hardware:** ")
st.write("- **Software:** ")