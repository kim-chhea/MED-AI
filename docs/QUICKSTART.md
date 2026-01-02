# Meddi AI - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies (1 minute)

```bash
# Install Python packages
pip install -r requirements.txt

# Install Tesseract OCR (optional, for image feature)
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# Linux: sudo apt-get install tesseract-ocr
# macOS: brew install tesseract
```

### Step 2: Train ML Models (2 minutes)

```bash
cd src
python train_models.py
```

**What happens:**
- Loads training data from CSV files
- Trains 2 Random Forest models
- Saves models to `src/models/` directory
- Shows accuracy metrics

**Expected output:**
```
✓ Feature 1 Training Complete! (95% accuracy)
✓ Feature 2 Training Complete! (92% accuracy)
✓ ALL MODELS TRAINED SUCCESSFULLY!
```

### Step 3: Run the Application

**Option A - Interactive CLI:**
```bash
python main.py --cli
```

**Option B - Run Demo:**
```bash
python demo.py
```

**Option C - Web Server:**
```bash
python main.py
# Access at: http://127.0.0.1:5001
```

## 📝 Quick Test Examples

### Test 1: Check Side Effects
```bash
python main.py --cli
# Select: 1
# Enter drug: aspirin
```

**Expected Result:**
```
✓ Analysis for: Aspirin
Side Effects (4 found):
  • stomach upset
  • bleeding
  • nausea
  • heartburn
```

### Test 2: Check Drug Interactions
```bash
python main.py --cli
# Select: 2
# Enter drugs: aspirin, warfarin
```

**Expected Result:**
```
🔴 Aspirin + Warfarin
Risk Level: Dangerous
⚠️ High risk! Do not combine without medical supervision.
```

### Test 3: Analyze Text
```bash
python main.py --cli
# Select: 4
# Enter text: Take Aspirin and Ibuprofen for pain
```

**Expected Result:**
```
✓ Detected 2 drugs: Aspirin, Ibuprofen

Side Effects:
  Aspirin:
    - stomach upset
    - bleeding
  
  Ibuprofen:
    - stomach pain
    - dizziness

⚠️ CAUTION: Moderate interaction detected!
```

## 🎯 Available Drugs in Database

The system comes with 30+ pre-loaded drugs:
- aspirin, ibuprofen, paracetamol
- metformin, insulin, lisinopril
- simvastatin, atorvastatin, omeprazole
- warfarin, clopidogrel, gabapentin
- sertraline, alprazolam, tramadol
- and more...

**Full list:** Check `data/drug_side_effects.csv`

## ➕ Adding New Drugs

### 1. Add to side effects database:
```csv
# Edit: data/drug_side_effects.csv
drug_name,side_effect
newdrug,headache
newdrug,nausea
```

### 2. Add interactions:
```csv
# Edit: data/drug_interactions.csv
drugA,drugB,interaction_risk
newdrug,aspirin,Moderate
```

### 3. Retrain models:
```bash
cd src
python train_models.py
```

## 🔧 Troubleshooting

### "Models not trained yet"
**Fix:** Run `python src/train_models.py`

### "Drug not found in database"
**Fix:** Add to CSV files and retrain

### Import errors
**Fix:** Run `pip install -r requirements.txt`

### OCR not working
**Fix:** Install Tesseract OCR separately (see Step 1)

## 📚 Project Structure

```
drug-side-effects-analyzer/
├── data/                    # Training datasets (CSV)
├── src/
│   ├── train_models.py      # Train ML models (run first!)
│   ├── main.py              # Main application
│   ├── models/              # Saved models (auto-generated)
│   └── services/            # ML prediction services
├── demo.py                  # Demo all features
├── requirements.txt         # Python dependencies
└── README_MEDDI_AI.md       # Full documentation
```

## 📖 Next Steps

1. ✅ Read full documentation: `README_MEDDI_AI.md`
2. ✅ Run the demo: `python demo.py`
3. ✅ Try the CLI: `python main.py --cli`
4. ✅ Explore the code: `src/services/`
5. ✅ Add more drugs to datasets
6. ✅ Build a custom web UI

## ⚠️ Important Notes

- This is for **educational purposes only**
- Not for medical diagnosis or treatment
- Always consult healthcare professionals
- Predictions based on limited training data

## 💡 Tips

- Drug names are case-insensitive
- You can check multiple drug pairs at once
- OCR works best with clear, high-contrast images
- Models can be retrained anytime with updated data

---

**Need Help?** Check the full README: `README_MEDDI_AI.md`

**Meddi AI** - Local AI for Healthcare Learning 🏥
