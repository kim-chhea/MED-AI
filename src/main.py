"""
Meddi AI - Healthcare AI System

A beginner-friendly AI system with three main features:
1. Predict side effects of a single drug (ML-based)
2. Predict drug interaction risks (ML-based)
3. Extract drug text from images using OCR and analyze

All predictions use local machine learning models - no online APIs required.
"""

from flask import Flask, jsonify, render_template
import sys
import traceback
import json
import os
import glob

# Import ML-based services
from services.side_effects_analyzer import SideEffectsAnalyzer
from services.interaction_checker import InteractionChecker

# Try to import image processor (may fail due to pytesseract compatibility)
try:
    from services.image_processor import ImageProcessor
    IMAGE_PROCESSOR_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Image processor unavailable: {e}")
    ImageProcessor = None
    IMAGE_PROCESSOR_AVAILABLE = False

from utils.helpers import validate_drug_name

# Create Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Register API routes blueprint
from routes.api_routes import api_bp
app.register_blueprint(api_bp)

@app.route('/')
def index():
    """Serve the web UI"""
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'Meddi AI Server is running'}), 200

@app.errorhandler(Exception)
def handle_error(error):
    """Global error handler"""
    print(f"Error: {error}")
    traceback.print_exc()
    return jsonify({'error': str(error)}), 500


def interactive_mode():
    """
    CLI interface for Meddi AI
    
    Provides an interactive command-line interface to test all three features:
    - Single drug side effects prediction
    - Drug interaction checking
    - Image-based drug analysis
    """
    print("\n" + "="*60)
    print("     MEDDI AI - Healthcare AI System")
    print("="*60)
    print("\nUsing Local Machine Learning Models")
    print("No Internet Connection Required")
    print("="*60)
    
    # Initialize ML-based analyzers
    analyzer = SideEffectsAnalyzer()
    checker = InteractionChecker()
    
    # Try to initialize image processor
    try:
        image_proc = ImageProcessor() if IMAGE_PROCESSOR_AVAILABLE else None
    except:
        image_proc = None
    
    # Check if models are trained
    if analyzer.model is None:
        print("\n⚠️  WARNING: ML models not found!")
        print("Please train the models first by running:")
        print("   python src/train_models.py")
        print("\nThis will train the models using the CSV datasets.")
        print("="*60 + "\n")
        return
    
    print("\n✓ ML models loaded successfully!")
    print(f"✓ {len(analyzer.drug_encoder.classes_)} drugs in database")
    print("="*60)
    
    while True:
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. Find side effects of a drug (Feature 1)")
        print("2. Check drug interactions (Feature 2)")
        print("3. Analyze drug image with OCR (Feature 3)")
        print("4. Analyze text for drugs (Feature 3 - text only)")
        print("5. Exit")
        print("="*60)
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            # Feature 1: Single Drug Side Effects
            print("\n" + "-"*60)
            print("FEATURE 1: Single Drug Side Effects Analysis")
            print("-"*60)
            drug_name = input("Enter drug name: ").strip()
            
            if validate_drug_name(drug_name):
                print("\nAnalyzing drug using ML model...")
                result = analyzer.analyze(drug_name)
                
                print("\n" + "="*60)
                if "error" in result:
                    print("❌ ERROR:")
                    print(json.dumps(result, indent=2))
                else:
                    print(f"✓ Analysis for: {result.get('drug', drug_name)}")
                    print(f"\nSide Effects ({result.get('count', 0)} found):")
                    for effect in result.get('side_effects', []):
                        print(f"  • {effect}")
                print("="*60)
            else:
                print("\n❌ Invalid drug name!")
        
        elif choice == "2":
            # Feature 2: Drug-Drug Interactions
            print("\n" + "-"*60)
            print("FEATURE 2: Drug-Drug Interaction Analysis")
            print("-"*60)
            drugs_input = input("Enter drug names (comma-separated): ").strip()
            drugs = [d.strip() for d in drugs_input.split(",")]
            drugs = [d for d in drugs if validate_drug_name(d)]
            
            if len(drugs) >= 2:
                print(f"\nChecking interactions between {len(drugs)} drugs using ML model...")
                
                if len(drugs) == 2:
                    result = checker.check(drugs)
                else:
                    result = checker.check_multiple_pairs(drugs)
                
                print("\n" + "="*60)
                if "error" in result:
                    print("❌ ERROR:")
                    print(json.dumps(result, indent=2))
                else:
                    if "interactions" in result:
                        # Multiple pairs
                        print(f"✓ Checked {result['total_pairs_checked']} drug pairs")
                        print(f"\nDangerous: {result['dangerous_interactions']}")
                        print(f"Moderate: {result['moderate_interactions']}")
                        print(f"\nDetailed Results:")
                        for interaction in result['interactions']:
                            risk = interaction['interaction_risk']
                            symbol = "🔴" if risk == "Dangerous" else "🟡" if risk == "Moderate" else "🟢"
                            print(f"\n{symbol} {interaction['drugA']} + {interaction['drugB']}")
                            print(f"   Risk: {risk} ({interaction['confidence']})")
                            print(f"   {interaction['description']}")
                    else:
                        # Single pair
                        risk = result['interaction_risk']
                        symbol = "🔴" if risk == "Dangerous" else "🟡" if risk == "Moderate" else "🟢"
                        print(f"{symbol} {result['drugA']} + {result['drugB']}")
                        print(f"\nRisk Level: {risk}")
                        print(f"Confidence: {result['confidence']}")
                        print(f"\n{result['description']}")
                print("="*60)
            else:
                print("\n❌ Please enter at least 2 valid drug names!")
        
        elif choice == "3":
            # Feature 3: Image Analysis with OCR
            print("\n" + "-"*60)
            print("FEATURE 3: Drug Image Analysis (OCR)")
            print("-"*60)
            image_path = input("Enter image path: ").strip()
            
            if image_path:
                print("\nProcessing image with OCR...")
                print("1. Extracting text using Tesseract OCR")
                print("2. Identifying drug names")
                print("3. Analyzing drugs with ML models")
                
                result = image_proc.extract_and_analyze(image_path)
                
                print("\n" + "="*60)
                if isinstance(result, dict) and "error" in result:
                    print("❌ ERROR:")
                    print(json.dumps(result, indent=2))
                else:
                    print("✓ Image Analysis Complete\n")
                    print(f"Extracted Text:\n{result.get('extracted_text', 'N/A')}\n")
                    print(f"Detected Drugs ({result.get('drugs_count', 0)}):")
                    for drug in result.get('detected_drugs', []):
                        print(f"  • {drug}")
                    
                    if result.get('drug_analyses'):
                        print("\nSide Effects Analysis:")
                        for drug_analysis in result['drug_analyses']:
                            print(f"\n  {drug_analysis['drug']}:")
                            analysis = drug_analysis['analysis']
                            if 'side_effects' in analysis:
                                for effect in analysis['side_effects']:
                                    print(f"    - {effect}")
                    
                    if result.get('interaction_check'):
                        inter = result['interaction_check']
                        if 'dangerous_interactions' in inter:
                            print(f"\nInteraction Check:")
                            print(f"  Dangerous: {inter['dangerous_interactions']}")
                            print(f"  Moderate: {inter['moderate_interactions']}")
                
                print("="*60)
            else:
                print("\n❌ No image path provided!")
        
        elif choice == "4":
            # Feature 3: Text Analysis (without image)
            print("\n" + "-"*60)
            print("FEATURE 3: Text Analysis (No Image)")
            print("-"*60)
            text = input("Enter text containing drug names: ").strip()
            
            if text:
                print("\nAnalyzing text for drug names...")
                result = image_proc.analyze_text_input(text)
                
                print("\n" + "="*60)
                if "error" in result:
                    print("❌ ERROR:")
                    print(json.dumps(result, indent=2))
                else:
                    print(f"✓ Detected {result.get('drugs_count', 0)} drugs\n")
                    
                    for drug in result.get('detected_drugs', []):
                        print(f"• {drug}")
                    
                    if result.get('drug_analyses'):
                        print("\nSide Effects:")
                        for drug_analysis in result['drug_analyses']:
                            print(f"\n  {drug_analysis['drug']}:")
                            analysis = drug_analysis['analysis']
                            if 'side_effects' in analysis:
                                for effect in analysis['side_effects']:
                                    print(f"    - {effect}")
                
                print("="*60)
            else:
                print("\n❌ No text provided!")
        
        elif choice == "5":
            print("\n" + "="*60)
            print("Thank you for using Meddi AI!")
            print("="*60 + "\n")
            break
        else:
            print("\n❌ Invalid option! Please select 1-5.")


