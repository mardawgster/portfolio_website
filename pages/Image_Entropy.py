import streamlit as st
import cv2
import numpy as np
import tempfile
import plotly.graph_objects as go
from scipy.stats import entropy
import EntropyHub as EH
from modules.nav import Navbar

st.set_page_config(page_title="Visual Entropy Video Analyzer", layout="wide")
st.title("Multidimensional Visual Entropy Video Analyzer")

st.write("""This tool is a part of an ongoing research project, allowing users to upload a video of an assembly process and analyzes the visual complexity of each frame to identify signatures of key events such as part placements, handoffs, and errors. By calculating multiple entropy measures, including Shannon, Tsallis, Renyi, and spatial entropies, the tool provides a comprehensive view of the visual information dynamics throughout the assembly process. The interactive player and synchronized charts enable users to explore the temporal evolution of visual complexity and correlate it with specific moments in the video, offering insights into operator behavior and assembly dynamics.""")

Navbar()

# 1. Accept uploaded video
uploaded_video = st.file_uploader("Upload an assembly video", type=["mp4", "mov", "avi"])

if uploaded_video is not None:
    # 2. Save to temporary file so OpenCV can read the datastream
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_video.read())
    
    cap = cv2.VideoCapture(tfile.name)
    
    # Correctly initialize empty lists to store time-series data
    frames = []
    shannon_entropies = []
    tsallis_entropies = []
    renyi_entropies = []
    spatial_entropies = []
    
    st.write("Processing video datastream... please wait. (This may take a moment for advanced spatial entropies)")
    progress_bar = st.progress(0.0)
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    current_frame = 0
    
    # Non-extensive parameters for generalized entropies
    q = 2.0 # Tsallis parameter
    alpha = 2.0 # Renyi parameter
    
    # 3. Process video datastream frame-by-frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert to grayscale and resize for performance limits (128x128 max for EntropyHub)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_small = cv2.resize(gray, (64, 64)) 
        
        # Store original color frame for playback display
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Calculate Probability Distribution for 1D Entropies
        hist, _ = np.histogram(gray_small.ravel(), bins=256, range=(0, 256))
        prob_dist = hist / (hist.sum() + 1e-7)
        prob_dist = prob_dist[prob_dist > 0] # Filter out zero probabilities
        
        # A. Shannon Entropy
        shannon = entropy(prob_dist, base=2)
        shannon_entropies.append(shannon)
        
        # B. Tsallis Entropy
        tsallis = (1 / (q - 1)) * (1 - np.sum(prob_dist ** q))
        tsallis_entropies.append(tsallis)
        
        # C. Renyi Entropy
        renyi = (1 / (1 - alpha)) * np.log2(np.sum(prob_dist ** alpha))
        renyi_entropies.append(renyi)
        
        # D. Bidimensional Dispersion Entropy (Spatial) via EntropyHub
        disp2d, _ = EH.DispEn2D(gray_small, m=2, tau=1, c=3, Lock=True)
        spatial_entropies.append(disp2d)
        
        current_frame += 1
        if total_frames > 0:
            progress_bar.progress(min(current_frame / total_frames, 1.0))
            
    cap.release()
    st.success("Processing complete!")
    
    # 4. Interactive synchronized player and chart
    time_idx = np.arange(len(frames))
    
    # Slider to scrub through the video and sync with the chart
    frame_idx = st.slider("Scrub through video timeline:", min_value=0, max_value=len(frames)-1, value=0, step=1)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("**Video Player (Current Frame)**")
        st.image(frames[frame_idx], use_container_width=True)
        
    with col2:
        st.write("**Entropy Time-Series Signatures**")
        fig = go.Figure()
        
        # Plot all processed data streams
        fig.add_trace(go.Scatter(x=time_idx, y=shannon_entropies, mode='lines', name='Shannon (Global)'))
        fig.add_trace(go.Scatter(x=time_idx, y=tsallis_entropies, mode='lines', name='Tsallis (Tunable)'))
        fig.add_trace(go.Scatter(x=time_idx, y=renyi_entropies, mode='lines', name='Renyi (Tunable)'))
        fig.add_trace(go.Scatter(x=time_idx, y=spatial_entropies, mode='lines', name='DispEn2D (Spatial)'))
        
        # Add vertical line to sync with the current frame
        fig.add_vline(x=frame_idx, line_width=2, line_color="red", line_dash="dash")
        
        fig.update_layout(
            xaxis_title="Frame Index",
            yaxis_title="Entropy Value",
            margin=dict(l=0, r=0, t=30, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)