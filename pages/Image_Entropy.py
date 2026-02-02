import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import graycomatrix, graycoprops
from skimage.measure import shannon_entropy
import tempfile

st.set_page_config(page_title="Video Texture Analyzer", layout="wide")

st.title("🎬 Haralick Feature Extractor")
st.markdown("""
Upload a video to analyze texture complexity (Entropy) and local variation (Contrast) over time. 
*Note: Processing every frame can be slow for long videos.*
""")

# Sidebar settings
st.sidebar.header("Settings")
skip_frames = st.sidebar.slider("Analyze every Nth frame", 1, 30, 5)
glcm_distance = st.sidebar.slider("GLCM Distance", 1, 10, 5)

uploaded_file = st.file_with_container = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Save uploaded file to a temporary location
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    st.info(f"Video loaded: {total_frames} total frames at {fps:.2f} FPS")

    entropy_values = []
    contrast_values = []
    timestamps = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Analyze only every Nth frame to save time
        if frame_count % skip_frames == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Haralick Calculations
            glcm = graycomatrix(gray, distances=[glcm_distance], angles=[0], 
                                levels=256, symmetric=True, normed=True)
            
            contrast = graycoprops(glcm, 'contrast')[0, 0]
            entropy = shannon_entropy(gray)
            
            entropy_values.append(entropy)
            contrast_values.append(contrast)
            timestamps.append(frame_count / fps)
            
            # Update Progress
            progress = frame_count / total_frames
            progress_bar.progress(progress)
            status_text.text(f"Processing frame {frame_count}/{total_frames}...")

        frame_count += 1

    cap.release()
    progress_bar.empty()
    status_text.success("Analysis Complete!")

    # --- Plotting ---
    fig, ax1 = plt.subplots(figsize=(10, 5))

    color_ent = 'tab:blue'
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Shannon Entropy', color=color_ent)
    ax1.plot(timestamps, entropy_values, color=color_ent, linewidth=2, label='Entropy')
    ax1.tick_params(axis='y', labelcolor=color_ent)

    ax2 = ax1.twinx()
    color_cont = 'tab:red'
    ax2.set_ylabel('Contrast', color=color_cont)
    ax2.plot(timestamps, contrast_values, color=color_cont, linestyle='--', alpha=0.7, label='Contrast')
    ax2.tick_params(axis='y', labelcolor=color_cont)

    plt.title('Texture Features Over Time')
    st.pyplot(fig)

    # Display raw data option
    if st.checkbox("Show raw data table"):
        st.write(np.array([timestamps, entropy_values, contrast_values]).T)