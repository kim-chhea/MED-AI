from .helpers import validate_drug_name

def validate_input(drug_name):
    """Validate user input for drug names"""
    if not isinstance(drug_name, str):
        return False
    drug_name = drug_name.strip()
    return len(drug_name) > 0 and len(drug_name) <= 100

__all__ = ['validate_input', 'validate_drug_name']