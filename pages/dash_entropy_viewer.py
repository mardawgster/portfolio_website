import argparse
import base64
import io
from functools import lru_cache
from pathlib import Path # <-- add this

import cv2
import numpy as np
import pandas as pd
import pywt
from dash import Dash, dcc, html, Input, Output, State, no_update
import plotly.graph_objects as go


# ------------------------
# Entropy definition
# ------------------------
def shannon_entropy_from_energies(energies: np.ndarray, eps: float = 1e-12) -> float:
    energies = energies.astype(np.float64, copy=False)
    total = float(np.sum(energies))
    if not np.isfinite(total) or total <= eps:
        return 0.0
    p = energies / total
    p = p[p > eps]
    if p.size == 0:
        return 0.0
    return float(-(p * np.log2(p)).sum())


def frame_entropy_coeff_energy(gray: np.ndarray, wavelet: str = "db2", level: int = 1) -> float:
    """
    ONE entropy per frame:
    wavelet coeffs -> energy per coeff (coeff^2) across ALL subbands -> normalize -> Shannon entropy (base-2).
    """
    img = gray.astype(np.float32, copy=False)
    coeffs = pywt.wavedec2(img, wavelet=wavelet, level=level)

    energies = []
    cA = coeffs[0]
    energies.append((cA * cA).ravel())
    for (cH, cV, cD) in coeffs[1:]:
        energies.append((cH * cH).ravel())
        energies.append((cV * cV).ravel())
        energies.append((cD * cD).ravel())

    all_energies = np.concatenate(energies)
    return shannon_entropy_from_energies(all_energies)


def compute_entropy_series(video_path: str, step_s: float, wavelet: str, level: int, max_seconds: float | None):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        cap.release()
        raise RuntimeError(f"Could not open video: {video_path}")

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    frame_count = float(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0.0)
    duration_s = (frame_count / fps) if (fps > 0 and frame_count > 0) else None

    if duration_s is not None:
        duration = duration_s if max_seconds is None else min(duration_s, max_seconds)
        times = np.arange(0.0, duration + 1e-9, step_s, dtype=float)
    else:
        # unknown duration: sample until read fails
        times = []
        t = 0.0
        for _ in range(10_000_000):
            times.append(t)
            t += step_s
        times = np.array(times, dtype=float)

    rows = []
    for t in times:
        cap.set(cv2.CAP_PROP_POS_MSEC, float(t) * 1000.0)
        ok, frame = cap.read()
        if not ok or frame is None:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ent = frame_entropy_coeff_energy(gray, wavelet=wavelet, level=level)
        rows.append((float(t), float(ent)))

    cap.release()

    if not rows:
        raise RuntimeError("No frames processed. Try converting the video to MP4 (H.264).")

    df = pd.DataFrame(rows, columns=["time_s", "entropy"])
    df["time_s"] = pd.to_numeric(df["time_s"], errors="coerce")
    df["entropy"] = pd.to_numeric(df["entropy"], errors="coerce")
    df = df.replace([np.inf, -np.inf], np.nan).dropna().sort_values("time_s").reset_index(drop=True)

    meta = {"fps": fps, "frame_count": frame_count, "duration_s": duration_s, "samples": len(df)}
    return df, meta


# ------------------------
# Frame extraction helpers
# ------------------------
def frame_to_data_url_bgr(frame_bgr: np.ndarray, jpeg_quality: int = 80) -> str:
    ok, buf = cv2.imencode(".jpg", frame_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), int(jpeg_quality)])
    if not ok:
        raise RuntimeError("Failed to encode frame as JPEG.")
    b64 = base64.b64encode(buf.tobytes()).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"


@lru_cache(maxsize=512)
def get_frame_data_url(video_path: str, t_rounded_ms: int) -> str:
    """
    Cached frame lookup.
    We cache by rounded milliseconds to keep hover responsive.
    """
    t_seconds = t_rounded_ms / 1000.0
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        cap.release()
        raise RuntimeError("Could not open video for frame read.")
    cap.set(cv2.CAP_PROP_POS_MSEC, float(t_seconds) * 1000.0)
    ok, frame = cap.read()
    cap.release()
    if not ok or frame is None:
        raise RuntimeError("Could not read frame at requested time.")
    return frame_to_data_url_bgr(frame)


