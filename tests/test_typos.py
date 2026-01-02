"""Test typo detection and fuzzy matching"""
import sys
sys.path.insert(0, 'src')

from services.side_effects_analyzer import SideEffectsAnalyzer

analyzer = SideEffectsAnalyzer()

print("\n" + "="*70)
print("TESTING IMPROVED TYPO DETECTION")
print("="*70 + "\n")

# Test various typos
test_cases = [
    ("apsrin", "transposed letters (p and s swapped)"),
    ("Asprin", "capitalized with missing 'i'"),
    ("asprin", "lowercase missing 'i'"),
    ("ASPRIN", "all caps missing 'i'"),
    ("asirin", "wrong vowel (i instead of p)"),
    ("asprinn", "double 'n' at end"),
    ("asprin", "common typo"),
    ("aspirin", "correct spelling (should work)"),
    ("ibuprofen", "correct spelling"),
    ("ibuprofin", "common typo"),
    ("ibuprfen", "missing vowel"),
]

for drug, description in test_cases:
    result = analyzer.analyze(drug)
    
    if "error" in result:
        suggestions = result.get("did_you_mean", [])
        if suggestions:
            print(f"✓ '{drug:15}' -> Found: {suggestions[0]}")
        else:
            print(f"✗ '{drug:15}' -> NOT FOUND")
    else:
        print(f"✓ '{drug:15}' -> EXACT MATCH! ({result['count']} side effects)")

print("\n" + "="*70)
print("TESTING COMPLETE")
print("="*70 + "\n")
