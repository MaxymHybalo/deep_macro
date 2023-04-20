from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')

res = model('logs/world_explorer/0.png', show=True)
cv2.waitKey(0)