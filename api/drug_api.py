from flask import Blueprint, request, jsonify
from services.side_effects_analyzer import SideEffectsAnalyzer
from services.interaction_checker import InteractionChecker

drug_api = Blueprint('drug_api', __name__)

@drug_api.route('/side_effects', methods=['GET'])
def get_side_effects():
    drug_name = request.args.get('drug_name')
    if not drug_name:
        return jsonify({'error': 'Drug name is required'}), 400
    
    analyzer = SideEffectsAnalyzer()
    side_effects = analyzer.analyze_side_effects(drug_name)
    
    return jsonify({'drug_name': drug_name, 'side_effects': side_effects})

@drug_api.route('/interactions', methods=['POST'])
def check_interactions():
    data = request.get_json()
    drug_list = data.get('drugs')
    
    if not drug_list or not isinstance(drug_list, list):
        return jsonify({'error': 'A list of drugs is required'}), 400
    
    checker = InteractionChecker()
    interactions = checker.check_interactions(drug_list)
    
    return jsonify({'drugs': drug_list, 'interactions': interactions})