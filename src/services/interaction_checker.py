"""
Meddi AI - Feature 2: Drug-Drug Interaction Checker

This module uses a trained model to predict interaction risks between two drugs.
"""

import joblib
import os
import numpy as np
from difflib import get_close_matches


class InteractionChecker:
    """
    Predicts interaction risk when two drugs are taken together.
    
    How it works:
    1. Load the trained model and encoders (trained in train_models.py)
    2. Convert both drug names to numerical format
    3. Use the model to classify interaction risk
    4. Return risk level with detailed explanation
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
            except:
                pass
        
        self.current_mode = mode  # Store the mode
        
        # Set models directory based on mode
        if mode == 'custom':
            self.models_dir = os.path.join(base_models_dir, 'custom')
        else:
            self.models_dir = base_models_dir
        
        # Check if models exist
        if not os.path.exists(self.models_dir):
            self.model = None
            self.drug_encoder = None
            self.risk_encoder = None
            return
        
        # Check if all required model files exist
        required_files = ['interaction_model.pkl', 'interaction_drug_encoder.pkl', 'risk_encoder.pkl']
        missing_files = [f for f in required_files if not os.path.exists(os.path.join(self.models_dir, f))]
        
        if missing_files:
            self.model = None
            self.drug_encoder = None
            self.risk_encoder = None
            return
        
        try:
            # Load the trained Random Forest classifier
            model_path = os.path.join(self.models_dir, 'interaction_model.pkl')
            self.model = joblib.load(model_path)
            
            # Load the drug name encoder (converts drug names to numbers)
            encoder_path = os.path.join(self.models_dir, 'interaction_drug_encoder.pkl')
            self.drug_encoder = joblib.load(encoder_path)
            
            # Load the risk level encoder (converts predictions to risk levels)
            risk_path = os.path.join(self.models_dir, 'risk_encoder.pkl')
            self.risk_encoder = joblib.load(risk_path)
            
        except FileNotFoundError:
            self.model = None
            self.drug_encoder = None
            self.risk_encoder = None
    
    def get_detailed_explanation(self, drugA, drugB, risk_level):
        """
        Generate detailed explanation of what happens when both drugs are taken together
        
        Args:
            drugA (str): First drug name
            drugB (str): Second drug name
            risk_level (str): Risk level (Safe, Moderate, Dangerous)
        
        Returns:
            str: Detailed explanation
        """
        drugA_title = drugA.title()
        drugB_title = drugB.title()
        
        if risk_level == "Dangerous":
            explanations = [
                f"Taking {drugA_title} and {drugB_title} together may cause serious health complications. These drugs can interact in ways that significantly increase side effects, reduce effectiveness, or create toxic effects in your body. The combined effect may overload your liver or kidneys, affect your heart rhythm, or cause dangerous changes in blood pressure or bleeding risk.",
                f"The combination of {drugA_title} and {drugB_title} is considered high-risk. When taken together, one drug may interfere with how your body processes the other, leading to dangerous accumulation of medication in your system. This can result in organ damage, severe adverse reactions, or life-threatening complications.",
                f"These medications ({drugA_title} and {drugB_title}) should not be taken together without medical supervision. Their interaction may cause dangerous side effects such as excessive bleeding, respiratory depression, heart problems, or toxic buildup in your bloodstream. Always consult your doctor before combining these drugs."
            ]
            import random
            return random.choice(explanations)
        
        elif risk_level == "Moderate":
            explanations = [
                f"Taking {drugA_title} and {drugB_title} together requires caution. These drugs may interact moderately, potentially reducing the effectiveness of one or both medications, or causing increased side effects. Your body may process one drug differently when the other is present, which could affect dosing requirements.",
                f"The combination of {drugA_title} and {drugB_title} shows moderate interaction potential. While not immediately dangerous, these drugs may affect each other's absorption, metabolism, or elimination from your body. This could lead to unexpected side effects or reduced therapeutic benefits. Monitor for any unusual symptoms.",
                f"When {drugA_title} and {drugB_title} are taken together, there's a moderate risk of interaction. One drug may enhance or diminish the effects of the other, potentially requiring dose adjustments. Common concerns include increased drowsiness, digestive issues, or changes in medication effectiveness."
            ]
            import random
            return random.choice(explanations)
        
        else:  # Safe
            explanations = [
                f"Taking {drugA_title} and {drugB_title} together appears to be safe based on available data. These medications work through different mechanisms and are unlikely to interfere with each other significantly. However, always follow your doctor's instructions regarding dosing and timing.",
                f"The combination of {drugA_title} and {drugB_title} shows low interaction risk. These drugs can generally be taken together without significant concerns. They don't substantially affect how your body processes each medication, and their side effects don't typically compound in problematic ways.",
                f"{drugA_title} and {drugB_title} have minimal interaction potential. Your body should be able to process both medications effectively without one interfering with the other. This combination is considered safe for most patients, though individual responses may vary."
            ]
            import random
            return random.choice(explanations)
    
    
    def check(self, drug_list):
        """
        Check interaction risk between two drugs
        
        Args:
            drug_list (list): List of drug names (must have at least 2 drugs)
        
        Returns:
            dict: Interaction risk prediction or error message
        """
        # Validate input
        if len(drug_list) < 2:
            return {"error": "At least 2 drugs required"}
        
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
        
        # Normalize drug names (lowercase for consistency)
        drug_list = [drug.strip().lower() for drug in drug_list]
        
        # For this implementation, we check pairs of drugs
        # If more than 2 drugs, we check the first two
        drugA = drug_list[0]
        drugB = drug_list[1]
        
        # Check if both drugs exist in training data
        unknown_drugs = []
        suggestions = {}
        
        if drugA not in self.drug_encoder.classes_:
            unknown_drugs.append(drugA)
            # Try more forgiving fuzzy matching
            similar = get_close_matches(drugA, self.drug_encoder.classes_, n=3, cutoff=0.5)
            if not similar:
                similar = get_close_matches(drugA, self.drug_encoder.classes_, n=3, cutoff=0.4)
            if similar:
                suggestions[drugA] = similar
                
        if drugB not in self.drug_encoder.classes_:
            unknown_drugs.append(drugB)
            # Try more forgiving fuzzy matching
            similar = get_close_matches(drugB, self.drug_encoder.classes_, n=3, cutoff=0.5)
            if not similar:
                similar = get_close_matches(drugB, self.drug_encoder.classes_, n=3, cutoff=0.4)
            if similar:
                suggestions[drugB] = similar
        
        if unknown_drugs:
            error_msg = {
                "error": f"Drugs not found in database: {', '.join(unknown_drugs)}"
            }
            
            if suggestions:
                error_msg["did_you_mean"] = suggestions
                suggestion_text = []
                for drug, matches in suggestions.items():
                    suggestion_text.append(f"{drug} → {', '.join(matches[:2])}")
                error_msg["suggestion"] = "Did you mean: " + " | ".join(suggestion_text) + "?"
            else:
                error_msg["suggestion"] = "Available drugs include: " + ", ".join(self.drug_encoder.classes_[:10]) + "..."
                
            error_msg["total_drugs"] = len(self.drug_encoder.classes_)
            return error_msg
        
        try:
            # PREDICTION PHASE
            # Step 1: Encode both drug names to numerical values
            drugA_encoded = self.drug_encoder.transform([drugA])[0]
            drugB_encoded = self.drug_encoder.transform([drugB])[0]
            
            # Step 2: Create feature vector [drugA_id, drugB_id]
            features = np.array([[drugA_encoded, drugB_encoded]])
            
            # Step 3: Use ML model to predict interaction risk
            prediction = self.model.predict(features)
            
            # Step 4: Convert numerical prediction to risk level name
            risk_level = self.risk_encoder.inverse_transform(prediction)[0]
            
            # Get prediction confidence (probability)
            probabilities = self.model.predict_proba(features)[0]
            confidence = max(probabilities) * 100
            
            # Get detailed explanation
            detailed_explanation = self.get_detailed_explanation(drugA, drugB, risk_level)
            
            # Format the result
            return {
                "drugA": drugA.title(),
                "drugB": drugB.title(),
                "interaction_risk": risk_level,
                "confidence": f"{confidence:.1f}%",
                "description": detailed_explanation,
                "warning": risk_level == "Dangerous"
            }
            
        except Exception as e:
            return {
                "error": f"Error during prediction: {str(e)}"
            }
    
    def check_multiple_pairs(self, drug_list):
        """
        Check all possible pairs of drugs for interactions
        
        Args:
            drug_list (list): List of drug names (3 or more)
        
        Returns:
            dict: All pairwise interaction predictions
        """
        if len(drug_list) < 2:
            return {"error": "At least 2 drugs required"}
        
        results = []
        
        # Check all pairs
        for i in range(len(drug_list)):
            for j in range(i + 1, len(drug_list)):
                pair_result = self.check([drug_list[i], drug_list[j]])
                if "error" not in pair_result:
                    results.append(pair_result)
        
        if not results:
            return {"error": "No valid drug pairs found"}
        
        # Find most dangerous interaction
        dangerous_count = sum(1 for r in results if r["interaction_risk"] == "Dangerous")
        moderate_count = sum(1 for r in results if r["interaction_risk"] == "Moderate")
        
        return {
            "total_pairs_checked": len(results),
            "dangerous_interactions": dangerous_count,
            "moderate_interactions": moderate_count,
            "interactions": results,
            "overall_warning": dangerous_count > 0
        }