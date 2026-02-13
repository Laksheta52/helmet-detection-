# Traffic Violation Detection - Custom Model Training

Complete Google Colab notebook for training a custom YOLOv8 model to detect traffic violations.

## 🎯 Classes to Detect

This model will detect:
1. **Helmet** - Person wearing helmet (compliant)
2. **No-Helmet** - Person without helmet (violation)
3. **Motorcycle** - Two-wheeler vehicle
4. **Car** - Four-wheeler vehicle
5. **Truck** - Heavy vehicle
6. **Bus** - Public transport
7. **Traffic-Light-Red** - Red signal
8. **Traffic-Light-Green** - Green signal
9. **Traffic-Light-Yellow** - Yellow signal
10. **Numberplate** - License plate

---

## 📦 Dataset Requirements

### Option 1: Use Existing Datasets (Recommended)

**Roboflow Public Datasets:**

1. **Helmet Detection:**
   - Search: "helmet detection yolo" on Roboflow Universe
   - Look for datasets with "helmet" and "no-helmet" classes
   - Example: https://universe.roboflow.com/search?q=helmet+detection

2. **Traffic Light Detection:**
   - Search: "traffic light detection"
   - Need datasets with red/yellow/green states
   - Example: LISA Traffic Light Dataset

3. **Vehicle + License Plate:**
   - Search: "license plate detection"
   - Includes vehicle types too

**Download in YOLOv8 format:**
- Format: YOLOv8
- Split: 70% train, 20% val, 10% test

### Option 2: Create Your Own Dataset

**Tools:**
- **Roboflow** - Free annotation tool
- **LabelImg** - Desktop annotation
- **CVAT** - Advanced annotation

**Requirements:**
- Minimum 500 images per class
- Diverse conditions (day/night, weather)
- Various angles and distances

---

## 🚀 Google Colab Training Notebook

Copy and run this in Google Colab:

```python
# ====================================
# Traffic Violation Detection Training
# ====================================

# 1. Check GPU
!nvidia-smi

# 2. Install Dependencies
!pip install ultralytics roboflow

from ultralytics import YOLO
import os
from roboflow import Roboflow

# 3. Setup Google Drive (Optional - to save model)
from google.colab import drive
drive.mount('/content/drive')

# Create output directory
output_dir = '/content/drive/MyDrive/traffic-violation-model'
os.makedirs(output_dir, exist_ok=True)

# 4. Download Dataset from Roboflow
# Method 1: Using Roboflow API
rf = Roboflow(api_key="YOUR_ROBOFLOW_API_KEY")
project = rf.workspace("YOUR_WORKSPACE").project("YOUR_PROJECT")
dataset = project.version(1).download("yolov8")

# OR Method 2: Upload your own dataset
# Upload a zip file with this structure:
# dataset/
#   ├── train/
#   │   ├── images/
#   │   └── labels/
#   ├── valid/
#   │   ├── images/
#   │   └── labels/
#   └── data.yaml

# 5. Create data.yaml file
data_yaml = '''
path: /content/YOUR_DATASET_PATH
train: train/images
val: valid/images

nc: 10  # number of classes
names:
  0: Helmet
  1: No-Helmet
  2: Motorcycle
  3: Car
  4: Truck
  5: Bus
  6: Traffic-Light-Red
  7: Traffic-Light-Green
  8: Traffic-Light-Yellow
  9: Numberplate
'''

with open('data.yaml', 'w') as f:
    f.write(data_yaml)

# 6. Load YOLOv8 Model
# Use yolov8s for balance, yolov8m or yolov8l for better accuracy
model = YOLO('yolov8s.pt')

# 7. Train the Model
results = model.train(
    data='data.yaml',
    epochs=100,              # Increase for better results
    imgsz=640,              # Image size
    batch=16,               # Adjust based on GPU memory
    name='traffic-violation-v1',
    patience=20,            # Early stopping
    save=True,
    device=0,               # GPU
    workers=8,
    optimizer='AdamW',
    lr0=0.01,
    weight_decay=0.0005,
    augment=True,           # Data augmentation
    plots=True
)

# 8. Validate the Model
metrics = model.val()
print(f"mAP50: {metrics.box.map50}")
print(f"mAP50-95: {metrics.box.map}")

# 9. Test Predictions
# Test on sample image
test_image = 'path/to/test/image.jpg'
results = model.predict(test_image, conf=0.25, save=True)

# Display results
from IPython.display import Image, display
display(Image(filename='runs/detect/predict/image0.jpg'))

# 10. Export Model
# Save best weights
best_model_path = 'runs/detect/traffic-violation-v1/weights/best.pt'

# Copy to Google Drive
import shutil
shutil.copy(best_model_path, f'{output_dir}/best.pt')

print(f"✓ Model saved to: {output_dir}/best.pt")
print(f"✓ Download this file and place in your backend folder!")

# 11. Export to ONNX (Optional - for faster inference)
model.export(format='onnx')

print("="*50)
print("Training Complete!")
print("="*50)
print(f"Best model: {best_model_path}")
print(f"Metrics: mAP50={metrics.box.map50:.3f}, mAP50-95={metrics.box.map:.3f}")
```

