"""
Meddi AI - OCR-to-Analysis Pipeline
====================================

This module takes raw OCR text from drug images and performs intelligent analysis:
1. Cleans and normalizes OCR text
2. Detects drug names using fuzzy matching (handles OCR spelling errors)
3. Analyzes detected drugs using existing trained ML models
4. Returns side effects (1 drug) or interactions (2 drugs)

NO API calls, NO retraining - uses existing local models only.
"""

import re
from difflib import get_close_matches
from services.side_effects_analyzer import SideEffectsAnalyzer
from services.interaction_checker import InteractionChecker


class OCRAnalysisPipeline:
    """
    Complete pipeline: OCR text → Drug detection → ML analysis
    """
    
    def __init__(self):
        """Initialize with existing trained models"""
        # Load existing analyzers (already trained)
        self.side_effects_analyzer = SideEffectsAnalyzer()
        self.interaction_checker = InteractionChecker()
        
        # Load drug database from existing model
        self.known_drugs = self._load_drug_database()
    
    def _load_drug_database(self):
        """
        Load known drug names from existing trained model
        
        Returns:
            set: Set of drug names from training data
        """
        try:
            if self.side_effects_analyzer.drug_encoder:
                # Get all drugs from the trained model's encoder
                return set(self.side_effects_analyzer.drug_encoder.classes_)
            return set()
        except:
            return set()
    
    def clean_ocr_text(self, raw_text):
        """
        Step 1: Clean and normalize raw OCR text
        
        OCR often produces:
        - Extra whitespace
        - Special characters
        - Mixed case
        - Line breaks
        
        Args:
            raw_text (str): Raw text from Tesseract OCR
        
        Returns:
            str: Cleaned, normalized text
        """
        if not raw_text:
            return ""
        
        # Convert to lowercase for consistency
        text = raw_text.lower()
        
        # Remove special characters but keep letters and spaces
        text = re.sub(r'[^a-z\s]', ' ', text)
        
        # Collapse multiple spaces into one
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def extract_drug_names(self, cleaned_text):
        """
        Step 2: Detect drug names from cleaned OCR text using fuzzy matching
        
        Strategy:
        1. Extract all words (3+ characters)
        2. Try exact matching first
        3. Use fuzzy matching for OCR spelling errors
        4. Return up to 2 drugs (for interaction checking)
        
        Args:
            cleaned_text (str): Cleaned OCR text
        
        Returns:
            list: List of detected drug names (0-2 drugs)
        """
        if not cleaned_text:
            return []
        
        # Extract words (minimum 3 characters to avoid noise)
        words = re.findall(r'\b[a-z]{3,}\b', cleaned_text)
        
        if not words:
            return []
        
        detected_drugs = set()
        
        # Method 1: EXACT MATCHING
        # Check if any known drug appears in the text
        for drug in self.known_drugs:
            if drug in cleaned_text:
                detected_drugs.add(drug)
                
                # Stop if we found 2 drugs (enough for interaction check)
                if len(detected_drugs) >= 2:
                    return list(detected_drugs)[:2]
        
        # Method 2: FUZZY MATCHING (handles OCR spelling errors)
        # Example: OCR reads "Asprin" → Match to "aspirin"
        #          OCR reads "lbuprofen" → Match to "ibuprofen"
        
        for word in words:
            # Skip if already found 2 drugs
            if len(detected_drugs) >= 2:
                break
            
            # Skip very short words or already matched words
            if len(word) < 4 or word in detected_drugs:
                continue
            
            # Fuzzy match with 70% similarity threshold
            # (lower = more forgiving, but may have false positives)
            matches = get_close_matches(
                word, 
                self.known_drugs, 
                n=1,           # Get best match only
                cutoff=0.70    # 70% similarity (handles OCR errors)
            )
            
            if matches:
                detected_drugs.add(matches[0])
        
        # Return up to 2 drugs for interaction checking
        return list(detected_drugs)[:2]
    
    def analyze_detected_drugs(self, drug_names):
        """
        Step 3: Analyze detected drugs using existing trained models
        
        Logic:
        - 0 drugs → "Drug not recognized"
        - 1 drug  → Side effects prediction
        - 2 drugs → Drug-drug interaction prediction
        
        Args:
            drug_names (list): List of detected drug names
        
        Returns:
            dict: Analysis results with predictions
        """
        num_drugs = len(drug_names)
        
        # Case 1: NO DRUGS DETECTED
        if num_drugs == 0:
            return {
                "status": "no_drug_detected",
                "message": "Drug not recognized from image",
                "suggestion": "Please ensure image contains clear drug names",
                "detected_drugs": []
            }
        
        # Case 2: ONE DRUG DETECTED → Side Effects Prediction
        elif num_drugs == 1:
            drug = drug_names[0]
            
            # Call existing side effects analyzer (already trained)
            analysis = self.side_effects_analyzer.analyze(drug)
            
            return {
                "status": "single_drug_analysis",
                "detected_drugs": [drug.title()],
                "drug_count": 1,
                "analysis_type": "side_effects",
                "result": analysis
            }
        
        # Case 3: TWO DRUGS DETECTED → Drug-Drug Interaction Prediction
        else:  # num_drugs == 2
            drug1, drug2 = drug_names[0], drug_names[1]
            
            # Call existing interaction checker (already trained)
            interaction = self.interaction_checker.check([drug1, drug2])
            
            return {
                "status": "two_drug_analysis",
                "detected_drugs": [drug1.title(), drug2.title()],
                "drug_count": 2,
                "analysis_type": "drug_interaction",
                "result": interaction
            }
    
    def process_ocr_text(self, raw_ocr_text):
        """
        MAIN PIPELINE: Complete OCR-to-analysis workflow
        
        Steps:
        1. Clean OCR text
        2. Detect drug names (fuzzy matching)
        3. Analyze using existing models
        
        Args:
            raw_ocr_text (str): Raw text from Tesseract OCR
        
        Returns:
            dict: Complete analysis with predictions
        
        Example Usage:
            >>> pipeline = OCRAnalysisPipeline()
            >>> 
            >>> # Example 1: One drug
            >>> result = pipeline.process_ocr_text("Aspirin 500mg tablet")
            >>> # Returns: Side effects of aspirin
            >>> 
            >>> # Example 2: Two drugs (OCR errors)
            >>> result = pipeline.process_ocr_text("Asprin and Warfarin")
            >>> # Returns: Drug-drug interaction (Dangerous risk)
            >>> 
            >>> # Example 3: No valid drug
            >>> result = pipeline.process_ocr_text("Take with food")
            >>> # Returns: "Drug not recognized from image"
        """
        
        # Validate input
        if not raw_ocr_text or not isinstance(raw_ocr_text, str):
            return {
                "status": "error",
                "message": "Invalid OCR text input",
                "detected_drugs": []
            }
        
        # STEP 1: Clean and normalize OCR text
        cleaned_text = self.clean_ocr_text(raw_ocr_text)
        
        if not cleaned_text:
            return {
                "status": "error",
                "message": "No valid text after cleaning",
                "detected_drugs": []
            }
        
        # STEP 2: Detect drug names using fuzzy matching
        detected_drugs = self.extract_drug_names(cleaned_text)
        
        # STEP 3: Analyze detected drugs using trained models
        analysis_result = self.analyze_detected_drugs(detected_drugs)
        
        # Add original OCR text for reference
        analysis_result["original_ocr_text"] = raw_ocr_text
        analysis_result["cleaned_text"] = cleaned_text
        
        return analysis_result


