# 🚀 Helmet Detection Application - Quick Start Guide

## Application Status

✅ **Frontend**: Running at **http://localhost:3000**  
✅ **Backend API**: Running at **http://localhost:5000**  
✅ **Helmet Detection Model**: Trained and integrated (76.3% mAP)

## How to Access

### Open the Application

1. **Open your web browser** (Chrome, Firefox, Edge, etc.)
2. **Navigate to**: `http://localhost:3000`
3. The Traffic Violation Detection interface will load

### Using the Application

#### Upload an Image
1. Click on the **upload area** or drag & drop an image
2. Select an image from your computer (or use test images from `helmet_detection/val/images/`)
3. Click **"Detect Violations"** button
4. View the results with:
   - Detected objects highlighted with bounding boxes
   - Green boxes = With Helmet ✅  
   - Red boxes = Without Helmet 🚨 (VIOLATION)
   - Violation summary and statistics

#### Test Images Available
- **Location**: `C:\Users\svlak\New folder (14)\helmet_detection\val\images\`
- **Count**: 153 validation images
- These are real images from the training dataset

## API Endpoints

### Image Detection
```http
POST http://localhost:5000/detect
Content-Type: multipart/form-data

{
  "image": <image_file>
}
```

### Health Check
```http
GET http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "model": "Custom Traffic Violation Detection",
  "custom_model": true,
  "ocr": "EasyOCR",
  "video_support": true
}
```

## Model Information

- **Architecture**: YOLOv8n (nano - optimized for speed)
- **Training Epochs**: 25
- **Performance**: 76.3% mAP
- **Classes**: 
  - `with_helmet` (Class 0)
  - `without_helmet` (Class 1)
- **Model File**: `backend/best.pt` (6.2 MB)

## Features

✅ Real-time helmet detection  
✅ Bounding box visualization  
✅ Violation counting and statistics  
✅ License plate recognition (OCR)  
✅ SMS notifications (demo mode)  
✅ Video upload support  
✅ Responsive web interface

## Troubleshooting

### Backend Not Running?
```powershell
cd "C:\Users\svlak\New folder (14)\backend"
python app.py
```

### Frontend Not Running?
```powershell
cd "C:\Users\svlak\New folder (14)\frontend"
npm run dev
```

### Test the Integration
```powershell
cd "C:\Users\svlak\New folder (14)"
python test_helmet_detection.py
```

## Screenshot Preview

The application includes:
- Clean, modern UI design
- Upload area with drag & drop support
- Real-time detection results
- Violation statistics dashboard
- Annotated images with color-coded bounding boxes

## Next Steps

1. **Open** http://localhost:3000 in your browser
2. **Upload** a test image from `helmet_detection/val/images/`
3. **Click** "Detect Violations"
4. **View** the results with highlighted detections!

---

**Note**: The backend runs in SMS demo mode (no Twilio credentials set). Violation notifications are logged to console instead of being sent via SMS.
