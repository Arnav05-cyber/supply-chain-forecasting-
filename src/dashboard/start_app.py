#!/usr/bin/env python3
"""
Simple app starter to ensure the dashboard runs properly
"""

import sys
import os
import subprocess

def check_requirements():
    """Check if required packages are installed"""
    required_packages = ['fastapi', 'uvicorn', 'joblib', 'pandas', 'numpy', 'scikit-learn']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} - MISSING")
    
    if missing:
        print(f"\n📦 Installing missing packages: {', '.join(missing)}")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing)
    
    return len(missing) == 0

def check_model_files():
    """Check if model files exist"""
    required_files = [
        'improved_forecasting_model.joblib',
        'improved_model_encoders.joblib', 
        'improved_model_info.json'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            missing_files.append(file)
            print(f"❌ {file} - Missing")
    
    return len(missing_files) == 0

def start_dashboard():
    """Start the dashboard application"""
    print("\n🚀 STARTING AI FORECASTING DASHBOARD")
    print("=" * 50)
    
    # Check requirements
    print("📦 Checking Python packages...")
    if not check_requirements():
        print("❌ Some packages are missing. Please install them first.")
        return False
    
    # Check model files
    print("\n🤖 Checking model files...")
    if not check_model_files():
        print("❌ Model files are missing. Please run create_improved_model.py first.")
        return False
    
    print("\n🎯 All requirements satisfied!")
    print("🚀 Starting dashboard server...")
    print("📊 Dashboard will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/api/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("\n⌨️ Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the server
    try:
        import uvicorn
        from smart_dashboard_backend import app
        
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        
    except ImportError:
        print("❌ uvicorn not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'uvicorn'])
        
        # Try again
        import uvicorn
        from smart_dashboard_backend import app
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = start_dashboard()
    if not success:
        print("\n❌ Dashboard failed to start. Please check the error messages above.")
        sys.exit(1)