from api.chatgpt_client import ChatGPTClient

class SideEffectsAnalyzer:
    def __init__(self):
        self.client = ChatGPTClient()
    
    def analyze(self, drug_name):
        """Analyze side effects of a drug"""
        if not drug_name or len(drug_name.strip()) == 0:
            return {"error": "Drug name cannot be empty"}
        return self.client.analyze_side_effects(drug_name)