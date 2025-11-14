from ultralytics import YOLO
from dotenv import load_dotenv
import os
import wandb

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

model.val()

model.export(format="onnx")
