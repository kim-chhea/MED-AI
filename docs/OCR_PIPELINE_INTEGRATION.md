# OCR Analysis Pipeline - Integration Guide

## 📋 Overview

The `OCRAnalysisPipeline` is a complete, modular solution that takes raw OCR text and automatically:
- Cleans and normalizes text
- Detects drug names using fuzzy matching (handles OCR spelling errors)
- Analyzes using existing trained ML models
- Returns side effects (1 drug) or interactions (2 drugs)

**No API calls. No retraining. Uses existing local models only.**

---

## 🚀 Quick Start

### Basic Usage

```python
from services.ocr_analysis_pipeline import OCRAnalysisPipeline

# Initialize pipeline (loads existing trained models)
pipeline = OCRAnalysisPipeline()

# Process OCR text
raw_text = "Aspirin 500mg tablet"
result = pipeline.process_ocr_text(raw_text)

print(result)
# {
#     'status': 'single_drug_analysis',
#     'detected_drugs': ['Aspirin'],
#     'analysis_type': 'side_effects',
#     'result': {
#         'drug': 'Aspirin',
#         'side_effects': ['nausea', 'headache', 'stomach upset', 'dizziness'],
#         'count': 4
#     }
# }
```

---

## 📊 Response Formats

### Case 1: No Drugs Detected

```python
{
    'status': 'no_drug_detected',
    'message': 'Drug not recognized from image',
    'suggestion': 'Please ensure image contains clear drug names',
    'detected_drugs': []
}
```

### Case 2: One Drug → Side Effects

```python
{
    'status': 'single_drug_analysis',
    'detected_drugs': ['Aspirin'],
    'drug_count': 1,
    'analysis_type': 'side_effects',
    'result': {
        'drug': 'Aspirin',
        'side_effects': ['nausea', 'headache', 'stomach upset', 'dizziness'],
        'count': 4,
        'message': 'Found 4 potential side effects'
    }
}
```

### Case 3: Two Drugs → Interaction

```python
{
    'status': 'two_drug_analysis',
    'detected_drugs': ['Aspirin', 'Warfarin'],
    'drug_count': 2,
    'analysis_type': 'drug_interaction',
    'result': {
        'drugA': 'Aspirin',
        'drugB': 'Warfarin',
        'interaction_risk': 'Dangerous',
        'confidence': '85%',
        'warning': True,
        'description': 'Increased risk of bleeding'
    }
}
```

---

## 🔧 Integration Examples

### Example 1: Integrate with Flask API

```python
from flask import Blueprint, request, jsonify
from services.ocr_analysis_pipeline import OCRAnalysisPipeline

api_bp = Blueprint('api', __name__)
pipeline = OCRAnalysisPipeline()

@api_bp.route('/analyze-ocr-text', methods=['POST'])
def analyze_ocr():
    data = request.get_json()
    ocr_text = data.get('ocr_text', '')
    
    # Process OCR text
    result = pipeline.process_ocr_text(ocr_text)
    
    return jsonify(result), 200
```

### Example 2: Integrate with Existing Image Processor

```python
from PIL import Image
import pytesseract
from services.ocr_analysis_pipeline import OCRAnalysisPipeline

def analyze_drug_image(image_path):
    # Step 1: Extract text using Tesseract (existing OCR)
    img = Image.open(image_path)
    raw_ocr_text = pytesseract.image_to_string(img)
    
    # Step 2: Process with pipeline (NEW)
    pipeline = OCRAnalysisPipeline()
    result = pipeline.process_ocr_text(raw_ocr_text)
    
    return result
```

### Example 3: Command-Line Tool

```python
import sys
from services.ocr_analysis_pipeline import OCRAnalysisPipeline

def main():
    if len(sys.argv) < 2:
        print("Usage: python ocr_tool.py 'OCR text here'")
        return
    
    ocr_text = sys.argv[1]
    pipeline = OCRAnalysisPipeline()
    result = pipeline.process_ocr_text(ocr_text)
    
    print(f"Status: {result['status']}")
    print(f"Detected: {result['detected_drugs']}")
    
    if result['status'] != 'no_drug_detected':
        print(f"Analysis: {result['analysis_type']}")

if __name__ == '__main__':
    main()
```

---

## 🧪 Test Cases

### Test 1: Exact Match

```python
result = pipeline.process_ocr_text("Aspirin 500mg")
assert result['detected_drugs'] == ['Aspirin']
assert result['analysis_type'] == 'side_effects'
```

### Test 2: OCR Spelling Error (Fuzzy Match)

```python
# OCR reads "Asprin" instead of "Aspirin"
result = pipeline.process_ocr_text("Asprin 100mg")
assert result['detected_drugs'] == ['Aspirin']  # Corrected!
```

### Test 3: Two Drugs

```python
result = pipeline.process_ocr_text("Aspirin and Warfarin")
assert len(result['detected_drugs']) == 2
assert result['analysis_type'] == 'drug_interaction'
```

### Test 4: No Valid Drug

```python
result = pipeline.process_ocr_text("Take with food")
assert result['status'] == 'no_drug_detected'
```

### Test 5: Complex Prescription

```python
ocr_text = """
PRESCRIPTION
Patient: John Doe
Medication: lbuprofen 400mg  # OCR error: "l" instead of "I"
Instructions: Take twice daily
"""
result = pipeline.process_ocr_text(ocr_text)
assert 'Ibuprofen' in result['detected_drugs']  # Fuzzy matched!
```

---

## 🎯 Key Features

