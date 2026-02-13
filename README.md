# 🚀 Helmet Detection - Quick Setup

Simple AI-powered helmet detection system. Upload an image and detect helmet violations instantly.

## Requirements

- Python 3.8+
- Node.js 18+

## Setup (5 minutes)

### 1. Install Backend
```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Frontend
```bash
cd frontend
npm install
```

### 3. Start Application
Double-click `start-all.bat` or run manually:

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Usage

1. Open **http://localhost:3000**
2. Upload an image (or drag & drop)
3. Click **Analyze Image**
4. View results with detection metrics!

## What's Included

- **AI Model**: Custom YOLOv8 trained on 764 helmet images (76.3% accuracy)
- **Backend**: Flask API at http://localhost:5000
- **Frontend**: Modern Next.js interface at http://localhost:3000

## Troubleshooting

**Port already in use?**
- Backend uses port 5000
- Frontend uses port 3000
- Close other applications using these ports

**Dependencies not installing?**
- Make sure Python and Node.js are installed correctly
- Try: `pip install --upgrade pip` and `npm cache clean --force`

**Model not found?**
- Ensure `backend/best.pt` exists (this is the trained model)

## Share This Project

To share with others, include:
- ✅ `backend/` folder (with best.pt model)
- ✅ `frontend/` folder
- ✅ `start-all.bat`
- ✅ This README

**Model Location:** `backend/best.pt` (6.2 MB)

---

Built with YOLOv8, Flask, Next.js & React
