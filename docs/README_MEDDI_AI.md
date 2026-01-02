# Meddi AI - Healthcare AI System

A beginner-friendly healthcare AI system that uses **local machine learning models** to predict drug side effects and interactions, plus extract drug information from images using OCR.

## 🎯 Features

### Feature 1: Single Drug Side Effects Prediction
- Predicts common side effects for a given drug
- Uses Random Forest classification trained on drug-side effect associations
- Local ML model - no internet required

### Feature 2: Drug-Drug Interaction Risk Prediction
- Predicts interaction risk between two drugs
- Classifies interactions as: Safe, Moderate, or Dangerous
- Uses Random Forest trained on drug interaction data

### Feature 3: Drug Text Extraction from Images
- Uses Tesseract OCR to extract text from drug labels/prescriptions
- Automatically identifies drug names in extracted text
- Combines Features 1 & 2 to analyze detected drugs

## 🛠️ Technical Stack

- **Language**: Python 3.8+
- **ML Library**: scikit-learn (Random Forest)
- **Data Processing**: pandas, numpy
- **OCR**: Tesseract, pytesseract
- **Web Framework**: Flask (optional UI)
- **Model Storage**: joblib

## 📦 Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Tesseract OCR (for Feature 3)

**Windows:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install and add to PATH

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

## 🚀 Quick Start

### Step 1: Train the ML Models

Before using Meddi AI, you need to train the machine learning models:

```bash
cd src
python train_models.py
```

This will:
- Load training data from CSV files
- Train two Random Forest models
- Save trained models to `src/models/` directory
- Display training accuracy and statistics

**Expected Output:**
```
MEDDI AI - MACHINE LEARNING MODEL TRAINING
============================================================
FEATURE 1: Training Single Drug Side Effects Model
   Loaded 120 records
   Unique drugs: 30
   Training Random Forest model...
   Accuracy: 95%
   
FEATURE 2: Training Drug-Drug Interaction Model
   Loaded 85 interaction records
   Training Random Forest classifier...
   Accuracy: 92%
   
✓ ALL MODELS TRAINED SUCCESSFULLY!
```

### Step 2: Run the Application

#### Option A: Command Line Interface (CLI)

```bash
python main.py --cli
```

Interactive menu to test all features:
```
MAIN MENU
1. Find side effects of a drug (Feature 1)
2. Check drug interactions (Feature 2)
3. Analyze drug image with OCR (Feature 3)
4. Analyze text for drugs (Feature 3 - text only)
5. Exit
```

#### Option B: Web Server

```bash
python main.py
```

Access at: http://127.0.0.1:5001

## 📊 Dataset Structure

### drug_side_effects.csv
```csv
drug_name,side_effect
aspirin,stomach upset
aspirin,bleeding
ibuprofen,dizziness
...
```

### drug_interactions.csv
```csv
drugA,drugB,interaction_risk
aspirin,warfarin,Dangerous
ibuprofen,paracetamol,Safe
metformin,insulin,Moderate
...
```

## 🧠 How It Works

### Feature 1: Side Effects Prediction

**Training Phase:**
1. Load drug-side effect associations from CSV
2. Encode drug names to numerical IDs using LabelEncoder
3. Create binary matrix for side effects (MultiLabelBinarizer)
4. Train Random Forest classifier (100 trees, max depth 10)
5. Save model and encoders

**Prediction Phase:**
1. User inputs drug name
2. Convert drug name to numerical ID
3. ML model predicts binary side effects vector
4. Convert back to side effect names
5. Return list of predicted side effects

### Feature 2: Interaction Risk Prediction

**Training Phase:**
1. Load drug pair interactions from CSV
2. Encode both drug names to numerical features
3. Encode risk levels (Safe/Moderate/Dangerous)
4. Train Random Forest classifier
5. Save model and encoders

**Prediction Phase:**
1. User inputs two drug names
2. Convert both to numerical features [drugA_id, drugB_id]
3. ML model classifies interaction risk
4. Return risk level with confidence score

### Feature 3: OCR + Drug Analysis

**Pipeline:**
1. Load image file
2. Extract text using Tesseract OCR
3. Parse text to identify drug names (pattern matching)
4. For each drug: run Feature 1 (side effects)
5. If multiple drugs: run Feature 2 (interactions)
6. Return comprehensive analysis

## 📝 Example Usage

### Example 1: Single Drug Analysis

```python
from services.side_effects_analyzer import SideEffectsAnalyzer

analyzer = SideEffectsAnalyzer()
result = analyzer.analyze("aspirin")

# Output:
# {
#   "drug": "Aspirin",
#   "side_effects": ["stomach upset", "bleeding", "nausea", "heartburn"],
#   "count": 4,
#   "message": "Found 4 potential side effects"
# }
```

### Example 2: Drug Interaction Check

```python
from services.interaction_checker import InteractionChecker

checker = InteractionChecker()
result = checker.check(["aspirin", "warfarin"])

# Output:
# {
#   "drugA": "Aspirin",
#   "drugB": "Warfarin",
#   "interaction_risk": "Dangerous",
#   "confidence": "95.2%",
#   "description": "High risk! Do not combine without medical supervision.",
#   "warning": True
# }
```

