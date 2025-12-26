from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/status', methods=['GET'])
def api_status():
    """Check API configuration status"""
    try:
        from config import Config
        from api.chatgpt_client import ChatGPTClient
        
        client = ChatGPTClient()
        
        return jsonify({
            'configured': Config.is_api_configured(),
            'operational': client.is_real,
            'mode': 'production' if client.is_real else 'demo'
        }), 200
    except Exception as e:
        return jsonify({
            'configured': False,
            'operational': False,
            'mode': 'demo',
            'error': str(e)
        }), 200

@api_bp.route('/side-effects', methods=['POST'])
def analyze_side_effects():
    """Analyze side effects of a drug"""
    try:
        data = request.get_json() or {}
        drug_name = data.get('drug_name', '').strip()
        
        if not drug_name:
            return jsonify({'error': 'Drug name is required'}), 400
        
        # Import here to avoid initialization issues
        from services.side_effects_analyzer import SideEffectsAnalyzer
        analyzer = SideEffectsAnalyzer()
        result = analyzer.analyze(drug_name)
        
        return jsonify({'result': result}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/interactions', methods=['POST'])
def check_interactions():
    """Check drug interactions"""
    try:
        data = request.get_json() or {}
        drug_list = data.get('drug_list', [])
        
        if not isinstance(drug_list, list) or len(drug_list) < 2:
            return jsonify({'error': 'At least 2 drug names required'}), 400
        
        # Import here to avoid initialization issues
        from services.interaction_checker import InteractionChecker
        checker = InteractionChecker()
        result = checker.check(drug_list)
        
        return jsonify({'result': result}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/analyze-image', methods=['POST'])
def analyze_image():
    """Analyze drug image"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Import here to avoid initialization issues
        from services.image_processor import ImageProcessor
        processor = ImageProcessor()
        result = processor.extract_and_analyze(file)
        
        return jsonify({'result': result}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

