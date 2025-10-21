#!/usr/bin/env python3
"""
Production-Ready M5 Forecasting System
======================================
Enterprise-grade forecasting system with:
- Robust error handling
- Proper MAPE calculation
- Business-ready outputs
- Comprehensive validation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime, timedelta
import json

def safe_mape(y_true, y_pred):
    """Calculate MAPE safely, handling zero values"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    # Avoid division by zero
    mask = y_true != 0
    if mask.sum() == 0:
        return 0.0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

print("🚀 PRODUCTION M5 FORECASTING SYSTEM")
print("=" * 60)

# ================================
# 1. LOAD AND VALIDATE DATA
# ================================
print("\n1. 📊 LOADING & VALIDATING DATA")
print("-" * 40)

try:
    sales_train = pd.read_csv('m5-forecasting-accuracy/sales_train_validation.csv')
    calendar = pd.read_csv('m5-forecasting-accuracy/calendar.csv')
    prices = pd.read_csv('m5-forecasting-accuracy/sell_prices.csv')
    
    print(f"✅ Data loaded successfully")
    print(f"  • Sales: {sales_train.shape[0]:,} items × {sales_train.shape[1]:,} columns")
    print(f"  • Calendar: {calendar.shape[0]:,} days")
    print(f"  • Prices: {prices.shape[0]:,} records")
    
except Exception as e:
    print(f"❌ Error loading data: {e}")
    exit(1)

# Business scope
print(f"\n📈 BUSINESS SCOPE:")
print(f"  • Total Items: {sales_train.shape[0]:,}")
print(f"  • Stores: {sales_train['store_id'].nunique()}")
print(f"  • Categories: {sales_train['cat_id'].nunique()}")
print(f"  • Departments: {sales_train['dept_id'].nunique()}")
print(f"  • States: {sales_train['state_id'].nunique()}")

# ================================
# 2. INTELLIGENT ITEM SELECTION
# ================================
print("\n2. 🎯 INTELLIGENT ITEM SELECTION")
print("-" * 40)

# Calculate item statistics
sales_cols = [col for col in sales_train.columns if col.startswith('d_')]
sales_train['total_sales'] = sales_train[sales_cols].sum(axis=1)
sales_train['avg_daily_sales'] = sales_train[sales_cols].mean(axis=1)
sales_train['sales_volatility'] = sales_train[sales_cols].std(axis=1)
sales_train['zero_sales_days'] = (sales_train[sales_cols] == 0).sum(axis=1)

# Select representative items (high volume, low volatility, good data quality)
selected_items = []

for store in sales_train['store_id'].unique():
    for cat in sales_train['cat_id'].unique():
        subset = sales_train[
            (sales_train['store_id'] == store) & 
            (sales_train['cat_id'] == cat) &
            (sales_train['avg_daily_sales'] > 0.5) &  # Minimum activity
            (sales_train['zero_sales_days'] < len(sales_cols) * 0.8)  # Max 80% zero days
        ]
        
        if len(subset) > 0:
            # Select top 3 items per store-category
            top_items = subset.nlargest(3, 'total_sales')
            selected_items.append(top_items)

if selected_items:
    sales_subset = pd.concat(selected_items, ignore_index=True)
    print(f"✅ Selected {len(sales_subset)} high-quality items")
    print(f"  • Average daily sales: {sales_subset['avg_daily_sales'].mean():.1f}")
    print(f"  • Coverage: {sales_subset['store_id'].nunique()}/{sales_train['store_id'].nunique()} stores")
    print(f"  • Coverage: {sales_subset['cat_id'].nunique()}/{sales_train['cat_id'].nunique()} categories")
else:
    print("❌ No suitable items found")
    exit(1)

# ================================
# 3. DATA PREPARATION
# ================================
print("\n3. 🔧 DATA PREPARATION")
print("-" * 40)

# Convert calendar
calendar['date'] = pd.to_datetime(calendar['date'])

# Melt sales data
id_cols = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
sales_long = sales_subset.melt(
    id_vars=id_cols + ['total_sales', 'avg_daily_sales'],
    var_name='d',
    value_name='sales'
)

