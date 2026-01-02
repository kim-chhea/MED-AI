# 💊 Drug Side Effects & Interaction Analyzer

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![Tesseract OCR](https://img.shields.io/badge/OCR-Tesseract-orange.svg)](https://github.com/tesseract-ocr/tesseract)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()

> **Intelligent healthcare assistant** that predicts drug side effects (categorized as common/serious), checks dangerous drug interactions with detailed explanations, and extracts drug information from images using **local machine learning models** - no API keys or internet required!

---

## 📋 Table of Contents

- [Features](#-features)
- [System Flow Chart](#-system-flow-chart)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Custom Dataset Training](#-custom-dataset-training)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Performance Metrics](#-performance-metrics)

---

## 🌟 Features

### 🔍 **1. Drug Side Effects Analysis**
- **Smart Categorization**: Separates effects into Common (✓) and Serious (⚠️)
- **Intelligent Search**: Fuzzy matching handles typos (e.g., "asprin" → "aspirin")
- **Instant Results**: No internet required - 100% local processing
- **Visual Display**: Color-coded sections (green for common, red for serious)
- **Coverage**: 30+ drugs with 120+ side effect records

### ⚠️ **2. Drug-Drug Interaction Checker**
- **Risk Assessment**: 🟢 Safe | 🟡 Moderate | 🔴 Dangerous
- **Detailed Explanations**: Clear descriptions of what happens when drugs interact
- **Multi-Drug Analysis**: Check interactions between 2+ medications
- **Smart Suggestions**: Recommends similar drug names for typos
- **Real-time Warnings**: Immediate alerts for dangerous combinations

### 📸 **3. OCR Image Analysis**
- **Text Extraction**: Upload prescription/drug label photos
- **Auto-Detection**: Identifies drug names from messy OCR text
- **Complete Analysis**: Automatically runs side effects + interaction checks
- **Multi-Format Support**: PNG, JPG, JPEG, GIF
- **Fuzzy Matching**: Handles OCR spelling errors intelligently

### 📊 **4. Custom Dataset Training**
- **Upload Your Data**: Train models with your own CSV files
- **Dataset Switching**: Toggle between built-in and custom models
- **Template Downloads**: CSV templates ensure correct format
- **Live Accuracy Metrics**: See training results instantly
- **Separate Model Storage**: Custom and built-in models stored independently

---

## 🔄 System Flow Chart

### **Overall Architecture**
```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│              (Web Browser - Modern UI with Tabs)                 │
└────────────┬────────────────────────────────────────────────────┘
             │
             ├──────────────────────────────────────────────────────┐
             │                                                       │
             ▼                                                       ▼
┌─────────────────────┐                              ┌──────────────────────┐
│  Dataset Manager    │                              │   Main Features      │
│  (Toggle Switch)    │                              │   (3 Tabs)           │
└──────────┬──────────┘                              └──────────┬───────────┘
           │                                                     │
    ┌──────┴──────┐                          ┌─────────────────┼──────────────┐
    │             │                          │                 │               │
    ▼             ▼                          ▼                 ▼               ▼
Built-in      Custom                   Side Effects    Interactions      OCR Image
Dataset       Dataset                   Analyzer         Checker          Analysis
(30 drugs)    (Upload)                      │                │               │
    │             │                          │                │               │
    └──────┬──────┘                          │                │               │
           │                                 │                │               │
           ▼                                 │                │               │
┌─────────────────────┐                     │                │               │
│  Model Config       │                     │                │               │
│  (model_config.json)│                     │                │               │
└──────────┬──────────┘                     │                │               │
           │                                 │                │               │
           ▼                                 │                │               │
┌─────────────────────┐                     │                │               │
│  Flask Backend      │◄────────────────────┴────────────────┴───────────────┘
│  (API Routes)       │
└──────────┬──────────┘
           │
    ┌──────┴──────────────┐
    │                     │
    ▼                     ▼
┌────────────────┐  ┌──────────────────┐
│ ML Services    │  │  Model Files     │
│ - Side Effects │  │  (.pkl files)    │
│ - Interactions │  │                  │
│ - OCR Pipeline │  │  models/         │
└────────────────┘  │  └─ built-in     │
                    │  └─ custom/      │
                    └──────────────────┘
```

### **Feature 1: Side Effects Analysis Flow**
```
User Input (Drug Name)
    │
    ▼
┌─────────────────────┐
│ Frontend Validation │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  POST /api/side-    │
│  effects            │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│ SideEffectsAnalyzer         │
│ 1. Load models (config mode)│
│ 2. Normalize drug name      │
│ 3. Check if exists           │
│ 4. Fuzzy match if not found │
└──────────┬──────────────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
Found         Not Found
    │             │
    ▼             ▼
┌────────────┐  ┌──────────────────┐
│ Predict    │  │ Show suggestions │
│ Side       │  │ (similar names)  │
│ Effects    │  └──────────────────┘
└─────┬──────┘
      │
      ▼
┌────────────────────┐
│ Categorize Effects │
│ - Common (green)   │
│ - Serious (red)    │
└─────────┬──────────┘
          │
          ▼
┌──────────────────┐
│ Return JSON      │
│ to Frontend      │
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│ Display Results  │
│ with Colors      │
└──────────────────┘
```

### **Feature 2: Drug Interaction Flow**
```
User Input (2+ Drug Names)
    │
    ▼
┌─────────────────────┐
│ Frontend Validation │
│ (min 2 drugs)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  POST /api/         │
│  interactions       │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────┐
│ InteractionChecker           │
│ 1. Load models (config mode) │
│ 2. Normalize names           │
│ 3. Check all pairs           │
└──────────┬───────────────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
All Found     Some Missing
    │             │
    ▼             ▼
┌────────────┐  ┌──────────────────┐
│ Predict    │  │ Show suggestions │
│ Risk Level │  │ for unknown drugs│
│ (ML Model) │  └──────────────────┘
└─────┬──────┘
      │
      ▼
┌────────────────────────┐
│ Generate Explanation   │
│ - Safe: No issues      │
│ - Moderate: Monitor    │
│ - Dangerous: AVOID!    │
└─────────┬──────────────┘
          │
          ▼
┌──────────────────┐
│ Return JSON      │
│ with risk level  │
└─────────┬────────┘
          │
          ▼
┌──────────────────────┐
│ Display with Color   │
│ 🟢 Safe 🟡 Moderate │
│ 🔴 Dangerous         │
└──────────────────────┘
```

### **Feature 3: OCR Image Analysis Flow**
```
User Upload (Image File)
    │
    ▼
┌─────────────────────┐
│ Validate File Type  │
│ (PNG/JPG/JPEG/GIF)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  POST /api/         │
│  analyze-image      │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────┐
│ OCRAnalysisPipeline          │
│ 1. Save temp file            │
│ 2. Run Tesseract OCR         │
│ 3. Extract text              │
└──────────┬───────────────────┘
           │
           ▼
┌────────────────────────┐
│ Parse OCR Text         │
│ - Split by whitespace  │
│ - Fuzzy match vs drugs │
│ - Filter valid matches │
└─────────┬──────────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
Drugs Found   No Drugs
    │           │
    ▼           ▼
┌──────────┐  ┌─────────────┐
│ Run Both │  │ Return Error│
│ Features:│  └─────────────┘
│ 1. Side  │
│   Effects│
│ 2. Inter-│
│   actions│
└────┬─────┘
     │
     ▼
┌────────────────┐
│ Combine Results│
│ & Display      │
└────────────────┘
```

### **Custom Dataset Training Flow**
```
User Action: Toggle to Custom
    │
    ▼
┌─────────────────────┐
│ POST /api/switch-   │
│ dataset-mode        │
│ {mode: "custom"}    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Create/Update       │
│ model_config.json   │
│ {mode: "custom"}    │
└──────────┬──────────┘
           │
           ▼
User Uploads CSV Files
    │
    ├─► Side Effects CSV
    └─► Interactions CSV
           │
           ▼
┌─────────────────────┐
│ POST /api/upload-   │
│ dataset             │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Validate CSV Format │
│ - Check columns     │
│ - Count records     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Save to uploads/    │
│ custom_*.csv        │
└──────────┬──────────┘
           │
           ▼
User Clicks "Train Models"
           │
           ▼
┌─────────────────────┐
│ POST /api/retrain-  │
│ models              │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────┐
│ train_models.py              │
│ (custom=True)                │
│ 1. Load custom CSVs          │
│ 2. Train Random Forest       │
│ 3. Calculate accuracy        │
│ 4. Save to models/custom/    │
└──────────┬───────────────────┘
           │
           ▼
┌─────────────────────┐
│ Display Accuracy    │
│ - Side Effects: %   │
│ - Interactions: %   │
└──────────┬──────────┘
           │
           ▼
Next Predictions Use Custom Models
```

---

## 🛠️ Technology Stack

### **Backend**
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.14+ | Core programming language |
| **Flask** | 3.1.2 | Web framework & REST API |
| **scikit-learn** | 1.8.0 | Machine learning models |
| **pandas** | 2.2.3 | Data processing & CSV handling |
| **numpy** | 2.2.1 | Numerical computations |
| **joblib** | 1.4.2 | Model serialization |

### **OCR & Image Processing**
| Technology | Purpose |
|------------|---------|
| **Tesseract OCR** | Text extraction from images |
| **pytesseract** | Python wrapper for Tesseract |
| **Pillow (PIL)** | Image preprocessing & enhancement |

### **Frontend**
| Technology | Purpose |
|------------|---------|
| **HTML5** | Structure & semantic markup |
| **CSS3** | Styling & responsive design |
| **JavaScript (Vanilla)** | DOM manipulation & API calls |
| **Fetch API** | AJAX requests |

### **Machine Learning**
- **Algorithm**: Random Forest Classifier
- **Encoding**: LabelEncoder for categorical data
- **Training**: Supervised learning on CSV datasets
- **Serialization**: Pickle (.pkl) for model persistence

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                         │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────┐        │
│  │Side      │  │Interactions  │  │Image Analysis  │        │
│  │Effects   │  │Checker       │  │& OCR           │        │
│  └────┬─────┘  └──────┬───────┘  └────────┬───────┘        │
└───────┼────────────────┼──────────────────┼────────────────┘
        │                │                   │
        │                │                   │
┌───────▼────────────────▼───────────────────▼────────────────┐
│                   FLASK WEB SERVER                          │
│                 (main.py - Port 5001)                       │
└───────┬────────────────┬───────────────────┬────────────────┘
        │                │                   │
        ▼                ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐
│Side Effects  │  │Interaction   │  │Image Processor       │
│Analyzer      │  │Checker       │  │+ OCR Pipeline        │
│              │  │              │  │                      │
│• Drug lookup │  │• Risk calc   │  │• Text extraction     │
│• Prediction  │  │• Pairwise    │  │• Drug detection      │
│• Categorize  │  │• Explanation │  │• Auto-analysis       │
└──────┬───────┘  └──────┬───────┘  └──────┬───────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│              MACHINE LEARNING MODELS (.pkl)                 │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐  │
│  │Side Effects    │  │Interaction     │  │Encoders      │  │
│  │Model (RF)      │  │Model (RF)      │  │(Label)       │  │
│  │2.8 MB          │  │471 KB          │  │1-2 KB each   │  │
│  └────────────────┘  └────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA SOURCES                            │
│  ┌────────────────────────┐  ┌──────────────────────────┐  │
│  │drug_side_effects.csv   │  │drug_interactions.csv     │  │
│  │120 records, 30 drugs   │  │85 records, 30 drugs      │  │
│  └────────────────────────┘  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Process Flow

### **1. Side Effects Analysis Flow**

```
User Input → Normalize → Database Lookup → Encode → ML Predict 
→ Decode → Categorize (Common/Serious) → Display Results
```

**Detailed Flow:**
```
┌─────────────┐
│ User Input  │ → "aspirin"
└──────┬──────┘
       │
       ▼
┌────────────────────────────┐
│ Normalize & Validate       │
│ • Lowercase                │
│ • Trim whitespace          │
└──────┬─────────────────────┘
       │
       ▼
┌────────────────────────────┐
│ Check Database             │
│ • Exact match?             │
│ • No? → Fuzzy matching     │
└──────┬─────────────────────┘
       │
       ├─── Found ────────────┐
       │                      ▼
       │           ┌────────────────────┐
       │           │ Encode Drug Name   │
       │           │ (LabelEncoder)     │
       │           └──────┬─────────────┘
       │                  │
       │                  ▼
       │           ┌────────────────────┐
       │           │ ML Model Predict   │
       │           │ (Random Forest)    │
       │           └──────┬─────────────┘
       │                  │
       │                  ▼
       │           ┌────────────────────┐
       │           │ Decode Predictions │
       │           │ (Side Effects)     │
       │           └──────┬─────────────┘
       │                  │
       │                  ▼
       │           ┌────────────────────┐
       │           │ Categorize Effects │
       │           │ • Common (green)   │
       │           │ • Serious (red)    │
       │           └──────┬─────────────┘
       │                  │
       └──────────────────┼───────────────┐
                          │               │
                          ▼               ▼
                    ┌──────────┐    ┌──────────┐
                    │ Display  │    │ Error +  │
                    │ Results  │    │ Suggest  │
                    └──────────┘    └──────────┘
```

### **2. Drug Interaction Flow**

```
User Input (2 drugs) → Validate → Database Lookup → Encode Both 
→ ML Predict Risk → Generate Explanation → Display Risk + Details
```

### **3. OCR Image Analysis Flow**

```
Upload Image → Preview → Preprocess → Tesseract OCR → Clean Text 
→ Detect Drugs → Analyze (Side Effects/Interactions) → Display All
```

---

## 🚀 Installation

### **Step 1: Install Tesseract OCR**

**Windows:**
- Download: https://github.com/UB-Mannheim/tesseract/wiki
- Run installer → Install to `C:\Program Files\Tesseract-OCR`
- ✓ Add to PATH during installation

**Linux:**
```bash
sudo apt install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

### **Step 2: Clone Repository**

```bash
git clone https://github.com/YOUR_USERNAME/drug-side-effects-analyzer.git
cd drug-side-effects-analyzer
```

### **Step 3: Setup Python Environment**

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **Step 4: Train Models**

```bash
python src/train_models.py
# Takes ~10-30 seconds
# Output: Models saved to src/models/
```

### **Step 5: Start Server**

```bash
python src/main.py
 C:/Users/DELL/Desktop/drug-side-effects-analyzer/venv/Scripts/python.exe src/main.py
# Open: http://127.0.0.1:5001
```

---

## 💡 Usage

### **Web Interface**

**Side Effects:**
1. Go to "Side Effects" tab
2. Enter "aspirin"
3. Click "Analyze"
4. View Common (green) + Serious (red) effects

**Interactions:**
1. Go to "Interactions" tab
2. Add "aspirin" → Press Enter
3. Add "warfarin" → Press Enter
4. Click "Analyze Interactions"
5. Read detailed explanation

**Image Analysis:**
1. Go to "Image Analysis" tab
2. Upload drug label photo
3. Click "Extract & Analyze Text"
4. View OCR + drugs + analysis

---

## 📂 Project Structure

```
drug-side-effects-analyzer/
├── README.md                  # This file
├── requirements.txt           # Dependencies
├── data/                      # CSV datasets
│   ├── drug_side_effects.csv
│   └── drug_interactions.csv
├── src/
│   ├── main.py               # Flask server
│   ├── train_models.py       # ML training
│   ├── services/             # Core logic
│   │   ├── side_effects_analyzer.py
│   │   ├── interaction_checker.py
│   │   ├── image_processor.py
│   │   └── ocr_analysis_pipeline.py
│   ├── routes/               # API endpoints
│   ├── templates/            # HTML
│   ├── static/               # CSS/JS
│   └── models/               # Trained models
├── docs/                     # Documentation
└── tests/                    # Test scripts
```

---

## 🔌 API Documentation

### **Base URL:** `http://127.0.0.1:5001`

### **Endpoints:**

**1. Side Effects**
```http
POST /api/side-effects
Content-Type: application/json

{
  "drug_name": "aspirin"
}
```

**2. Interactions**
```http
POST /api/interactions
Content-Type: application/json

{
  "drug_list": ["aspirin", "warfarin"]
}
```

**3. Image Analysis**
```http
POST /api/analyze-image
Content-Type: multipart/form-data

file: <image_file>
```

---

## 📊 Performance Metrics

| Model | Accuracy | Records | Drugs |
|-------|----------|---------|-------|
| Side Effects | 86.23% | 120 | 30 |
| Interactions | 41.18% | 85 | 30 |

**System Performance:**
- Response Time: < 100ms
- OCR Processing: 1-3s
- Memory Usage: ~50MB

---

## 🐛 Troubleshooting

**Tesseract Not Found:**
```bash
# Install Tesseract and add to PATH
# Restart terminal
```

**Models Not Found:**
```bash
python src/train_models.py
```

**Port Already in Use:**
- Change port in `src/main.py`

---

## ⚠️ Disclaimer

**Educational project - NOT for medical diagnosis**
- Consult healthcare professionals
- Limited drug database
- ML predictions are estimates

---

## 📝 License

MIT License - Open Source

---

## 🎓 Learning Outcomes

- ✅ Machine Learning (Random Forest, scikit-learn)
- ✅ Web Development (Flask, REST APIs)
- ✅ OCR Technology (Tesseract)
- ✅ Data Science (pandas, numpy)
- ✅ Frontend (HTML/CSS/JavaScript)

---

<div align="center">

**Built with ❤️ for Healthcare & Education**

⭐ Star this repo if you found it helpful! ⭐

</div>
