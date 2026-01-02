# 📊 Custom Dataset Upload Guide

This guide explains how to use your own datasets to train custom machine learning models.

---

## 🎯 Feature Overview

The Drug Side Effects Analyzer now supports **custom dataset uploads**, allowing you to:

✅ Upload your own CSV datasets for side effects and interactions  
✅ Download CSV templates to see the required format  
✅ Train models with your custom data  
✅ Switch between built-in and custom datasets  

---

## 🔄 How to Use

### **Step 1: Toggle to Custom Dataset Mode**

1. Open the application at `http://127.0.0.1:5001`
2. Look for the **"Dataset Source"** section at the top
3. Click the **toggle switch** to switch from "Built-in Dataset" to "Custom Dataset"

```
Built-in Dataset  [ ○――― ]  Custom Dataset  ← Click to switch
```

### **Step 2: Download CSV Templates**

Before uploading your data, download the templates to understand the required format:

#### **Side Effects Template Format:**
```csv
drug_name,side_effect
aspirin,nausea
aspirin,headache
ibuprofen,dizziness
paracetamol,fatigue
```

**Required Columns:**
- `drug_name`: Name of the drug (lowercase recommended)
- `side_effect`: One side effect per row

#### **Interactions Template Format:**
```csv
drugA,drugB,interaction_risk
aspirin,ibuprofen,Moderate
aspirin,warfarin,Dangerous
paracetamol,metformin,Safe
```

**Required Columns:**
- `drugA`: First drug name (lowercase recommended)
- `drugB`: Second drug name (lowercase recommended)
- `interaction_risk`: Must be one of: `Safe`, `Moderate`, or `Dangerous`

### **Step 3: Prepare Your Custom Datasets**

Create your own CSV files following the template format:

**Tips:**
- Use lowercase for drug names for consistency
- One side effect per row (drugs can appear multiple times)
- For interactions, list each drug pair once
- Risk levels are case-sensitive: `Safe`, `Moderate`, `Dangerous`
- Save files with `.csv` extension
- Use UTF-8 encoding

**Minimum Recommended Data:**
- Side Effects: At least 50 records
- Interactions: At least 30 records

### **Step 4: Upload Your Datasets**

1. Click **"Download Template"** for each dataset type (optional)
2. Click **"Choose CSV File"** under each section:
   - Side Effects Dataset
   - Interactions Dataset
3. Select your prepared CSV file
4. Wait for upload confirmation ✓

The system will automatically validate your CSV structure and show:
- ✓ **Success**: Number of records uploaded
- ✕ **Error**: If columns are missing or format is invalid

### **Step 5: Train Models**

Once both datasets are uploaded:

1. The **"Train Models with Custom Data"** button will become active 🟢
2. Click the button to start training
3. Wait for the training process to complete (may take 10-60 seconds)
4. View accuracy metrics:
   - Side Effects Accuracy: XX.XX%
   - Interactions Accuracy: XX.XX%

### **Step 6: Use Your Custom Models**

After training completes:
- All features now use your custom trained models ✅
- Side Effects Analysis uses your custom data
- Interaction Checker uses your custom data
- Image Analysis (OCR) uses your custom data

---

## 📋 Dataset Requirements

### **Side Effects Dataset**

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `drug_name` | string | ✓ | Drug name (e.g., "aspirin") |
| `side_effect` | string | ✓ | Side effect name (e.g., "nausea") |

**Example:**
```csv
drug_name,side_effect
aspirin,nausea
aspirin,headache
aspirin,stomach pain
ibuprofen,nausea
ibuprofen,dizziness
ibuprofen,drowsiness
paracetamol,liver damage
paracetamol,rash
```

### **Interactions Dataset**

| Column | Type | Required | Description | Valid Values |
|--------|------|----------|-------------|--------------|
| `drugA` | string | ✓ | First drug name | Any string |
| `drugB` | string | ✓ | Second drug name | Any string |
| `interaction_risk` | string | ✓ | Risk level | `Safe`, `Moderate`, `Dangerous` |