# ------------------------
# Plot
# ------------------------
def build_figure(df: pd.DataFrame, current_time: float | None = None) -> go.Figure:
    x = df["time_s"].to_numpy(dtype=float)
    y = df["entropy"].to_numpy(dtype=float)

    # robust y-range padding
    y_min = float(np.nanmin(y))
    y_max = float(np.nanmax(y))
    if np.isclose(y_min, y_max):
        pad = 1e-6 if y_min == 0 else abs(y_min) * 0.01
        y_min -= pad
        y_max += pad
    else:
        pad = 0.05 * (y_max - y_min)
        y_min -= pad
        y_max += pad

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines+markers",
        marker=dict(size=6),
        hovertemplate="t=%{x:.3f}s<br>entropy=%{y:.6f}<extra></extra>",
        name="Entropy"
    ))
    fig.update_layout(
        margin=dict(l=45, r=20, t=40, b=40),
        height=480,
        xaxis_title="Time (s)",
        yaxis_title="Entropy",
        xaxis=dict(rangeslider=dict(visible=True)),
    )
    fig.update_yaxes(range=[y_min, y_max])

    # Add a vertical line marker for "current playback time"
    if current_time is not None and np.isfinite(current_time):
        fig.add_vline(x=float(current_time), line_width=2)

    return fig


