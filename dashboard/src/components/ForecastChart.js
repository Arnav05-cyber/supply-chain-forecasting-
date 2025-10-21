import React from 'react';
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

export default ForecastChart;