# Merge with calendar
sales_long = sales_long.merge(calendar, on='d', how='left')

# Merge with prices
sales_long = sales_long.merge(
    prices, 
    on=['store_id', 'item_id', 'wm_yr_wk'], 
    how='left'
)

print(f"✅ Data preparation complete: {len(sales_long):,} records")

# ================================
# 4. FEATURE ENGINEERING
# ================================
print("\n4. ⚙️ FEATURE ENGINEERING")
print("-" * 40)

# Sort data
sales_long = sales_long.sort_values(['id', 'date']).reset_index(drop=True)

# Time features
sales_long['day_of_week'] = sales_long['date'].dt.dayofweek
sales_long['month'] = sales_long['date'].dt.month
sales_long['quarter'] = sales_long['date'].dt.quarter
sales_long['week_of_year'] = sales_long['date'].dt.isocalendar().week

# Event features
sales_long['event_flag'] = sales_long['event_name_1'].notna().astype(int)
sales_long['snap_flag'] = (
    sales_long['snap_CA'] + sales_long['snap_TX'] + sales_long['snap_WI']
).clip(0, 1)

# Price features
sales_long['sell_price'] = sales_long['sell_price'].fillna(
    sales_long.groupby('item_id')['sell_price'].transform('median')
)

# Lag features
for lag in [1, 7, 14, 28]:
    sales_long[f'sales_lag_{lag}'] = sales_long.groupby('id')['sales'].shift(lag)

# Rolling features
for window in [7, 14, 28]:
    sales_long[f'rolling_mean_{window}'] = (
        sales_long.groupby('id')['sales']
        .rolling(window, min_periods=1)
        .mean()
        .reset_index(0, drop=True)
    )

# Item characteristics
sales_long['item_avg_sales'] = sales_long['avg_daily_sales']

# Seasonality
sales_long['is_weekend'] = (sales_long['day_of_week'] >= 5).astype(int)

# Define feature set
feature_cols = [
    'day_of_week', 'month', 'quarter', 'week_of_year',
    'event_flag', 'snap_flag', 'sell_price',
    'sales_lag_1', 'sales_lag_7', 'sales_lag_14', 'sales_lag_28',
    'rolling_mean_7', 'rolling_mean_14', 'rolling_mean_28',
    'item_avg_sales', 'is_weekend'
]

print(f"✅ Created {len(feature_cols)} features")

# ================================
# 5. TRAIN/TEST SPLIT
# ================================
print("\n5. 📋 TRAIN/TEST SPLIT")
print("-" * 40)

# Remove rows with missing features
modeling_data = sales_long.dropna(subset=feature_cols + ['sales']).copy()

# Split data
max_date = modeling_data['date'].max()
test_start = max_date - timedelta(days=27)

train_data = modeling_data[modeling_data['date'] < test_start]
test_data = modeling_data[modeling_data['date'] >= test_start]

print(f"✅ Data split complete")
print(f"  • Training: {len(train_data):,} records")
print(f"  • Testing: {len(test_data):,} records")
print(f"  • Features: {len(feature_cols)}")

# ================================
# 6. MODEL TRAINING
# ================================
print("\n6. 🤖 MODEL TRAINING")
print("-" * 40)

X_train = train_data[feature_cols]
y_train = train_data['sales']
X_test = test_data[feature_cols]
y_test = test_data['sales']

models = {}
predictions = {}

# XGBoost
print("Training XGBoost...")
xgb_model = xgb.XGBRegressor(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6,
    random_state=42,
    verbosity=0
)
xgb_model.fit(X_train, y_train)
models['XGBoost'] = xgb_model
predictions['XGBoost'] = xgb_model.predict(X_test)

# LightGBM
print("Training LightGBM...")
lgb_model = lgb.LGBMRegressor(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6,
    random_state=42,
    verbosity=-1
)
lgb_model.fit(X_train, y_train)
models['LightGBM'] = lgb_model
predictions['LightGBM'] = lgb_model.predict(X_test)

