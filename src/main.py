from flask import Flask, jsonify, render_template
import sys
import traceback

# Create app first
app = Flask(__name__, template_folder='templates', static_folder='static')

# Register blueprint
from routes.api_routes import api_bp
app.register_blueprint(api_bp)

@app.route('/')
def index():
    """Serve the web UI"""
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'Server is running'}), 200

@app.errorhandler(Exception)
def handle_error(error):
    """Global error handler"""
    print(f"Error: {error}")
    traceback.print_exc()
    return jsonify({'error': str(error)}), 500

def interactive_mode():
    """CLI interface for the application"""
    print("=== Drug Side Effects Analyzer ===\n")
    
    analyzer = SideEffectsAnalyzer()
    checker = InteractionChecker()
    image_proc = ImageProcessor()
    
    while True:
        print("\n1. Find side effects of a drug")
        print("2. Check drug interactions")
        print("3. Analyze drug image")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            drug_name = input("Enter drug name: ").strip()
            if validate_input(drug_name):
                result = analyzer.analyze(drug_name)
                print(f"\nSide Effects:\n{result}\n")
            else:
                print("Invalid input!")
        
        elif choice == "2":
            drugs = input("Enter drug names (comma-separated): ").strip().split(",")
            drugs = [d.strip() for d in drugs if validate_input(d.strip())]
            if len(drugs) >= 2:
                result = checker.check(drugs)
                print(f"\nInteractions:\n{result}\n")
            else:
                print("Please enter at least 2 valid drug names!")
        
        elif choice == "3":
            image_path = input("Enter image path: ").strip()
            result = image_proc.extract_text(image_path)
            if isinstance(result, str):
                print(f"\nExtracted Text:\n{result}\n")
            else:
                print(f"Error: {result.get('error')}")
        
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        interactive_mode()
    else:
        app.run(debug=False, port=5001, host='127.0.0.1', use_reloader=False)