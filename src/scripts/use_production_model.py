#!/usr/bin/env python3
"""
Load and use the production forecasting model
"""

import joblib
import json
import pandas as pd
import numpy as np

def load_production_model():
    """Load the production model"""
    model = joblib.load('production_forecasting_model.joblib')
    encoders = joblib.load('production_encoders.joblib')
    
    with open('production_model_info.json', 'r') as f:
        info = json.load(f)
    
    return model, encoders, info

def predict_sales(model, encoders, data):
    """Make predictions using the model"""
    feature_columns = [
        'item_id_encoded', 'dept_id_encoded', 'cat_id_encoded', 
        'store_id_encoded', 'state_id_encoded', 'sell_price', 
        'day_of_week', 'month', 'quarter', 'is_weekend',
        'lag_7', 'lag_14', 'lag_28', 'rolling_mean_7', 
        'rolling_mean_14', 'rolling_std_7', 'rolling_std_14'
    ]
    
    X = data[feature_columns].fillna(0)
    predictions = model.predict(X)
    
    return predictions

if __name__ == "__main__":
    # Load model
    model, encoders, info = load_production_model()
    print(f"Model loaded: {info['performance']['mape']:.2f}% MAPE")
    print("Ready for predictions!")