**Example:**
```csv
drugA,drugB,interaction_risk
aspirin,ibuprofen,Moderate
aspirin,warfarin,Dangerous
aspirin,paracetamol,Safe
ibuprofen,paracetamol,Safe
metformin,insulin,Moderate
lisinopril,amlodipine,Safe
```

---

## ⚠️ Common Errors & Solutions

### **Error: "Missing required columns"**

**Cause:** CSV doesn't have the correct column names

**Solution:**
- Side Effects: Must have `drug_name` and `side_effect` columns
- Interactions: Must have `drugA`, `drugB`, and `interaction_risk` columns
- Check spelling and case sensitivity

### **Error: "Invalid CSV format"**

**Cause:** File is not a valid CSV or contains formatting errors

**Solution:**
- Save file as CSV (not Excel .xlsx)
- Use commas as delimiters
- Avoid special characters in column names
- Use UTF-8 encoding

### **Error: "File must be CSV format"**

**Cause:** Uploaded file is not a .csv file

**Solution:**
- Rename file extension to `.csv`
- Export from Excel using "Save As" → "CSV (Comma delimited)"

### **Low Accuracy After Training**

**Cause:** Insufficient or poor quality data

**Solution:**
- Add more records (aim for 100+ side effects, 50+ interactions)
- Ensure consistent drug name formatting
- Check for typos in drug names
- Use lowercase for all drug names
- Verify risk levels are spelled correctly: `Safe`, `Moderate`, `Dangerous`

---

## 🔄 Switching Back to Built-in Dataset

To return to using the built-in dataset:

1. Click the toggle switch back to "Built-in Dataset"
2. The system will immediately use the original trained models
3. Your uploaded files remain in the `uploads/` folder
4. You can switch back to custom anytime

---

## 📁 File Storage

### **Uploaded Files Location:**
```
drug-side-effects-analyzer/
└── uploads/
    ├── custom_side_effects.csv
    └── custom_interactions.csv
```

### **Trained Models Location:**
```
drug-side-effects-analyzer/
└── src/
    └── models/
        ├── side_effects_model.pkl      (overwritten with custom)
        ├── drug_encoder.pkl
        ├── side_effects_encoder.pkl
        ├── interaction_model.pkl       (overwritten with custom)
        ├── interaction_drug_encoder.pkl
        └── risk_encoder.pkl
```

⚠️ **Note:** Custom training overwrites the original models. To restore built-in models, run:
```bash
python src/train_models.py
```

---

## 💡 Best Practices

### **Data Quality**

✅ **DO:**
- Use consistent drug name formatting (lowercase)
- Include 50+ records minimum
- Verify data accuracy before uploading
- Use common, recognizable drug names
- List multiple side effects per drug (separate rows)

❌ **DON'T:**
- Mix uppercase and lowercase drug names
- Use brand names and generic names interchangeably
- Include duplicate drug pairs in interactions
- Use typos or abbreviations

### **Dataset Size Recommendations**

| Dataset Type | Minimum | Recommended | Optimal |
|--------------|---------|-------------|---------|
| Side Effects | 50 rows | 120 rows | 500+ rows |
| Interactions | 30 rows | 87 rows | 300+ rows |

### **Risk Level Guidelines**

**Dangerous:**
- Life-threatening combinations
- Causes serious adverse effects
- May result in hospitalization
- Example: Warfarin + Aspirin (bleeding risk)

**Moderate:**
- Requires caution
- May need dose adjustment
- Monitor for side effects
- Example: Aspirin + Ibuprofen (GI issues)

**Safe:**
- No significant interaction
- Can be taken together
- Routine monitoring sufficient
- Example: Paracetamol + Metformin

---

## 🧪 Testing Your Custom Models

After training, test your models:

### **1. Side Effects Tab**
- Enter a drug name from your dataset
- Verify side effects are categorized correctly
- Check if confidence scores seem reasonable

