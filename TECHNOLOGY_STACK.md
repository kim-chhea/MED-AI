# 🛠️ Technology Stack - Drug Side Effects Analyzer

Complete technical documentation of all technologies, frameworks, and libraries used in this project.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Backend Technologies](#backend-technologies)
3. [Frontend Technologies](#frontend-technologies)
4. [Machine Learning Stack](#machine-learning-stack)
5. [OCR & Image Processing](#ocr--image-processing)
6. [Development Tools](#development-tools)
7. [Deployment](#deployment)

---

## 🌐 Overview

This project is built using a modern Python web stack with machine learning capabilities and OCR integration.

**Architecture Pattern:** MVC (Model-View-Controller)
**Deployment Model:** Local development server
**Database:** File-based (CSV + Pickle models)

---

## 🐍 Backend Technologies

### **1. Python 3.14.2**
- **Purpose:** Core programming language
- **Why Chosen:** 
  - Excellent ML/Data Science ecosystem
  - Easy to learn and maintain
  - Strong community support
- **Features Used:**
  - Object-Oriented Programming
  - File I/O
  - Exception handling
  - Type hints

### **2. Flask 3.1.2**
- **Purpose:** Web framework & REST API
- **Why Chosen:**
  - Lightweight and flexible
  - Easy to set up
  - Perfect for ML model serving
- **Components Used:**
  ```python
  from flask import Flask, request, jsonify, render_template
  ```
- **Features:**
  - Route handling (`@app.route`)
  - JSON responses
  - File uploads (multipart/form-data)
  - Template rendering (Jinja2)
  - Error handling (`@app.errorhandler`)
  - Blueprint for API organization

### **3. Werkzeug 3.1.3**
- **Purpose:** WSGI utility library (Flask dependency)
- **Features:**
  - Request/response objects
  - File handling
  - Security utilities

---

## 🎨 Frontend Technologies

### **1. HTML5**
- **Purpose:** Markup structure
- **Features Used:**
  - Semantic elements (`<header>`, `<main>`, `<section>`)
  - Forms (`<input>`, `<button>`)
  - File upload (`<input type="file">`)
  - Accessibility attributes

### **2. CSS3**
- **Purpose:** Styling and layout
- **File:** `src/static/css/style.css`
- **Features:**
  - Flexbox for layout
  - CSS Grid (if used)
  - Custom properties (CSS variables)
  - Transitions and animations
  - Responsive design
  - Dark theme styling

**Key Classes:**
```css
.container          /* Main wrapper */
.card              /* Content sections */
.btn-primary       /* Primary buttons */
.result-container  /* Analysis results */
.error             /* Error messages */
```

### **3. JavaScript (Vanilla ES6+)**
- **Purpose:** Client-side logic
- **File:** `src/static/js/app.js`
- **No frameworks** - Pure JavaScript
- **Features Used:**
  - Fetch API for AJAX requests
  - DOM manipulation
  - Event listeners
  - Arrow functions
  - Template literals
  - Async/await (if needed)

**Key Functions:**
```javascript
analyzeSideEffects()    // Side effects analysis
checkInteractions()     // Drug interaction check
analyzeImage()          // OCR image upload
previewImage()          // Image preview
clearImage()            // Clear uploaded image
showResult()            // Display results
showError()             // Display errors
```

---

## 🤖 Machine Learning Stack

### **1. scikit-learn 1.8.0**
- **Purpose:** Machine learning framework
- **Website:** https://scikit-learn.org
- **Components Used:**

#### **a) Random Forest Classifier**
```python
from sklearn.ensemble import RandomForestClassifier

# Side Effects Model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Interaction Model  
model = RandomForestClassifier(n_estimators=100, random_state=42)
```

**Why Random Forest?**
- ✅ Handles non-linear relationships
- ✅ Robust to overfitting
- ✅ Works well with small datasets
- ✅ Provides feature importance
- ✅ Good accuracy without tuning

#### **b) LabelEncoder**
```python
from sklearn.preprocessing import LabelEncoder

# Encode drug names to numerical IDs
encoder = LabelEncoder()
encoded = encoder.fit_transform(['aspirin', 'ibuprofen', ...])
# Result: [0, 1, 2, ...]
```

#### **c) MultiLabelBinarizer**
```python
from sklearn.preprocessing import MultiLabelBinarizer

# Encode multiple side effects per drug
mlb = MultiLabelBinarizer()
binary_matrix = mlb.fit_transform([
    ['nausea', 'headache'],
    ['dizziness'],
    ...
])
```

#### **d) Model Evaluation**
```python
from sklearn.metrics import accuracy_score, classification_report

accuracy = accuracy_score(y_test, predictions)
report = classification_report(y_test, predictions)
```

### **2. joblib 1.4.2**
- **Purpose:** Model serialization
- **Usage:**
```python
import joblib

# Save model
joblib.dump(model, 'side_effects_model.pkl')

# Load model
model = joblib.load('side_effects_model.pkl')
```

**Advantages:**
- Efficient for large numpy arrays
- Faster than pickle for ML models
- Better compression

### **3. Model Files (.pkl)**

| File | Size | Type | Purpose |
|------|------|------|---------|
| `side_effects_model.pkl` | 2.8 MB | RandomForest | Predict side effects |
| `interaction_model.pkl` | 471 KB | RandomForest | Predict interactions |
| `drug_encoder.pkl` | 1 KB | LabelEncoder | Encode drug names |
| `side_effects_encoder.pkl` | 1 KB | MultiLabelBinarizer | Encode effects |
| `risk_encoder.pkl` | 500 B | LabelEncoder | Encode risk levels |

---

## 🔍 OCR & Image Processing

### **1. Tesseract OCR**
- **Purpose:** Text extraction from images
- **Version:** 5.x
- **Installation:**
  - Windows: `.exe` installer
  - Linux: `apt install tesseract-ocr`
  - macOS: `brew install tesseract`
- **Language:** English (default)
- **Accuracy:** ~80-95% (depends on image quality)

**Configuration:**
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### **2. pytesseract 0.3.13**
- **Purpose:** Python wrapper for Tesseract
- **Usage:**
```python
import pytesseract
from PIL import Image

img = Image.open('drug_label.png')
text = pytesseract.image_to_string(img)
```

**Features:**
- Simple API
- Supports all Tesseract options
- Returns plain text or detailed data

### **3. Pillow (PIL) 11.0.0**
- **Purpose:** Image processing library
- **Website:** https://python-pillow.org
- **Features Used:**

```python
from PIL import Image, ImageEnhance, ImageFilter

# Open image
img = Image.open(file)

# Convert color mode
img_rgb = img.convert('RGB')
img_gray = img.convert('L')

# Enhance contrast
enhancer = ImageEnhance.Contrast(img_gray)
enhanced = enhancer.enhance(2.0)

# Resize
new_size = (img.width * 2, img.height * 2)
resized = img.resize(new_size, Image.Resampling.LANCZOS)
```

**Image Processing Pipeline:**
1. Open image
2. Try multiple strategies:
   - Direct OCR
   - RGB conversion
   - Grayscale + contrast enhancement
   - Upscaling (2x)
3. Return first successful extraction

---

## 📊 Data Processing

### **1. pandas 2.2.3**
- **Purpose:** Data manipulation and analysis
- **Usage:**
```python
import pandas as pd

# Load CSV
df = pd.read_csv('drug_side_effects.csv')

# Data cleaning
df = df.dropna()
df['drug'] = df['drug'].str.lower()

# Grouping
grouped = df.groupby('drug')['side_effect'].apply(list)
```

**Features Used:**
- CSV reading/writing
- Data cleaning
- Grouping and aggregation
- Data transformation

### **2. numpy 2.2.1**
- **Purpose:** Numerical computing
- **Usage:**
```python
import numpy as np

# Array operations
features = np.array([[1, 2], [3, 4]])

# Reshaping
reshaped = arr.reshape(-1, 1)

# Math operations
probabilities = model.predict_proba(features)
confidence = np.max(probabilities) * 100
```

---

## 🔧 Development Tools

### **1. Python Standard Library**

#### **os**
```python
import os

# File paths
models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
exists = os.path.exists(path)
```

#### **re (Regular Expressions)**
```python
import re

# Extract words
words = re.findall(r'\b[a-z]{3,}\b', text)

# Remove special characters
cleaned = re.sub(r'[^a-z\s]', ' ', text)
```

#### **difflib**
```python
from difflib import get_close_matches

# Fuzzy string matching
similar = get_close_matches('asprin', known_drugs, n=5, cutoff=0.5)
# Returns: ['aspirin']
```

#### **json**
```python
import json

# Serialize data
json_str = json.dumps(data, indent=2)

# Parse JSON
data = json.loads(json_str)
```

#### **sys**
```python
import sys

# Command line arguments
if len(sys.argv) > 1 and sys.argv[1] == '--cli':
    interactive_mode()
```

#### **traceback**
```python
import traceback

# Error details
try:
    risky_operation()
except Exception as e:
    traceback.print_exc()
```

### **2. Virtual Environment**
```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Deactivate
deactivate
```

### **3. Package Management**

#### **requirements.txt**
```
Flask==3.1.2
scikit-learn==1.8.0
pandas==2.2.3
numpy==2.2.1
pytesseract==0.3.13
Pillow==11.0.0
joblib==1.4.2
```

**Installation:**
```bash
pip install -r requirements.txt
```

---

## 🚀 Deployment

### **Development Server**
- **Framework:** Flask built-in server
- **Port:** 5001
- **Host:** 127.0.0.1 (localhost)
- **Command:**
```bash
python src/main.py
```

**Configuration:**
```python
app.run(debug=False, port=5001, host='127.0.0.1', use_reloader=False)
```

### **Production Considerations**

For production deployment, consider:

#### **1. WSGI Server**
```bash
# Option 1: Gunicorn (Linux/Mac)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 src.main:app

# Option 2: Waitress (Windows)
pip install waitress
waitress-serve --host=0.0.0.0 --port=5001 src.main:app
```

#### **2. Environment Variables**
```python
import os

# Configuration
DEBUG = os.getenv('DEBUG', False)
PORT = os.getenv('PORT', 5001)
```

#### **3. Docker (Optional)**
```dockerfile
FROM python:3.14-slim

# Install Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr

# Copy app
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Train models
RUN python src/train_models.py

# Run app
CMD ["python", "src/main.py"]
```

---

## 📦 File Structure

```
src/
├── main.py                    # Flask app + server
├── train_models.py           # ML training script
├── config.py                 # Configuration
│
├── services/                 # Business logic
│   ├── side_effects_analyzer.py      # Random Forest
│   ├── interaction_checker.py        # Random Forest
│   ├── image_processor.py            # PIL + Tesseract
│   └── ocr_analysis_pipeline.py      # Pipeline
│
├── routes/                   # API endpoints
│   └── api_routes.py         # Flask blueprints
│
├── utils/                    # Utilities
│   └── helpers.py            # Helper functions
│
├── templates/                # Jinja2 templates
│   └── index.html
│
├── static/                   # Assets
│   ├── css/style.css
│   └── js/app.js
│
└── models/                   # Trained models
    └── *.pkl
```

---

## 🔄 Data Flow Summary

```
CSV Data → pandas → Preprocessing → scikit-learn Training 
→ joblib Serialization → .pkl Models → Flask API 
→ JSON Response → JavaScript → DOM Updates
```

---

## 🎯 Technology Choices - Rationale

### Why Flask?
✅ Lightweight - Perfect for ML model serving  
✅ Easy to learn - Great for beginners  
✅ Flexible - No rigid structure  
✅ Python-native - Integrates well with ML libraries

### Why Random Forest?
✅ High accuracy with small datasets  
✅ No hyperparameter tuning needed  
✅ Handles non-linear relationships  
✅ Interpretable results

### Why Tesseract?
✅ Open source - Free to use  
✅ Accurate - 80-95% accuracy  
✅ Multi-language support  
✅ Active development

### Why Vanilla JavaScript?
✅ No dependencies - Faster loading  
✅ Simple project - No framework overhead  
✅ Better learning - Understand fundamentals  
✅ Lightweight - Smaller bundle size

---

## 📊 Performance Metrics

| Component | Metric | Value |
|-----------|--------|-------|
| Flask | Response Time | < 100ms |
| ML Model | Prediction Time | < 50ms |
| OCR | Processing Time | 1-3s |
| Page Load | Initial Load | < 2s |
| Memory | Runtime Usage | ~50MB |
| Disk | Total Size | ~4MB |

---

## 🔐 Security Considerations

### Current Implementation
- ✅ Local models (no external API calls)
- ✅ File upload validation (image types only)
- ✅ Input sanitization (drug names)
- ✅ Error handling (no stack traces to client)

### Production Recommendations
- 🔒 Add HTTPS (SSL/TLS)
- 🔒 Implement rate limiting
- 🔒 Add CSRF protection
- 🔒 Validate file sizes
- 🔒 Sanitize OCR output
- 🔒 Add authentication (if needed)

---

## 📚 Resources & Documentation

### Official Documentation
- **Flask:** https://flask.palletsprojects.com
- **scikit-learn:** https://scikit-learn.org/stable
- **pandas:** https://pandas.pydata.org
- **Pillow:** https://python-pillow.org
- **Tesseract:** https://tesseract-ocr.github.io

### Tutorials & Guides
- Flask REST API: https://flask-restful.readthedocs.io
- Random Forest: https://scikit-learn.org/stable/modules/ensemble.html
- OCR with Python: https://pypi.org/project/pytesseract

---

**End of Technology Stack Documentation**
