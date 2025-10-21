#!/usr/bin/env python3
"""
Evaluate the improved forecasting model
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import json
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

def safe_mape(y_true, y_pred):
    """Calculate MAPE safely"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mask = y_true != 0
    if mask.sum() == 0:
        return 0.0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

def evaluate_improved_model():
    """Evaluate the improved model"""
    
    print("🚀 EVALUATING IMPROVED FORECASTING MODEL")
    print("=" * 50)
    
    # Load improved model
    print("📂 Loading improved model...")
    model = joblib.load('improved_forecasting_model.joblib')
    encoders = joblib.load('improved_model_encoders.joblib')
    
    with open('improved_model_info.json', 'r') as f:
        model_info = json.load(f)
    
    print(f"✅ Model loaded: {model_info['performance']['validation_mape']:.2f}% MAPE")
    print(f"🤖 Algorithm: {model_info['performance']['model_algorithm']}")
    
    # Load test data (same as training for consistency)
    print("📊 Loading test data...")
    try:
        sales_train = pd.read_csv('m5-forecasting-accuracy/sales_train_validation.csv')
        calendar = pd.read_csv('m5-forecasting-accuracy/calendar.csv')
        sell_prices = pd.read_csv('m5-forecasting-accuracy/sell_prices.csv')
        
        # Use same high-volume items
        sales_cols = [f'd_{i}' for i in range(1, 1914)]
        sales_train['total_sales'] = sales_train[sales_cols].sum(axis=1)
        top_items = sales_train.nlargest(200, 'total_sales')
        
        # Prepare test data
        id_cols = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
        melted_data = top_items.melt(
            id_vars=id_cols,
            value_vars=sales_cols,
            var_name='d',
            value_name='sales'
        )
        
        # Add features (same as training)
        melted_data = melted_data.merge(calendar, on='d', how='left')
        melted_data = melted_data.merge(sell_prices, on=['store_id', 'item_id', 'wm_yr_wk'], how='left')
        
        # Feature engineering (abbreviated for evaluation)
        categorical_cols = ['item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
        for col in categorical_cols:
            if col in encoders:
                melted_data[f'{col}_encoded'] = melted_data[col].astype(str).map(
                    lambda x: encoders[col].transform([x])[0] if x in encoders[col].classes_ else 0
                )
            else:
                melted_data[f'{col}_encoded'] = 0
        
        # Date features
        melted_data['date'] = pd.to_datetime(melted_data['date'])
        melted_data['day_of_week'] = melted_data['date'].dt.dayofweek
        melted_data['month'] = melted_data['date'].dt.month
        melted_data['quarter'] = melted_data['date'].dt.quarter
        melted_data['is_weekend'] = (melted_data['day_of_week'] >= 5).astype(int)
        melted_data['day_of_month'] = melted_data['date'].dt.day
        melted_data['week_of_year'] = melted_data['date'].dt.isocalendar().week
        
        # Price features
        melted_data['sell_price'] = melted_data['sell_price'].fillna(melted_data['sell_price'].median())
        
        # Sort for time series features
        melted_data = melted_data.sort_values(['id', 'date'])
        
        # Lag and rolling features
        for lag in [1, 7, 14, 28, 56]:
            melted_data[f'lag_{lag}'] = melted_data.groupby('id')['sales'].shift(lag)
        
        for window in [3, 7, 14, 28]:
            melted_data[f'rolling_mean_{window}'] = melted_data.groupby('id')['sales'].rolling(window, min_periods=1).mean().reset_index(0, drop=True)
            melted_data[f'rolling_std_{window}'] = melted_data.groupby('id')['sales'].rolling(window, min_periods=1).std().reset_index(0, drop=True)
            melted_data[f'rolling_max_{window}'] = melted_data.groupby('id')['sales'].rolling(window, min_periods=1).max().reset_index(0, drop=True)
            melted_data[f'rolling_min_{window}'] = melted_data.groupby('id')['sales'].rolling(window, min_periods=1).min().reset_index(0, drop=True)
        
        # Trend features
        melted_data['sales_trend_7'] = melted_data.groupby('id')['sales'].pct_change(7)
        melted_data['sales_trend_28'] = melted_data.groupby('id')['sales'].pct_change(28)
        
        # Price features
        melted_data['price_change'] = melted_data.groupby('id')['sell_price'].pct_change()
        melted_data['price_vs_mean'] = melted_data['sell_price'] / melted_data.groupby('item_id')['sell_price'].transform('mean')
        
        # Event features
        melted_data['is_event'] = (~melted_data['event_name_1'].isna()).astype(int)
        
        # Clean data
        melted_data = melted_data.replace([np.inf, -np.inf], np.nan)
        melted_data = melted_data.fillna(0)
        
        print("✅ Test data prepared")
        
    except FileNotFoundError:
        print("❌ M5 dataset not found")
        return
    
    # Prepare test sets
    feature_columns = model_info['feature_columns']
    melted_data['d_num'] = melted_data['d'].str.replace('d_', '').astype(int)
    
    # Different test periods
    test_periods = {
        'Recent': melted_data[melted_data['d_num'] > 1800],
        'Mid-term': melted_data[(melted_data['d_num'] > 1600) & (melted_data['d_num'] <= 1800)],
        'Long-term': melted_data[(melted_data['d_num'] > 1400) & (melted_data['d_num'] <= 1600)]
    }
    
    print("\n📊 COMPREHENSIVE EVALUATION RESULTS")
    print("=" * 45)
    
    results = {}
    
    for period_name, test_data in test_periods.items():
        if len(test_data) == 0:
            continue
            
        X_test = test_data[feature_columns].fillna(0)
        y_test = test_data['sales'].fillna(0)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        mape = safe_mape(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results[period_name] = {
            'mape': mape,
            'rmse': rmse,
            'mae': mae,
            'r2': r2,
            'samples': len(X_test)
        }
        
        print(f"\n🎯 {period_name.upper()} PERIOD:")
        print(f"   MAPE: {mape:.2f}%")
        print(f"   RMSE: {rmse:.2f}")
        print(f"   MAE:  {mae:.2f}")
        print(f"   R²:   {r2:.3f}")
        print(f"   Samples: {len(X_test):,}")
    
    # Overall assessment
    avg_mape = np.mean([r['mape'] for r in results.values()])
    
    print(f"\n🏆 OVERALL PERFORMANCE")
    print(f"   Average MAPE: {avg_mape:.2f}%")
    
    # Business impact
    if avg_mape < 5:
        impact = "🏆 EXCELLENT - World-class performance"
    elif avg_mape < 10:
        impact = "✅ VERY GOOD - Production ready"
    elif avg_mape < 20:
        impact = "👍 GOOD - Suitable for business use"
    else:
        impact = "⚠️ NEEDS IMPROVEMENT"
    
    print(f"   Assessment: {impact}")
    
    # Feature importance
    if hasattr(model, 'feature_importances_'):
        print(f"\n🔍 TOP 10 FEATURE IMPORTANCE:")
        importance = model.feature_importances_
        feature_importance = pd.DataFrame({
            'feature': feature_columns,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        for i, (_, row) in enumerate(feature_importance.head(10).iterrows(), 1):
            print(f"   {i:2d}. {row['feature']:<25} {row['importance']:.4f}")
    
    # Save evaluation results
    evaluation_results = {
        'model_name': model_info['model_name'],
        'evaluation_date': pd.Timestamp.now().isoformat(),
        'overall_performance': {
            'average_mape': avg_mape,
            'assessment': impact
        },
        'period_results': results,
        'model_info': model_info
    }
    
    with open('improved_model_evaluation.json', 'w') as f:
        json.dump(evaluation_results, f, indent=2)
    
    print(f"\n💾 Evaluation results saved to 'improved_model_evaluation.json'")
    print(f"\n🎉 EVALUATION COMPLETE!")
    print(f"📊 Final MAPE: {avg_mape:.2f}%")
    print(f"🚀 {impact}")

if __name__ == "__main__":
    evaluate_improved_model()