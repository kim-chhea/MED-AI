"""
Meddi AI - ML Model Training Script

This script trains machine learning models for:
1. Single Drug Side Effects Prediction
2. Drug-Drug Interaction Risk Prediction

The models are saved locally and can be loaded for inference without retraining.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, hamming_loss
import joblib
import os


def create_models_directory(custom=False):
    """Create directory to store trained models"""
    base_dir = os.path.join(os.path.dirname(__file__), 'models')
    
    if custom:
        models_dir = os.path.join(base_dir, 'custom')
    else:
        models_dir = base_dir
        
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    return models_dir


def train_side_effects_model(data_path='data/drug_side_effects.csv', custom=False):
    """
    Feature 1: Train model to predict side effects for a single drug
    
    Approach:
    - Load dataset with drug_name and side_effect columns
    - Group multiple side effects per drug into a multi-label format
    - Use Random Forest to learn the association
    - Save the trained model and encoders
    """
    print("\n" + "="*60)
    print("FEATURE 1: Training Single Drug Side Effects Model")
    print("="*60)
    
    # Load dataset
    print(f"\n1. Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"   Loaded {len(df)} records")
    print(f"   Unique drugs: {df['drug_name'].nunique()}")
    print(f"   Unique side effects: {df['side_effect'].nunique()}")
    
    # Group side effects by drug (each drug can have multiple side effects)
    print("\n2. Grouping side effects by drug...")
    drug_effects = df.groupby('drug_name')['side_effect'].apply(list).reset_index()
    print(f"   Created {len(drug_effects)} drug-side_effects mappings")
    
    # Encode drug names to numbers
    print("\n3. Encoding drug names to numerical values...")
    drug_encoder = LabelEncoder()
    X = drug_encoder.fit_transform(drug_effects['drug_name'])
    X = X.reshape(-1, 1)  # Reshape for sklearn
    print(f"   Encoded {len(drug_encoder.classes_)} unique drugs")
    
    # Encode side effects using MultiLabelBinarizer
    # This creates a binary matrix where each column is a side effect
    print("\n4. Encoding side effects to binary matrix...")
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(drug_effects['side_effect'])
    print(f"   Created binary matrix with {y.shape[1]} side effect classes")
    
    # Split data for training and testing
    print("\n5. Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    
    # Train Random Forest model
    # Random Forest is good for multi-label classification
    print("\n6. Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,      # Number of trees
        max_depth=10,          # Maximum depth of trees
        random_state=42,
        n_jobs=-1              # Use all CPU cores
    )
    model.fit(X_train, y_train)
    print("   Model training completed!")
    
    # Evaluate model
    print("\n7. Evaluating model performance...")
    y_pred = model.predict(X_test)
    
    # Calculate accuracy for multi-label classification
    # Exact match accuracy (all labels must match) - very strict!
    exact_match_accuracy = accuracy_score(y_test, y_pred)
    print(f"   Exact match accuracy: {exact_match_accuracy:.2%}")
    
    # Hamming accuracy (percentage of correct labels) - more realistic!
    # Hamming loss measures the fraction of wrong labels
    # So accuracy = 1 - hamming_loss
    hamming_accuracy = 1 - hamming_loss(y_test, y_pred)
    print(f"   Label-wise accuracy (Hamming): {hamming_accuracy:.2%}")
    
    # Calculate per-sample accuracy (how many labels are correct on average)
    per_sample_accuracy = (y_test == y_pred).mean()
    print(f"   Per-label accuracy: {per_sample_accuracy:.2%}")
    
    # Use Hamming accuracy as it's more representative for multi-label
    final_accuracy = hamming_accuracy
    
    # Save model and encoders
    models_dir = create_models_directory(custom=custom)
    print(f"\n8. Saving model and encoders to {models_dir}/...")
    
    joblib.dump(model, os.path.join(models_dir, 'side_effects_model.pkl'))
    joblib.dump(drug_encoder, os.path.join(models_dir, 'drug_encoder.pkl'))
    joblib.dump(mlb, os.path.join(models_dir, 'side_effects_encoder.pkl'))
    
    print("   ✓ Saved: side_effects_model.pkl")
    print("   ✓ Saved: drug_encoder.pkl")
    print("   ✓ Saved: side_effects_encoder.pkl")
    
    print("\n" + "="*60)
    print(f"Feature 1 Training Complete! (Accuracy: {final_accuracy:.2%})")
    print("="*60)
    
    return final_accuracy


def train_interaction_model(data_path='data/drug_interactions.csv', custom=False):
    """
    Feature 2: Train model to predict drug-drug interaction risk
    
    Approach:
    - Load dataset with drugA, drugB, and interaction_risk columns
    - Encode both drug names into numerical features
    - Use Random Forest to classify interaction risk
    - Save the trained model and encoders
    """
    print("\n" + "="*60)
    print("FEATURE 2: Training Drug-Drug Interaction Model")
    print("="*60)
    
    # Load dataset
    print(f"\n1. Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"   Loaded {len(df)} interaction records")
    
    # Count risk categories
    risk_counts = df['interaction_risk'].value_counts()
    print(f"   Risk categories:")
    for risk, count in risk_counts.items():
        print(f"      {risk}: {count}")
    
    # Encode drug names
    print("\n2. Encoding drug names to numerical values...")
    drug_encoder = LabelEncoder()
    
    # Combine all unique drug names from both columns
    all_drugs = pd.concat([df['drugA'], df['drugB']]).unique()
    drug_encoder.fit(all_drugs)
    
    # Encode drugA and drugB separately
    drugA_encoded = drug_encoder.transform(df['drugA'])
    drugB_encoded = drug_encoder.transform(df['drugB'])
    
    # Combine as features (each row has 2 features: drugA_id and drugB_id)
    X = np.column_stack([drugA_encoded, drugB_encoded])
    print(f"   Encoded {len(drug_encoder.classes_)} unique drugs")
    print(f"   Feature matrix shape: {X.shape}")
    
    # Encode interaction risk labels
    print("\n3. Encoding interaction risk labels...")
    risk_encoder = LabelEncoder()
    y = risk_encoder.fit_transform(df['interaction_risk'])
    print(f"   Encoded {len(risk_encoder.classes_)} risk categories:")
    print(f"   {list(risk_encoder.classes_)}")
    
    # Split data for training and testing
    print("\n4. Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    
    # Train Random Forest Classifier
    print("\n5. Training Random Forest classifier...")
    model = RandomForestClassifier(
        n_estimators=100,      # Number of trees
        max_depth=10,          # Maximum depth of trees
        random_state=42,
        n_jobs=-1              # Use all CPU cores
    )
    model.fit(X_train, y_train)
    print("   Model training completed!")
    
    # Evaluate model
    print("\n6. Evaluating model performance...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"   Accuracy: {accuracy:.2%}")
    
    # Show detailed classification report
    print("\n   Classification Report:")
    print(classification_report(
        y_test, y_pred, 
        target_names=risk_encoder.classes_,
        zero_division=0
    ))
    
    # Save model and encoders
    models_dir = create_models_directory(custom=custom)
    print(f"\n7. Saving model and encoders to {models_dir}/...")
    
    joblib.dump(model, os.path.join(models_dir, 'interaction_model.pkl'))
    joblib.dump(drug_encoder, os.path.join(models_dir, 'interaction_drug_encoder.pkl'))
    joblib.dump(risk_encoder, os.path.join(models_dir, 'risk_encoder.pkl'))
    
    print("   ✓ Saved: interaction_model.pkl")
    print("   ✓ Saved: interaction_drug_encoder.pkl")
    print("   ✓ Saved: risk_encoder.pkl")
    
    print("\n" + "="*60)
    print("Feature 2 Training Complete!")
    print("="*60)
    
    return accuracy


def main():
    """Main training function"""
    print("\n" + "="*60)
    print("MEDDI AI - MACHINE LEARNING MODEL TRAINING")
    print("="*60)
    print("\nThis script will train two ML models:")
    print("1. Single Drug Side Effects Predictor")
    print("2. Drug-Drug Interaction Risk Predictor")
    print("\nTraining Phase: Models learn from CSV datasets")
    print("Prediction Phase: Trained models make predictions")
    print("="*60)
    
    # Get the correct paths relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    side_effects_path = os.path.join(project_root, 'data', 'drug_side_effects.csv')
    interactions_path = os.path.join(project_root, 'data', 'drug_interactions.csv')
    
    # Check if data files exist
    if not os.path.exists(side_effects_path):
        print(f"\n❌ Error: Data file not found: {side_effects_path}")
        return
    
    if not os.path.exists(interactions_path):
        print(f"\n❌ Error: Data file not found: {interactions_path}")
        return
    
    try:
        # Train Feature 1: Single Drug Side Effects
        train_side_effects_model(side_effects_path)
        
        # Train Feature 2: Drug-Drug Interactions
        train_interaction_model(interactions_path)
        
        print("\n" + "="*60)
        print("✓ ALL MODELS TRAINED SUCCESSFULLY!")
        print("="*60)
        print("\nModels saved in 'models/' directory:")
        print("- side_effects_model.pkl")
        print("- drug_encoder.pkl")
        print("- side_effects_encoder.pkl")
        print("- interaction_model.pkl")
        print("- interaction_drug_encoder.pkl")
        print("- risk_encoder.pkl")
        print("\nYou can now use these models for predictions!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during training: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
