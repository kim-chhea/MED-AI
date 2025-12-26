from .side_effects_analyzer import SideEffectsAnalyzer
from .interaction_checker import InteractionChecker

# Image processor might fail on Python 3.14 due to pytesseract compatibility
try:
    from .image_processor import ImageProcessor
except ImportError as e:
    print(f"Warning: Image processor unavailable: {e}")
    ImageProcessor = None

__all__ = ['SideEffectsAnalyzer', 'InteractionChecker', 'ImageProcessor']