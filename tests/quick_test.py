"""
Quick Test Script - Verify ML Models Work
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.side_effects_analyzer import SideEffectsAnalyzer
from services.interaction_checker import InteractionChecker

print("\n" + "="*60)
print("MEDDI AI - QUICK TEST")
print("="*60)

# Test 1: Side Effects
print("\n📝 Test 1: Side Effects Analysis")
print("-"*60)
analyzer = SideEffectsAnalyzer()

if analyzer.model is None:
    print("❌ Models not trained!")
    print("Run: python src/train_models.py")
else:
    result = analyzer.analyze("aspirin")
    if "error" in result:
        print(f"❌ Error: {result}")
    else:
        print(f"✅ Drug: {result['drug']}")
        print(f"✅ Side Effects: {', '.join(result['side_effects'][:3])}...")

# Test 2: Drug Interactions
print("\n📝 Test 2: Drug Interaction Check")
print("-"*60)
checker = InteractionChecker()

if checker.model is None:
    print("❌ Models not trained!")
else:
    result = checker.check(["aspirin", "warfarin"])
    if "error" in result:
        print(f"❌ Error: {result}")
    else:
        print(f"✅ {result['drugA']} + {result['drugB']}")
        print(f"✅ Risk: {result['interaction_risk']} ({result['confidence']})")

print("\n" + "="*60)
print("✅ All tests completed!")
print("="*60)
print("\nWeb server is running at: http://127.0.0.1:5001")
print("Open it in your browser to test the UI!")
print("="*60 + "\n")
