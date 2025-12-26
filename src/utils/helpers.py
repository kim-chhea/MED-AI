def format_response(response):
    # Function to format the API response for better readability
    return response.get('choices', [{}])[0].get('text', '').strip()

def handle_api_error(error):
    # Function to handle API errors gracefully
    return {"error": str(error)}

def extract_drug_name_from_text(text):
    # Function to extract drug names from a given text
    # This is a placeholder for a more complex extraction logic
    return text.splitlines()  # Example: split by lines to get potential drug names

def validate_drug_name(drug_name):
    # Function to validate the drug name input
    return isinstance(drug_name, str) and len(drug_name) > 0

def prepare_request_payload(drug_name):
    # Function to prepare the payload for API requests
    return {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"Tell me about the side effects of {drug_name}."}]
    }