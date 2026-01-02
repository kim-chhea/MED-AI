"""
Meddi AI - Feature 1: Single Drug Side Effects Analyzer

This module uses a trained model to predict side effects for a single drug.
"""

import joblib
import os
import numpy as np
from difflib import get_close_matches


class SideEffectsAnalyzer:
    """
    Predicts side effects for a given drug using a trained model.
    
    How it works:
    1. Load the trained model and encoders (trained in train_models.py)
    2. Convert drug name to numerical format using the encoder
    3. Use the model to predict side effects
    4. Convert predictions back to human-readable side effects
    5. Categorize effects as common or serious
    """
    
    def __init__(self):
        """Load trained models and encoders"""
        self.current_mode = None  # Track which mode is active
        self.load_models()
    
    def load_models(self):
        """Load or reload models based on current config"""
        # Check which mode is active (builtin or custom)
        base_models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        config_path = os.path.join(base_models_dir, 'model_config.json')
        
        # Read config to determine which models to load
        mode = 'builtin'  # default
        if os.path.exists(config_path):
            try:
                import json
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    mode = config.get('mode', 'builtin')
                    print(f"[SideEffectsAnalyzer] Loading models in '{mode}' mode")
            except Exception as e:
                print(f"[SideEffectsAnalyzer] Error reading config: {e}")
                pass
        else:
            print(f"[SideEffectsAnalyzer] No config found, using 'builtin' mode")
        
        self.current_mode = mode  # Store the mode
        
        # Set models directory based on mode
        if mode == 'custom':
            self.models_dir = os.path.join(base_models_dir, 'custom')
        else:
            self.models_dir = base_models_dir
        
        print(f"[SideEffectsAnalyzer] Models directory: {self.models_dir}")
        
        # Check if models exist
        if not os.path.exists(self.models_dir):
            print(f"[SideEffectsAnalyzer] ⚠️ Models directory not found!")
            self.model = None
            self.drug_encoder = None
            self.side_effects_encoder = None
            return
        
        # Check if all required model files exist
        required_files = ['side_effects_model.pkl', 'drug_encoder.pkl', 'side_effects_encoder.pkl']
        missing_files = [f for f in required_files if not os.path.exists(os.path.join(self.models_dir, f))]
        
        if missing_files:
            print(f"[SideEffectsAnalyzer] ⚠️ Missing model files: {missing_files}")
            self.model = None
            self.drug_encoder = None
            self.side_effects_encoder = None
            return
        
        try:
            # Load the trained Random Forest model
            model_path = os.path.join(self.models_dir, 'side_effects_model.pkl')
            self.model = joblib.load(model_path)
            
            # Load the drug name encoder (converts drug names to numbers)
            encoder_path = os.path.join(self.models_dir, 'drug_encoder.pkl')
            self.drug_encoder = joblib.load(encoder_path)
            
            # Load the side effects encoder (converts predictions to side effect names)
            effects_path = os.path.join(self.models_dir, 'side_effects_encoder.pkl')
            self.side_effects_encoder = joblib.load(effects_path)
            
            print(f"[SideEffectsAnalyzer] ✓ Models loaded successfully from {mode} mode")
            
        except FileNotFoundError as e:
            print(f"[SideEffectsAnalyzer] ✗ Model files not found: {e}")
            self.model = None
            self.drug_encoder = None
            self.side_effects_encoder = None
    
    def categorize_side_effects(self, side_effects):
        """
        Categorize side effects into common and serious
        
        Args:
            side_effects (list): List of side effect names
        
        Returns:
            dict: Categorized effects with 'common' and 'serious' lists
        """
        # Serious side effects keywords (case-insensitive matching)
        serious_keywords = [
            'death', 'fatal', 'cardiac', 'heart', 'stroke', 'seizure',
            'liver', 'kidney', 'failure', 'hemorrhage', 'bleeding',
            'anaphylaxis', 'allergic', 'respiratory', 'depression',
            'suicidal', 'coma', 'unconscious', 'severe', 'toxic',
            'cancer', 'tumor', 'damage', 'disease', 'disorder'
        ]
        
        common_effects = []
        serious_effects = []
        
        for effect in side_effects:
            effect_lower = effect.lower()
            is_serious = any(keyword in effect_lower for keyword in serious_keywords)
            
            if is_serious:
                serious_effects.append(effect)
            else:
                common_effects.append(effect)
        
        return {
            'common': common_effects,
            'serious': serious_effects
        }
    
    def analyze(self, drug_name):
        """
        Predict side effects for a given drug
        
        Args:
            drug_name (str): Name of the drug (e.g., "aspirin")
        
        Returns:
            dict or str: Predicted side effects or error message
        """
        # Validate input
        if not drug_name or len(drug_name.strip()) == 0:
            return {"error": "Drug name cannot be empty"}
        
        # Check if models are loaded
        if self.model is None:
            if self.current_mode == 'custom':
                return {
                    "error": "Custom models not trained yet. Please upload your datasets and click 'Train Custom Models' first.",
                    "instructions": "Switch to Custom Dataset mode, upload your CSV files, and train the models."
                }
            else:
                return {
                    "error": "Models not trained yet. Please run train_models.py first.",
                    "instructions": "Run: python src/train_models.py"
                }
        
        # Normalize drug name (lowercase for consistency)
        drug_name = drug_name.strip().lower()
        
        # Check if drug exists in training data
        if drug_name not in self.drug_encoder.classes_:
            # Try to find similar drug names (fuzzy matching with lower threshold)
            # Lower threshold = more forgiving with typos
            similar_drugs = get_close_matches(
                drug_name, 
                self.drug_encoder.classes_, 
                n=5,  # Get top 5 matches
                cutoff=0.5  # 50% similarity threshold (more forgiving)
            )
            
            # If still no matches, try even more lenient matching
            if not similar_drugs:
                similar_drugs = get_close_matches(
                    drug_name, 
                    self.drug_encoder.classes_, 
                    n=5,
                    cutoff=0.4  # 40% similarity for very different typos
                )
            
            if similar_drugs:
                return {
                    "error": f"Drug '{drug_name}' not found in database",
                    "did_you_mean": similar_drugs,
                    "suggestion": f"Did you mean: {', '.join(similar_drugs[:3])}?",
                    "total_drugs": len(self.drug_encoder.classes_)
                }
            else:
                return {
                    "error": f"Drug '{drug_name}' not found in database",
                    "suggestion": "Available drugs include: " + ", ".join(self.drug_encoder.classes_[:10]) + "...",
                    "total_drugs": len(self.drug_encoder.classes_)
                }
        
        try:
            # PREDICTION PHASE
            # Step 1: Encode drug name to numerical value
            drug_encoded = self.drug_encoder.transform([drug_name])
            drug_encoded = drug_encoded.reshape(-1, 1)
            
            # Step 2: Use model to predict side effects (binary array)
            prediction = self.model.predict(drug_encoded)
            
            # Step 3: Convert binary prediction to actual side effect names
            side_effects = self.side_effects_encoder.inverse_transform(prediction)
            
            # Format the result
            if side_effects and len(side_effects[0]) > 0:
                all_effects = list(side_effects[0])
                categorized = self.categorize_side_effects(all_effects)
                
                return {
                    "drug": drug_name.title(),
                    "side_effects": all_effects,
                    "common_effects": categorized['common'],
                    "serious_effects": categorized['serious'],
                    "count": len(all_effects),
                    "common_count": len(categorized['common']),
                    "serious_count": len(categorized['serious']),
                    "message": f"Found {len(all_effects)} potential side effects"
                }
            else:
                return {
                    "drug": drug_name.title(),
                    "side_effects": [],
                    "common_effects": [],
                    "serious_effects": [],
                    "message": "No side effects predicted for this drug"
                }
                
        except Exception as e:
            return {
                "error": f"Error during prediction: {str(e)}"
            }