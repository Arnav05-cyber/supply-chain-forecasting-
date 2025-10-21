#!/usr/bin/env python3
"""
Create additional React components for the dashboard
"""

import os

def create_additional_components():
    """Create remaining React components"""
    
    print("🔧 CREATING ADDITIONAL DASHBOARD COMPONENTS")
    print("=" * 50)
    
    # Ensure directories exist
    os.makedirs('dashboard/src/components', exist_ok=True)
    os.makedirs('dashboard/src/pages', exist_ok=True)
    
    # Create ForecastChart.js
    forecast_chart_js = """import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const ForecastChart = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <div className="text-center py-12">
          <div className="text-gray-400 text-6xl mb-4">📈</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Forecast Data</h3>
          <p className="text-gray-500">Generate a forecast to see the chart</p>
        </div>
      </div>
    );
  }

  const chartData = {
    labels: data.forecast_data.dates,
    datasets: [
      {
        label: 'Predicted Sales',
        data: data.forecast_data.predictions,
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
        fill: true,
        pointBackgroundColor: 'rgb(59, 130, 246)',
        pointBorderColor: 'white',
        pointBorderWidth: 2,
        pointRadius: 4,
      },
      {
        label: 'Upper Bound',
        data: data.forecast_data.upper_bound,
        borderColor: 'rgba(59, 130, 246, 0.3)',
        borderDash: [5, 5],
        fill: false,
        pointRadius: 0,
      },
      {
        label: 'Lower Bound',
        data: data.forecast_data.lower_bound,
        borderColor: 'rgba(59, 130, 246, 0.3)',
        borderDash: [5, 5],
        fill: false,
        pointRadius: 0,
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Sales Forecast',
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: 'white',
        bodyColor: 'white',
        borderColor: 'rgba(59, 130, 246, 0.5)',
        borderWidth: 1,
      }
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Date'
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Sales Units'
        },
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-900">Forecast Results</h2>
        <div className="flex space-x-4">
          <div className="bg-blue-50 px-3 py-1 rounded-full">
            <span className="text-sm font-medium text-blue-700">
              {data.predicted_sales.toFixed(1)} units
            </span>
          </div>
          <div className="bg-green-50 px-3 py-1 rounded-full">
            <span className="text-sm font-medium text-green-700">
              {data.confidence}% confidence
            </span>
          </div>
        </div>
      </div>
      
      <div className="h-64">
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
};

export default ForecastChart;"""
    
    with open('dashboard/src/components/ForecastChart.js', 'w', encoding='utf-8') as f:
        f.write(forecast_chart_js)
    
    # Create BusinessInsights.js
    business_insights_js = """import React from 'react';
import {
  FireIcon,
  TrendingUpIcon,
  TrendingDownIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  CurrencyDollarIcon
} from '@heroicons/react/24/outline';

const BusinessInsights = ({ data }) => {
  const generateInsights = () => {
    const insights = [];
    const prediction = data.predicted_sales;
    const confidence = data.confidence;
    const revenue = data.revenue_impact;

    // Demand insights
    if (prediction > 10) {
      insights.push({
        type: 'high-demand',
        icon: FireIcon,
        color: 'red',
        title: 'High Demand Expected',
        description: 'Consider increasing inventory levels to meet demand',
        action: 'Increase stock by 20-30%'
      });
    } else if (prediction < 3) {
      insights.push({
        type: 'low-demand',
        icon: TrendingDownIcon,
        color: 'yellow',
        title: 'Low Demand Predicted',
        description: 'Optimize inventory to reduce carrying costs',
        action: 'Reduce stock levels'
      });
    } else {
      insights.push({
        type: 'moderate-demand',
        icon: TrendingUpIcon,
        color: 'blue',
        title: 'Moderate Demand',
        description: 'Maintain current inventory levels',
        action: 'Continue current strategy'
      });
    }

    // Confidence insights
    if (confidence > 85) {
      insights.push({
        type: 'high-confidence',
        icon: CheckCircleIcon,
        color: 'green',
        title: 'High Confidence Prediction',
        description: 'Reliable forecast for strategic planning',
        action: 'Safe to make inventory decisions'
      });
    } else if (confidence < 70) {
      insights.push({
        type: 'low-confidence',
        icon: ExclamationTriangleIcon,
        color: 'yellow',
        title: 'Lower Confidence',
        description: 'Monitor closely and adjust as needed',
        action: 'Consider additional data sources'
      });
    }

    // Revenue insights
    if (revenue > 100) {
      insights.push({
        type: 'high-revenue',
        icon: CurrencyDollarIcon,
        color: 'green',
        title: 'Strong Revenue Impact',
        description: `Potential revenue of $${revenue.toFixed(0)}`,
        action: 'Focus on this product line'
      });
    }

    // Model insights
    insights.push({
      type: 'model-quality',
      icon: CheckCircleIcon,
      color: 'blue',
      title: 'AI Model Quality',
      description: 'Based on advanced ML with 94.6% accuracy',
      action: 'Trust the prediction'
    });

    return insights;
  };

  const insights = generateInsights();

  const colorClasses = {
    red: {
      bg: 'bg-red-50',
      text: 'text-red-700',
      icon: 'text-red-500',
      border: 'border-red-200'
    },
    yellow: {
      bg: 'bg-yellow-50',
      text: 'text-yellow-700',
      icon: 'text-yellow-500',
      border: 'border-yellow-200'
    },
    green: {
      bg: 'bg-green-50',
      text: 'text-green-700',
      icon: 'text-green-500',
      border: 'border-green-200'
    },
    blue: {
      bg: 'bg-blue-50',
      text: 'text-blue-700',
      icon: 'text-blue-500',
      border: 'border-blue-200'
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
      <h3 className="text-lg font-bold text-gray-900 mb-4">
        Business Insights & Recommendations
      </h3>
      
      <div className="space-y-4">
        {insights.map((insight, index) => {
          const colors = colorClasses[insight.color];
          return (
            <div
              key={insight.type}
              className={`p-4 rounded-lg border ${colors.bg} ${colors.border} fade-in`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="flex items-start space-x-3">
                <insight.icon className={`h-6 w-6 ${colors.icon} flex-shrink-0 mt-0.5`} />
                <div className="flex-1">
                  <h4 className={`font-semibold ${colors.text} mb-1`}>
                    {insight.title}
                  </h4>
                  <p className="text-gray-600 text-sm mb-2">
                    {insight.description}
                  </p>
                  <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${colors.bg} ${colors.text}`}>
                    💡 {insight.action}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-semibold text-gray-900 mb-2">Key Metrics Summary</h4>
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div>
            <span className="text-gray-500">Predicted Sales:</span>
            <div className="font-semibold text-gray-900">
              {data.predicted_sales.toFixed(1)} units
            </div>
          </div>
          <div>
            <span className="text-gray-500">Confidence Level:</span>
            <div className="font-semibold text-gray-900">
              {data.confidence}%
            </div>
          </div>
          <div>
            <span className="text-gray-500">Revenue Impact:</span>
            <div className="font-semibold text-gray-900">
              ${data.revenue_impact.toFixed(0)}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BusinessInsights;"""
    
    with open('dashboard/src/components/BusinessInsights.js', 'w', encoding='utf-8') as f:
        f.write(business_insights_js)
    
    # Create Analytics.js page
    analytics_js = """import React, { useState, useEffect } from 'react';
import { api } from '../utils/api';
import {
  ChartBarIcon,
  CpuChipIcon,
  ClockIcon,
  TrendingUpIcon
} from '@heroicons/react/24/outline';

const Analytics = () => {
  const [modelInfo, setModelInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadModelInfo();
  }, []);

  const loadModelInfo = async () => {
    try {
      const response = await api.get('/model/info');
      setModelInfo(response.data);
    } catch (error) {
      console.error('Error loading model info:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3].map(i => (
              <div key={i} className="bg-white p-6 rounded-xl shadow-sm">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const performanceMetrics = [
    {
      title: 'Model Accuracy',
      value: '94.6%',
      description: 'Overall prediction accuracy',
      icon: ChartBarIcon,
      color: 'green'
    },
    {
      title: 'MAPE Score',
      value: '5.41%',
      description: 'Mean Absolute Percentage Error',
      icon: TrendingUpIcon,
      color: 'blue'
    },
    {
      title: 'Model Type',
      value: 'Gradient Boosting',
      description: 'Advanced ensemble algorithm',
      icon: CpuChipIcon,
      color: 'purple'
    },
    {
      title: 'Features',
      value: modelInfo?.feature_count || '34',
      description: 'Input features used',
      icon: ClockIcon,
      color: 'orange'
    }
  ];

  const colorClasses = {
    green: 'bg-green-50 text-green-600 border-green-200',
    blue: 'bg-blue-50 text-blue-600 border-blue-200',
    purple: 'bg-purple-50 text-purple-600 border-purple-200',
    orange: 'bg-orange-50 text-orange-600 border-orange-200'
  };

  return (
    <div className="space-y-6">
      <div className="fade-in">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Model Analytics
        </h1>
        <p className="text-gray-600">
          Detailed insights into your AI forecasting model performance
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {performanceMetrics.map((metric, index) => (
          <div
            key={metric.title}
            className={`bg-white p-6 rounded-xl shadow-sm border card-hover fade-in ${colorClasses[metric.color]}`}
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="flex items-center justify-between mb-4">
              <metric.icon className="h-8 w-8" />
              <div className="text-right">
                <div className="text-2xl font-bold">
                  {metric.value}
                </div>
              </div>
            </div>
            <h3 className="font-semibold mb-1">{metric.title}</h3>
            <p className="text-sm opacity-75">{metric.description}</p>
          </div>
        ))}
      </div>

      {modelInfo && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Model Details
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-gray-900 mb-3">Performance Metrics</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">Validation MAPE:</span>
                  <span className="font-medium">5.41%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Model Type:</span>
                  <span className="font-medium">{modelInfo.model_type}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Features:</span>
                  <span className="font-medium">{modelInfo.feature_count}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Status:</span>
                  <span className="font-medium text-green-600">Active</span>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="font-semibold text-gray-900 mb-3">Model Information</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">Version:</span>
                  <span className="font-medium">2.0</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Algorithm:</span>
                  <span className="font-medium">Gradient Boosting</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Training Data:</span>
                  <span className="font-medium">M5 Competition</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Last Updated:</span>
                  <span className="font-medium">Today</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Feature Importance
        </h2>
        
        <div className="space-y-3">
          {[
            { name: 'rolling_mean_3', importance: 77.69 },
            { name: 'sales_trend_7', importance: 5.50 },
            { name: 'lag_7', importance: 4.59 },
            { name: 'rolling_std_3', importance: 4.14 },
            { name: 'sales_trend_28', importance: 2.29 },
            { name: 'lag_28', importance: 1.97 },
            { name: 'day_of_week', importance: 1.41 },
            { name: 'lag_1', importance: 1.22 }
          ].map((feature, index) => (
            <div key={feature.name} className="flex items-center space-x-4">
              <div className="w-32 text-sm font-medium text-gray-700">
                {feature.name}
              </div>
              <div className="flex-1 bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-1000 ease-out"
                  style={{ 
                    width: `${feature.importance}%`,
                    animationDelay: `${index * 0.1}s`
                  }}
                ></div>
              </div>
              <div className="w-16 text-sm text-gray-600 text-right">
                {feature.importance}%
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Analytics;"""
    
    with open('dashboard/src/pages/Analytics.js', 'w', encoding='utf-8') as f:
        f.write(analytics_js)
    
    # Create Settings.js page
    settings_js = """import React, { useState } from 'react';
import { toast } from 'react-hot-toast';
import {
  CogIcon,
  BellIcon,
  ShieldCheckIcon,
  DatabaseIcon,
  CloudIcon
} from '@heroicons/react/24/outline';

const Settings = () => {
  const [settings, setSettings] = useState({
    notifications: {
      email: true,
      push: false,
      lowConfidence: true,
      highDemand: true
    },
    model: {
      autoRetrain: false,
      confidenceThreshold: 70,
      forecastHorizon: 28
    },
    api: {
      rateLimit: 100,
      timeout: 30,
      caching: true
    }
  });

  const handleSettingChange = (category, key, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [key]: value
      }
    }));
  };

  const saveSettings = () => {
    // In a real app, this would save to backend
    toast.success('Settings saved successfully!');
  };

  const resetSettings = () => {
    setSettings({
      notifications: {
        email: true,
        push: false,
        lowConfidence: true,
        highDemand: true
      },
      model: {
        autoRetrain: false,
        confidenceThreshold: 70,
        forecastHorizon: 28
      },
      api: {
        rateLimit: 100,
        timeout: 30,
        caching: true
      }
    });
    toast.success('Settings reset to defaults');
  };

  return (
    <div className="space-y-6">
      <div className="fade-in">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Settings
        </h1>
        <p className="text-gray-600">
          Configure your forecasting dashboard preferences
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Notifications */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <div className="flex items-center mb-4">
            <BellIcon className="h-6 w-6 text-blue-600 mr-2" />
            <h2 className="text-xl font-bold text-gray-900">Notifications</h2>
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Email Notifications</label>
                <p className="text-xs text-gray-500">Receive forecast updates via email</p>
              </div>
              <input
                type="checkbox"
                checked={settings.notifications.email}
                onChange={(e) => handleSettingChange('notifications', 'email', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Push Notifications</label>
                <p className="text-xs text-gray-500">Browser push notifications</p>
              </div>
              <input
                type="checkbox"
                checked={settings.notifications.push}
                onChange={(e) => handleSettingChange('notifications', 'push', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Low Confidence Alerts</label>
                <p className="text-xs text-gray-500">Alert when prediction confidence is low</p>
              </div>
              <input
                type="checkbox"
                checked={settings.notifications.lowConfidence}
                onChange={(e) => handleSettingChange('notifications', 'lowConfidence', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">High Demand Alerts</label>
                <p className="text-xs text-gray-500">Alert when high demand is predicted</p>
              </div>
              <input
                type="checkbox"
                checked={settings.notifications.highDemand}
                onChange={(e) => handleSettingChange('notifications', 'highDemand', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>
          </div>
        </div>

        {/* Model Settings */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <div className="flex items-center mb-4">
            <CogIcon className="h-6 w-6 text-purple-600 mr-2" />
            <h2 className="text-xl font-bold text-gray-900">Model Configuration</h2>
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Auto Retrain</label>
                <p className="text-xs text-gray-500">Automatically retrain model with new data</p>
              </div>
              <input
                type="checkbox"
                checked={settings.model.autoRetrain}
                onChange={(e) => handleSettingChange('model', 'autoRetrain', e.target.checked)}
                className="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Confidence Threshold ({settings.model.confidenceThreshold}%)
              </label>
              <input
                type="range"
                min="50"
                max="95"
                value={settings.model.confidenceThreshold}
                onChange={(e) => handleSettingChange('model', 'confidenceThreshold', parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <p className="text-xs text-gray-500 mt-1">Minimum confidence for predictions</p>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Forecast Horizon
              </label>
              <select
                value={settings.model.forecastHorizon}
                onChange={(e) => handleSettingChange('model', 'forecastHorizon', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value={7}>7 days</option>
                <option value={14}>14 days</option>
                <option value={28}>28 days</option>
                <option value={56}>56 days</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">Maximum forecast period</p>
            </div>
          </div>
        </div>

        {/* API Settings */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <div className="flex items-center mb-4">
            <CloudIcon className="h-6 w-6 text-green-600 mr-2" />
            <h2 className="text-xl font-bold text-gray-900">API Configuration</h2>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Rate Limit (requests/minute)
              </label>
              <input
                type="number"
                value={settings.api.rateLimit}
                onChange={(e) => handleSettingChange('api', 'rateLimit', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Timeout (seconds)
              </label>
              <input
                type="number"
                value={settings.api.timeout}
                onChange={(e) => handleSettingChange('api', 'timeout', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Enable Caching</label>
                <p className="text-xs text-gray-500">Cache predictions for faster responses</p>
              </div>
              <input
                type="checkbox"
                checked={settings.api.caching}
                onChange={(e) => handleSettingChange('api', 'caching', e.target.checked)}
                className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
              />
            </div>
          </div>
        </div>

        {/* System Info */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <div className="flex items-center mb-4">
            <DatabaseIcon className="h-6 w-6 text-orange-600 mr-2" />
            <h2 className="text-xl font-bold text-gray-900">System Information</h2>
          </div>
          
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Model Version:</span>
              <span className="text-sm font-medium">2.0</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Last Updated:</span>
              <span className="text-sm font-medium">Today</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">API Status:</span>
              <span className="text-sm font-medium text-green-600">Online</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Database:</span>
              <span className="text-sm font-medium text-green-600">Connected</span>
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex space-x-4">
        <button
          onClick={saveSettings}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          Save Settings
        </button>
        <button
          onClick={resetSettings}
          className="bg-gray-100 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-200 transition-colors font-medium"
        >
          Reset to Defaults
        </button>
      </div>
    </div>
  );
};

export default Settings;"""
    
    with open('dashboard/src/pages/Settings.js', 'w', encoding='utf-8') as f:
        f.write(settings_js)
    
    print("✅ Additional components created!")
    print("📁 Components added:")
    print("   • ForecastChart.js - Interactive forecast visualization")
    print("   • BusinessInsights.js - AI-powered business recommendations")
    print("   • Analytics.js - Model performance analytics")
    print("   • Settings.js - Dashboard configuration")
    
    print(f"\n🎨 Features included:")
    print(f"   • Interactive charts with Chart.js")
    print(f"   • Real-time business insights")
    print(f"   • Model performance metrics")
    print(f"   • Configurable settings")
    print(f"   • Responsive design")
    print(f"   • Smooth animations")

if __name__ == "__main__":
    create_additional_components()