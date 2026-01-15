import os
import tempfile

import cv2
import gradio as gr
from ultralytics import YOLO
from loguru import logger

MODEL_PATH = "notebooks/yolo11n.pt"
model = YOLO(MODEL_PATH)


def track_video(
    video_path: str, conf_threshold: float, iou_threshold: float, tracker_name: str
) -> str:
    """
    Run YOLO11 tracking on an uploaded video and return an annotated video file.
    """
    logger.info(
        f"Tracking video: {video_path} with {tracker_name} and conf={conf_threshold}, iou={iou_threshold}"
    )
    if video_path is None:
        logger.error("No video uploaded.")
        raise gr.Error("Please upload a video first.")

    # Map human-readable tracker names to Ultralytics tracker configs
    tracker_cfg_map = {
        "BoT-SORT (default)": "botsort.yaml",
        "ByteTrack": "bytetrack.yaml",
    }
    tracker_cfg = tracker_cfg_map.get(tracker_name, "botsort.yaml")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logger.error("Could not open the uploaded video.")
        raise gr.Error("Could not open the uploaded video.")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)

    # Prepare temporary output path
    tmp_dir = tempfile.mkdtemp()
    out_path = os.path.join(tmp_dir, "tracked_output.mp4")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    # Persist tracks across frames
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Run tracking; persist=True keeps IDs across frames
        logger.info("Processing frame for tracking.")
        results = model.track(
            frame,
            conf=conf_threshold,
            iou=iou_threshold,
            tracker=tracker_cfg,
            persist=True,
            verbose=False,
        )

        logger.info("Frame processed.")
        # Plot boxes + IDs onto the frame
        annotated_frame = results[0].plot()
        writer.write(annotated_frame)

    cap.release()
    writer.release()
    logger.info(f"Tracking complete. Output saved to {out_path}")

    return out_path


def build_interface():
    video_input = gr.Video(
        label="Upload video",
    )

    conf_slider = gr.Slider(
        minimum=0.0,
        maximum=1.0,
        value=0.25,
        step=0.01,
        label="Confidence threshold",
    )

    iou_slider = gr.Slider(
        minimum=0.0,
        maximum=1.0,
        value=0.45,
        step=0.01,
        label="IoU threshold",
    )

    tracker_dropdown = gr.Dropdown(
        choices=["BoT-SORT (default)", "ByteTrack"],
        value="BoT-SORT (default)",
        label="Tracker",
    )

    video_output = gr.Video(
        label="Tracked output video",
    )

    iface = gr.Interface(
        fn=track_video,
        inputs=[video_input, conf_slider, iou_slider, tracker_dropdown],
        outputs=video_output,
        title="YOLO11 Multi-Object Tracking",
        description=(
            "Upload a video and run YOLO11 tracking with selectable tracker "
            "(BoT-SORT / ByteTrack), confidence, and IoU thresholds."
        ),
    )

    return iface


if __name__ == "__main__":
    iface = build_interface()
    iface.launch()
