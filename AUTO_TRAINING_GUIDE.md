# 📥 Automated Model Training - Quick Guide

## 🎯 What This Does

I've created a **fully automated training notebook** that:
- ✅ Automatically downloads a public helmet detection dataset from Kaggle
- ✅ Sets up everything for you
- ✅ Trains the YOLOv8 model
- ✅ Saves the trained model to Google Drive
- ✅ **No manual dataset preparation needed!**

## 🚀 How to Use

### Option 1: Get Kaggle API Key (1 minute)

1. Go to https://www.kaggle.com and sign in (or create free account)
2. Click your profile icon → **Settings**
3. Scroll to **API** section
4. Click **"Create New Token"**
5. Download `kaggle.json` file

### Option 2: Upload Notebook to Colab

1. Open Google Colab: https://colab.research.google.com
2. Click **File → Upload notebook**
3. Upload: `AUTOMATED_Training.ipynb`
4. **Important**: Enable GPU
   - Runtime → Change runtime type → GPU (T4)

### Option 3: Run All Cells

1. Click **Runtime → Run all** (or press Ctrl+F9)
2. When prompted, upload your `kaggle.json` file
3. **That's it!** The notebook does everything automatically:
   - Downloads dataset (~500MB)
   - Trains model (30-45 minutes for 50 epochs)
   - Saves to Google Drive

## ⏱️ Training Time

- **50 epochs**: ~30-45 minutes (good accuracy)
- **100 epochs**: ~1-1.5 hours (better accuracy)
- **150 epochs**: ~2-2.5 hours (best accuracy)

**Recommendation**: Start with 50 epochs to test, then retrain with 100+ if needed.

## 📥 After Training

### Step 1: Download Model
- Open Google Drive
- Navigate to: `MyDrive/traffic-violation-model/`
- Download `best.pt` (~15-25 MB)

### Step 2: Deploy to Backend
```bash
# Place the downloaded file:
C:\Users\svlak\New folder (14)\backend\best.pt
```

### Step 3: Restart Backend
```bash
cd backend
.\start.bat
```

You should see:
```
✓ Found custom traffic violation model: best.pt
✓ Model loaded: Custom Traffic Violation Detection
```

### Step 4: Test!
- Open http://localhost:3000
- Upload a traffic image
- See helmet violations detected!

## 📊 What Gets Detected

The trained model can detect:
- **with_helmet** - Person wearing helmet ✅ (compliant)
- **without_helmet** - Person without helmet ❌ (violation)

## 🎯 Expected Accuracy

After training, you should get:
- **mAP50**: 0.80-0.95 (80-95% accuracy)
- **Precision**: 0.85-0.95 (correct detections)
- **Recall**: 0.80-0.90 (found violations)

## 📈 Training Process

The automated notebook:
1. ✅ Checks GPU availability
2. ✅ Mounts Google Drive
3. ✅ Downloads Kaggle dataset automatically
4. ✅ Extracts and prepares data
5. ✅ Configures YOLOv8 training
6. ✅ Trains the model
7. ✅ Validates performance
8. ✅ Tests on sample images
9. ✅ Saves model to Drive
10. ✅ Shows training graphs

## 🆘 Troubleshooting

**"Kaggle API error"**
- Make sure you uploaded `kaggle.json`
- Verify file isn't corrupted

**"GPU not available"**
- Runtime → Change runtime type → T4 GPU
- Click Save

**"Out of memory"**
- In training cell, change `batch=16` to `batch=8`
- Rerun that cell

**"Dataset not found"**
- The notebook handles this automatically
- If issues persist, manually check `/content/helmet-dataset`

## 🔧 Advanced Options

### Train for Better Accuracy
Edit training cell:
```python
epochs=100,  # Change from 50 to 100 or 150
```

### Use Larger Model
Change model loading:
```python
model = YOLO('yolov8m.pt')  # Medium (slower, more accurate)
# or
model = YOLO('yolov8l.pt')  # Large (best accuracy)
```

## 📚 Datasets Used

**Primary Dataset**: Kaggle - Smart Helmet Detection
- Created for motorcycle rider safety
- YOLOv8 format ready-to-use
- Train/Valid/Test splits included
- ~1000+ images with annotations

## ✨ Summary

**Before**: Manual dataset hunting, complex setup
**After**: Just run the notebook, get trained model!

**Total time from start to deployed model**: ~45 minutes

Questions? Check the detailed `TRAINING_GUIDE.md` for more information!

---

**Ready to train?** Upload `AUTOMATED_Training.ipynb` to Google Colab now! 🚀
