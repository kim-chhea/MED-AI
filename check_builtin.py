import joblib
import numpy as np

# Load built-in models
encoder = joblib.load('src/models/drug_encoder.pkl')
mlb = joblib.load('src/models/side_effects_encoder.pkl')
model = joblib.load('src/models/side_effects_model.pkl')

# Predict for aspirin
drug_idx = encoder.transform(['aspirin'])[0]
pred = model.predict([[drug_idx]])
effects = [e for e, v in zip(mlb.classes_, pred[0]) if v == 1]

print('Built-in model aspirin side effects:')
for i, e in enumerate(effects, 1):
    print(f'{i}. {e}')
print(f'\nTotal: {len(effects)} side effects')
