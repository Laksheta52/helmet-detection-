# Helmet Detection Setup Guide

Quick guide to run the helmet detection application.

## Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- Git (optional)

## Quick Start (Windows)

### Option 1: One-Click Start
1. Double-click `start-all.bat`
2. Wait for both servers to start
3. Open http://localhost:3000 in your browser

### Option 2: Manual Start

**Step 1: Install Backend Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**Step 2: Install Frontend Dependencies**
```bash
cd frontend
npm install
```

**Step 3: Start Backend** (in terminal 1)
```bash
cd backend
python app.py
```
Backend runs at http://localhost:5000

**Step 4: Start Frontend** (in terminal 2)
```bash
cd frontend
npm run dev
```
Frontend runs at http://localhost:3000

## Using the Application

1. Open http://localhost:3000
2. Click or drag & drop an image
3. Click "Analyze Image"
4. View detection results!

## File Structure

```
helmet-detection/
├── backend/
│   ├── best.pt          ← TRAINED MODEL (required!)
│   ├── app.py           ← Flask API server
│   └── requirements.txt ← Python dependencies
├── frontend/
│   ├── app/             ← Next.js pages
│   └── package.json     ← Node dependencies
└── start-all.bat        ← One-click launcher
```

## Important Files

- **Model:** `backend/best.pt` - The trained YOLOv8 model (76.3% mAP)
- **Backend:** `backend/app.py` - Flask server with detection API
- **Frontend:** `frontend/app/page.tsx` - Next.js UI

## Troubleshooting

**Backend won't start:**
- Check if port 5000 is available
- Install dependencies: `pip install ultralytics flask flask-cors easyocr`

**Frontend won't start:**
- Check if port 3000 is available
- Delete `frontend/node_modules` and run `npm install` again

**Detection not working:**
- Ensure `backend/best.pt` exists
- Check backend is running at http://localhost:5000/health

## Model Information

- **Type:** YOLOv8n (nano)
- **Accuracy:** 76.3% mAP
- **Classes:** Helmet, Without-Helmet
- **Training:** 764 images, 25 epochs
- **File:** `backend/best.pt`

## Optional Features

**SMS Notifications:** See `SMS_SETUP_GUIDE.md` for Twilio setup (optional)

## System Requirements

- **RAM:** 4GB minimum (8GB recommended)
- **Storage:** 2GB for dependencies + models
- **GPU:** Not required (CPU inference works fine)
