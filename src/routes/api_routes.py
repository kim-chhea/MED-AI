from flask import Blueprint, request, jsonify, send_file
import os

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/status', methods=['GET'])
def api_status():
    """Check ML models status"""
    try:
        from services.side_effects_analyzer import SideEffectsAnalyzer
        from services.interaction_checker import InteractionChecker
        import os
        
        # Check if ML models are trained and available
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        models_exist = os.path.exists(models_dir) and len(os.listdir(models_dir)) > 0
        
        # Try to load analyzers
        analyzer = SideEffectsAnalyzer()
        checker = InteractionChecker()
        
        models_loaded = (analyzer.model is not None and checker.model is not None)
        
        return jsonify({
            'configured': True,
            'operational': models_loaded,
            'mode': 'ml_local',
            'models_trained': models_loaded,
            'system': 'Drug Analysis System',
            'message': 'System operational' if models_loaded else 'System not ready. Run train_models.py first.'
        }), 200
    except Exception as e:
        return jsonify({
            'configured': False,
            'operational': False,
            'mode': 'ml_local',
            'models_trained': False,
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
        # Check if image processor is available
        try:
            from services.image_processor import ImageProcessor
        except ImportError:
            return jsonify({'error': 'Image analysis feature is temporarily unavailable due to OCR library compatibility'}), 503
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Import here to avoid initialization issues
        processor = ImageProcessor()
        result = processor.extract_and_analyze(file)
        
        return jsonify({'result': result}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/download-template', methods=['GET'])
def download_template():
    """Download CSV template for custom dataset"""
    try:
        import os
        dataset_type = request.args.get('type', '')
        
        # Define template paths
        templates = {
            'side_effects': os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'drug_side_effects.csv'),
            'interactions': os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'drug_interactions.csv')
        }
        
        if dataset_type not in templates:
            return jsonify({'error': 'Invalid template type'}), 400
        
        template_path = templates[dataset_type]
        
        if not os.path.exists(template_path):
            return jsonify({'error': 'Template file not found'}), 404
        
        return send_file(
            template_path,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{dataset_type}_template.csv'
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/upload-dataset', methods=['POST'])
def upload_dataset():
    """Upload custom dataset CSV file"""
    try:
        import os
        import pandas as pd
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        dataset_type = request.form.get('type', '')
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'success': False, 'error': 'File must be CSV format'}), 400
        
        if dataset_type not in ['side_effects', 'interactions']:
            return jsonify({'success': False, 'error': 'Invalid dataset type'}), 400
        
        # Create uploads directory if it doesn't exist
        uploads_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads')
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        
        # Save the uploaded file
        filename = f'custom_{dataset_type}.csv'
        filepath = os.path.join(uploads_dir, filename)
        file.save(filepath)
        
        # Validate CSV structure
        try:
            df = pd.read_csv(filepath)
            
            # Check required columns
            if dataset_type == 'side_effects':
                required_columns = ['drug_name', 'side_effect']
            else:  # interactions
                required_columns = ['drugA', 'drugB', 'interaction_risk']
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                os.remove(filepath)
                return jsonify({
                    'success': False, 
                    'error': f'Missing required columns: {", ".join(missing_columns)}'
                }), 400
            
            record_count = len(df)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'records': record_count,
                'message': f'Successfully uploaded {record_count} records'
            }), 200
            
        except Exception as e:
            # Clean up file if validation fails
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({
                'success': False,
                'error': f'Invalid CSV format: {str(e)}'
            }), 400
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/retrain-models', methods=['POST'])
def retrain_models():
    """Retrain models with custom datasets"""
    try:
        import os
        import sys
        
        data = request.get_json() or {}
        side_effects_file = data.get('side_effects_file')
        interactions_file = data.get('interactions_file')
        
        if not side_effects_file or not interactions_file:
            return jsonify({
                'success': False,
                'error': 'Both dataset files are required'
            }), 400
        
        # Construct file paths
        uploads_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads')
        side_effects_path = os.path.join(uploads_dir, side_effects_file)
        interactions_path = os.path.join(uploads_dir, interactions_file)
        
        # Verify files exist
        if not os.path.exists(side_effects_path):
            return jsonify({
                'success': False,
                'error': 'Side effects dataset not found'
            }), 404
        
        if not os.path.exists(interactions_path):
            return jsonify({
                'success': False,
                'error': 'Interactions dataset not found'
            }), 404
        
        # Import training functions
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from train_models import train_side_effects_model, train_interaction_model
        
        # Train models with custom datasets (save to models/custom/)
        side_effects_accuracy = train_side_effects_model(data_path=side_effects_path, custom=True)
        interactions_accuracy = train_interaction_model(data_path=interactions_path, custom=True)
        
        # Save config to indicate custom models are active
        config_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'model_config.json')
        with open(config_path, 'w') as f:
            import json
            json.dump({'mode': 'custom'}, f)
        
        return jsonify({
            'success': True,
            'side_effects_accuracy': f'{side_effects_accuracy:.2%}',
            'interactions_accuracy': f'{interactions_accuracy:.2%}',
            'message': 'Models trained successfully with custom datasets'
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/switch-dataset-mode', methods=['POST'])
def switch_dataset_mode():
    """Switch between built-in and custom dataset mode"""
    try:
        import json
        
        data = request.get_json() or {}
        mode = data.get('mode', 'builtin')  # 'builtin' or 'custom'
        
        # Save config
        config_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'model_config.json')
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump({'mode': mode}, f)
        
        return jsonify({
            'success': True,
            'mode': mode,
            'message': f'Switched to {mode} dataset mode'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
