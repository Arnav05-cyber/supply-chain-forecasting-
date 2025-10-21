# Trained Models

Pre-trained machine learning models and encoders.

## Files
- `improved_forecasting_model.joblib` - Best model (5.41% MAPE)
- `improved_model_encoders.joblib` - Categorical encoders
- `improved_model_info.json` - Model metadata
- `*_package.pkl` - Complete model packages

## Usage
```python
import joblib
model = joblib.load('improved_forecasting_model.joblib')
```