def cleanup_uploaded_files():
    """
    Clean up uploaded CSV files and custom models from previous sessions.
    Resets the system to built-in mode.
    Keeps .gitkeep file to preserve the uploads directory structure.
    """
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    uploads_dir = os.path.join(base_dir, 'uploads')
    custom_models_dir = os.path.join(os.path.dirname(__file__), 'models', 'custom')
    config_path = os.path.join(os.path.dirname(__file__), 'models', 'model_config.json')
    
    cleanup_count = 0
    
    try:
        # 1. Clean up CSV files in uploads directory
        csv_files = glob.glob(os.path.join(uploads_dir, '*.csv'))
        if csv_files:
            print(f"🧹 Cleaning up {len(csv_files)} uploaded CSV file(s)...")
            for file_path in csv_files:
                try:
                    os.remove(file_path)
                    print(f"   ✓ Removed: {os.path.basename(file_path)}")
                    cleanup_count += 1
                except Exception as e:
                    print(f"   ⚠ Could not remove {os.path.basename(file_path)}: {e}")
        
        # 2. Clean up custom model files
        if os.path.exists(custom_models_dir):
            model_files = glob.glob(os.path.join(custom_models_dir, '*.pkl'))
            if model_files:
                print(f"🧹 Cleaning up {len(model_files)} custom model file(s)...")
                for file_path in model_files:
                    try:
                        os.remove(file_path)
                        print(f"   ✓ Removed: {os.path.basename(file_path)}")
                        cleanup_count += 1
                    except Exception as e:
                        print(f"   ⚠ Could not remove {os.path.basename(file_path)}: {e}")
        
        # 3. Reset config to built-in mode
        if os.path.exists(config_path):
            try:
                with open(config_path, 'w') as f:
                    json.dump({"mode": "builtin"}, f)
                print("✓ Reset to built-in dataset mode")
            except Exception as e:
                print(f"⚠ Could not reset config: {e}")
        
        if cleanup_count > 0:
            print(f"✓ Cleanup complete! Removed {cleanup_count} file(s)\n")
        else:
            print("✓ No files to clean up - starting fresh!\n")
            
    except Exception as e:
        print(f"⚠ Error during cleanup: {e}\n")


if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        # Run in CLI mode
        interactive_mode()
    else:
        # Run Flask web server
        print("\n" + "="*60)
        print("Starting Meddi AI Web Server...")
        print("="*60)
        
        # Clean up uploaded files from previous sessions
        cleanup_uploaded_files()
        
        print("Access the application at: http://127.0.0.1:5001")
        print("Press CTRL+C to stop the server")
        print("="*60 + "\n")
        
        app.run(debug=False, port=5001, host='127.0.0.1', use_reloader=False)