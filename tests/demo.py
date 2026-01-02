"""
Meddi AI - Demo Script

This script demonstrates all three features of Meddi AI:
1. Single drug side effects prediction
2. Drug-drug interaction checking
3. Text analysis for drug detection

Run this after training models to see the system in action.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.side_effects_analyzer import SideEffectsAnalyzer
from services.interaction_checker import InteractionChecker
from services.image_processor import ImageProcessor
import json


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def print_result(result):
    """Pretty print JSON results"""
    print(json.dumps(result, indent=2))


def demo_feature_1():
    """Demo: Single Drug Side Effects Analysis"""
    print_section("FEATURE 1: Single Drug Side Effects Analysis")
    
    analyzer = SideEffectsAnalyzer()
    
    # Check if models are trained
    if analyzer.model is None:
        print("\n❌ Models not trained yet!")
        print("Please run: python src/train_models.py")
        return
    
    print("\n✓ Model loaded successfully\n")
    
    # Test with multiple drugs
    test_drugs = ["aspirin", "metformin", "ibuprofen", "insulin"]
    
    for drug in test_drugs:
        print(f"\n{'─'*70}")
        print(f"Analyzing: {drug.upper()}")
        print('─'*70)
        
        result = analyzer.analyze(drug)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✓ Drug: {result['drug']}")
            print(f"✓ Side Effects Found: {result['count']}")
            print("\nPredicted Side Effects:")
            for i, effect in enumerate(result['side_effects'], 1):
                print(f"  {i}. {effect}")
    
    # Test with unknown drug
    print(f"\n{'─'*70}")
    print("Testing with unknown drug: UNKNOWNDRUG")
    print('─'*70)
    result = analyzer.analyze("unknowndrug")
    print(f"❌ {result.get('error', 'Unknown error')}")
    if 'suggestion' in result:
        print(f"\nℹ️  {result['suggestion']}")


def demo_feature_2():
    """Demo: Drug-Drug Interaction Analysis"""
    print_section("FEATURE 2: Drug-Drug Interaction Analysis")
    
    checker = InteractionChecker()
    
    # Check if models are trained
    if checker.model is None:
        print("\n❌ Models not trained yet!")
        print("Please run: python src/train_models.py")
        return
    
    print("\n✓ Model loaded successfully\n")
    
    # Test with different drug combinations
    test_pairs = [
        (["aspirin", "warfarin"], "Expected: Dangerous"),
        (["ibuprofen", "paracetamol"], "Expected: Safe"),
        (["metformin", "insulin"], "Expected: Moderate"),
        (["aspirin", "ibuprofen"], "Expected: Moderate")
    ]
    
    for drugs, expected in test_pairs:
        print(f"\n{'─'*70}")
        print(f"Checking: {drugs[0].upper()} + {drugs[1].upper()}")
        print(f"({expected})")
        print('─'*70)
        
        result = checker.check(drugs)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            risk = result['interaction_risk']
            symbol = "🔴" if risk == "Dangerous" else "🟡" if risk == "Moderate" else "🟢"
            
            print(f"{symbol} Risk Level: {risk}")
            print(f"✓ Confidence: {result['confidence']}")
            print(f"\n📝 Description:")
            print(f"   {result['description']}")
            
            if result.get('warning'):
                print("\n⚠️  WARNING: Dangerous interaction detected!")
    
    # Test with multiple drugs
    print(f"\n{'─'*70}")
    print("Checking multiple drugs: ASPIRIN + IBUPROFEN + WARFARIN")
    print('─'*70)
    
    result = checker.check_multiple_pairs(["aspirin", "ibuprofen", "warfarin"])
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"✓ Checked {result['total_pairs_checked']} drug pairs")
        print(f"🔴 Dangerous: {result['dangerous_interactions']}")
        print(f"🟡 Moderate: {result['moderate_interactions']}")
        
        if result['overall_warning']:
            print("\n⚠️  OVERALL WARNING: Dangerous interactions found!")
        
        print("\nDetailed Results:")
        for interaction in result['interactions']:
            risk = interaction['interaction_risk']
            symbol = "🔴" if risk == "Dangerous" else "🟡" if risk == "Moderate" else "🟢"
            print(f"\n  {symbol} {interaction['drugA']} + {interaction['drugB']}")
            print(f"     Risk: {risk} ({interaction['confidence']})")


def demo_feature_3():
    """Demo: Text Analysis for Drug Detection"""
    print_section("FEATURE 3: Drug Text Analysis")
    
    processor = ImageProcessor()
    
    print("\n✓ Processor initialized\n")
    
    # Test with sample prescription texts
    test_texts = [
        "Patient should take Aspirin 100mg daily for heart health.",
        "Prescription: Metformin 500mg twice daily and Insulin as directed.",
        "Take Ibuprofen 200mg for pain and Paracetamol 500mg for fever.",
        "Warfarin 5mg daily. Avoid taking with Aspirin."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{'─'*70}")
        print(f"Test {i}: Analyzing prescription text")
        print('─'*70)
        print(f"\nInput Text:\n\"{text}\"\n")
        
        result = processor.analyze_text_input(text)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            continue
        
        print(f"✓ Detected {result['drugs_count']} drugs: {', '.join(result['detected_drugs'])}")
        
        # Show side effects for each drug
        if result.get('drug_analyses'):
            print("\n📋 Side Effects Analysis:")
            for drug_analysis in result['drug_analyses']:
                drug_data = drug_analysis['analysis']
                if 'side_effects' in drug_data:
                    print(f"\n  {drug_analysis['drug']} ({drug_data['count']} effects):")
                    for effect in drug_data['side_effects'][:3]:  # Show first 3
                        print(f"    • {effect}")
                    if drug_data['count'] > 3:
                        print(f"    ... and {drug_data['count'] - 3} more")
        
        # Show interaction warnings
        if result.get('interaction_check'):
            inter = result['interaction_check']
            if 'dangerous_interactions' in inter and inter['dangerous_interactions'] > 0:
                print(f"\n⚠️  WARNING: {inter['dangerous_interactions']} dangerous interaction(s) detected!")
            elif 'moderate_interactions' in inter and inter['moderate_interactions'] > 0:
                print(f"\n⚠️  CAUTION: {inter['moderate_interactions']} moderate interaction(s) detected!")
            else:
                print("\n✓ No dangerous interactions detected")


def demo_summary():
    """Show summary of capabilities"""
    print_section("MEDDI AI - Summary")
    
    analyzer = SideEffectsAnalyzer()
    
    if analyzer.model is None:
        print("\n❌ Models not trained yet!")
        print("\nTo get started:")
        print("1. Run: python src/train_models.py")
        print("2. Run: python demo.py")
        return
    
    print("\n✓ All systems operational!\n")
    print("Capabilities:")
    print("  ✓ Single drug side effects prediction")
    print("  ✓ Drug-drug interaction risk assessment")
    print("  ✓ Text analysis for automatic drug detection")
    print("  ✓ Multi-drug interaction checking")
    
    if analyzer.drug_encoder:
        print(f"\nDatabase Statistics:")
        print(f"  • Total drugs in database: {len(analyzer.drug_encoder.classes_)}")
        print(f"  • Sample drugs: {', '.join(list(analyzer.drug_encoder.classes_)[:10])}")
    
    print("\n" + "="*70)
    print("  Ready for production use!")
    print("="*70 + "\n")


def main():
    """Run all demos"""
    print("\n" + "="*70)
    print("  MEDDI AI - COMPREHENSIVE DEMO")
    print("="*70)
    print("\n  Demonstrating all three AI features:")
    print("  1. Side Effects Prediction (ML-based)")
    print("  2. Drug Interaction Checking (ML-based)")
    print("  3. Text Analysis with Drug Detection")
    print("\n  Using LOCAL machine learning models (no internet required)")
    print("="*70)
    
    try:
        # Check if models exist
        models_dir = os.path.join('src', 'models')
        if not os.path.exists(models_dir) or len(os.listdir(models_dir)) == 0:
            print("\n❌ ERROR: ML models not found!")
            print("\nPlease train the models first:")
            print("  python src/train_models.py")
            print("\nThen run this demo again:")
            print("  python demo.py")
            return
        
        # Run all feature demos
        demo_feature_1()
        demo_feature_2()
        demo_feature_3()
        demo_summary()
        
        print("\nDemo completed successfully!")
        print("\nNext steps:")
        print("  • Try the CLI: python src/main.py --cli")
        print("  • Start web server: python src/main.py")
        print("  • Add more drugs to data/drug_side_effects.csv")
        print("  • Retrain models: python src/train_models.py")
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