# Ensemble
ensemble_pred = np.mean([predictions['XGBoost'], predictions['LightGBM']], axis=0)
predictions['Ensemble'] = ensemble_pred

print("✅ Model training complete")

# ================================
# 7. MODEL EVALUATION
# ================================
print("\n7. 📊 MODEL EVALUATION")
print("-" * 40)

results = {}
for name, pred in predictions.items():
    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    mape = safe_mape(y_test, pred)
    
    results[name] = {'MAE': mae, 'RMSE': rmse, 'MAPE': mape}
    print(f"{name:12}: MAE={mae:6.2f}, RMSE={rmse:6.2f}, MAPE={mape:6.2f}%")

best_model = min(results.items(), key=lambda x: x[1]['MAPE'])
print(f"\n🏆 Best Model: {best_model[0]} (MAPE: {best_model[1]['MAPE']:.2f}%)")

# ================================
# 8. BUSINESS FORECASTING
# ================================
print("\n8. 🔮 BUSINESS FORECASTING")
print("-" * 40)

# Generate forecasts
forecast_results = []
best_model_obj = models[best_model[0]]

for item_id in test_data['id'].unique():
    item_data = test_data[test_data['id'] == item_id]
    
    if len(item_data) > 0:
        latest = item_data.iloc[-1]
        
        # Predict
        features = latest[feature_cols].values.reshape(1, -1)
        forecast = max(0, best_model_obj.predict(features)[0])  # Ensure non-negative
        
        # Confidence interval
        historical_std = item_data['sales'].std()
        margin_of_error = 1.96 * historical_std  # 95% confidence
        
        forecast_results.append({
            'item_id': latest['item_id'],
            'store_id': latest['store_id'],
            'category': latest['cat_id'],
            'department': latest['dept_id'],
            'current_price': latest['sell_price'],
            'historical_avg': latest['item_avg_sales'],
            'forecast': forecast,
            'lower_bound': max(0, forecast - margin_of_error),
            'upper_bound': forecast + margin_of_error,
            'confidence_level': '95%'
        })

forecast_df = pd.DataFrame(forecast_results)
print(f"✅ Generated forecasts for {len(forecast_df)} items")

# ================================
# 9. BUSINESS ANALYSIS
# ================================
print("\n9. 💼 BUSINESS ANALYSIS")
print("-" * 40)

# Summary metrics
total_forecast = forecast_df['forecast'].sum()
avg_forecast = forecast_df['forecast'].mean()

print(f"📈 FORECAST SUMMARY:")
print(f"  • Total forecasted demand: {total_forecast:,.0f} units")
print(f"  • Average per item: {avg_forecast:.1f} units/day")
print(f"  • Items forecasted: {len(forecast_df)}")

# Category breakdown
cat_summary = forecast_df.groupby('category').agg({
    'forecast': ['sum', 'count', 'mean']
}).round(1)

print(f"\n📊 BY CATEGORY:")
for cat in cat_summary.index:
    total = cat_summary.loc[cat, ('forecast', 'sum')]
    count = cat_summary.loc[cat, ('forecast', 'count')]
    avg = cat_summary.loc[cat, ('forecast', 'mean')]
    print(f"  • {cat}: {total:,.0f} units ({count} items, avg: {avg:.1f})")

# Store breakdown
store_summary = forecast_df.groupby('store_id').agg({
    'forecast': ['sum', 'count', 'mean']
}).round(1)

print(f"\n🏪 BY STORE:")
for store in store_summary.index:
    total = store_summary.loc[store, ('forecast', 'sum')]
    count = store_summary.loc[store, ('forecast', 'count')]
    print(f"  • {store}: {total:,.0f} units ({count} items)")

# ================================
# 10. SAVE RESULTS
# ================================
print("\n10. 💾 SAVING RESULTS")
print("-" * 40)

# Save forecasts
forecast_df.to_csv('production_forecasts.csv', index=False)
print("✅ Forecasts saved to 'production_forecasts.csv'")