### ✅ OCR Error Handling

- **Fuzzy matching** with 70% similarity threshold
- Handles common OCR errors:
  - Letter substitution: `lbuprofen` → `ibuprofen`
  - Missing letters: `asprin` → `aspirin`
  - Transposed letters: `apsrin` → `aspirin`
  - Case variations: `ASPIRIN` → `aspirin`

### ✅ Modular Design

- **Plugs into existing code** - no modifications needed
- Uses existing trained models (no retraining)
- Clean separation of concerns:
  1. `clean_ocr_text()` - Text preprocessing
  2. `extract_drug_names()` - Drug detection
  3. `analyze_detected_drugs()` - ML analysis

### ✅ Smart Analysis Logic

- 0 drugs → Clear error message
- 1 drug → Side effects prediction
- 2 drugs → Interaction prediction
- 3+ drugs → Takes first 2 (interaction focus)

---

## 📝 Code Architecture

```
OCRAnalysisPipeline
│
├── __init__()
│   └── Loads existing trained models
│
├── clean_ocr_text(raw_text)
│   └── Normalizes text (lowercase, remove special chars)
│
├── extract_drug_names(cleaned_text)
│   ├── Exact matching (fast)
│   └── Fuzzy matching (handles OCR errors)
│
├── analyze_detected_drugs(drug_names)
│   ├── 0 drugs → Error message
│   ├── 1 drug → SideEffectsAnalyzer
│   └── 2 drugs → InteractionChecker
│
└── process_ocr_text(raw_ocr_text)  ← MAIN METHOD
    ├── Clean text
    ├── Detect drugs
    └── Analyze with models
```

---

## 🔄 Workflow Diagram

```
┌─────────────────────┐
│   Raw OCR Text      │
│ "Asprin and Warfrin"│
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   Clean & Normalize │
│  "asprin and warfrin"│
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Fuzzy Drug Match   │
│ "asprin"→"aspirin"  │
│ "warfrin"→"warfarin"│
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   2 Drugs Detected  │
│ ['aspirin','warfarin']│
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│ Interaction Checker │
│  Risk: Dangerous ⚠️ │
└─────────────────────┘
```

---

## 💡 Advanced Usage

### Custom Fuzzy Matching Threshold

```python
# In extract_drug_names(), modify cutoff:
matches = get_close_matches(
    word, 
    self.known_drugs, 
    n=1,
    cutoff=0.60  # Lower = more forgiving (default: 0.70)
)
```

### Add Pre-processing Rules

```python
def clean_ocr_text(self, raw_text):
    text = raw_text.lower()
    
    # Custom: Remove common OCR artifacts
    text = text.replace('|', 'i')  # Vertical bar → i
    text = text.replace('0', 'o')  # Zero → o
    
    # ... rest of cleaning
    return text
```

### Detect More Than 2 Drugs

```python
# In extract_drug_names(), change limit:
return list(detected_drugs)[:5]  # Up to 5 drugs
```

---

## ⚠️ Important Notes

1. **No Retraining Required**
   - Pipeline uses existing models from `src/models/`
   - Models must be trained first (`python src/train_models.py`)

2. **Fuzzy Matching Trade-offs**
   - Higher cutoff (0.80) = fewer false positives, may miss OCR errors
   - Lower cutoff (0.60) = catches more OCR errors, more false positives
   - Current: 0.70 (balanced)

3. **Drug Database**
   - Automatically loaded from trained model's encoder
   - Currently: 30 drugs (aspirin, ibuprofen, warfarin, etc.)
   - To add drugs: Update `data/drug_side_effects.csv` and retrain

---

## 🎓 Example Session

```bash
$ python src/services/ocr_analysis_pipeline.py

======================================================================
MEDDI AI - OCR ANALYSIS PIPELINE EXAMPLES
======================================================================

[Example 1] Single Drug - Exact Match
----------------------------------------------------------------------
Input: 'Aspirin 500mg tablet'
Detected: ['Aspirin']
Analysis: side_effects

[Example 2] Single Drug - OCR Spelling Error
----------------------------------------------------------------------
Input: 'Asprin 100mg' (OCR error)
Detected: ['Aspirin']
Analysis: side_effects

[Example 3] Two Drugs - Interaction Check
----------------------------------------------------------------------
Input: 'Aspirin and Warfarin prescribed'
Detected: ['Aspirin', 'Warfarin']
Analysis: drug_interaction

[Example 4] No Valid Drug
----------------------------------------------------------------------
Input: 'Take with food and water'
Message: Drug not recognized from image

[Example 5] Complex OCR Text
----------------------------------------------------------------------
Input: Complex prescription text
Detected: ['Ibuprofen']
Analysis: side_effects
```

---

## 📚 Dependencies

- **difflib** (built-in Python) - Fuzzy string matching
- **re** (built-in Python) - Text cleaning
- **SideEffectsAnalyzer** (existing) - Side effects prediction
- **InteractionChecker** (existing) - Drug interaction prediction

**No additional packages required!**

---

## 🎯 Summary

✅ **Modular** - Drop-in solution for existing project  
✅ **No APIs** - Fully offline, local ML models  
✅ **No Retraining** - Uses existing trained models  
✅ **Fuzzy Matching** - Handles OCR spelling errors  
✅ **Smart Logic** - Adapts to 0/1/2 drug scenarios  
✅ **Well-Documented** - Clear comments and examples  

**File Location:** `src/services/ocr_analysis_pipeline.py`

**Ready to use!** Just import and call `process_ocr_text()`.
