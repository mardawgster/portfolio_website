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
    
    /* Header Social Icons */
    .social-dock {
        display: flex;
        justify-content: flex-start;
        gap: 15px;
        margin-top: 10px;
    }

    .social-icon {
        width: 35px !important;
        height: 35px !important;
        transition: transform 0.3s ease, filter 0.3s ease;
        filter: grayscale(100%) brightness(0.8); /* Muted look until hover */
    }

    .social-icon:hover {
        transform: translateY(-5px) scale(1.1);
        filter: grayscale(0%) brightness(1.2); /* Pops into color on hover */
        cursor: pointer;
    }

    /* Styling for the Name and Subheader */
    .header-name {
        font-size: 2.8em;
        font-weight: 800;
        margin-bottom: 0px;
        color: #fafafa;
    }

    .header-sub {
        color: #ba0c2f; /* UGA Red */
        font-weight: 500;
        font-size: 1.3em;
        margin-bottom: 15px;
    }
    /* Main container to ensure all experience elements align */
    .experience-container {
        display: flex;
        flex-direction: column;
        align-items: center; /* Centers the cards on the page */
        width: 100%;
    }

/* Style the Streamlit Expander to match your tech theme */
    .streamlit-expanderHeader {
        background-color: #1f2937 !important;
        color: #ba0c2f !important; /* UGA Red for the Title */
        font-weight: bold !important;
        font-size: 1.2em !important;
        border-radius: 8px !important;
    }

    .streamlit-expanderContent {
        background-color: #111827 !important; /* Darker interior */
        color: #d1d5db !important;
        border-radius: 0 0 8px 8px !important;
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

def render_experience(role, company, date, description_bullets):
    bullets_html = "".join([f"<li>{bullet}</li>" for bullet in description_bullets])
    
    exp_html = f"""
    <div class="exp-card">
        <div class="exp-header">
            <div style="color: #ba0c2f; font-size: 1.4em; font-weight: bold;">{role}</div>
            <div style="color: #9ca3af; font-size: 0.9em; font-style: italic; min-width: 150px; text-align: right;">{date}</div>
        </div>
        <div style="color: #fafafa; font-size: 1.1em; font-weight: 500; margin-top: 5px;">{company}</div>
        <ul style="color: #d1d5db; font-size: 0.95em; line-height: 1.6; margin-top: 15px; padding-left: 20px;">
            {bullets_html}
        </ul>
    </div>
    """
    st.markdown(exp_html, unsafe_allow_html=True)

# --- HEADER SECTION ---

# Use the same base64 trick if you want the headshot to have the hover flare
img = Image.open("assets/Headshot.png")
headshot_b64 = get_image_base64(img, "PNG")
st.markdown(f'<img src="data:image/png;base64,{headshot_b64}" class="project-thumbnail" style="width:160px; border-radius:50%; border: 2px solid #ba0c2f;">', unsafe_allow_html=True)

st.markdown('<div class="header-name">Marcus DiBattista</div>', unsafe_allow_html=True)
st.markdown('<div class="header-sub">PhD Candidate & Manufacturing Technologist | Mechanical Engineering @ UGA</div>', unsafe_allow_html=True)

# Define your social links and their local logo paths
socials = [
    ("https://www.linkedin.com/in/marcusdibattista/", "assets/linkedin.png"),
    ("https://scholar.google.com/citations?user=ixBhetgAAAAJ", "assets/scholar.png"),
    ("https://www.thingiverse.com/MADmarcus/designs", "assets/thingiverse.png"),
    ("https://www.youtube.com/@MarcusDiBattista", "assets/youtube.png")
]

# Build the social dock HTML
social_html = '<div class="social-dock">'
for link, logo_path in socials:
    try:
        logo_img = Image.open(logo_path)
        logo_b64 = get_image_base64(logo_img, "PNG")
        social_html += f'<a href="{link}" target="_blank"><img src="data:image/png;base64,{logo_b64}" class="social-icon"></a>'
    except:
        continue # Skip if logo missing
social_html += '</div>'
st.markdown(social_html, unsafe_allow_html=True)
st.space("medium")

# --- PROFESSIONAL PROJECTS SECTION ---

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

# --- WORK EXPERIENCE ---
st.markdown("---")
st.markdown("# 💼 Work Experience")
st.space("small")

# 1. Graduate Research & Teaching Assistant
with st.expander("🎓  Graduate Research & Teaching Assistant | UGA College of Engineering| 2023-Present", expanded=True):
    st.markdown("### UGA College of Engineering")
    st.write("- Developed Automated AI Computer Vision Fruit Sorting system for Georgia AI in Manufacturing Project. [cite: 26]")
    st.write("- Directed team for Hardware & Software integration of Innovation Factory Cyber-Physical Assembly Testbed. [cite: 26]")
    st.write("- Supervised capstone projects for MiR200/UR-10 integration and process improvements at SMI Composites. [cite: 26]")

# 2. Director - UGA Create Labs
with st.expander("🛠️  Director | UGA Create Labs | 2022-2024"):
    st.markdown("### UGA Create Labs")
    st.write("- Managed a $50,000 Lab buildout for Create Labs to increase prototyping and manufacturing capabilities. [cite: 30]")
    st.write("- Led successful project to design mechanism for collection of water samples from a UAV. [cite: 30]")
    st.write("- Recruited, onboarded, and trained 8 additional members to add diverse capabilities to the lab. [cite: 30]")

# 3. Lab Manager - Innovation Factory
with st.expander("🏭  Lab Manager | UGA Innovation Factory | 2022-2023"):
    st.markdown("### UGA Innovation Factory")
    st.write("- Responsible for facility activities, including recruitment, hiring, and project management. [cite: 33]")
    st.write("- Advised projects involving robotics, computer vision, additive manufacturing, and industrial IOT. [cite: 33]")
    st.write("- Successfully led project to upgrade assembly line to increase data collection capabilities. [cite: 33]")

# 4. Manufacturing Engineering Intern
with st.expander("⚙️  Manufacturing Engineering Intern | Price Industries | 2022"):
    st.markdown("### Price Industries")
    st.write("- Performed process analysis for multiple products and created assembly process reports. [cite: 35]")
    st.write("- Performed logistics efficiency study aimed to improve product tracking throughout the assembly process. [cite: 37]")

# 5. Lead Project Management Co-op
with st.expander("📋  Lead Project Management Co-op | McKenney's Inc. | 2020-2021"):
    st.markdown("### McKenney's Inc.")
    st.write("- Assisted management with a $500,000 equipment installation in an active retail center. [cite: 40]")
    st.write("- Designed a system that organized maintenance reports for the company's largest service account. [cite: 40]")
    st.write("- Led the department's intern team, delegating tasks and training interns as needed. [cite: 40]")

## PERSONAL PROJECTS
st.space("medium")
st.markdown("# 🪚 Personal Projects")
