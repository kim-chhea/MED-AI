from config import Config

class ChatGPTClient:
    def __init__(self):
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.is_real = True
        except Exception as e:
            print(f"Warning: Could not initialize OpenAI client: {e}")
            self.client = None
            self.is_real = False
    
    def _get_mock_side_effects(self, drug_name):
        """Get mock side effects when API is not available"""
        mock_responses = {
            "aspirin": "1. Stomach upset or heartburn\n2. Easy bruising or bleeding\n3. Allergic reactions\n4. Rash or itching",
            "ibuprofen": "1. Stomach pain or upset\n2. Nausea or vomiting\n3. Headache\n4. Dizziness",
            "paracetamol": "1. Liver damage (with overdose)\n2. Allergic reactions\n3. Severe skin reactions\n4. Low blood cell counts"
        }
        return mock_responses.get(drug_name.lower(), f"Common side effects for {drug_name}:\n1. Nausea\n2. Headache\n3. Dizziness\n4. Fatigue\n\n[Note: Using demo data. Please check your OpenAI API billing]")
    
    def analyze_side_effects(self, drug_name):
        """Get side effects of a drug from ChatGPT"""
        if not self.is_real or not self.client:
            return self._get_mock_side_effects(drug_name)
        
        try:
            prompt = f"List the common side effects of {drug_name}. Format as a numbered list."
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API Error: {str(e)}")
            return self._get_mock_side_effects(drug_name)
    
    def check_drug_interactions(self, drug_list):
        """Check interactions between multiple drugs"""
        if not self.is_real or not self.client:
            return f"Potential interactions between {', '.join(drug_list)}:\n\n⚠️ Note: Using demo data.\n\nTo analyze real drug interactions:\n1. Check your OpenAI API billing\n2. Ensure your API key is valid\n3. Verify your account has active credits"
        
        try:
            drugs_str = ", ".join(drug_list)
            prompt = f"Analyze potential interactions between these drugs: {drugs_str}. List serious interactions and their severity."
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API Error: {str(e)}")
            return f"Potential interactions between {', '.join(drug_list)}:\n\n⚠️ Note: Using demo data.\n\nTo analyze real drug interactions:\n1. Check your OpenAI API billing\n2. Ensure your API key is valid\n3. Verify your account has active credits"
    
    def analyze_extracted_text(self, text):
        """Analyze drug information from extracted text"""
        if not self.is_real or not self.client:
            return f"Extracted Information Analysis:\n\nText: {text[:200]}...\n\n📝 Demo Analysis:\n- Drug name detected\n- Common side effects may include: nausea, headache, dizziness\n- Recommended to consult healthcare provider\n\n[Using demo data. Please check OpenAI API billing]"
        
        try:
            prompt = f"Based on this drug information: {text}\n\nProvide side effects and warnings."
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API Error: {str(e)}")
            return f"Extracted Information Analysis:\n\nText: {text[:200]}...\n\n📝 Demo Analysis:\n- Drug name detected\n- Common side effects may include: nausea, headache, dizziness\n- Recommended to consult healthcare provider\n\n[Using demo data. Please check OpenAI API billing]"