# 🔄 Drug Side Effects Analyzer - Process Flowcharts

This document provides detailed visual flowcharts for all major processes in the application.

---

## 📊 Table of Contents

1. [System Overview](#system-overview)
2. [Side Effects Analysis Flow](#side-effects-analysis-flow)
3. [Drug Interaction Check Flow](#drug-interaction-check-flow)
4. [OCR Image Analysis Flow](#ocr-image-analysis-flow)
5. [Data Flow Architecture](#data-flow-architecture)

---

## 🏗️ System Overview

### High-Level Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                        USER LAYER                             │
│                                                               │
│   Web Browser → HTML/CSS/JavaScript → Fetch API              │
└───────────────┬───────────────────────────────────────────────┘
                │
                │ HTTP Requests (JSON/FormData)
                ▼
┌───────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                          │
│                                                               │
│   Flask Web Server (Port 5001)                               │
│   ├── Routes (api_routes.py)                                 │
│   ├── Request Validation                                     │
│   └── Response Formatting                                    │
└───────────────┬───────────────────────────────────────────────┘
                │
                │ Service Calls
                ▼
┌───────────────────────────────────────────────────────────────┐
│                     SERVICE LAYER                             │
│                                                               │
│   ┌──────────────────┐ ┌────────────────┐ ┌──────────────┐  │
│   │ Side Effects     │ │ Interaction    │ │ Image        │  │
│   │ Analyzer         │ │ Checker        │ │ Processor    │  │
│   │                  │ │                │ │              │  │
│   │ • Normalize      │ │ • Validate     │ │ • OCR        │  │
│   │ • Fuzzy match    │ │ • Encode       │ │ • Extract    │  │
│   │ • Predict        │ │ • Predict      │ │ • Analyze    │  │
│   │ • Categorize     │ │ • Explain      │ │              │  │
│   └──────────────────┘ └────────────────┘ └──────────────┘  │
└───────────────┬───────────────┬──────────────┬────────────────┘
                │               │              │
                │ Model Calls   │              │ Pipeline Call
                ▼               ▼              ▼
┌───────────────────────────────────────────────────────────────┐
│                      MODEL LAYER                              │
│                                                               │
│   ┌──────────────────────────────────────────────────────┐   │
│   │  Trained Machine Learning Models (.pkl files)        │   │
│   │                                                       │   │
│   │  • side_effects_model.pkl (Random Forest)            │   │
│   │  • interaction_model.pkl (Random Forest)             │   │
│   │  • drug_encoder.pkl (LabelEncoder)                   │   │
│   │  • side_effects_encoder.pkl (MultiLabelBinarizer)    │   │
│   │  • risk_encoder.pkl (LabelEncoder)                   │   │
│   └──────────────────────────────────────────────────────┘   │
└───────────────┬───────────────────────────────────────────────┘
                │
                │ Training Data
                ▼
┌───────────────────────────────────────────────────────────────┐
│                       DATA LAYER                              │
│                                                               │
│   CSV Files (data/)                                           │
│   ├── drug_side_effects.csv  (120 records)                   │
│   └── drug_interactions.csv  (85 records)                    │
└───────────────────────────────────────────────────────────────┘
```

---

## 🔍 Side Effects Analysis Flow

### Complete Process Flow

```
START
  │
  ▼
┌─────────────────────────────────────┐
│ 1. USER INPUT                       │
│    • User enters drug name          │
│    • Example: "aspirin"             │
│    • Frontend validates non-empty   │
└────────────┬────────────────────────┘
             │
             │ POST /api/side-effects
             │ { drug_name: "aspirin" }
             ▼
┌─────────────────────────────────────┐
│ 2. FLASK ROUTE HANDLER              │
│    • Receive JSON request           │
│    • Extract drug_name              │
│    • Call analyzer service          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 3. NORMALIZE INPUT                  │
│    • Convert to lowercase           │
│    • Trim whitespace                │
│    • Remove special characters      │
│    Result: "aspirin"                │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 4. DATABASE LOOKUP                  │
│    • Check if drug in encoder       │
│    • 30 drugs available             │
└────────────┬────────────────────────┘
             │
             ├─── FOUND ──────────────┬─── NOT FOUND ────┐
             │                        │                   │
             ▼                        ▼                   ▼
┌──────────────────────┐  ┌─────────────────────┐  ┌──────────────┐
│ 5A. ENCODE DRUG      │  │ 5B. FUZZY MATCHING  │  │ 5C. ERROR    │
│     • LabelEncoder   │  │     • get_close     │  │     • Return │
│     • drug → ID      │  │       _matches()    │  │       error  │
│     Result: 3        │  │     • Cutoff: 50%   │  │     • Suggest│
└──────────┬───────────┘  └──────────┬──────────┘  └──────────────┘
           │                         │
           │              ┌──────────┴──────────┐
           │              │ Found: "aspirin"    │
           │              │ Suggest to user     │
           │              └─────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ 6. ML MODEL PREDICTION              │
│    • Load Random Forest model       │
│    • Input: [drug_id]               │
│    • Predict: binary array          │
│    Result: [1,0,1,1,0,...]          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 7. DECODE PREDICTIONS               │
│    • MultiLabelBinarizer            │
│    • Binary → Side effect names     │
│    Result: ["nausea", "heartburn",  │
│             "stomach pain"]         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 8. CATEGORIZE EFFECTS               │
│    • Check keywords in each effect  │
│    • Serious keywords:              │
│      - death, cardiac, liver, etc.  │
│    • Split into:                    │
│      - common_effects: []           │
│      - serious_effects: []          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 9. FORMAT RESPONSE                  │
│    {                                │
│      drug: "Aspirin",               │
│      count: 3,                      │
│      common_effects: ["nausea"],    │
│      serious_effects: ["bleeding"], │
│      common_count: 2,               │
│      serious_count: 1               │
│    }                                │
└────────────┬────────────────────────┘
             │
             │ JSON Response
             ▼
┌─────────────────────────────────────┐
│ 10. DISPLAY RESULTS                 │
│     • Parse JSON                    │
│     • Render HTML sections:         │
│       - Common (green background)   │
│       - Serious (red background)    │
│     • Show counts                   │
└─────────────────────────────────────┘
  │
  ▼
END
```

### Decision Tree for Drug Lookup

```
Drug Name Input
       │
       ▼
   Normalize
       │
       ▼
    ┌──────────────┐
    │ In Database? │
    └──────┬───────┘
           │
      ┌────┴────┐
      │         │
     YES       NO
      │         │
      │         ▼
      │    ┌─────────────────┐
      │    │ Fuzzy Match     │
      │    │ Threshold: 50%  │
      │    └────┬────────────┘
      │         │
      │    ┌────┴────┐
      │    │         │
      │   Found   Not Found
      │    │         │
      │    ▼         ▼
      │  Suggest   Show Error
      │  Similar   + Top 10
      │  Drugs     Drugs List
      │    │
      └────┴───────┐
                   │
                   ▼
              Proceed to
              Prediction
```

---

## ⚠️ Drug Interaction Check Flow

### Complete Process Flow

```
START
  │
  ▼
┌─────────────────────────────────────┐
│ 1. USER INPUT                       │
│    • User adds drug tags            │
│    • Example: ["aspirin","warfarin"]│
│    • Minimum: 2 drugs required      │
└────────────┬────────────────────────┘
             │
             │ POST /api/interactions
             │ { drug_list: [...] }
             ▼
┌─────────────────────────────────────┐
│ 2. VALIDATE INPUT                   │
│    • Check array length >= 2        │
│    • Normalize all drug names       │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 3. LOOKUP BOTH DRUGS                │
│    DrugA: "aspirin"                 │
│    DrugB: "warfarin"                │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 4. VALIDATE BOTH IN DATABASE        │
│    • Check DrugA exists             │
│    • Check DrugB exists             │
└────────────┬────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
 FOUND           NOT FOUND
    │                 │
    ▼                 ▼
┌────────────┐  ┌─────────────────┐
│ Continue   │  │ Fuzzy Match     │
│            │  │ Suggest Similar │
└─────┬──────┘  └─────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│ 5. ENCODE BOTH DRUGS                │
│    • DrugA_ID = encoder.transform() │
│    • DrugB_ID = encoder.transform() │
│    Result: [3, 15]                  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 6. CREATE FEATURE VECTOR            │
│    features = [[drugA_id, drugB_id]]│
│    Example: [[3, 15]]               │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 7. ML MODEL PREDICTION              │
│    • Random Forest Classifier       │
│    • Input: [[3, 15]]               │
│    • Predict: risk_level            │
│    • Get probability confidence     │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 8. DECODE RISK LEVEL                │
│    • LabelEncoder inverse           │
│    • 0 → "Safe"                     │
│    • 1 → "Moderate"                 │
│    • 2 → "Dangerous"                │
│    Result: "Dangerous"              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 9. GENERATE EXPLANATION             │
│    • Call get_detailed_explanation()│
│    • Based on risk level:           │
│      - Dangerous: Severe warnings   │
│      - Moderate: Caution advised    │
│      - Safe: Minimal risk           │
│    • Explain health impacts         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 10. FORMAT RESPONSE                 │
│     {                               │
│       drugA: "Aspirin",             │
│       drugB: "Warfarin",            │
│       interaction_risk: "Dangerous",│
│       confidence: "95.3%",          │
│       description: "Taking both...",│
│       warning: true                 │
│     }                               │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 11. DISPLAY RESULTS                 │
│     • Show risk icon (🔴/🟡/🟢)     │
│     • Display drug names            │
│     • Show risk level (colored)     │
│     • Render detailed explanation   │
│     • Show warning if dangerous     │
└─────────────────────────────────────┘
  │
  ▼
END
```

### Risk Level Decision Matrix

```
┌────────────────────────────────────────────────────────┐
│            ML MODEL OUTPUT → RISK LEVEL                │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Prediction = 0  →  🟢 SAFE                           │
│  │                                                     │
│  │  Example: "Aspirin + Ibuprofen"                    │
│  │  Explanation: "Can generally be taken together"    │
│  │  Action: Monitor for side effects                  │
│                                                        │
│  Prediction = 1  →  🟡 MODERATE                       │
│  │                                                     │
│  │  Example: "Aspirin + Antacids"                     │
│  │  Explanation: "May reduce effectiveness"           │
│  │  Action: Consult doctor, adjust timing            │
│                                                        │
│  Prediction = 2  →  🔴 DANGEROUS                      │
│  │                                                     │
│  │  Example: "Aspirin + Warfarin"                     │
│  │  Explanation: "Serious bleeding risk"              │
│  │  Action: DO NOT COMBINE without supervision       │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 📸 OCR Image Analysis Flow

### Complete Process Flow

```
START
  │
  ▼
┌─────────────────────────────────────┐
│ 1. USER UPLOADS IMAGE               │
│    • Drag & drop OR click browse    │
│    • Supported: PNG, JPG, JPEG, GIF │
│    • Max size: 16MB                 │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 2. PREVIEW IMAGE                    │
│    • FileReader API reads file      │
│    • Display thumbnail              │
│    • Show "Extract & Analyze" btn   │
└────────────┬────────────────────────┘
             │
             │ Click "Extract & Analyze"
             ▼
┌─────────────────────────────────────┐
│ 3. SEND TO BACKEND                  │
│    • FormData with file             │
│    • POST /api/analyze-image        │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 4. IMAGE PREPROCESSING              │
│    • Open image with PIL            │
│    • Try multiple strategies:       │
│      a) Direct OCR                  │
│      b) Convert to RGB              │
│      c) Grayscale + contrast        │
│      d) Resize (2x larger)          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 5. TESSERACT OCR                    │
│    • pytesseract.image_to_string()  │
│    • Extract all text from image    │
│    Raw Output:                      │
│    "ASPIRIN 75 mg                   │
│     GASTRO-RESISTANT TABLETS        │
│     Enteric-Coated                  │
│     56 Tablets"                     │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 6. CLEAN OCR TEXT                   │
│    • Convert to lowercase           │
│    • Remove special characters      │
│    • Collapse multiple spaces       │
│    Result: "aspirin 75 mg gastro..."│
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 7. DRUG NAME DETECTION              │
│    Step 1: EXACT MATCH              │
│    • Check if known drug in text    │
│    • Use word boundaries            │
│                                     │
│    Step 2: FUZZY MATCH              │
│    • Extract words (3+ chars)       │
│    • Match against database (70%)   │
│    • Handle OCR errors              │
│    Result: ["aspirin"]              │
└────────────┬────────────────────────┘
             │
             ▼
        ┌────┴────┐
        │         │
     0 Drugs   1+ Drugs
        │         │
        ▼         ▼
   ┌─────────┐  ┌──────────────────┐
   │ ERROR   │  │ ANALYZE DRUGS    │
   │ Message │  │                  │
   └─────────┘  └────┬─────────────┘
                     │
              ┌──────┴──────┐
              │             │
           1 Drug        2 Drugs
              │             │
              ▼             ▼
    ┌──────────────┐  ┌──────────────┐
    │ Side Effects │  │ Interactions │
    │ Analysis     │  │ Check        │
    │ (Flow 1)     │  │ (Flow 2)     │
    │     +        │  │     +        │
    │ (Common/     │  │ Side Effects │
    │  Serious)    │  │ for each     │
    └──────┬───────┘  └──────┬───────┘
           │                 │
           └────────┬────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│ 8. FORMAT COMPLETE RESPONSE         │
│    {                                │
│      extracted_text: "...",         │
│      detected_drugs: ["Aspirin"],   │
│      drug_analyses: [               │
│        {                            │
│          drug: "Aspirin",           │
│          common_effects: [...],     │
│          serious_effects: [...]     │
│        }                            │
│      ],                             │
│      interaction_check: {...}       │
│    }                                │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 9. DISPLAY COMPREHENSIVE RESULTS    │
│    • Show extracted OCR text        │
│    • List detected drugs            │
│    • Display side effects           │
│      (Common in green)              │
│      (Serious in red)               │
│    • Show interaction warnings      │
│    • Render risk explanation        │
└─────────────────────────────────────┘
  │
  ▼
END
```

### OCR Multi-Strategy Approach

```
┌────────────────────────────────────────────────────┐
│              OCR EXTRACTION STRATEGIES             │
├────────────────────────────────────────────────────┤
│                                                    │
│  Strategy 1: DIRECT OCR                           │
│  ├─ Use original image                            │
│  └─ Best for: Clear, high-resolution images       │
│                                                    │
│  Strategy 2: RGB CONVERSION                       │
│  ├─ Convert RGBA/other → RGB                      │
│  └─ Best for: PNG with transparency               │
│                                                    │
│  Strategy 3: GRAYSCALE + CONTRAST                 │
│  ├─ Convert to grayscale                          │
│  ├─ Enhance contrast (2x)                         │
│  └─ Best for: Low contrast images                 │
│                                                    │
│  Strategy 4: RESIZE (2x)                          │
│  ├─ Upscale image (2x larger)                     │
│  ├─ Use Lanczos resampling                        │
│  └─ Best for: Small text, low resolution          │
│                                                    │
│  → Try strategies sequentially until text found   │
│  → Return first successful extraction             │
└────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Architecture

### Training Phase (One-Time Setup)

```
┌──────────────────────────────────┐
│  CSV Files (data/)               │
│  • drug_side_effects.csv         │
│  • drug_interactions.csv         │
└────────────┬─────────────────────┘
             │
             │ Load & Parse
             ▼
┌──────────────────────────────────┐
│  pandas DataFrames               │
│  • Clean data                    │
│  • Handle missing values         │
└────────────┬─────────────────────┘
             │
             │ Encode
             ▼
┌──────────────────────────────────┐
│  Feature Engineering             │
│  • LabelEncoder (drugs)          │
│  • MultiLabelBinarizer (effects) │
└────────────┬─────────────────────┘
             │
             │ Split Data
             ▼
┌──────────────────────────────────┐
│  Train/Test Split                │
│  • 80% training                  │
│  • 20% testing                   │
└────────────┬─────────────────────┘
             │
             │ Train
             ▼
┌──────────────────────────────────┐
│  Random Forest Training          │
│  • n_estimators: 100             │
│  • Fit on training data          │
└────────────┬─────────────────────┘
             │
             │ Evaluate
             ▼
┌──────────────────────────────────┐
│  Model Evaluation                │
│  • Calculate accuracy            │
│  • Print metrics                 │
└────────────┬─────────────────────┘
             │
             │ Save Models
             ▼
┌──────────────────────────────────┐
│  Serialize to .pkl Files         │
│  • joblib.dump()                 │
│  • Save to src/models/           │
└──────────────────────────────────┘
```

### Prediction Phase (Runtime)

```
┌──────────────────────────────────┐
│  Load Trained Models             │
│  • joblib.load()                 │
│  • Load on server startup        │
└────────────┬─────────────────────┘
             │
             │ User Request
             ▼
┌──────────────────────────────────┐
│  Preprocess Input                │
│  • Normalize                     │
│  • Validate                      │
└────────────┬─────────────────────┘
             │
             │ Encode
             ▼
┌──────────────────────────────────┐
│  Transform to Model Input        │
│  • Use same encoders             │
│  • Convert to numerical          │
└────────────┬─────────────────────┘
             │
             │ Predict
             ▼
┌──────────────────────────────────┐
│  ML Model Prediction             │
│  • model.predict()               │
│  • model.predict_proba()         │
└────────────┬─────────────────────┘
             │
             │ Decode
             ▼
┌──────────────────────────────────┐
│  Post-processing                 │
│  • Inverse transform             │
│  • Format results                │
│  • Add metadata                  │
└────────────┬─────────────────────┘
             │
             │ Response
             ▼
┌──────────────────────────────────┐
│  JSON Response to Client         │
│  • Status code                   │
│  • Formatted data                │
└──────────────────────────────────┘
```

### Request-Response Cycle

```
CLIENT                      SERVER                      SERVICES
  │                           │                            │
  │ 1. HTTP Request          │                            │
  ├─────────────────────────►│                            │
  │    (JSON/FormData)        │                            │
  │                           │                            │
  │                           │ 2. Route Handler           │
  │                           ├───────────────────────────►│
  │                           │    Call Service            │
  │                           │                            │
  │                           │                            │ 3. Process
  │                           │                            │    • Normalize
  │                           │                            │    • Validate
  │                           │                            │    • Predict
  │                           │                            │    • Format
  │                           │                            │
  │                           │ 4. Return Result           │
  │                           │◄───────────────────────────┤
  │                           │                            │
  │ 5. HTTP Response          │                            │
  │◄─────────────────────────┤                            │
  │    (JSON)                 │                            │
  │                           │                            │
  │ 6. Render UI              │                            │
  │    • Parse JSON           │                            │
  │    • Update DOM           │                            │
  │    • Display Results      │                            │
```

---

## 🎯 Summary

### Key Process Features

✅ **Side Effects Analysis**
- Fuzzy matching for typos
- Common vs Serious categorization
- Color-coded display

✅ **Drug Interactions**
- Risk level prediction
- Detailed health explanations
- Multi-drug support

✅ **OCR Image Analysis**
- Multi-strategy text extraction
- Automatic drug detection
- Complete analysis pipeline

### Technology Highlights

- **Machine Learning**: Random Forest
- **OCR**: Tesseract multi-strategy
- **Backend**: Flask REST API
- **Frontend**: Vanilla JavaScript
- **Data**: CSV → pandas → ML models

---

**End of Flowchart Documentation**
