import streamlit as st
from PIL import Image
import base64
import os
import io

## CSS FOR IMAGES
st.markdown("""
    <style>
    /* Centering the column content */
    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    /* The Hover Flare Effect */
    .project-thumbnail {
        transition: transform .3s ease, box-shadow .3s ease;
        border-radius: 10px;
        width: 100%;
        cursor: pointer;
    }
    .project-thumbnail:hover {
        transform: scale(1.05); /* Slight grow */
        box-shadow: 0px 10px 20px rgba(0,0,0,0.2); /* Shadow depth */
    }
    </style>
""", unsafe_allow_html=True)

## IMG TO BASE64
def get_image_base64(pil_img):
    buffer = io.BytesIO()
    pil_img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode()

# Page Config
st.set_page_config(page_title="Home", layout="wide")

# --- HEADER SECTION ---
col1head, col2head = st.columns([4, 1])
with col1head:
    st.title("Marcus DiBattista, PhD Candidate")
    st.subheader("Mechanical Engineering @ University of Georgia")
    st.write("Specializing in SME-accessible manufacturing technology and IoT integration.")
with col2head:
    st.image("assets/Headshot.png", width=150)



colmain1, colmain2, colmain3, colmain4 = st.columns(4)

with colmain1:

    vig_photo = Image.open("assets/vignette_photo.JPG")
    rot_vig_photo = vig_photo.rotate(270, expand=True)
    img_b64 = get_image_base64(rot_vig_photo)

    st.markdown(
            f"""
            <a href="/lem_sort" target="_self">
                <img src="data:image/jpeg;base64,{img_b64}" class="project-thumbnail">
            </a>
            """,
            unsafe_allow_html=True
        )
    st.space("small")
    st.write(" 🍋 Lemon Sorter Project 🍋 ")

with colmain2:
    
    vig_photo = Image.open("assets/vignette_photo.JPG")
    rot_vig_photo = vig_photo.rotate(270, expand=True)
    img_b64 = get_image_base64(rot_vig_photo)

    st.markdown(
            f"""
            <a href="/smi_3dp" target="_self">
                <img src="data:image/jpeg;base64,{img_b64}" class="project-thumbnail">
            </a>
            """,
            unsafe_allow_html=True
        )
    st.space("small")
    st.write(" 🍋 Lemon Sorter Project 🍋 ")