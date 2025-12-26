from api.chatgpt_client import ChatGPTClient

class InteractionChecker:
    def __init__(self):
        self.client = ChatGPTClient()
    
    def check(self, drug_list):
        """Check interactions between multiple drugs"""
        if len(drug_list) < 2:
            return {"error": "At least 2 drugs required"}
        return self.client.check_drug_interactions(drug_list)