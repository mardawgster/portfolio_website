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
def get_image_base64(pil_img, format):
    if format == "JPEG":
        buffer = io.BytesIO()
        pil_img.save(buffer, format="JPEG")
        return base64.b64encode(buffer.getvalue()).decode()
    elif format == "PNG":
        buffer = io.BytesIO()
        pil_img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()
    else:
        return pil_img

# Page Config
st.set_page_config(page_title="Home", layout="wide")

# --- HEADER SECTION ---
col1head, col2head, col3head = st.columns([1, 5, 1])
with col1head:
    st.image("assets/Headshot.png", width=150)
with col2head:
    st.title("Marcus DiBattista, PhD Candidate")
    st.subheader("Mechanical Engineering @ University of Georgia")
    # st.markdown("#### Specializing in SME-accessible manufacturing technology and IoT integration.")
with col3head:
    st.link_button("LinkedIn", "https://www.linkedin.com/in/marcusdibattista/")
    st.link_button("Google Scholar", "https://scholar.google.com/citations?user=ixBhetgAAAAJ&hl=en")
    st.link_button("Thingiverse", "https://www.thingiverse.com/MADmarcus/designs")
    st.link_button("YouTube", "https://www.youtube.com/@MarcusDiBattista")
st.markdown("# 🏗️ Professional Projects")
st.markdown("Click on a Project to Learn More")

colmain1, colmain2, colmain3, colmain4 = st.columns(4)

with colmain1:

    vig_photo = Image.open("assets/vignette_photo.jpeg")
    img_b64 = get_image_base64(vig_photo, "JPEG")

    st.markdown(
            f"""
            <a href="/lem_sort" target="_self">
                <img src="data:image/jpeg;base64,{img_b64}" class="project-thumbnail">
            </a>
            """,
            unsafe_allow_html=True
        )
    st.space("small")
    st.write(" 🍋 Automated Lemon Sorter 🍋 ")
    st.space("small")

with colmain2:
    
    smi_photo = Image.open("assets/smi_tools.png")
    img_b64 = get_image_base64(smi_photo, "PNG")

    st.markdown(
            f"""
            <a href="/smi_3dp" target="_self">
                <img src="data:image/jpeg;base64,{img_b64}" class="project-thumbnail">
            </a>
            """,
            unsafe_allow_html=True
        )
    st.space("small")
    st.write(" 🏎️ SMI Composites Process Improvement 🛩️ ")
    st.space("small")

with colmain3:
    
    assy_photo = Image.open("assets/assy_line.jpeg")
    img_b64 = get_image_base64(assy_photo, "JPEG")

    st.markdown(
            f"""
            <a href="/assy_line" target="_self">
                <img src="data:image/jpeg;base64,{img_b64}" class="project-thumbnail">
            </a>
            """,
            unsafe_allow_html=True
        )
    st.space("small")
    st.write(" 🛠️ Cyber-Physical Assembly Line 🛠️ ")
    st.space("small")

with colmain4:
    
    scout_photo = Image.open("assets/scout.jpeg")
    img_b64 = get_image_base64(scout_photo, "JPEG")

    st.markdown(
            f"""
            <a href="/scout" target="_self">
                <img src="data:image/jpeg;base64,{img_b64}" class="project-thumbnail">
            </a>
            """,
            unsafe_allow_html=True
        )
    st.space("small")
    st.write(" 🐶 SCOUT: RFID Robot Dog 🐶 ")
    st.space("small")

## PUBLICATIONS
st.space("medium")
st.markdown("# 📖 Publications")
st.space("small")
st.link_button("Framework for LLM applications in manufacturing", "https://www.sciencedirect.com/science/article/pii/S2213846324000920")
st.link_button("SCOUT: an autonomous UHF RFID-equipped robot dog for flexible inventory monitoring", "https://www.sciencedirect.com/science/article/pii/S2213846325002081")

## ORGANIZATIONS

st.space("medium")
st.markdown("# 📢 Organizations")
colorg1, colorg2, colorg3, colorg4 = st.columns(4)
with colorg1:
    
    st.link_button("Engineers without Borders, UGA Chapter\nCo-founder & Vice President", "https://www.instagram.com/ewb.uga/?hl=en")
with colorg2:
    st.link_button("Manufacturing Club\nFounder & Graduate Advisor", "https://www.instagram.com/uga.mfg/?hl=en")
with colorg3:
    st.link_button("Create Engineering @\nFounder & Lead Engineer", "https://create.uga.edu/about/")
with colorg4:
    st.link_button("UGA Aviation Club\nVice President", "https://ugaaviationclub.com/")

## PERSONAL PROJECTS
st.space("medium")
st.markdown("# 🪚 Personal Projects")
