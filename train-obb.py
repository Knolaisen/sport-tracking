from ultralytics import YOLO
from dotenv import load_dotenv
import os
import wandb
from codecarbon import EmissionsTracker

tracker = EmissionsTracker(project_name="sport-tracking-yolo11l-rbk-all")
tracker.start()

load_dotenv()

wandb.login(key=os.getenv("WANDB_API_KEY"))
wandb.init(
    project="sport-tracking",
    mode="online",
    name="yolo11l-rbk-all",
)


model = YOLO("yolo11l.pt")

model.train(
    data="/cluster/work/sverrnys/sport-tracking/rbk_all.yaml",
    epochs=100,
    imgsz=1280,
    batch=-1,
    workers=8,
    project="runs/train",
    name="rbk_all",
)

emmissions = tracker.stop()
print(f"Emmissions: {emmissions} kg CO2")

model.val()

model.export(format="onnx")
