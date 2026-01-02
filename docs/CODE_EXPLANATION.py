"""
MEDDI AI - CODE EXPLANATION FOR BEGINNERS

This document explains how the machine learning models work in simple terms.
Perfect for beginners learning AI/ML concepts.
"""

# ==============================================================================
# PART 1: UNDERSTANDING THE DATA
# ==============================================================================

"""
WHAT IS TRAINING DATA?

Training data is like a textbook that teaches the AI model. It contains 
examples that the model learns from.

Example from drug_side_effects.csv:
    drug_name     | side_effect
    --------------|----------------
    aspirin       | stomach upset
    aspirin       | bleeding
    aspirin       | nausea
    ibuprofen     | dizziness
    ibuprofen     | stomach pain

The model learns: "When I see aspirin, I should predict these side effects"
"""

# ==============================================================================
# PART 2: HOW FEATURE 1 WORKS (Side Effects Prediction)
# ==============================================================================

"""
FEATURE 1: Single Drug Side Effects Prediction

PROBLEM: Given a drug name, predict its side effects

SOLUTION: Multi-Label Classification
- One drug can have MULTIPLE side effects
- We need to predict ALL of them

STEP-BY-STEP PROCESS:

1. TRAINING PHASE (Done once in train_models.py)
   ================================================
   
   Step 1: Load the data
   ---------------------
   drug_name     | side_effect
   aspirin       | stomach upset
   aspirin       | bleeding
   ibuprofen     | dizziness
   
   Step 2: Convert drug names to numbers (LabelEncoder)
   ----------------------------------------------------
   Why? Computers only understand numbers, not text!
   
   aspirin   -> 0
   ibuprofen -> 1
   metformin -> 2
   
   Step 3: Convert side effects to binary matrix (MultiLabelBinarizer)
   ------------------------------------------------------------------
   Each column represents one side effect. 1 = has it, 0 = doesn't
   
   Drug      | bleeding | dizziness | nausea | stomach_pain
   ----------|----------|-----------|--------|-------------
   aspirin   |    1     |     0     |   1    |      0
   ibuprofen |    0     |     1     |   0    |      1
   metformin |    0     |     0     |   1    |      0
   
   Step 4: Train Random Forest Model
   ---------------------------------
   Random Forest = Multiple decision trees working together
   
   Each tree learns patterns like:
   - If drug_id = 0 (aspirin), predict [1, 0, 1, 0]
   - If drug_id = 1 (ibuprofen), predict [0, 1, 0, 1]
   
   Why 100 trees? More trees = better accuracy
   
   Step 5: Save the trained model
   ------------------------------
   Save to disk so we don't need to retrain every time!
   - side_effects_model.pkl (the trained model)
   - drug_encoder.pkl (remembers drug name -> number mapping)
   - side_effects_encoder.pkl (remembers side effect names)


2. PREDICTION PHASE (Done in side_effects_analyzer.py)
   ===================================================
   
   User Input: "aspirin"
   
   Step 1: Load saved models
   ------------------------
   Load the models we trained earlier
   
   Step 2: Convert "aspirin" to number
   ----------------------------------
   "aspirin" -> 0 (using drug_encoder)
   
   Step 3: Ask the model to predict
   --------------------------------
   Input: [0]
   Model thinks: "I learned that 0 means these side effects..."
   Output: [1, 0, 1, 0] (binary array)
   
   Step 4: Convert back to human-readable text
   -------------------------------------------
   [1, 0, 1, 0] -> ["bleeding", "nausea"]
   
   Return to user: "Side effects: bleeding, nausea"


SIMPLE ANALOGY:
--------------
Training = Teacher showing flashcards to a student
- Flashcard front: "aspirin"
- Flashcard back: "bleeding, nausea"
- Student memorizes the patterns

Prediction = Student takes a test
- Question: "What are side effects of aspirin?"
- Student recalls from memory: "bleeding, nausea"
"""