# ------------------------
# Dash app
# ------------------------
def make_app(video_path: str, df: pd.DataFrame, meta: dict) -> Dash:
    app = Dash(__name__)

    # initial frame preview (t=0)
    try:
        initial_frame = get_frame_data_url(video_path, 0)
    except Exception:
        initial_frame = None

    app.layout = html.Div(
        style={"maxWidth": "1200px", "margin": "0 auto", "fontFamily": "system-ui, -apple-system, Segoe UI, Roboto"},
        children=[
            html.H2("Video Entropy Explorer (hover graph → frame preview; play video → marker moves)"),

            html.Div(
                style={"display": "grid", "gridTemplateColumns": "2fr 1fr", "gap": "18px", "alignItems": "start"},
                children=[
                    html.Div(
                        children=[
                            html.Video(
                                id="video",
                                src=f"file://{video_path}",
                                controls=True,
                                style={"width": "100%", "borderRadius": "10px", "background": "#000"},
                            ),
                            html.Div(
                                style={"marginTop": "10px", "display": "flex", "gap": "10px", "alignItems": "center"},
                                children=[
                                    dcc.Checklist(
                                        id="sync_toggle",
                                        options=[
                                            {"label": "Sync marker to video playback", "value": "sync_marker"},
                                            {"label": "Seek video on graph hover", "value": "seek_on_hover"},
                                        ],
                                        value=["sync_marker"],  # default
                                        style={"display": "flex", "gap": "14px"},
                                    ),
                                    html.Div(
                                        children=f"Samples: {meta['samples']} | FPS: {meta['fps']:.3f} | "
                                                + (f"Duration: {meta['duration_s']:.3f}s" if meta.get("duration_s") else "Duration: unknown"),
                                        style={"opacity": 0.75, "fontSize": "0.9rem"},
                                    ),
                                ],
                            ),

                            # graph
                            dcc.Graph(
                                id="entropy_graph",
                                figure=build_figure(df, current_time=0.0),
                                clear_on_unhover=False,
                                config={"displayModeBar": True},
                                style={"marginTop": "12px"},
                            ),

                            # interval to poll playback time
                            dcc.Interval(id="poll_video_time", interval=250, n_intervals=0),

                            # stores
                            dcc.Store(id="store_current_time", data=0.0),
                        ]
                    ),

                    html.Div(
                        children=[
                            html.H4("Frame at hovered time"),
                            html.Div(id="hover_time_label", style={"marginBottom": "8px", "opacity": 0.8}),
                            html.Img(
                                id="frame_preview",
                                src=initial_frame,
                                style={"width": "100%", "borderRadius": "10px", "border": "1px solid #ddd"},
                            ),
                            html.Div(
                                style={"marginTop": "10px", "fontSize": "0.9rem", "opacity": 0.75},
                                children=(
                                    "Tip: Hover a point on the chart to update the frame. "
                                    "Enable “Seek video on graph hover” if you want the video to jump too "
                                    "(can be jumpy while moving the mouse)."
                                ),
                            ),
                        ],
                        style={"position": "sticky", "top": "12px"},
                    ),
                ]
            ),
        ],
    )

    # ---- Client-side callback: read video.currentTime periodically into store ----
    app.clientside_callback(
        """
        function(n, sync_values, current_store) {
            // Only update if syncing is enabled
            const syncEnabled = (sync_values || []).includes("sync_marker");
            if (!syncEnabled) return window.dash_clientside.no_update;

            const vid = document.getElementById("video");
            if (!vid) return window.dash_clientside.no_update;

            // currentTime is seconds (float)
            return vid.currentTime || 0.0;
        }
        """,
        Output("store_current_time", "data"),
        Input("poll_video_time", "n_intervals"),
        State("sync_toggle", "value"),
        State("store_current_time", "data"),
    )

    # ---- Server callback: update graph marker line to current playback time ----
    @app.callback(
        Output("entropy_graph", "figure"),
        Input("store_current_time", "data"),
        State("entropy_graph", "relayoutData"),
    )
    def update_marker(current_time, relayout):
        # Keep zoom/scroll state by reusing relayout if possible (basic approach)
        fig = build_figure(df, current_time=float(current_time))
        if relayout and isinstance(relayout, dict):
            # preserve x-axis range if user zoomed
            if "xaxis.range[0]" in relayout and "xaxis.range[1]" in relayout:
                fig.update_xaxes(range=[relayout["xaxis.range[0]"], relayout["xaxis.range[1]"]])
        return fig

    # ---- Server callback: on hover, show frame (and optionally seek video via a clientside callback) ----
    @app.callback(
        Output("frame_preview", "src"),
        Output("hover_time_label", "children"),
        Input("entropy_graph", "hoverData"),
        State("sync_toggle", "value"),
    )
    def update_frame_on_hover(hover_data, sync_values):
        if not hover_data or "points" not in hover_data or not hover_data["points"]:
            return no_update, no_update

        t = float(hover_data["points"][0]["x"])
        # cache key: rounded milliseconds
        t_ms = int(round(t * 1000.0))
        try:
            src = get_frame_data_url(video_path, t_ms)
        except Exception:
            return no_update, f"Hover time: {t:.3f} s (frame read failed)"

        return src, f"Hover time: {t:.3f} s"

    # ---- Client-side callback: optionally seek video to hovered time ----
    app.clientside_callback(
        """
        function(hoverData, sync_values) {
            const seekEnabled = (sync_values || []).includes("seek_on_hover");
            if (!seekEnabled) return window.dash_clientside.no_update;

            const vid = document.getElementById("video");
            if (!vid) return window.dash_clientside.no_update;

            if (!hoverData || !hoverData.points || hoverData.points.length === 0) {
                return window.dash_clientside.no_update;
            }
            const t = hoverData.points[0].x;
            if (typeof t === "number" && isFinite(t)) {
                // Seeking on hover can feel jumpy; you can switch this to click if you prefer.
                vid.currentTime = t;
            }
            return window.dash_clientside.no_update;
        }
        """,
        Output("video", "data-dummy"),  # dummy output; doesn't change anything visible
        Input("entropy_graph", "hoverData"),
        State("sync_toggle", "value"),
        prevent_initial_call=True,
    )

    return app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="Path to a local video file (mp4 recommended)")
    parser.add_argument("--step", type=float, default=0.5, help="Sampling step in seconds (default 0.5)")
    parser.add_argument("--wavelet", type=str, default="db2", help="Wavelet name (default db2)")
    parser.add_argument("--level", type=int, default=1, help="Wavelet level (default 1)")
    parser.add_argument("--max_seconds", type=float, default=0.0, help="0=full video, else process up to this time")
    parser.add_argument("--port", type=int, default=8050, help="Dash server port")
    args = parser.parse_args()

    video_path = str(Path(args.video).expanduser().resolve())
    max_seconds = None if args.max_seconds == 0.0 else float(args.max_seconds)

    df, meta = compute_entropy_series(video_path, float(args.step), args.wavelet, int(args.level), max_seconds)
    app = make_app(video_path, df, meta)
    app.run(debug=True, port=args.port)



if __name__ == "__main__":
    main()


