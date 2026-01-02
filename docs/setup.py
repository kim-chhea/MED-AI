"""
Meddi AI - Automated Setup Script

This script automates the complete setup process:
1. Checks if dependencies are installed
2. Trains the ML models
3. Runs a quick test
4. Provides next steps

Run this after installing requirements.txt
"""

import subprocess
import sys
import os


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def print_step(number, text):
    """Print step number"""
    print(f"\n{'─'*70}")
    print(f"STEP {number}: {text}")
    print('─'*70 + "\n")


def check_dependencies():
    """Check if required packages are installed"""
    print_step(1, "Checking Dependencies")
    
    required_packages = [
        'sklearn',
        'pandas',
        'numpy',
        'joblib',
        'flask',
        'PIL'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} missing")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("\nPlease run: pip install -r requirements.txt")
        return False
    
    print("\n✓ All required packages installed!")
    return True


def check_tesseract():
    """Check if Tesseract OCR is installed"""
    print("\nChecking Tesseract OCR (optional for Feature 3)...")
    
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        print("✓ Tesseract OCR installed")
        return True
    except:
        print("⚠️  Tesseract OCR not installed (Feature 3 will have limited functionality)")
        print("   Install from: https://github.com/UB-Mannheim/tesseract/wiki")
        return False


def check_data_files():
    """Check if training data exists"""
    print_step(2, "Checking Training Data")
    
    data_files = [
        'data/drug_side_effects.csv',
        'data/drug_interactions.csv'
    ]
    
    for file in data_files:
        if os.path.exists(file):
            print(f"✓ {file} found")
        else:
            print(f"✗ {file} missing")
            return False
    
    print("\n✓ All training data files present!")
    return True


def train_models():
    """Train the ML models"""
    print_step(3, "Training ML Models")
    
    print("This may take 1-2 minutes...\n")
    
    try:
        # Change to src directory
        os.chdir('src')
        
        # Import and run training
        import train_models
        train_models.main()
        
        # Change back
        os.chdir('..')
        
        print("\n✓ Models trained successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during training: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_quick_test():
    """Run a quick test of all features"""
    print_step(4, "Running Quick Tests")
    
    try:
        # Add src to path
        sys.path.insert(0, 'src')
        
        from services.side_effects_analyzer import SideEffectsAnalyzer
        from services.interaction_checker import InteractionChecker
        
        print("Testing Feature 1: Side Effects Prediction...")
        analyzer = SideEffectsAnalyzer()
        result = analyzer.analyze("aspirin")
        
        if "error" in result:
            print(f"✗ Feature 1 failed: {result['error']}")
            return False
        else:
            print(f"✓ Feature 1 working! Found {result['count']} side effects for aspirin")
        
        print("\nTesting Feature 2: Drug Interactions...")
        checker = InteractionChecker()
        result = checker.check(["aspirin", "warfarin"])
        
        if "error" in result:
            print(f"✗ Feature 2 failed: {result['error']}")
            return False
        else:
            print(f"✓ Feature 2 working! Interaction risk: {result['interaction_risk']}")
        
        print("\n✓ All core features working!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def show_next_steps():
    """Show what to do next"""
    print_header("Setup Complete! 🎉")
    
    print("Your Meddi AI system is ready to use!\n")
    
    print("Quick Start Commands:")
    print("─"*70)
    print("\n1. Run Demo (Recommended first):")
    print("   python demo.py")
    
    print("\n2. Interactive CLI:")
    print("   python src/main.py --cli")
    
    print("\n3. Start Web Server:")
    print("   python src/main.py")
    print("   Then visit: http://127.0.0.1:5001")
    
    print("\n" + "─"*70)
    print("\nDocumentation:")
    print("  • Quick Start Guide: QUICKSTART.md")
    print("  • Full Documentation: README_MEDDI_AI.md")
    print("  • Code Tutorial: CODE_EXPLANATION.py")
    print("  • Project Summary: PROJECT_SUMMARY.md")
    
    print("\n" + "─"*70)
    print("\nDatabase Info:")
    print("  • 30+ drugs available")
    print("  • 120+ side effect records")
    print("  • 85+ interaction records")
    
    print("\n" + "─"*70)
    print("\nAdd More Drugs:")
    print("  1. Edit data/drug_side_effects.csv")
    print("  2. Edit data/drug_interactions.csv")
    print("  3. Run: python src/train_models.py")
    
    print("\n" + "="*70)
    print("  Happy Learning! 🚀")
    print("="*70 + "\n")


def main():
    """Main setup function"""
    print_header("MEDDI AI - Automated Setup")
    
    print("This script will:")
    print("  1. Check if dependencies are installed")
    print("  2. Verify training data exists")
    print("  3. Train ML models")
    print("  4. Run quick tests")
    print("  5. Show you how to use the system")
    
    print("\n" + "="*70)
    input("\nPress Enter to start setup...")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Setup failed: Missing dependencies")
        print("Please run: pip install -r requirements.txt")
        return
    
    # Check Tesseract (optional)
    check_tesseract()
    
    # Step 2: Check data files
    if not check_data_files():
        print("\n❌ Setup failed: Missing training data files")
        print("Please ensure data/ directory has the CSV files")
        return
    
    # Step 3: Train models
    if not train_models():
        print("\n❌ Setup failed: Model training error")
        return
    
    # Step 4: Run tests
    if not run_quick_test():
        print("\n❌ Setup failed: Tests failed")
        return
    
    # Step 5: Show next steps
    show_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