# ==============================================================================
# PART 3: HOW FEATURE 2 WORKS (Drug Interactions)
# ==============================================================================

"""
FEATURE 2: Drug-Drug Interaction Risk Prediction

PROBLEM: Given TWO drugs, predict if they're Safe/Moderate/Dangerous together

SOLUTION: Multi-Class Classification
- Input: Two drugs
- Output: One risk level (Safe, Moderate, or Dangerous)

STEP-BY-STEP PROCESS:

1. TRAINING PHASE (Done once in train_models.py)
   ================================================
   
   Step 1: Load interaction data
   -----------------------------
   drugA     | drugB     | interaction_risk
   aspirin   | warfarin  | Dangerous
   ibuprofen | metformin | Safe
   aspirin   | ibuprofen | Moderate
   
   Step 2: Convert drug names to numbers
   -------------------------------------
   aspirin   -> 0
   warfarin  -> 1
   ibuprofen -> 2
   metformin -> 3
   
   Step 3: Create feature pairs
   ----------------------------
   Each row becomes [drugA_id, drugB_id]
   
   [0, 1]  <- aspirin + warfarin
   [2, 3]  <- ibuprofen + metformin
   [0, 2]  <- aspirin + ibuprofen
   
   Step 4: Encode risk levels
   --------------------------
   Safe      -> 0
   Moderate  -> 1
   Dangerous -> 2
   
   Step 5: Train Random Forest Classifier
   --------------------------------------
   Model learns patterns:
   - If drugs are [0, 1], predict 2 (Dangerous)
   - If drugs are [2, 3], predict 0 (Safe)
   
   Step 6: Save the trained model
   ------------------------------


2. PREDICTION PHASE (Done in interaction_checker.py)
   =================================================
   
   User Input: ["aspirin", "warfarin"]
   
   Step 1: Convert both drugs to numbers
   ------------------------------------
   "aspirin"  -> 0
   "warfarin" -> 1
   Feature: [0, 1]
   
   Step 2: Ask model to predict
   ----------------------------
   Input: [0, 1]
   Model: "I learned this combination is risky..."
   Output: 2 (Dangerous)
   
   Step 3: Convert number back to risk level
   -----------------------------------------
   2 -> "Dangerous"
   
   Step 4: Add helpful description
   -------------------------------
   Return: {
       "risk": "Dangerous",
       "description": "High risk! Do not combine without supervision"
   }


SIMPLE ANALOGY:
--------------
Training = Learning which food combinations are bad
- Pizza + Ice cream = Safe
- Milk + Fish = Moderate (some people get upset stomach)
- Alcohol + Medicine = Dangerous!

Prediction = Checking if new combination is safe
- Input: "Milk + Fish"
- Memory: "Oh, I learned this is Moderate risk"
- Output: "Be careful, might cause issues"
"""

# ==============================================================================
# PART 4: HOW FEATURE 3 WORKS (OCR + Analysis)
# ==============================================================================

