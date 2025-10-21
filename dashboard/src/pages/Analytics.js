import React, { useState, useEffect } from 'react';
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

export default Analytics;