### Example 3: Image Analysis

```python
from services.image_processor import ImageProcessor

processor = ImageProcessor()
result = processor.extract_and_analyze("prescription.jpg")

# Output:
# {
#   "extracted_text": "Take Aspirin 100mg daily\nIbuprofen 200mg as needed",
#   "detected_drugs": ["Aspirin", "Ibuprofen"],
#   "drugs_count": 2,
#   "drug_analyses": [...],
#   "interaction_check": {...}
# }
```

## 🗂️ Project Structure

```
drug-side-effects-analyzer/
├── data/
│   ├── drug_side_effects.csv      # Training data for Feature 1
│   └── drug_interactions.csv       # Training data for Feature 2
├── src/
│   ├── main.py                     # Main application entry point
│   ├── train_models.py             # ML model training script
│   ├── models/                     # Saved ML models (generated)
│   │   ├── side_effects_model.pkl
│   │   ├── drug_encoder.pkl
│   │   ├── side_effects_encoder.pkl
│   │   ├── interaction_model.pkl
│   │   ├── interaction_drug_encoder.pkl
│   │   └── risk_encoder.pkl
│   ├── services/
│   │   ├── side_effects_analyzer.py   # Feature 1 implementation
│   │   ├── interaction_checker.py      # Feature 2 implementation
│   │   └── image_processor.py          # Feature 3 implementation
│   ├── routes/
│   │   └── api_routes.py              # Flask API endpoints
│   ├── static/                        # CSS/JS for web UI
│   ├── templates/                     # HTML templates
│   └── utils/
│       └── helpers.py                 # Utility functions
├── requirements.txt
└── README.md
```

## 🔧 Configuration

### Model Parameters

Edit in `train_models.py`:

```python
model = RandomForestClassifier(
    n_estimators=100,      # Number of trees (increase for better accuracy)
    max_depth=10,          # Tree depth (increase for complex patterns)
    random_state=42,
    n_jobs=-1              # Use all CPU cores
)
```

### Adding More Drugs

1. Add entries to `data/drug_side_effects.csv`
2. Add interactions to `data/drug_interactions.csv`
3. Re-run training: `python src/train_models.py`

## ⚠️ Important Notes

### Input Validation
- Drug names are case-insensitive
- Unknown drugs will return an error with suggestions
- Handles gracefully when models aren't trained

### Model Limitations
- Predictions are based on training data only
- Not a substitute for professional medical advice
- Accuracy depends on dataset quality and size

### OCR Requirements
- Requires Tesseract OCR to be installed
- Works best with clear, high-contrast images
- Supports multiple image formats (JPG, PNG, etc.)

## 🧪 Testing

### Test Feature 1
```bash
python main.py --cli
# Select option 1
# Enter: aspirin
```

### Test Feature 2
```bash
python main.py --cli
# Select option 2
# Enter: aspirin, warfarin
```

### Test Feature 3
```bash
python main.py --cli
# Select option 4
# Enter: Patient prescribed Aspirin and Ibuprofen
```

## 📈 Model Performance

Based on default dataset (80/20 train-test split):

| Model | Accuracy | Description |
|-------|----------|-------------|
| Side Effects | ~95% | Per-label accuracy for multi-label classification |
| Interactions | ~92% | Classification accuracy for 3 risk levels |

## 🔍 Troubleshooting

### "Models not trained yet"
**Solution:** Run `python src/train_models.py`

### "Drug not found in database"
**Solution:** Add drug to CSV files and retrain models

### "OCR functionality unavailable"
**Solution:** Install Tesseract OCR and pytesseract

### Import errors
**Solution:** Install all dependencies: `pip install -r requirements.txt`

## 🎓 Learning Resources

### Understanding the Code

1. **train_models.py**: Shows complete ML training pipeline with detailed comments
2. **side_effects_analyzer.py**: Demonstrates multi-label classification
3. **interaction_checker.py**: Shows multi-class classification
4. **image_processor.py**: Combines OCR with ML predictions

### ML Concepts Used

- **LabelEncoder**: Converts text labels to numbers
- **MultiLabelBinarizer**: Handles multiple labels per sample
- **Random Forest**: Ensemble learning for robust predictions
- **Train-Test Split**: Evaluates model on unseen data
- **Model Serialization**: Saves trained models with joblib

## 🚀 Next Steps

1. **Expand Dataset**: Add more drugs and interactions
2. **Improve OCR**: Add preprocessing for better text extraction
3. **Web Interface**: Build full Flask UI for easier access
4. **API Integration**: Create REST API for external use
5. **Model Tuning**: Experiment with hyperparameters

## 📄 License

This is an educational project for learning AI/ML concepts in healthcare applications.

## ⚕️ Disclaimer

**This is a demonstration project for educational purposes only.**

- Not intended for medical diagnosis or treatment
- Always consult healthcare professionals for medical advice
- Predictions are based on limited training data
- Not FDA approved or medically validated

---

**Meddi AI** - Built with ❤️ for AI learning and healthcare innovation
