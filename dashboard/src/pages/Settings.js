import React, { useState } from 'react';
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

export default Settings;