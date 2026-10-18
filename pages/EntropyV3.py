import streamlit as st
import cv2
import numpy as np
import plotly.graph_objects as go
from scipy.stats import entropy
import pandas as pd
import tempfile
import os
from pathlib import Path

# --- Page Config & Styling ---
st.set_page_config(layout="wide", page_title="Entropy Assembly Lab")

# Initialize session state for caching
if 'processed_videos' not in st.session_state:
    st.session_state.processed_videos = {}
if 'video_files' not in st.session_state:
    st.session_state.video_files = {}
if 'current_time' not in st.session_state:
    st.session_state.current_time = 0
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False
if 'hidden_traces' not in st.session_state:
    st.session_state.hidden_traces = set()

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
    """Process video with optimized frame extraction"""
    cap = cv2.VideoCapture(file_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps > 0 else 0
    
    if total_frames == 0 or fps == 0:
        cap.release()
        return pd.DataFrame(), fps, duration
    
    # Calculate frames to process
    frames_to_process = list(range(0, total_frames, n_frame))
    
    # Limit to max 500 frames for performance
    if len(frames_to_process) > 500:
        step = len(frames_to_process) // 500
        frames_to_process = frames_to_process[::step]
    
    cap.release()
    
    data = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Sequential processing with progress updates (more stable)
        for idx, frame_num in enumerate(frames_to_process):
            try:
                cap = cv2.VideoCapture(file_path)
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret, frame = cap.read()
                cap.release()
                
                if not ret:
                    continue
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                x, y, w, h = mask_params
                roi = gray[y:y+h, x:x+w]
                
                hist = cv2.calcHist([roi], [0], None, [256], [0, 256]).flatten()
                hist = hist / (hist.sum() + 1e-10)
                
                data.append({
                    "Frame": frame_num,
                    "Time": frame_num / fps,
                    "Shannon": calculate_shannon(hist),
                    "Renyi": calculate_renyi(hist, alpha),
                    "Tsallis": calculate_tsallis(hist, q)
                })
            except Exception as e:
                continue
            
            # Update progress every 5 frames
            if idx % 5 == 0:
                progress = (idx + 1) / len(frames_to_process)
                progress_bar.progress(min(progress, 0.99))
                status_text.text(f"Extracting frames: {idx + 1}/{len(frames_to_process)}")
        
        progress_bar.progress(1.0)
        status_text.text("✓ Extraction complete")
        
    finally:
        progress_bar.empty()
        status_text.empty()
    
    return pd.DataFrame(data), fps, duration

# --- Sidebar Controls ---
st.sidebar.header("🔬 Research Parameters")

uploaded_files = st.sidebar.file_uploader("Upload Assembly Videos", type=['mp4', 'mov', 'avi'], accept_multiple_files=True)

sampling_n = st.sidebar.select_slider(
    "Temporal Resolution (Analyze every nth frame)", 
    options=[1, 2, 5, 10, 30, 60], 
    value=10
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

# --- Main Interface ---
st.title("Visual Entropy: Comparative Analysis")

if uploaded_files:
    # Preload and cache all videos
    st.subheader("📊 Pre-loading Videos...")
    
    for uploaded_file in uploaded_files:
        file_key = uploaded_file.name
        
        # Check if already processed (cached)
        if file_key not in st.session_state.processed_videos:
            # Save temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                tmp.write(uploaded_file.read())
                tfile = tmp.name
            
            st.session_state.video_files[file_key] = tfile
            
            try:
                st.write(f"🎬 Processing {uploaded_file.name}...")
                df, fps, duration = process_video(tfile, sampling_n, renyi_alpha, tsallis_q, (m_x, m_y, m_w, m_h))
                st.session_state.processed_videos[file_key] = {
                    'data': df,
                    'fps': fps,
                    'duration': duration,
                    'file_path': tfile
                }
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")
    
    if st.session_state.processed_videos:
        st.success(f"✓ Loaded {len(st.session_state.processed_videos)} video(s)")
        
        # --- Video Selection & Settings ---
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_video = st.selectbox(
                "Select video to preview",
                list(st.session_state.processed_videos.keys())
            )
        
        with col2:
            metric_to_plot = st.selectbox("Entropy Metric", ["Shannon", "Renyi", "Tsallis"])
        
        # --- Video Player & Scrubber ---
        video_info = st.session_state.processed_videos[selected_video]
        df = video_info['data']
        duration = video_info['duration']
        file_path = video_info['file_path']
        fps = video_info['fps']
        
        # Display video player (smaller - 50% width)
        col_video, col_spacer = st.columns([1, 1])
        with col_video:
            st.subheader("📹 Video Preview")
            if os.path.exists(file_path):
                st.video(file_path, start_time=int(st.session_state.current_time))
        
        # Time scrubber below video
        current_time = st.slider(
            "Time Position",
            0.0,
            duration,
            st.session_state.current_time,
            0.01,
            key="video_scrubber",
            format="%.2f s"
        )
        st.session_state.current_time = current_time
        
        # Play/Pause controls
        col_play, col_time_display = st.columns([1, 3])
        with col_play:
            if st.button("▶️ Play Auto-Update", help="Auto-sync graph with playback (updates every 0.5s)"):
                st.session_state.is_playing = not st.session_state.is_playing
        
        with col_time_display:
            status = "🔴 Playing" if st.session_state.is_playing else "⏸️ Paused"
            st.metric("Status", f"{status} | {current_time:.2f}s / {duration:.2f}s")
        
        # --- Comparison Graph with Current Time Indicator ---
        st.subheader("📊 Entropy Analysis")
        
        # Get frame range for consistent visualization
        # Snap to nearest frame in data
        time_range = df['Time'].max() - df['Time'].min()
        visible_range = min(time_range, 60)  # Show up to 60 seconds at a time
        start_time = max(0, current_time - visible_range / 4)
        end_time = min(duration, start_time + visible_range)
        
        fig = go.Figure()
        
        # Add traces for all videos (respect hidden state)
        for name, video_data in st.session_state.processed_videos.items():
            data_df = video_data['data']
            is_hidden = name in st.session_state.hidden_traces
            fig.add_trace(go.Scatter(
                x=data_df['Time'],
                y=data_df[metric_to_plot],
                mode='lines',
                name=name,
                visible=(not is_hidden),
                hovertemplate="Time: %{x:.2f}s<br>Entropy: %{y:.4f}"
            ))
        
        # Add vertical line at current time
        fig.add_vline(
            x=current_time,
            line_dash="dash",
            line_color="red",
            line_width=2,
            annotation_text=f"Now: {current_time:.2f}s",
            annotation_position="top right"
        )
        
        fig.update_xaxes(range=[start_time, end_time])
        fig.update_layout(
            title=f"Comparative {metric_to_plot} Entropy Streams",
            xaxis_title="Time (seconds)",
            yaxis_title="Information Bits / Units",
            template="plotly_white",
            height=500,
            hovermode="x unified"
        )
        
        # Display graph and capture visibility state
        st.plotly_chart(fig, use_container_width=True, key=f"entropy_graph_{selected_video}")
        
        # Auto-update loop for playback
        if st.session_state.is_playing:
            import time
            time.sleep(0.5)
            new_time = current_time + 0.5
            if new_time < duration:
                st.session_state.current_time = new_time
            else:
                st.session_state.is_playing = False
                st.session_state.current_time = 0
            st.rerun()
        
        # --- Data Export ---
        st.subheader("📥 Data Export")
        if st.button("Export Combined Data to CSV"):
            combined_data = []
            for name, video_data in st.session_state.processed_videos.items():
                data_df = video_data['data'].copy()
                data_df['Video'] = name
                combined_data.append(data_df)
            
            export_df = pd.concat(combined_data, ignore_index=True)
            csv = export_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="entropy_analysis.csv",
                mime="text/csv"
            )

else:
    st.info("Please upload one or more videos in the sidebar to begin the entropy comparison.")