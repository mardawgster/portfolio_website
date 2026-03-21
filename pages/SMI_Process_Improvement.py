import streamlit as st
from PIL import Image

# Page Config
st.set_page_config(page_title="SMI Composites Tooling Improvement", layout="wide")

# --- HEADER SECTION ---
col1head, col2head = st.columns([10, 1])
with col1head:
    st.title("SMI Composites Tooling Improvement")

with col2head:
    st.page_link("streamlit_app.py", label="Home 🏠")

# --- PROJECT: FRUIT SORTING VIGNETTE ---

col1main1, col2main1 = st.columns([1, 2])

with col1main1:
    st.write("**Tech Stack:**")
    st.code("CAD: Fusion 360\n FDM AM: Carbon Fiber Infused Nylon PA12,\nPETG, PLA\n SLA AM: Rigid 10k Resin")
    # with open("assets/vignette_docs.pdf", "rb") as file:
    #     st.download_button("Download Full Documentation", data=file, mime="application/pdf")
    vig_photo = Image.open("assets/smi_tools.png")
    st.image(vig_photo, caption="3D Printed Tab Covers (TOP), Slot & Pin Gauges (MID LEFT), Autoclave Mounts (MID RIGHT), Dibber Tools (BOTTOM) .")



with col2main1:
    st.markdown("""
    ### Process Improvement for Composites Tooling using Additive Manufacturing
    This project demonstrates the design and development of a custom additive manufacturing system for tooling improvement in composites manufacturing, with a focus on the design, fabrication, and testing of 3D-printed solutions for common challenges in composites tooling manufacturing.
    
    **Key Engineering Achievements:**
    * **Custom Autoclave-Compatible Mounts:** Designed and 3D-printed (FDM) custom mounts for autoclave curing of composite parts, improving the quality and consistency of the curing process while reducing costs and lead times.
    * **Paint Tabs:** Developed 3D-printed (FDM) paint tabs for composite parts, covering crictial dimensions and features to ensure accurate paint application and reduce the need for manual masking, improving efficiency and quality in the painting process.
    * **Ergonomic Dibber Tools:** Created custom 3D-printed (FDM) dibber tools for composite layup, designed with ergonomic features to improve operator comfort and reduce fatigue during the layup process, while also improving the precision and consistency of the layup.
    * **Slot Gauges:** Designed and fabricated 3D-printed (SLA) slot & pin gauges for quality control in composites manufacturing, enabling quick and accurate measurement of critical dimensions and features on composite parts, improving quality assurance.
                """)
    
    # Demo Video
    st.video("assets/smi_vid.mp4") 

# --- SKILLS & RESEARCH ---
st.divider()
st.header("Core Competencies")
st.write("- **Hardware:** 3D Printing Bambu, Prusa, and Formlabs (FDM & SLA), CAD Design, Composites Manufacturing")
st.write("- **Software:** Fusion 360, PrusaSlicer, BambuStudio, PreForm")