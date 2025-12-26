# Drug Side Effects Analyzer

## Overview
The Drug Side Effects Analyzer is a Python application that integrates the ChatGPT API to analyze drug side effects. It provides users with the ability to identify side effects of specific drugs, check interactions between multiple drugs, and upload images of drugs for text extraction.

## Features
- **Side Effects Analysis**: Users can input a drug name to retrieve associated side effects using the ChatGPT API.
- **Drug Interaction Checker**: Analyze potential side effects from interactions between multiple drugs.
- **Image Upload and Text Extraction**: Users can upload images of drugs, and the application will extract text for further analysis.

## Project Structure
```
drug-side-effects-analyzer
├── src
│   ├── main.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── chatgpt_client.py
│   │   └── drug_api.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── side_effects_analyzer.py
│   │   ├── interaction_checker.py
│   │   └── image_processor.py
│   ├── models
│   │   ├── __init__.py
│   │   └── drug.py
│   └── utils
│       ├── __init__.py
│       └── helpers.py
├── tests
│   ├── __init__.py
│   ├── test_side_effects.py
│   ├── test_interactions.py
│   └── test_image_processor.py
├── config
│   ├── __init__.py
│   └── settings.py
├── requirements.txt
├── .env.example
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/drug-side-effects-analyzer.git
   ```
2. Navigate to the project directory:
   ```
   cd drug-side-effects-analyzer
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Set up your environment variables by copying `.env.example` to `.env` and filling in the necessary values.
2. Run the application:
   ```
   python src/main.py
   ```
3. Access the application through your web browser or API client.

## Testing
To run the tests, use the following command:
```
pytest
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.