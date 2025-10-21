#!/usr/bin/env python3
"""
Save a working high-performance forecasting model
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import pickle
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def safe_mape(y_true, y_pred):
    """Calculate MAPE safely"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mask = y_true != 0
    if mask.sum() == 0:
        return 0.0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

def clean_data(df):
    """Clean data to remove infinities and extreme values"""
    # Replace infinities with NaN
    df = df.replace([np.inf, -np.inf], np.nan)
    
    # Fill NaN values with appropriate defaults
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if df[col].isna().any():
            median_val = df[col].median()
            if pd.isna(median_val):
                df[col] = df[col].fillna(0)
            else:
                df[col] = df[col].fillna(median_val)
    
    return df

def create_and_save_production_model():
    """Create and save a production-ready forecasting model"""
    
    print("🚀 CREATING PRODUCTION FORECASTING MODEL")
    print("=" * 50)
    
    # Load M5 dataset
    print("📊 Loading M5 dataset...")
    try:
        sales_train = pd.read_csv('m5-forecasting-accuracy/sales_train_validation.csv')
        calendar = pd.read_csv('m5-forecasting-accuracy/calendar.csv')
        sell_prices = pd.read_csv('m5-forecasting-accuracy/sell_prices.csv')
        print(f"✅ Loaded {len(sales_train)} items")
    except FileNotFoundError:
        print("❌ M5 dataset not found.")
        return None
    
    # Use a manageable sample
    print("🎯 Sampling data for optimal performance...")
    sample_items = sales_train.sample(n=500, random_state=42)  # Smaller sample for stability
    
    # Melt the data
    print("🔄 Preparing data...")
    id_cols = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
    sales_cols = [f'd_{i}' for i in range(1, 1914)]
    
    melted_data = sample_items.melt(
        id_vars=id_cols,
        value_vars=sales_cols,
        var_name='d',
        value_name='sales'
    )
    
    # Add calendar features
    melted_data = melted_data.merge(calendar, on='d', how='left')
    
    # Add price features
    melted_data = melted_data.merge(sell_prices, on=['store_id', 'item_id', 'wm_yr_wk'], how='left')
    
    # Create features
    print("🛠️ Engineering features...")
    
    # Encode categorical variables
    encoders = {}
    categorical_cols = ['item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
    
    for col in categorical_cols:
        encoder = LabelEncoder()
        melted_data[f'{col}_encoded'] = encoder.fit_transform(melted_data[col].astype(str))
        encoders[col] = encoder
    
    # Date features
    melted_data['date'] = pd.to_datetime(melted_data['date'])
    melted_data['day_of_week'] = melted_data['date'].dt.dayofweek
    melted_data['month'] = melted_data['date'].dt.month
    melted_data['quarter'] = melted_data['date'].dt.quarter
    melted_data['is_weekend'] = (melted_data['day_of_week'] >= 5).astype(int)
    
    # Price features (handle missing values)
    melted_data['sell_price'] = melted_data['sell_price'].fillna(melted_data['sell_price'].median())
    
    # Sort data for lag features
    melted_data = melted_data.sort_values(['id', 'date'])
    
    # Lag features (safe implementation)
    for lag in [7, 14, 28]:
        melted_data[f'lag_{lag}'] = melted_data.groupby('id')['sales'].shift(lag)
    
    # Rolling features (safe implementation)
    for window in [7, 14]:
        melted_data[f'rolling_mean_{window}'] = melted_data.groupby('id')['sales'].rolling(window, min_periods=1).mean().reset_index(0, drop=True)
        melted_data[f'rolling_std_{window}'] = melted_data.groupby('id')['sales'].rolling(window, min_periods=1).std().reset_index(0, drop=True)
    
    # Clean the data
    melted_data = clean_data(melted_data)
    
    # Prepare feature set
    feature_columns = [
        'item_id_encoded', 'dept_id_encoded', 'cat_id_encoded', 'store_id_encoded', 'state_id_encoded',
        'sell_price', 'day_of_week', 'month', 'quarter', 'is_weekend',
        'lag_7', 'lag_14', 'lag_28', 
        'rolling_mean_7', 'rolling_mean_14',
        'rolling_std_7', 'rolling_std_14'
    ]
    
    # Split data
    melted_data['d_num'] = melted_data['d'].str.replace('d_', '').astype(int)
    train_data = melted_data[melted_data['d_num'] <= 1913].copy()
    
    X_train = train_data[feature_columns].fillna(0)
    y_train = train_data['sales'].fillna(0)
    
    # Final data cleaning
    X_train = X_train.replace([np.inf, -np.inf], 0)
    y_train = y_train.replace([np.inf, -np.inf], 0)
    
    print(f"📊 Training data: {len(X_train)} samples, {len(feature_columns)} features")
    
    # Train the model
    print("🤖 Training RandomForest model...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_train)
    mape = safe_mape(y_train, y_pred)
    rmse = np.sqrt(np.mean((y_train - y_pred) ** 2))
    mae = np.mean(np.abs(y_train - y_pred))
    
    print(f"✅ Model trained successfully!")
    print(f"📊 Performance: MAPE: {mape:.2f}%, RMSE: {rmse:.2f}, MAE: {mae:.2f}")
    
    # Save the model
    save_production_model_files(model, encoders, feature_columns, mape, rmse, mae)
    
    return model, encoders, feature_columns

def save_production_model_files(model, encoders, feature_columns, mape, rmse, mae):
    """Save production model files"""
    
    print("\n💾 SAVING PRODUCTION MODEL...")
    print("-" * 35)
    
    # Model metadata
    model_info = {
        'model_name': 'Production Forecasting Model',
        'model_type': 'RandomForestRegressor',
        'version': '1.0 - Production Ready',
        'feature_columns': feature_columns,
        'training_date': datetime.now().isoformat(),
        'performance': {
            'mape': float(mape),
            'rmse': float(rmse),
            'mae': float(mae),
            'features_count': len(feature_columns)
        },
        'model_parameters': {
            'n_estimators': 100,
            'max_depth': 15,
            'min_samples_split': 5,
            'min_samples_leaf': 2,
            'random_state': 42
        }
    }
    
    # Save model files
    joblib.dump(model, 'production_forecasting_model.joblib')
    print("✅ Model saved as 'production_forecasting_model.joblib'")
    
    joblib.dump(encoders, 'production_encoders.joblib')
    print("✅ Encoders saved as 'production_encoders.joblib'")
    
    with open('production_model_info.json', 'w') as f:
        json.dump(model_info, f, indent=2)
    print("✅ Model info saved as 'production_model_info.json'")
    
    # Complete package
    model_package = {
        'model': model,
        'encoders': encoders,
        'feature_columns': feature_columns,
        'metadata': model_info
    }
    
    with open('production_model_package.pkl', 'wb') as f:
        pickle.dump(model_package, f)
    print("✅ Complete package saved as 'production_model_package.pkl'")
    
    # Create simple usage script
    usage_script = '''#!/usr/bin/env python3
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
'''
    
    with open('use_production_model.py', 'w') as f:
        f.write(usage_script)
    print("✅ Usage script saved as 'use_production_model.py'")
    
    print(f"\n🎉 PRODUCTION MODEL SAVED!")
    print(f"📊 Performance: {mape:.2f}% MAPE")
    print(f"📁 Files created:")
    print(f"   • production_forecasting_model.joblib")
    print(f"   • production_encoders.joblib") 
    print(f"   • production_model_info.json")
    print(f"   • production_model_package.pkl")
    print(f"   • use_production_model.py")

if __name__ == "__main__":
    model, encoders, features = create_and_save_production_model()
    
    if model is not None:
        print("\n✅ SUCCESS! Production model saved and ready!")
        
        # Test loading
        try:
            test_model = joblib.load('production_forecasting_model.joblib')
            test_encoders = joblib.load('production_encoders.joblib')
            
            with open('production_model_info.json', 'r') as f:
                test_info = json.load(f)
            
            print(f"🔄 Load test: {test_info['performance']['mape']:.2f}% MAPE")
            print("🚀 Model is ready for production use!")
            
        except Exception as e:
            print(f"❌ Load test failed: {e}")
    else:
        print("❌ Model creation failed.")