# ==============================================================================
# USAGE EXAMPLES
# ==============================================================================

def example_usage():
    """
    Examples showing how to use the OCR analysis pipeline
    """
    
    # Initialize pipeline
    pipeline = OCRAnalysisPipeline()
    
    print("=" * 70)
    print("MEDDI AI - OCR ANALYSIS PIPELINE EXAMPLES")
    print("=" * 70)
    
    # Example 1: Single drug (exact match)
    print("\n[Example 1] Single Drug - Exact Match")
    print("-" * 70)
    result = pipeline.process_ocr_text("Aspirin 500mg tablet")
    print(f"Input: 'Aspirin 500mg tablet'")
    print(f"Detected: {result['detected_drugs']}")
    print(f"Analysis: {result['analysis_type']}")
    print()
    
    # Example 2: Single drug with OCR error (fuzzy match)
    print("[Example 2] Single Drug - OCR Spelling Error")
    print("-" * 70)
    result = pipeline.process_ocr_text("Asprin 100mg")  # Typo: Asprin
    print(f"Input: 'Asprin 100mg' (OCR error)")
    print(f"Detected: {result['detected_drugs']}")
    print(f"Analysis: {result['analysis_type']}")
    print()
    
    # Example 3: Two drugs - interaction check
    print("[Example 3] Two Drugs - Interaction Check")
    print("-" * 70)
    result = pipeline.process_ocr_text("Aspirin and Warfarin prescribed")
    print(f"Input: 'Aspirin and Warfarin prescribed'")
    print(f"Detected: {result['detected_drugs']}")
    print(f"Analysis: {result['analysis_type']}")
    print()
    
    # Example 4: No valid drug
    print("[Example 4] No Valid Drug")
    print("-" * 70)
    result = pipeline.process_ocr_text("Take with food and water")
    print(f"Input: 'Take with food and water'")
    print(f"Message: {result['message']}")
    print()
    
    # Example 5: Complex OCR text
    print("[Example 5] Complex OCR Text")
    print("-" * 70)
    result = pipeline.process_ocr_text("""
        PRESCRIPTION
        Patient: John Doe
        Medication: lbuprofen 400mg
        Instructions: Take twice daily
    """)
    print(f"Input: Complex prescription text")
    print(f"Detected: {result['detected_drugs']}")
    print(f"Analysis: {result['analysis_type']}")
    print()


if __name__ == "__main__":
    # Run examples
    example_usage()