"""
FEATURE 3: Extract Drug Text from Image and Analyze

PROBLEM: User has a photo of prescription. Extract drugs and analyze them.

SOLUTION: OCR (Optical Character Recognition) + ML Models

STEP-BY-STEP PROCESS:

1. OCR (Text Extraction)
   ======================
   
   Input: Image file (prescription.jpg)
   
   Step 1: Load image
   -----------------
   Use PIL (Python Imaging Library)
   
   Step 2: Extract text using Tesseract
   ------------------------------------
   Tesseract = Free OCR software by Google
   Scans image and converts to text
   
   Input:  [Image of prescription]
   Output: "Take Aspirin 100mg daily and Ibuprofen 200mg for pain"


2. Drug Name Detection
   ====================
   
   Step 1: Get list of known drugs
   ------------------------------
   Load from drug_encoder (all drugs we trained on)
   
   Step 2: Search for drug names in text
   -------------------------------------
   Text: "Take Aspirin 100mg daily and Ibuprofen 200mg"
   
   Pattern matching:
   - Search for "aspirin" -> FOUND!
   - Search for "ibuprofen" -> FOUND!
   - Search for "paracetamol" -> NOT FOUND
   
   Result: ["aspirin", "ibuprofen"]


3. Analysis Pipeline
   ==================
   
   Step 1: For each detected drug, run Feature 1
   ---------------------------------------------
   Aspirin:
   - Side effects: bleeding, nausea, stomach upset
   
   Ibuprofen:
   - Side effects: dizziness, stomach pain
   
   Step 2: If multiple drugs found, run Feature 2
   ----------------------------------------------
   Check: aspirin + ibuprofen
   Result: Moderate risk
   
   Step 3: Compile comprehensive report
   -----------------------------------
   Return:
   - Extracted text
   - Detected drugs
   - Side effects for each
   - Interaction warnings


SIMPLE ANALOGY:
--------------
Like a doctor reading a prescription:

1. Read the handwriting (OCR)
2. Identify the medicines (Drug Detection)
3. Look up each medicine's effects (Feature 1)
4. Check if they interact badly (Feature 2)
5. Give complete advice to patient (Report)
"""

# ==============================================================================
# PART 5: UNDERSTANDING RANDOM FOREST
# ==============================================================================

"""
WHAT IS RANDOM FOREST?

Imagine asking 100 doctors about a drug:
- Doctor 1: "This drug causes nausea"
- Doctor 2: "This drug causes dizziness"
- Doctor 3: "This drug causes nausea"
...
- Majority vote: "Nausea" wins!

Random Forest = Multiple decision trees voting together

DECISION TREE EXAMPLE:
----------------------

                    Drug ID = 0?
                   /            \\
                 Yes             No
                  |              |
           Predict: bleeding     Drug ID = 1?
                                /          \\
                              Yes           No
                               |            |
                        Predict: dizziness  ...


WHY RANDOM FOREST IS GOOD:
--------------------------
1. Accurate: Multiple trees reduce mistakes
2. Fast: Can predict quickly once trained
3. Handles complex patterns: Each tree learns different things
4. No internet needed: Runs locally on your computer


HYPERPARAMETERS EXPLAINED:
--------------------------
n_estimators=100
    How many trees? More = better accuracy, slower training
    
max_depth=10
    How deep can each tree grow?
    Deeper = more complex patterns, risk of overfitting
    
random_state=42
    Random seed for reproducibility
    Same seed = same results every time
    
n_jobs=-1
    Use all CPU cores for faster training
"""

# ==============================================================================
# PART 6: UNDERSTANDING ENCODERS
# ==============================================================================

"""
WHY DO WE NEED ENCODERS?

Problem: Machine learning models only understand numbers
Solution: Convert text to numbers!


1. LABEL ENCODER
   ==============
   
   Converts categories to numbers (one-to-one mapping)
   
   Example:
   --------
   Drug names:
   - "aspirin"   -> 0
   - "ibuprofen" -> 1
   - "metformin" -> 2
   
   Risk levels:
   - "Safe"      -> 0
   - "Moderate"  -> 1
   - "Dangerous" -> 2
   
   Usage:
   ------
   encoder.fit(['aspirin', 'ibuprofen'])  # Learn mapping
   encoder.transform(['aspirin'])          # Convert to [0]
   encoder.inverse_transform([0])          # Convert back to ['aspirin']


2. MULTI-LABEL BINARIZER
   ======================
   
   Converts multiple labels to binary matrix
   
   Example:
   --------
   Drug -> Side effects (multiple possible)
   
   Input:
   - aspirin: ['bleeding', 'nausea']
   - ibuprofen: ['dizziness']
   
   Output (binary matrix):
   
            bleeding | dizziness | nausea
   aspirin     1     |     0     |   1
   ibuprofen   0     |     1     |   0
   
   Usage:
   ------
   mlb.fit([['bleeding', 'nausea'], ['dizziness']])
   mlb.transform([['bleeding', 'nausea']])  # -> [[1, 0, 1]]
   mlb.inverse_transform([[1, 0, 1]])       # -> [['bleeding', 'nausea']]


WHY SAVE ENCODERS?
------------------
Without saving:
- User inputs "aspirin"
- We don't know what number it was encoded to!
- Can't make prediction

With saving:
- Load encoder from disk
- "aspirin" -> 0 (remember from training)
- Make prediction successfully!
"""

