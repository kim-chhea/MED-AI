try:
    import pytesseract
    from PIL import Image
    PYTESSERACT_AVAILABLE = True
except ImportError as e:
    print(f"Warning: pytesseract not available: {e}")
    PYTESSERACT_AVAILABLE = False
    Image = None

from api.chatgpt_client import ChatGPTClient

class ImageProcessor:
    def __init__(self):
        self.client = ChatGPTClient()
        self.ocr_available = PYTESSERACT_AVAILABLE
    
    def extract_text(self, file):
        """Extract text from image using OCR"""
        if not self.ocr_available:
            return "OCR functionality unavailable due to Python 3.14 compatibility. Please use Python 3.11 or 3.12."
        
        try:
            img = Image.open(file)
            text = pytesseract.image_to_string(img)
            return text if text and text.strip() else "No text extracted"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def extract_and_analyze(self, file):
        """Extract text and analyze with ChatGPT"""
        text = self.extract_text(file)
        return text if "Error" in text or "unavailable" in text else self.client.analyze_extracted_text(text)

