"""
Meddi AI - Feature 3: Drug Text Extraction from Image

This module uses OCR (Optical Character Recognition) to extract drug text from images,
then analyzes the detected drugs using the trained ML models.
"""

import os

# Compatibility shim for Python 3.12+ where pkgutil.find_loader was removed
import sys
import pkgutil
if not hasattr(pkgutil, 'find_loader'):
    # Add compatibility for pytesseract with Python 3.12+
    from importlib.util import find_spec
    pkgutil.find_loader = lambda name: find_spec(name)

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

# Configure Tesseract path for Windows
tesseract_paths = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    r'C:\Tesseract-OCR\tesseract.exe'
]

tesseract_found = False
for path in tesseract_paths:
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        tesseract_found = True
        print(f"✓ Tesseract found at: {path}")
        break

if not tesseract_found:
    print("⚠ Tesseract executable not found in common locations")

import re
from services.ocr_analysis_pipeline import OCRAnalysisPipeline


class ImageProcessor:
    """
    Extracts drug names from images and analyzes them using ML models.
    
    How it works:
    1. Use Tesseract OCR to extract text from drug label/prescription image
    2. Use OCR Analysis Pipeline to detect drugs and analyze them
    3. Return complete analysis with side effects and interactions
    """
    
    def __init__(self):
        """Initialize OCR and analysis pipeline"""
        # Use the new OCR Analysis Pipeline for intelligent drug detection
        self.pipeline = OCRAnalysisPipeline()
    
    def extract_text(self, file):
        """
        Extract text from image using OCR with preprocessing
        
        Args:
            file: Image file path or file object
        
        Returns:
            str: Extracted text or error message
        """
        try:
            # Reset file pointer to beginning (important for Flask file uploads!)
            if hasattr(file, 'seek'):
                file.seek(0)
            
            # Open image
            img = Image.open(file)
            
            # Try multiple OCR strategies
            text = None
            
            # Strategy 1: Direct OCR
            try:
                text = pytesseract.image_to_string(img)
                if text and text.strip():
                    return text.strip()
            except:
                pass
            
            # Strategy 2: Convert to RGB (in case of RGBA or other modes)
            if img.mode != 'RGB':
                img = img.convert('RGB')
                text = pytesseract.image_to_string(img)
                if text and text.strip():
                    return text.strip()
            
            # Strategy 3: Grayscale with enhanced contrast
            img_gray = img.convert('L')
            enhancer = ImageEnhance.Contrast(img_gray)
            img_enhanced = enhancer.enhance(2.0)  # Increase contrast
            text = pytesseract.image_to_string(img_enhanced)
            if text and text.strip():
                return text.strip()
            
            # Strategy 4: Larger size for small text
            new_size = (img.size[0] * 2, img.size[1] * 2)
            img_large = img.resize(new_size, Image.Resampling.LANCZOS)
            text = pytesseract.image_to_string(img_large)
            if text and text.strip():
                return text.strip()
            
            # If all strategies fail
            return "No text extracted from image"
                
        except pytesseract.TesseractNotFoundError:
            return {
                "error": "Tesseract executable not found",
                "instructions": "Please install Tesseract OCR from https://github.com/UB-Mannheim/tesseract/wiki and restart the server"
            }
        except Exception as e:
            return {"error": f"Error processing image: {str(e)}"}
    
    def identify_drugs(self, text):
        """
        Identify drug names from extracted text using exact matching and fuzzy matching
        
        Args:
            text (str): Extracted text from image
        
        Returns:
            list: List of identified drug names
        """
        if not text or isinstance(text, dict):
            return []
        
        # Convert text to lowercase for matching
        text_lower = text.lower()
        
        # Split text into words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text_lower)
        
        # Find drug names in the text
        found_drugs = set()
        
        # Method 1: Exact matching (check if any known drug appears in text)
        for drug in self.known_drugs:
            # Use word boundaries to match whole words
            pattern = r'\b' + re.escape(drug) + r'\b'
            if re.search(pattern, text_lower):
                found_drugs.add(drug)
        
        # Method 2: Fuzzy matching for OCR errors (check each word against known drugs)
        from difflib import get_close_matches
        
        for word in words:
            if len(word) >= 4:  # Only check words with 4+ characters
                # Skip if already found exact match
                if word in found_drugs:
                    continue
                    
                # Try fuzzy matching with high similarity (70% for OCR errors)
                matches = get_close_matches(word, self.known_drugs, n=1, cutoff=0.7)
                
                if matches:
                    found_drugs.add(matches[0])
        
        return list(found_drugs)
    
    def extract_and_analyze(self, file):
        """
        Full pipeline: Extract text from image and analyze detected drugs
        
        Args:
            file: Image file path or file object
        
        Returns:
            dict: Complete analysis including OCR text, detected drugs, side effects, and interactions
        """
        # Step 1: Extract text using OCR
        extracted_text = self.extract_text(file)
        
        # Check for errors
        if isinstance(extracted_text, dict) and "error" in extracted_text:
            return extracted_text
        
        if not extracted_text or extracted_text == "No text extracted from image":
            return {
                "error": "No text extracted from image",
                "message": "Please ensure the image contains clear, readable text"
            }
        
        # Step 2: Use OCR Analysis Pipeline for intelligent drug detection and analysis
        analysis_result = self.pipeline.process_ocr_text(extracted_text)
        
        # Format the result for web interface
        if analysis_result['status'] == 'no_drug_detected':
            return {
                "extracted_text": extracted_text,
                "detected_drugs": [],
                "message": analysis_result['message'],
                "suggestion": analysis_result.get('suggestion', '')
            }
        
        elif analysis_result['status'] == 'single_drug_analysis':
            # Single drug - side effects
            drug_result = analysis_result['result']
            
            return {
                "extracted_text": extracted_text,
                "detected_drugs": analysis_result['detected_drugs'],
                "drugs_count": 1,
                "drug_analyses": [{
                    "drug": analysis_result['detected_drugs'][0],
                    "side_effects": drug_result.get('side_effects', []),
                    "common_effects": drug_result.get('common_effects', []),
                    "serious_effects": drug_result.get('serious_effects', []),
                    "count": len(drug_result.get('side_effects', [])),
                    "common_count": len(drug_result.get('common_effects', [])),
                    "serious_count": len(drug_result.get('serious_effects', [])),
                    "status": "success"
                }] if 'side_effects' in drug_result else [],
                "total_side_effects": len(drug_result.get('side_effects', [])),
                "summary": f"Found 1 drug with {len(drug_result.get('side_effects', []))} side effects"
            }
        
        elif analysis_result['status'] == 'two_drug_analysis':
            # Two drugs - interaction check
            interaction_result = analysis_result['result']
            
            # Also get side effects for each drug
            drug_analyses = []
            from services.side_effects_analyzer import SideEffectsAnalyzer
            analyzer = SideEffectsAnalyzer()
            
            for drug_name in analysis_result['detected_drugs']:
                se_analysis = analyzer.analyze(drug_name.lower())
                if isinstance(se_analysis, dict) and 'side_effects' in se_analysis:
                    drug_analyses.append({
                        "drug": drug_name,
                        "side_effects": se_analysis['side_effects'],
                        "common_effects": se_analysis.get('common_effects', []),
                        "serious_effects": se_analysis.get('serious_effects', []),
                        "count": len(se_analysis['side_effects']),
                        "common_count": len(se_analysis.get('common_effects', [])),
                        "serious_count": len(se_analysis.get('serious_effects', [])),
                        "status": "success"
                    })
            
            risk_warning = None
            if interaction_result.get('interaction_risk') == 'Dangerous':
                risk_warning = "⚠️ DANGEROUS INTERACTION DETECTED! Consult healthcare provider immediately."
            
            return {
                "extracted_text": extracted_text,
                "detected_drugs": analysis_result['detected_drugs'],
                "drugs_count": 2,
                "drug_analyses": drug_analyses,
                "interaction_check": interaction_result,
                "risk_warning": risk_warning,
                "summary": f"Found 2 drugs - interaction risk: {interaction_result.get('interaction_risk', 'Unknown')}"
            }
        
        else:
            return {
                "extracted_text": extracted_text,
                "error": "Unknown analysis status",
                "message": "Unable to complete analysis"
            }
    
    def analyze_text_input(self, text):
        """
        Analyze drug text directly (without image OCR)
        Useful for testing or when drug names are already known
        
        Args:
            text (str): Text containing drug names
        
        Returns:
            dict: Analysis results
        """
        # Identify drugs in the text
        detected_drugs = self.identify_drugs(text)
        
        if not detected_drugs:
            return {
                "input_text": text,
                "detected_drugs": [],
                "message": "No known drug names detected in the text"
            }
        
        # Analyze detected drugs
        drug_analyses = []
        
        for drug in detected_drugs:
            analysis = self.side_effects_analyzer.analyze(drug)
            drug_analyses.append({
                "drug": drug.title(),
                "analysis": analysis
            })
        
        # Check interactions if multiple drugs
        interaction_result = None
        
        if len(detected_drugs) >= 2:
            interaction_result = self.interaction_checker.check_multiple_pairs(detected_drugs)
        
        return {
            "input_text": text,
            "detected_drugs": [d.title() for d in detected_drugs],
            "drugs_count": len(detected_drugs),
            "drug_analyses": drug_analyses,
            "interaction_check": interaction_result
        }