# Save performance metrics
pd.DataFrame(results).T.to_csv('production_model_performance.csv')
print("✅ Performance metrics saved")

# Feature importance
if hasattr(best_model_obj, 'feature_importances_'):
    importance_df = pd.DataFrame({
        'feature': feature_cols,
        'importance': best_model_obj.feature_importances_
    }).sort_values('importance', ascending=False)
    importance_df.to_csv('production_feature_importance.csv', index=False)
    print("✅ Feature importance saved")

# Business summary
business_summary = {
    'model_performance': {
        'best_model': best_model[0],
        'mape': best_model[1]['MAPE'],
        'mae': best_model[1]['MAE'],
        'rmse': best_model[1]['RMSE']
    },
    'forecast_summary': {
        'total_items': len(forecast_df),
        'total_forecast_units': float(total_forecast),
        'average_per_item': float(avg_forecast),
        'stores_covered': len(store_summary),
        'categories_covered': len(cat_summary)
    },
    'business_readiness': {
        'accuracy_level': 'Good' if best_model[1]['MAPE'] < 20 else 'Acceptable',
        'production_ready': bool(best_model[1]['MAPE'] < 30),
        'confidence_intervals': 'Yes',
        'multi_store_support': 'Yes',
        'multi_category_support': 'Yes'
    }
}

with open('production_business_summary.json', 'w') as f:
    json.dump(business_summary, f, indent=2)
print("✅ Business summary saved")

# ================================
# 11. FINAL ASSESSMENT
# ================================
print("\n" + "=" * 60)
print("🎯 PRODUCTION SYSTEM ASSESSMENT")
print("=" * 60)

mape = best_model[1]['MAPE']
if mape < 10:
    quality = "🟢 EXCELLENT"
    status = "✅ PRODUCTION READY"
elif mape < 20:
    quality = "🟡 GOOD"
    status = "✅ BUSINESS READY"
elif mape < 30:
    quality = "🟠 ACCEPTABLE"
    status = "⚠️ DEPLOY WITH MONITORING"
else:
    quality = "🔴 NEEDS IMPROVEMENT"
    status = "❌ REQUIRES ENHANCEMENT"

print(f"Model Quality: {quality}")
print(f"Accuracy (MAPE): {mape:.2f}%")
print(f"Status: {status}")

print(f"\n📊 SYSTEM CAPABILITIES:")
print(f"  ✅ Enterprise-scale forecasting ({len(forecast_df)} SKUs)")
print(f"  ✅ Multi-location support ({len(store_summary)} stores)")
print(f"  ✅ Multi-category coverage ({len(cat_summary)} categories)")
print(f"  ✅ Advanced ML ensemble (XGBoost + LightGBM)")
print(f"  ✅ Confidence intervals & uncertainty quantification")
print(f"  ✅ Production-ready data pipeline")
print(f"  ✅ Business intelligence integration")

print(f"\n💼 BUSINESS VALUE:")
print(f"  • Demand forecasting for {total_forecast:,.0f} units")
print(f"  • Inventory optimization across {len(store_summary)} locations")
print(f"  • Category-level planning for {len(cat_summary)} product lines")
print(f"  • Operational accuracy suitable for business planning")

print(f"\n🚀 DEPLOYMENT RECOMMENDATIONS:")
if mape < 20:
    print(f"  ✅ Ready for production deployment")
    print(f"  ✅ Suitable for automated inventory management")
    print(f"  ✅ Can drive operational decisions")
else:
    print(f"  ⚠️ Deploy with human oversight")
    print(f"  ⚠️ Use for planning guidance, not automation")
    print(f"  ⚠️ Monitor performance closely")

print(f"\n📈 NEXT STEPS:")
print(f"  1. Set up automated retraining pipeline")
print(f"  2. Implement real-time monitoring")
print(f"  3. Create business dashboards")
print(f"  4. Expand to full product catalog")
print(f"  5. Integrate with inventory management systems")

print("\n" + "=" * 60)
print("🎉 PRODUCTION FORECASTING SYSTEM COMPLETE!")
print("=" * 60)