# 🚀 QUICK START - Traffic Violation Detection

## Step 1: Setup (First Time Only)

### Backend Setup
```bash
cd backend
.\setup.bat
```
⏱️ Takes ~5 minutes to install YOLOv8, EasyOCR, PyTorch

### Frontend Setup
No manual setup needed! Happens automatically on first run.

---

## Step 2: Start Application

**Easiest Way:**
```bash
.\start-all.bat
```

**Or start separately:**
```bash
# Terminal 1
cd backend
.\start.bat

# Terminal 2  
cd frontend
npm run dev
```

---

## Step 3: Access Application

Open browser: **http://localhost:3000**

---

## Step 4: Train Custom Model (Optional but Recommended)

### Why Train?
- ✅ Detect helmet violations accurately
- ✅ Identify traffic light states (red/yellow/green)
- ✅ Recognize 10 violation classes
- ❌ Without it: Basic detection only

### How to Train:

**1. Open Training Notebook:**
- Upload `Traffic_Violation_Training.ipynb` to Google Colab
- Enable GPU (Runtime → Change runtime type → T4 GPU)

**2. Get Dataset:**
- Visit https://universe.roboflow.com
- Search: "helmet detection"
- Download in YOLOv8 format
- Or use your own annotated images

**3. Run All Cells:**
- Paste your Roboflow API key
- Run training (100 epochs ≈ 1-2 hours)
- Download `best.pt` from Google Drive

**4. Deploy Model:**
```bash
# Place downloaded best.pt in:
C:\Users\svlak\New folder (14)\backend\best.pt

# Restart backend
cd backend
.\start.bat
```

---

## 🎯 Usage

1. **Upload** - Drag & drop image or click "Choose Image"
2. **Analyze** - Click "Analyze Image"  
3. **View Results** - See violations, penalties, and license plates

---

## 📊 What Gets Detected

### With Custom Model (after training):
- ✅ Helmet / No-Helmet violations
- ✅ Red light jumping
- ✅ All vehicle types
- ✅ Traffic light states
- ✅ License plates

### Without Custom Model (generic YOLOv8):
- ⚠️ Basic person/vehicle detection
- ⚠️ Helmet violations (heuristic-based)
- ✅ License plates (OCR)

---

## ⚖️ Violations & Penalties

| Violation | Fine | Section |
|-----------|------|---------|
| No Helmet | ₹1,000 | MV Act 129 |
| Red Light | ₹1,000 | MV Act 177 |
| Wrong Side | ₹10,000 | MV Act 184 |
| Overspeeding | ₹1,000-₹2,000 | MV Act 183 |

---

## 🆘 Troubleshooting

**Backend won't start:**
```bash
cd backend
.\setup.bat  # Run setup again
```

**Frontend won't start:**
```bash
cd frontend
npm install
```

**Port already in use:**
- Check if another instance is running
- Kill process using port 3000 or 5000

**Model not loading:**
- Check `backend/best.pt` exists
- File size should be ~15-25 MB

---

## 📁 Project Files

```
Traffic_Violation_Training.ipynb  # Colab training notebook
TRAINING_GUIDE.md                 # Detailed training instructions
start-all.bat                     # Start both servers
backend/                          # Flask API
frontend/                         # Next.js UI
```

---

## 🎓 Resources

- **Training Guide:** See `TRAINING_GUIDE.md`
- **Full Walkthrough:** Check artifacts walkthrough
- **Roboflow Datasets:** https://universe.roboflow.com
- **YOLOv8 Docs:** https://docs.ultralytics.com

---

## ✨ That's It!

Your traffic violation detection system is ready to use! 🚀

**Questions?** Check the full documentation in README.md
