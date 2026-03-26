import streamlit as st

def Navbar():
    with st.sidebar:
        st.page_link('streamlit_app.py', label='Home', icon='🏠')
        #st.page_link('pages/Additive_Manufacturing_Demo.py', label='Additive Manufacturing Demo', icon='🖨️')
        st.page_link('pages/Assembly_Line.py', label='Cyber-Physical Assembly Line', icon='🛠️')
        st.page_link('pages/Lemon_Sorter.py', label='Automated Lemon Sorter', icon='🍋')
        st.page_link('pages/SCOUT_Robot_Dog.py', label='SCOUT Robot Dog', icon='🐶')
        st.page_link('pages/Image_Entropy.py', label='Video Entropy Analyzer', icon='🎬')
        #st.page_link('pages/Assembly_Artifact.py', label='Manual Assembly Artifact', icon='⚙️')
        st.page_link('pages/SMI_Process_Improvement.py', label='SMI Process Improvement', icon='📈')
        st.page_link('pages/EntropyV3.py', label='EntropyV3', icon='📊')
