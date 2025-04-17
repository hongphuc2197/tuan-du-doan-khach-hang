import sys
import json
import joblib
import numpy as np
import pandas as pd
import os

def predict_customer(data):
    # Get the directory path of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(current_dir))
    
    # Load model and scaler
    model_path = os.path.join(root_dir, 'optimized_model.pkl')
    scaler_path = os.path.join(root_dir, 'optimized_scaler.pkl')
    
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
    except Exception as e:
        return {
            'error': f'Error loading model or scaler: {str(e)}'
        }
    
    try:
        # Convert data to DataFrame
        input_data = pd.DataFrame([data])
        
        # Scale the data
        input_scaled = scaler.transform(input_data)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]
        
        return {
            'prediction': int(prediction),
            'probability': float(probability),
            'success': True
        }
    except Exception as e:
        return {
            'error': f'Error during prediction: {str(e)}'
        }

if __name__ == '__main__':
    try:
        # Read data from command line
        data = json.loads(sys.argv[1])
        
        # Make prediction
        result = predict_customer(data)
        
        # Print result
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({
            'error': f'Error processing request: {str(e)}'
        })) 