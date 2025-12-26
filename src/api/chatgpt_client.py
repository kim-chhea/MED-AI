from config import Config
import time

class ChatGPTClient:
    def __init__(self):
        try:
            from openai import OpenAI
            if not Config.is_api_configured():
                print("⚠️ Warning: OpenAI API key not configured. Using demo mode.")
                self.client = None
                self.is_real = False
                return
                
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.is_real = True
            self.model = "gpt-3.5-turbo"  # Professional model configuration
            print("✓ OpenAI API client initialized successfully")
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize OpenAI client: {e}")
            self.client = None
            self.is_real = False
    
    def _make_api_call(self, messages, max_retries=2):
        """Make API call with retry logic and error handling"""
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=800
                )
                return response.choices[0].message.content
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "quota" in error_str.lower():
                    return None  # Quota exceeded
                if attempt < max_retries - 1:
                    time.sleep(1)  # Brief pause before retry
                    continue
                return None
        return None
    
    def _get_mock_side_effects(self, drug_name):
        """Get mock side effects when API is not available"""
        mock_responses = {
            "aspirin": """📋 Common Side Effects of Aspirin:

1. **Gastrointestinal Issues**
   • Stomach upset or heartburn
   • Nausea
   • Stomach ulcers with prolonged use

2. **Bleeding Risks**
   • Easy bruising
   • Increased bleeding time
   • Risk of internal bleeding

3. **Allergic Reactions**
   • Rash or hives
   • Difficulty breathing (rare)
   • Swelling of face or throat (rare)

4. **Other Effects**
   • Ringing in ears (tinnitus)
   • Headache
   • Dizziness

⚠️ Note: This is demo data. For real-time analysis, please configure your OpenAI API key.""",

            "ibuprofen": """📋 Common Side Effects of Ibuprofen:

1. **Digestive System**
   • Stomach pain or upset
   • Nausea or vomiting
   • Indigestion
   • Diarrhea or constipation

2. **Cardiovascular**
   • Increased blood pressure
   • Fluid retention
   • Heart attack risk (with long-term use)

3. **Central Nervous System**
   • Headache
   • Dizziness
   • Nervousness

4. **Other Effects**
   • Skin rash
   • Ringing in ears
   • Kidney problems (with prolonged use)

⚠️ Note: This is demo data. For real-time analysis, please configure your OpenAI API key.""",

            "paracetamol": """📋 Common Side Effects of Paracetamol (Acetaminophen):

1. **Rare but Serious**
   • Liver damage (especially with overdose)
   • Acute liver failure

2. **Allergic Reactions**
   • Skin rash or itching
   • Severe skin reactions (rare)
   • Swelling of face, lips, or tongue

3. **Blood-Related**
   • Low blood cell counts (rare)
   • Anemia
   • Thrombocytopenia

4. **General**
   • Nausea
   • Stomach pain
   • Loss of appetite

✓ Generally well-tolerated when used as directed

⚠️ Note: This is demo data. For real-time analysis, please configure your OpenAI API key."""
        }
        
        drug_lower = drug_name.lower()
        if drug_lower in mock_responses:
            return mock_responses[drug_lower]
        
        return f"""📋 Common Side Effects for {drug_name}:

1. **Gastrointestinal**
   • Nausea
   • Stomach upset
   • Diarrhea

2. **Central Nervous System**
   • Headache
   • Dizziness
   • Drowsiness

3. **General**
   • Fatigue
   • Weakness
   • Dry mouth

⚠️ **DEMO MODE ACTIVE**
This is sample data. To get real drug information:

1. ✓ Check your OpenAI API key is valid
2. ✓ Ensure your API account has active credits
3. ✓ Visit: https://platform.openai.com/account/billing

Current Status: API quota exceeded or key invalid."""
    
    def analyze_side_effects(self, drug_name):
        """Get side effects of a drug from ChatGPT with professional medical context"""
        if not self.is_real or not self.client:
            return self._get_mock_side_effects(drug_name)
        
        # Professional prompt for medical information
        prompt = f"""As a pharmaceutical information assistant, provide a comprehensive analysis of {drug_name}.

Please structure your response as follows:

**Common Side Effects:**
List the most frequently reported side effects with their frequency (common, uncommon, rare)

**Serious Side Effects:**
Highlight any severe or life-threatening reactions that require immediate medical attention

**Who Should Avoid:**
List contraindications and groups who should not take this medication

**Important Warnings:**
Include any critical safety information or precautions

**Drug Interactions:**
Mention major classes of drugs that may interact

Format the response professionally with clear sections and bullet points. Be precise and evidence-based."""

        messages = [
            {"role": "system", "content": "You are a professional pharmaceutical information assistant providing accurate, evidence-based drug information. Always include safety warnings and advise consulting healthcare professionals."},
            {"role": "user", "content": prompt}
        ]
        
        result = self._make_api_call(messages)
        
        if result:
            return f"📋 **{drug_name.title()} - Comprehensive Analysis**\n\n{result}\n\n---\n⚠️ *This information is for educational purposes only. Always consult with a healthcare professional before starting, stopping, or changing any medication.*"
        else:
            # Fallback to demo data if API fails
            return self._get_mock_side_effects(drug_name)
    
    def check_drug_interactions(self, drug_list):
        """Check interactions between multiple drugs with professional analysis"""
        drugs_str = ", ".join(drug_list)
        
        if not self.is_real or not self.client:
            return self._get_mock_interactions(drugs_str)
        
        # Professional prompt for drug interactions
        prompt = f"""As a clinical pharmacology expert, analyze potential interactions between these medications: {drugs_str}

Provide a detailed interaction analysis structured as follows:

**1. Interaction Overview:**
Brief summary of the most significant interactions

**2. Specific Drug-Drug Interactions:**
For each pair of drugs that interact, describe:
- The type of interaction (pharmacokinetic, pharmacodynamic)
- Severity level (Minor, Moderate, Major, Contraindicated)
- Clinical significance and potential consequences
- Mechanism of interaction

**3. Risk Assessment:**
Overall risk level when combining these medications

**4. Clinical Recommendations:**
- Monitoring requirements
- Dose adjustments needed
- Alternative medications to consider
- When to seek immediate medical attention

**5. Time-Sensitive Considerations:**
Spacing requirements or timing of administration

Be specific, evidence-based, and clinically relevant. Prioritize patient safety."""

        messages = [
            {"role": "system", "content": "You are a clinical pharmacology expert specializing in drug interactions. Provide accurate, evidence-based analysis with clear safety recommendations. Always emphasize the importance of consulting healthcare professionals."},
            {"role": "user", "content": prompt}
        ]
        
        result = self._make_api_call(messages)
        
        if result:
            return f"""🔍 **Drug Interaction Analysis**
{'=' * 60}

**Medications Analyzed:** {drugs_str}

{result}

{'=' * 60}
⚠️ **IMPORTANT DISCLAIMER:**
This interaction analysis is for informational purposes only. Drug interactions can be complex and patient-specific. Always consult with a healthcare professional or pharmacist before combining medications."""
        else:
            return self._get_mock_interactions(drugs_str)
    
    def _get_mock_interactions(self, drugs_str):
        """Fallback interaction data when API is unavailable"""
        return f"""🔍 Drug Interaction Analysis (Demo Mode)
{'=' * 60}

Drugs: {drugs_str}

⚠️ **API Service Unavailable**

**General Interaction Guidance:**

**High-Risk Combinations:**
• Multiple NSAIDs (e.g., Aspirin + Ibuprofen)
  - Risk: Increased GI bleeding
  - Severity: HIGH
  - Action: Avoid combination

• Blood Thinners + Antiplatelet agents
  - Risk: Enhanced bleeding effects
  - Severity: MAJOR
  - Action: Requires medical supervision

• Medications affecting liver enzymes
  - Risk: Altered drug metabolism
  - Severity: MODERATE to HIGH
  - Action: Monitor closely

**Recommended Actions:**
1. Consult pharmacist or physician
2. Provide complete medication list
3. Report all supplements and OTC drugs
4. Monitor for unusual symptoms

{'=' * 60}
🔧 **Enable Real-Time Analysis:** Valid API key required
Status: Using fallback information"""
    
    def analyze_extracted_text(self, text):
        """Analyze drug information from extracted text with professional medical review"""
        if not self.is_real or not self.client:
            return self._get_mock_text_analysis(text)
        
        # Professional prompt for analyzing extracted drug information
        prompt = f"""As a pharmaceutical information specialist, analyze the following text extracted from a medication label or prescription:

TEXT CONTENT:
{text[:1500]}

Please provide a structured analysis:

**1. Medication Identification:**
- Drug name(s) and active ingredients
- Strength/dosage
- Pharmaceutical form (tablet, capsule, liquid, etc.)

**2. Usage Information:**
- Therapeutic use/indications
- Recommended dosage and frequency
- Administration instructions

**3. Safety Profile:**
- Key side effects to monitor
- Critical warnings and precautions
- Contraindications (who should not take this)

**4. Storage and Handling:**
- Proper storage conditions
- Expiration considerations

**5. Patient Counseling Points:**
- Important information for patients
- When to contact healthcare provider

Be thorough but concise. Prioritize safety-critical information."""

        messages = [
            {"role": "system", "content": "You are a pharmaceutical information specialist helping interpret medication labels and prescriptions. Provide accurate, safety-focused analysis. Always recommend consulting healthcare professionals for personalized medical advice."},
            {"role": "user", "content": prompt}
        ]
        
        result = self._make_api_call(messages)
        
        if result:
            return f"""📄 **Medication Information Analysis**
{'=' * 60}

**Extracted Text Preview:**
{text[:200]}{'...' if len(text) > 200 else ''}

{'─' * 60}

{result}

{'=' * 60}
⚠️ **Medical Disclaimer:**
This analysis is AI-generated and for informational purposes only. 
Always follow your healthcare provider's instructions and consult 
them with any questions about your medication."""
        else:
            return self._get_mock_text_analysis(text)
    
    def _get_mock_text_analysis(self, text):
        """Fallback text analysis when API is unavailable"""
        preview = text[:300] if len(text) > 300 else text
        return f"""📄 **OCR Text Extraction - Demo Mode**
{'=' * 60}

**Extracted Text:**
{preview}...

**Demo Analysis:**

**Medication Information Detected:**
• Drug name: [Extracted from image]
• Dosage form: [Tablet/Capsule/Liquid]
• Active ingredients identified

**Common Safety Points:**
1. **Side Effects to Monitor:**
   - Nausea or upset stomach
   - Dizziness or drowsiness
   - Allergic reactions (rash, itching)

2. **Important Warnings:**
   - Take as directed by physician
   - Do not exceed recommended dose
   - Store at room temperature

3. **When to Contact Doctor:**
   - Severe side effects
   - No improvement after specified time
   - Signs of allergic reaction

**Storage Instructions:**
• Keep in original container
• Protect from light and moisture
• Keep out of reach of children

{'=' * 60}
🔧 **Enable Professional AI Analysis:**
Configure OpenAI API key for detailed medication review

⚠️ Status: Using demonstration interpretation (API unavailable)"""