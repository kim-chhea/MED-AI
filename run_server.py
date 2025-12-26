import sys
import traceback
sys.path.insert(0, '.')

try:
    from flask import Flask, jsonify
    from routes.api_routes import api_bp
    from utils import validate_input
    
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    
    @app.route('/')
    def health_check():
        """Health check endpoint"""
        return {'status': 'Server is running'}, 200
    
    @app.errorhandler(Exception)
    def handle_error(error):
        """Global error handler"""
        print(f"ERROR: {error}", file=sys.stderr)
        traceback.print_exc()
        return jsonify({'error': str(error)}), 500
    
    if __name__ == "__main__":
        print("Starting server...")
        app.run(debug=False, port=5000, host='127.0.0.1', use_reloader=False, threaded=True)
    
except Exception as e:
    print(f"FATAL ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
