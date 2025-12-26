import pytesseract
from PIL import Image
from api.chatgpt_client import ChatGPTClient

class ImageProcessor:
    def __init__(self):
        self.client = ChatGPTClient()
    
    def extract_text(self, file):
        """Extract text from image using OCR"""
        try:
            img = Image.open(file)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            return {"error": str(e)}
    
    def extract_and_analyze(self, file):
        """Extract text and analyze with ChatGPT"""
        text = self.extract_text(file)
        if isinstance(text, dict) and "error" in text:
            return text
        return self.client.analyze_extracted_text(text)