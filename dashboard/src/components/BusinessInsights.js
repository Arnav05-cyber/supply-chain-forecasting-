import React from 'react';
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

export default BusinessInsights;