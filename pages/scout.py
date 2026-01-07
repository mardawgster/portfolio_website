import streamlit as st
from PIL import Image
from streamlit_image_comparison import image_comparison

# Page Config
st.set_page_config(page_title="PAGE TITLE", layout="wide")

# --- HEADER SECTION ---
col1head, col2head = st.columns([4, 1])
with col1head:
    st.title("HEADER")

# --- PROJECT:  ---

col1main1, col2main1 = st.columns([1, 2])

with col1main1:
    st.write("**Tech Stack:**")
    st.code("")
    # with open("assets/FILE_PATH", "rb") as file:
    #     st.download_button("Download Full Documentation", data=file, mime="application/pdf")
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
    )

# --- SKILLS & RESEARCH ---
st.divider()
st.header("Skills Used in Project")
st.write("- **Hardware:** ")
st.write("- **Software:** ")