# ==============================================================================
# PART 7: MODEL PERSISTENCE (Saving/Loading)
# ==============================================================================

"""
WHY SAVE MODELS?

Training takes time (minutes)
Prediction should be instant (milliseconds)

Solution: Train once, save to disk, load when needed!


USING JOBLIB:
=============

Saving:
-------
import joblib

# After training
joblib.dump(model, 'model.pkl')
joblib.dump(encoder, 'encoder.pkl')

Loading:
--------
# Later, when making predictions
model = joblib.load('model.pkl')
encoder = joblib.load('encoder.pkl')

# Now use them!
prediction = model.predict(data)


FILE FORMATS:
-------------
.pkl = Pickle file (Python object serialization)
- Stores trained models
- Stores encoders with their learned mappings
- Can be loaded back into memory


WHAT GETS SAVED:
----------------

For Feature 1 (Side Effects):
- side_effects_model.pkl (Random Forest model)
- drug_encoder.pkl (drug name -> ID mapping)
- side_effects_encoder.pkl (side effect names)

For Feature 2 (Interactions):
- interaction_model.pkl (Random Forest classifier)
- interaction_drug_encoder.pkl (drug names -> IDs)
- risk_encoder.pkl (risk level mappings)


WORKFLOW:
---------

TRAINING (once):
train_models.py runs -> Models saved to disk

PREDICTION (many times):
main.py starts -> Load models from disk -> Make predictions
"""

# ==============================================================================
# PART 8: CODE STRUCTURE EXPLAINED
# ==============================================================================

"""
PROJECT FILES & WHAT THEY DO:

1. DATA FILES
   ===========
   data/drug_side_effects.csv
   - Training data for Feature 1
   - Contains drug-side effect pairs
   
   data/drug_interactions.csv
   - Training data for Feature 2
   - Contains drug pairs and risk levels


2. TRAINING
   =========
   src/train_models.py
   - Loads CSV data
   - Trains ML models
   - Saves models to disk
   - RUN THIS FIRST!


3. PREDICTION SERVICES
   ===================
   src/services/side_effects_analyzer.py
   - Implements Feature 1
   - Loads saved model
   - Predicts side effects
   
   src/services/interaction_checker.py
   - Implements Feature 2
   - Loads saved model
   - Predicts interaction risk
   
   src/services/image_processor.py
   - Implements Feature 3
   - OCR text extraction
   - Uses Features 1 & 2


4. USER INTERFACES
   ===============
   src/main.py
   - Main application
   - CLI interface (--cli flag)
   - Web server (Flask)
   
   demo.py
   - Demonstrates all features
   - Shows example outputs


5. SAVED MODELS
   ============
   src/models/ (auto-generated after training)
   - *.pkl files (binary)
   - Loaded at runtime
"""

# ==============================================================================
# PART 9: COMMON QUESTIONS
# ==============================================================================

