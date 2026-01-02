# 🏥 Getting Started with Meddi AI

Welcome to **Meddi AI** - Your healthcare AI learning project!

## 🎯 What You'll Build

A complete AI system with:
- ✅ Drug side effects prediction (ML model)
- ✅ Drug interaction risk detection (ML model)
- ✅ OCR text extraction from images
- ✅ No internet required - everything runs locally!

## ⚡ 2-Minute Quick Start

### Option 1: Automated Setup (Easiest)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run automated setup
python setup.py
```

The setup script will:
- Check dependencies
- Train ML models
- Run tests
- Show you what to do next

### Option 2: Manual Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train models
cd src
python train_models.py
cd ..

# 3. Run demo
python demo.py
```

## 🎮 Try It Now!

### Quick Test (30 seconds)

```bash
# Run the demo
python demo.py
```

You'll see:
- Feature 1: Predict side effects for aspirin, metformin, etc.
- Feature 2: Check if aspirin + warfarin is dangerous (it is!)
- Feature 3: Analyze text for drug names

### Interactive Mode (Most Fun!)

```bash
# Start CLI
python src/main.py --cli
```

Then try:
1. Option 1: Enter "aspirin" → See side effects
2. Option 2: Enter "aspirin, warfarin" → See dangerous interaction warning
3. Option 4: Enter "Take Aspirin and Ibuprofen" → Auto-detect drugs

## 📚 Documentation Guide

Choose your path:

### 🚀 Beginner Path
1. Start here: **[QUICKSTART.md](QUICKSTART.md)** (5 min read)
2. Run: `python demo.py`
3. Then read: **[CODE_EXPLANATION.py](CODE_EXPLANATION.py)** (understand how it works)

### 🔬 Advanced Path
1. Full docs: **[README_MEDDI_AI.md](README_MEDDI_AI.md)** (complete guide)
2. Overview: **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** (what was built)
3. Dive into code: `src/train_models.py` (training logic)

## 🎓 What You'll Learn

By exploring this project:
- ✅ How machine learning models are trained
- ✅ How to use Random Forest for classification
- ✅ How to convert text to numbers (encoding)
- ✅ How to save and load models
- ✅ How to build a complete AI system
- ✅ Real-world ML best practices

## 📁 Key Files to Explore

| File | What It Does | Start Here? |
|------|--------------|-------------|
| `setup.py` | Automated setup | ✅ YES |
| `demo.py` | Demo all features | ✅ YES |
| `src/train_models.py` | Train ML models | ⭐ Learn ML |
| `src/services/side_effects_analyzer.py` | Feature 1 code | ⭐ See predictions |
| `CODE_EXPLANATION.py` | Code tutorial | ⭐ Understand everything |

## 🎨 Example Outputs

### Feature 1: Side Effects
```
Input: "aspirin"
Output:
  ✓ Drug: Aspirin
  ✓ Side Effects (4 found):
    • stomach upset
    • bleeding
    • nausea  
    • heartburn
```

### Feature 2: Interactions
```
Input: "aspirin, warfarin"
Output:
  🔴 Risk Level: Dangerous
  Confidence: 95.2%
  Description: High risk! Do not combine without medical supervision.
```

### Feature 3: Text Analysis
```
Input: "Take Aspirin 100mg and Ibuprofen 200mg"
Output:
  ✓ Detected 2 drugs: Aspirin, Ibuprofen
  ✓ Side effects for each drug
  ⚠️  CAUTION: Moderate interaction detected
```

## 🔧 Common Issues

### "Module not found"
**Solution:** `pip install -r requirements.txt`

### "Models not trained"
**Solution:** `python src/train_models.py`

### "Drug not found"
**Solution:** Check available drugs with `python demo.py` or add to `data/drug_side_effects.csv`

## 🚀 Next Steps

After getting started:

1. **Experiment:**
   - Try different drugs
   - Check various combinations
   - See how accurate the predictions are

2. **Customize:**
   - Add your own drugs to CSV files
   - Retrain models
   - See your changes in action

3. **Learn:**
   - Read the code comments
   - Understand the ML pipeline
   - Experiment with parameters

4. **Build:**
   - Create a web interface
   - Add more features
   - Make it your own!

## 📖 Learning Path

### Day 1: Get It Working
- ✅ Run `python setup.py`
- ✅ Try `python demo.py`
- ✅ Use CLI: `python src/main.py --cli`

### Day 2: Understand It
- ✅ Read `CODE_EXPLANATION.py`
- ✅ Study `src/train_models.py`
- ✅ Look at the CSV data files

### Day 3: Customize It
- ✅ Add new drugs to CSV files
- ✅ Retrain models
- ✅ Experiment with parameters

### Day 4: Extend It
- ✅ Add new features
- ✅ Build a web UI
- ✅ Make it your own project!

## 💡 Pro Tips

1. **Drug names are case-insensitive**
   - "aspirin" = "Aspirin" = "ASPIRIN"

2. **Models need retraining after data changes**
   - Edit CSV → Run `python src/train_models.py`

3. **Check available drugs**
   - Look in `data/drug_side_effects.csv`
   - Or run demo to see examples

4. **OCR requires Tesseract**
   - Feature 3 (image) needs Tesseract installed
   - Features 1 & 2 work without it

## 🎯 Your First 5 Minutes

```bash
# Minute 1: Install
pip install -r requirements.txt

# Minute 2-3: Setup
python setup.py

# Minute 4-5: Try it!
python demo.py
```

## 🆘 Need Help?

1. **Quick answers:** See [QUICKSTART.md](QUICKSTART.md)
2. **Full guide:** See [README_MEDDI_AI.md](README_MEDDI_AI.md)
3. **Understanding code:** See [CODE_EXPLANATION.py](CODE_EXPLANATION.py)
4. **Project overview:** See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## ⚠️ Important Note

This is an **educational project** for learning AI/ML:
- ✅ Great for learning
- ✅ Demonstrates real ML techniques
- ❌ NOT for medical use
- ❌ NOT FDA approved

Always consult healthcare professionals for medical advice!

## 🎉 Ready?

Pick one:

```bash
# Automated (recommended)
python setup.py

# Quick demo
python demo.py

# Interactive CLI
python src/main.py --cli
```

---

**Welcome to AI in Healthcare! Let's get started! 🚀**

*Built with ❤️ for learning and innovation*
