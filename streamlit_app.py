import streamlit as st
from PIL import Image
import base64
import os
import streamlit as st

# --- 1. CUSTOM CSS FOR HOVER EFFECT ---
st.markdown("""
    <style>
    .project-card {
        border-radius: 10px;
        padding: 10px;
        background-color: #f0f2f6;
        transition: transform .2s; /* Animation speed */
        cursor: pointer;
        border: 1px solid #ddd;
        text-align: center;
        margin-bottom: 20px;
    }
    .project-card:hover {
        transform: scale(1.05); /* Zoom effect on hover */
        border-color: #ff4b4b; /* Change border color */
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    .project-card img {
        width: 100%;
        border-radius: 5px;
    }
    a {
        text-decoration: none !important;
        color: inherit !important;
    }
    </style>
""", unsafe_allow_html=True)

def get_base64_image(image_path):
    """Converts a local image to a base64 string for HTML use."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        # Returns a placeholder if the image is missing
        return ""

# Page Config
st.set_page_config(page_title="Home", layout="wide", )

# --- HEADER SECTION ---
col1head, col2head = st.columns([4, 1])
with col1head:
    st.title("Marcus DiBattista, PhD Candidate")
    st.subheader("Mechanical Engineering @ University of Georgia")
    st.write("Specializing in SME-accessible manufacturing technology and IoT integration.")
with col2head:
    st.image("assets/Headshot.png", width=150)

# Create a grid (e.g., 2 columns)
col1, col2 = st.columns(2)

# Helper function to create a card
def project_card(col, title, image_url, page_name, caption):
    with col:
        # We wrap the whole div in an <a> tag to make it clickable
        st.markdown(f"""
            <a href="./{page_name}" target="_self">
                <div class="project-card">
                    <img src="{image_url}">
                    <h3>{title}</h3>
                    <p>{caption}</p>
                </div>
            </a>
        """, unsafe_allow_html=True)

# --- 3. ADD YOUR PROJECTS ---
# Replace URLs with your image links (or base64 strings)
# Note: page_name should match the name of the file in /pages/ (without .py)
lemon_img = get_base64_image("images/vignette_photo.JPG")
project_card(col1, "Lemon Sorter", lemon_img, "lem_sort", "Created Custom Lemon Quality Sorting System using Computer Vision.")
project_card(col2, "SMI 3D Printing Project", lemon_img, "3dp_smi", "Integrating ESPHome with Home Assistant.")