"""
Q: Why Random Forest and not other algorithms?

A: Random Forest is great for beginners because:
   - Easy to understand (voting concept)
   - Works well with small datasets
   - No complex hyperparameter tuning needed
   - Fast predictions
   - Handles both classification tasks


Q: Can I use this for real medical decisions?

A: NO! This is for EDUCATION ONLY because:
   - Limited training data
   - Not validated by medical experts
   - Not FDA approved
   - Missing many drug interactions
   - Always consult real doctors!


Q: How accurate is the model?

A: Depends on training data quality:
   - With provided data: ~90-95% accuracy
   - With more data: Can improve
   - But predictions are only as good as training data


Q: Do I need internet to run this?

A: NO! Everything runs locally:
   - Models saved on your computer
   - Predictions made offline
   - No API calls
   - Privacy-friendly


Q: How do I add more drugs?

A: 3 steps:
   1. Add rows to CSV files
   2. Run train_models.py again
   3. Models automatically updated!


Q: Can I use other ML algorithms?

A: YES! Easy to swap:
   
   Instead of:
   model = RandomForestClassifier()
   
   Try:
   from sklearn.tree import DecisionTreeClassifier
   model = DecisionTreeClassifier()
   
   Or:
   from sklearn.svm import SVC
   model = SVC()
   
   Just change in train_models.py!


Q: What if drug is not in database?

A: Model returns friendly error:
   "Drug 'xyz' not found in database"
   "Available drugs include: ..."
   
   Solution: Add to CSV and retrain


Q: How long does training take?

A: Very fast!
   - ~30 drugs: 1-2 seconds
   - ~100 drugs: 5-10 seconds
   - ~1000 drugs: 1-2 minutes
   
   Depends on your computer speed
"""

# ==============================================================================
# PART 10: LEARNING RESOURCES
# ==============================================================================

"""
WANT TO LEARN MORE?

1. Machine Learning Basics:
   - Course: Andrew Ng's ML course (Coursera)
   - Book: "Hands-On Machine Learning" by Aurélien Géron
   
2. Scikit-learn (Library we use):
   - Website: scikit-learn.org
   - Tutorials: scikit-learn.org/stable/tutorial
   
3. Random Forest:
   - Visual explanation: r2d3.us/visual-intro-to-machine-learning
   - sklearn docs: scikit-learn.org/stable/modules/ensemble.html
   
4. OCR with Tesseract:
   - GitHub: github.com/tesseract-ocr/tesseract
   - Tutorial: pyimagesearch.com/category/ocr
   
5. Flask (Web framework):
   - Tutorial: flask.palletsprojects.com/quickstart
   

KEY CONCEPTS TO UNDERSTAND:
---------------------------
1. Supervised Learning: Learning from labeled examples
2. Classification: Predicting categories
3. Multi-label: Multiple outputs per input
4. Train-Test Split: Evaluate on unseen data
5. Ensemble Methods: Combining multiple models
6. Feature Engineering: Converting data for models
7. Model Persistence: Saving and loading models


EXPERIMENT IDEAS:
-----------------
1. Try different ML algorithms (Decision Tree, SVM, etc.)
2. Add more drugs to the datasets
3. Build a web UI with better styling
4. Add a recommendation system
5. Create a mobile app interface
6. Add more features (dosage, drug form, etc.)
7. Implement model versioning
8. Add model performance monitoring


NEXT STEPS:
-----------
1. ✓ Read this file
2. ✓ Read train_models.py (well commented!)
3. ✓ Read service files (prediction logic)
4. ✓ Run demo.py to see it working
5. ✓ Experiment with parameters
6. ✓ Add your own drugs
7. ✓ Build new features!
"""

# ==============================================================================
# CONCLUSION
# ==============================================================================

"""
CONGRATULATIONS! 🎉

You now understand:
✓ How ML models learn from data
✓ How predictions are made
✓ How text is converted to numbers
✓ How models are saved and loaded
✓ How all three features work together

This is a complete, working AI system that you can:
- Study and learn from
- Modify and experiment with
- Use as a foundation for your own projects

Remember: The best way to learn is by doing!
Try changing things, break stuff, fix it, and learn.

Good luck with your AI journey! 🚀

-- Meddi AI Team
"""
