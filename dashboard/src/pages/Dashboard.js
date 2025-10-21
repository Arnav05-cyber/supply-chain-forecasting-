import React, { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';
import StatsCards from '../components/StatsCards';
import PredictionForm from '../components/PredictionForm';
import ForecastChart from '../components/ForecastChart';
import BusinessInsights from '../components/BusinessInsights';
import { api } from '../utils/api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    total_predictions: 0,
    daily_predictions: 0,
    model_accuracy: 94.6
  });
  const [forecastData, setForecastData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await api.get('/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handlePrediction = async (formData) => {
    setLoading(true);
    try {
      const response = await api.post('/predict', formData);
      setForecastData(response.data);
      await loadStats(); // Refresh stats
      toast.success('Forecast generated successfully!');
    } catch (error) {
      toast.error('Error generating forecast: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="fade-in">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Forecasting Dashboard
        </h1>
        <p className="text-gray-600">
          Generate AI-powered sales forecasts for your business
        </p>
      </div>

      <StatsCards stats={stats} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <PredictionForm onSubmit={handlePrediction} loading={loading} />
        </div>
        
        <div className="lg:col-span-2 space-y-6">
          <ForecastChart data={forecastData} loading={loading} />
          {forecastData && <BusinessInsights data={forecastData} />}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;