# Models Directory

This directory should contain the trained ML model files:

- `improved_forecasting_model.joblib` - Main trained model
- `improved_model_encoders.joblib` - Categorical encoders
- `improved_model_info.json` - Model metadata

## Note for Render Deployment

Due to file size limitations, you may need to:
1. Upload model files separately after deployment
2. Use a cloud storage service (AWS S3, Google Cloud Storage)
3. Or deploy without the model files (app will use fallback prediction logic)

The application will work with or without these files.