from ultralytics import YOLO
import torch

# Check if CUDA is available
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Load YOLOv8n model
print("\nLoading YOLOv8n model...")
model = YOLO('yolov8n.pt')

# Train the model
print("\nStarting training...")
results = model.train(
    data='helmet_data.yaml',
    epochs=50,
    imgsz=640,
    batch=16,
    name='helmet_detection',
    device=device,
    patience=10,
    save=True,
    plots=True,
    verbose=True
)

print("\n" + "="*50)
print("Training completed!")
print("="*50)
print(f"\nBest model saved to: runs/detect/helmet_detection/weights/best.pt")
print(f"Last model saved to: runs/detect/helmet_detection/weights/last.pt")
print(f"\nTraining metrics and plots saved to: runs/detect/helmet_detection/")
