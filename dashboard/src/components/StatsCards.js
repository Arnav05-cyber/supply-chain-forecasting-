import React from 'react';
import {
  CpuChipIcon,
  ChartBarIcon,
  CubeIcon,
  CurrencyDollarIcon
} from '@heroicons/react/24/outline';

const StatsCards = ({ stats }) => {
  const cards = [
    {
      title: 'Model Accuracy',
      value: `${stats.model_accuracy}%`,
      icon: CpuChipIcon,
      color: 'blue',
      change: '+2.1%'
    },
    {
      title: 'Today's Predictions',
      value: stats.daily_predictions,
      icon: ChartBarIcon,
      color: 'green',
      change: '+12%'
    },
    {
      title: 'Total Forecasts',
      value: stats.total_predictions,
      icon: CubeIcon,
      color: 'purple',
      change: '+5.4%'
    },
    {
      title: 'Est. Savings',
      value: '$125K',
      icon: CurrencyDollarIcon,
      color: 'orange',
      change: '+8.2%'
    }
  ];

  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    purple: 'bg-purple-50 text-purple-600',
    orange: 'bg-orange-50 text-orange-600'
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, index) => (
        <div
          key={card.title}
          className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 card-hover fade-in"
          style={{ animationDelay: `${index * 0.1}s` }}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 mb-1">
                {card.title}
              </p>
              <p className="text-2xl font-bold text-gray-900">
                {card.value}
              </p>
              <p className="text-sm text-green-600 mt-1">
                {card.change} from last month
              </p>
            </div>
            <div className={`p-3 rounded-lg ${colorClasses[card.color]}`}>
              <card.icon className="h-6 w-6" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default StatsCards;