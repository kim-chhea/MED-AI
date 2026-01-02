"""
Test OCR on uploaded images to debug extraction issues
"""

import sys
import os

# Add src to path
sys.path.insert(0, 'src')

try:
    import pytesseract
    from PIL import Image
    
    # Configure Tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    print("=" * 70)
    print("OCR DEBUGGING TOOL")
    print("=" * 70)
    
    # Test with a sample text
    print("\n[Test 1] Checking Tesseract installation...")
    try:
        version = pytesseract.get_tesseract_version()
        print(f"✓ Tesseract version: {version}")
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    
    # Ask for image path
    print("\n[Test 2] Ready to test image OCR")
    print("Please provide the path to your drug image:")
    print("Example: C:/Users/DELL/Desktop/ibuprofen.jpg")
    print("\nOr press Enter to skip manual test")
    
    image_path = input("\nImage path: ").strip()
    
    if image_path and os.path.exists(image_path):
        print(f"\nTesting OCR on: {image_path}")
        
        # Load image
        img = Image.open(image_path)
        print(f"✓ Image loaded: {img.size[0]}x{img.size[1]} pixels, mode: {img.mode}")
        
        # Try basic OCR
        print("\n--- RAW OCR OUTPUT ---")
        text = pytesseract.image_to_string(img)
        print(f"'{text}'")
        print("--- END OUTPUT ---")
        
        if text.strip():
            print(f"\n✓ Extracted {len(text)} characters")
            
            # Look for drug names
            from services.ocr_analysis_pipeline import OCRAnalysisPipeline
            pipeline = OCRAnalysisPipeline()
            
            result = pipeline.process_ocr_text(text)
            print(f"\n--- ANALYSIS RESULT ---")
            print(f"Status: {result['status']}")
            print(f"Detected drugs: {result.get('detected_drugs', [])}")
            
        else:
            print("\n✗ NO TEXT EXTRACTED!")
            print("\nPossible reasons:")
            print("1. Image quality too low")
            print("2. Text too small or blurry")
            print("3. Image needs preprocessing (contrast, rotation)")
            print("4. Wrong image format")
            
            # Try with preprocessing
            print("\n[Test 3] Trying with image preprocessing...")
            
            # Convert to grayscale
            img_gray = img.convert('L')
            text = pytesseract.image_to_string(img_gray)
            
            if text.strip():
                print(f"✓ Grayscale extraction worked! Got: '{text[:100]}...'")
            else:
                print("✗ Grayscale didn't help")
                
                # Try with higher DPI
                print("\n[Test 4] Trying with higher resolution...")
                # Increase image size
                new_size = (img.size[0] * 2, img.size[1] * 2)
                img_large = img.resize(new_size, Image.Resampling.LANCZOS)
                text = pytesseract.image_to_string(img_large)
                
                if text.strip():
                    print(f"✓ High-res extraction worked! Got: '{text[:100]}...'")
                else:
                    print("✗ High-res didn't help either")
    
    else:
        print("\nNo image path provided. Test complete.")
    
    print("\n" + "=" * 70)
    
except ImportError as e:
    print(f"Error: Required module not installed: {e}")
    print("Run: pip install pytesseract Pillow")
except Exception as e:
    print(f"Unexpected error: {e}")
    import traceback
    traceback.print_exc()
