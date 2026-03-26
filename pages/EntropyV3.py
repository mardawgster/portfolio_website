import streamlit as st
import cv2
import numpy as np
import plotly.graph_objects as go
from scipy.stats import entropy
import pandas as pd

# --- Page Config & Styling ---
st.set_page_config(layout="wide", page_title="Entropy Assembly Lab")

# --- Custom Entropy Functions ---
def calculate_shannon(hist):
    return entropy(hist, base=2)

def calculate_renyi(hist, alpha):
    if alpha == 1: return calculate_shannon(hist)
    return (1 / (1 - alpha)) * np.log2(np.sum(hist**alpha) + 1e-10)

def calculate_tsallis(hist, q):
    if q == 1: return calculate_shannon(hist)
    return (1 / (q - 1)) * (1 - np.sum(hist**q))

def process_video(file_path, n_frame, alpha, q, mask_params):
    cap = cv2.VideoCapture(file_path)
    data = []
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        if frame_count % n_frame == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply Spatial Mask (Weighting)
            # x, y, w, h from mask_params
            x, y, w, h = mask_params
            roi = gray[y:y+h, x:x+w]
            
            # Generate normalized histogram
            hist = cv2.calcHist([roi], [0], None, [256], [0, 256]).flatten()
            hist = hist / (hist.sum() + 1e-10)
            
            data.append({
                "Frame": frame_count,
                "Time": frame_count / cap.get(cv2.CAP_PROP_FPS),
                "Shannon": calculate_shannon(hist),
                "Renyi": calculate_renyi(hist, alpha),
                "Tsallis": calculate_tsallis(hist, q)
            })
        frame_count += 1
    cap.release()
    return pd.DataFrame(data)

# --- Sidebar Controls ---
st.sidebar.header("🔬 Research Parameters")

uploaded_files = st.sidebar.file_uploader("Upload Assembly Videos", type=['mp4', 'mov', 'avi'], accept_multiple_files=True)

sampling_n = st.sidebar.select_slider(
    "Temporal Resolution (Analyze every nth frame)", 
    options=[1, 2, 5, 10, 30, 60], 
    value=5
)

st.sidebar.subheader("Algorithm Settings")
renyi_alpha = st.sidebar.slider("Rényi Alpha (α)", 0.1, 5.0, 2.0)
tsallis_q = st.sidebar.slider("Tsallis q", 0.1, 5.0, 2.0)

st.sidebar.subheader("Spatial Mask (ROI)")
# In a real app, these could be drawn on a canvas, here we use sliders for the rectangle
col_m1, col_m2 = st.sidebar.columns(2)
m_x = col_m1.number_input("X Offset", 0, 1000, 0)
m_y = col_m2.number_input("Y Offset", 0, 1000, 0)
m_w = col_m1.number_input("Width", 10, 2000, 500)
m_h = col_m2.number_input("Height", 10, 2000, 500)

# --- Main Interface ---
st.title("Visual Entropy: Comparative Analysis")

if uploaded_files:
    # We use a dict to store dataframes for comparison
    comparison_data = {}
    
    with st.status("Processing videos...", expanded=True) as status:
        for uploaded_file in uploaded_files:
            # Save temp file for OpenCV
            tfile = f"temp_{uploaded_file.name}"
            with open(tfile, "wb") as f:
                f.write(uploaded_file.read())
            
            st.write(f"Analyzing {uploaded_file.name}...")
            df = process_video(tfile, sampling_n, renyi_alpha, tsallis_q, (m_x, m_y, m_w, m_h))
            comparison_data[uploaded_file.name] = df
        status.update(label="Analysis Complete!", state="complete")

    # --- Visualization ---
    metric_to_plot = st.selectbox("Select Entropy Metric to Compare", ["Shannon", "Renyi", "Tsallis"])
    
    fig = go.Figure()
    for name, df in comparison_data.items():
        fig.add_trace(go.Scatter(
            x=df['Time'], 
            y=df[metric_to_plot], 
            mode='lines', 
            name=name,
            hovertemplate="Time: %{x:.2f}s<br>Entropy: %{y:.4f}"
        ))

    fig.update_layout(
        title=f"Comparative {metric_to_plot} Entropy Streams",
        xaxis_title="Time (seconds)",
        yaxis_title="Information Bits / Units",
        template="plotly_white",
        height=600,
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Data Export ---
    if st.button("Export Combined Data to CSV"):
        # Logic to merge dataframes and download
        st.write("Generating export...")

else:
    st.info("Please upload one or more videos in the sidebar to begin the entropy comparison.")