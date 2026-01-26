import streamlit as st
from PIL import Image
import base64
import os
import io

# Page Config (Must be first)
st.set_page_config(page_title="Home", layout="wide")

## CSS
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
    
    .org-icon {
        width: 100px !important;
        height: 100px !important;
        object-fit: contain;
        margin-bottom: 10px;
    }
    .org-title {
        font-weight: bold;
        font-size: 1.1em;
        line-height: 1.2;
        color: #ba0c2f; /* Red titles */
        margin-top: 10px;
    }

    .org-subtitle {
        font-size: 0.9em;
        color: #d9d9d9; /* Muted grey for subtitles */
        margin-top: 5px;
    }
            
    /* Publication Card Styling */
    .pub-card {
        background-color: #1f2937; /* Matches secondary tech background */
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #374151;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        text-decoration: none !important;
        display: block;
    }

    .pub-card:hover {
        border-left: 5px solid #ba0c2f; /* Red accent on hover */
        background-color: #2d3748;
        transform: translateX(10px); /* Subtle slide effect */
    }

    .pub-title {
        color: #fafafa;
        font-weight: bold;
        font-size: 1.15em;
        margin-bottom: 5px;
    }

    .pub-journal {
        color: #9ca3af;
        font-style: italic;
        font-size: 0.9em;
    }

    .pub-badge {
        display: inline-block;
        background-color: rgba(186, 12, 47, 0.1);
        color: #ba0c2f;
        padding: 2px 10px;
        border-radius: 20px;
        border: 1px solid #ba0c2f;
        font-size: 0.8em;
        margin-top: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

## IMG TO BASE64 HELPER
def get_image_base64(pil_img, img_format):
    buffer = io.BytesIO()
    # Handle both JPEG and PNG
    pil_img.save(buffer, format=img_format)
    return base64.b64encode(buffer.getvalue()).decode()

def render_org_card(img_path, title, subtitle, link):
    """Helper to process image and render the organization card"""
    try:
        # Determine format based on extension
        ext = os.path.splitext(img_path)[1].lower()
        fmt = "PNG" if ext == ".png" else "JPEG"
        
        img = Image.open(img_path)
        b64 = get_image_base64(img, fmt)
        
        html = f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <a href="{link}" target="_blank" style="text-decoration: none; color: inherit;">
                <img src="data:image/{fmt.lower()};base64,{b64}" class="project-thumbnail org-icon">
                <div class="org-title">{title}</div>
                <div class="org-subtitle">{subtitle}</div>
            </a>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading {img_path}")

def render_publication(title, journal, link):
    pub_html = f"""
    <a href="{link}" target="_blank" class="pub-card">
        <div class="pub-title">{title}</div>
        <div class="pub-journal">Published in: {journal}</div>
        <div class="pub-badge">View Full Paper →</div>
    </a>
    """
    st.markdown(pub_html, unsafe_allow_html=True)

# --- HEADER SECTION ---
col1head, col2head, col3head = st.columns([1, 5, 1])
with col1head:
    st.image("assets/Headshot.png", width=150)
with col2head:
    st.title("Marcus DiBattista, PhD Candidate")
    st.subheader("Mechanical Engineering @ University of Georgia")
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
st.markdown("---")
st.markdown("# 📖 Publications")
st.write("Click on a paper to view the full publication.")

render_publication(
    "Framework for LLM applications in manufacturing", 
    "Manufacturing Letters / 52nd SME North American Manufacturing Research Conference", 
    "https://www.sciencedirect.com/science/article/pii/S2213846324000920"
)

render_publication(
    "SCOUT: an autonomous UHF RFID-equipped robot dog for flexible inventory monitoring", 
    "Manufacturing Letters / 53rd SME North American Manufacturing Research Conference",
    "https://www.sciencedirect.com/science/article/pii/S2213846325002081"
)
## ORGANIZATIONS

def organization_card(image_path, title, subtitle, link):
    """Renders a centered, clickable card for organizations."""
    card_html = f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <a href="{link}" target="_blank" style="text-decoration: none; color: inherit;">
            <img src="{image_path}" style="width: 80px; height: 80px; object-fit: contain; margin-bottom: 10px; border-radius: 10px;">
            <div style="font-weight: bold; font-size: 1.1em; line-height: 1.2; color: #ba0c2f;">{title}</div>
            <div style="font-size: 0.9em; color: #555; margin-top: 5px;">{subtitle}</div>
        </a>
    </div>
    """
    return st.markdown(card_html, unsafe_allow_html=True)

st.write("---")
st.markdown("# 📢 Organizations")
st.space("small")

colorg1, colorg2, colorg3, colorg4 = st.columns(4)

with colorg1:
    render_org_card("assets/ewbUga.jpg", "Engineers Without Borders @ UGA", "Co-founder & Vice President", "https://www.instagram.com/ewb.uga/")
with colorg2:
    render_org_card("assets/ugaMfg.png", "UGA Manufacturing Club", "Founder & Graduate Advisor", "https://www.instagram.com/uga.mfg/")
with colorg3:
    render_org_card("assets/create.png", "Create Engineering", "Founder & Chief Engineer", "https://create.uga.edu/about/")
with colorg4:
    render_org_card("assets/aviation.png", "UGA Aviation Club", "Vice President", "https://ugaaviationclub.com/")

## PERSONAL PROJECTS
st.space("medium")
st.markdown("# 🪚 Personal Projects")
