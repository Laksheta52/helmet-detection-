# Helmet Detection Backend

Flask API for helmet detection and license plate recognition using YOLOv8 and EasyOCR.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /health
```

### Detect Objects
```
POST /detect
Content-Type: multipart/form-data

Body: image file
```

Response:
```json
{
  "success": true,
  "detections": [
    {
      "class": "person",
      "confidence": 95.5,
      "bbox": [100, 150, 300, 400],
      "helmet_related": true
    }
  ],
  "total_detections": 3,
  "annotated_image": "data:image/jpeg;base64,..."
}
```