---

## 📊 Quick Setup with Pre-annotated Dataset

If you want to start training immediately:

```python
# Use a public helmet detection dataset from Roboflow
!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="YOUR_API_KEY")  # Get free API key from roboflow.com

# Example: Helmet Detection Dataset
project = rf.workspace("helmet-detection").project("helmet-detection-yolo")
dataset = project.version(1).download("yolov8")

# This will download a ready-to-use YOLOv8 format dataset!
```

---

## 🎓 Training Tips

### Best Practices:

1. **Start Small:**
   - Begin with 50-100 epochs
   - Use yolov8s (faster training)
   - Test quickly, iterate

2. **Data Quality > Quantity:**
   - Clean annotations are crucial
   - Remove bad images
   - Balance classes

3. **Augmentation:**
   - Helps with small datasets
   - Already enabled in training config

4. **Monitor Training:**
   - Watch loss curves
   - Use early stopping
   - Check validation metrics

### Expected Training Time:

- **YOLOv8s:** ~1-2 hours (100 epochs, T4 GPU)
- **YOLOv8m:** ~2-4 hours
- **YOLOv8l:** ~4-6 hours

---

## 📥 After Training

1. **Download `best.pt`** from Colab
2. Place in: `C:\Users\svlak\New folder (14)\backend\best.pt`
3. Restart backend server
4. System will automatically use custom model!

---

## 🔧 Alternative: Pre-trained Model

If you want to test the system first, you can use a pre-existing helmet detection model:

```python
# In Colab
from ultralytics import YOLO

# Download a pre-trained helmet detection model
!wget https://github.com/YOUR-PRETRAINED-MODEL-LINK/best.pt

# Test it
model = YOLO('best.pt')
results = model.predict('test_image.jpg')
```

---

## 📝 Dataset Structure

Your dataset should follow this structure:

```
traffic-violations-dataset/
├── train/
│   ├── images/
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   │   └── ...
│   └── labels/
│       ├── img001.txt
│       ├── img002.txt
│       └── ...
├── valid/
│   ├── images/
│   └── labels/
└── data.yaml
```

**Label Format (YOLO):**
```
# img001.txt
0 0.5 0.6 0.3 0.4  # class_id x_center y_center width height (normalized)
1 0.2 0.3 0.1 0.15
```

---

## 🎯 Next Steps

1. **Choose dataset source** (Roboflow or custom)
2. **Run training notebook** in Google Colab
3. **Download trained model** (best.pt)
4. **Place in backend folder**
5. **Test with real images**

Would you like me to:
1. Help you find/prepare a dataset?
2. Create a simplified training notebook for a specific violation type?
3. Set up the backend to work with the trained model?