### **2. Interactions Tab**
- Add two drugs from your dataset
- Verify risk level matches your data
- Read the explanation for accuracy

### **3. Image Analysis (OCR)**
- Upload an image with drug names from your dataset
- Verify extracted drugs are analyzed correctly

---

## 📊 Example Datasets

### **Sample Side Effects Dataset (20 records)**

```csv
drug_name,side_effect
aspirin,nausea
aspirin,headache
aspirin,stomach pain
aspirin,bleeding
ibuprofen,nausea
ibuprofen,dizziness
ibuprofen,heartburn
ibuprofen,drowsiness
paracetamol,liver damage
paracetamol,rash
paracetamol,nausea
metformin,diarrhea
metformin,nausea
metformin,vomiting
lisinopril,dizziness
lisinopril,cough
lisinopril,headache
warfarin,bleeding
warfarin,bruising
warfarin,hair loss
```

### **Sample Interactions Dataset (15 records)**

```csv
drugA,drugB,interaction_risk
aspirin,ibuprofen,Moderate
aspirin,warfarin,Dangerous
aspirin,paracetamol,Safe
ibuprofen,paracetamol,Safe
ibuprofen,warfarin,Dangerous
metformin,insulin,Moderate
metformin,lisinopril,Safe
lisinopril,amlodipine,Safe
lisinopril,hydrochlorothiazide,Moderate
warfarin,aspirin,Dangerous
warfarin,omeprazole,Moderate
paracetamol,metformin,Safe
paracetamol,lisinopril,Safe
simvastatin,amlodipine,Moderate
simvastatin,omeprazole,Safe
```

---

## 🛠️ Troubleshooting

### **Training Takes Too Long**

**Normal:** 10-60 seconds for datasets with 100-500 records  
**Slow:** 1-3 minutes for datasets with 1000+ records

If training exceeds 5 minutes:
- Reduce dataset size
- Check for infinite loops in CSV
- Restart the server

### **Models Not Loading After Training**

**Solution:**
1. Check browser console for errors (F12)
2. Refresh the page
3. Toggle dataset mode off and on
4. Check `src/models/` folder for .pkl files

### **Upload Button Greyed Out**

**Cause:** Files already uploaded or validation failed

**Solution:**
- Check upload status messages
- Clear the files and re-upload
- Ensure both datasets are valid CSV files

---

## 📝 API Endpoints

For developers integrating this feature:

### **Download Template**
```http
GET /api/download-template?type=side_effects
GET /api/download-template?type=interactions
```

### **Upload Dataset**
```http
POST /api/upload-dataset
Content-Type: multipart/form-data

file: <CSV file>
type: side_effects | interactions
```

### **Retrain Models**
```http
POST /api/retrain-models
Content-Type: application/json

{
  "side_effects_file": "custom_side_effects.csv",
  "interactions_file": "custom_interactions.csv"
}
```

---

## 🎓 Learning Resources

- **Machine Learning Basics:** How models learn from your data
- **Random Forest:** The algorithm used for predictions
- **CSV Format:** Understanding comma-separated values
- **Data Preprocessing:** Why data quality matters

---

## ⚡ Quick Start Example

1. **Download templates** → Click both "Download Template" buttons
2. **Edit templates** → Add your drug data (minimum 10 drugs each)
3. **Upload files** → Choose your edited CSV files
4. **Train models** → Click "Train Models with Custom Data"
5. **Test predictions** → Try the three main features

**Total time:** 5-10 minutes

---

## 🔐 Privacy & Security

- All uploads are stored **locally** on your machine
- No data is sent to external servers
- Files are stored in `uploads/` directory
- You can delete uploaded files anytime
- Models are trained locally (no cloud processing)

---

## 📞 Support

If you encounter issues:

1. Check this guide for common errors
2. Verify CSV format matches templates
3. Ensure both datasets are uploaded before training
4. Check browser console for error messages (F12)
5. Try re-uploading with smaller datasets first

---

**Happy Dataset Uploading! 🚀**

---

*Last Updated: January 2, 2026*
