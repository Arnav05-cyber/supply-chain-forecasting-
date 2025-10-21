import React, { useState } from 'react';
import { SparklesIcon } from '@heroicons/react/24/outline';

const PredictionForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    item_id: '',
    store_id: '',
    dept_id: '',
    cat_id: '',
    state_id: '',
    sell_price: '',
    days_ahead: 7
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      ...formData,
      sell_price: parseFloat(formData.sell_price),
      days_ahead: parseInt(formData.days_ahead)
    });
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const loadSampleData = () => {
    setFormData({
      item_id: 'FOODS_3_001',
      store_id: 'CA_1',
      dept_id: 'FOODS_3',
      cat_id: 'FOODS',
      state_id: 'CA',
      sell_price: '2.99',
      days_ahead: 7
    });
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-900">
          Generate Forecast
        </h2>
        <SparklesIcon className="h-6 w-6 text-blue-600" />
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Item ID
          </label>
          <input
            type="text"
            name="item_id"
            value={formData.item_id}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="FOODS_3_001"
            required
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Store
            </label>
            <select
              name="store_id"
              value={formData.store_id}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            >
              <option value="">Select Store</option>
              <option value="CA_1">CA_1</option>
              <option value="CA_2">CA_2</option>
              <option value="TX_1">TX_1</option>
              <option value="WI_1">WI_1</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Department
            </label>
            <select
              name="dept_id"
              value={formData.dept_id}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            >
              <option value="">Select Dept</option>
              <option value="FOODS_1">FOODS_1</option>
              <option value="FOODS_3">FOODS_3</option>
              <option value="HOBBIES_1">HOBBIES_1</option>
              <option value="HOUSEHOLD_1">HOUSEHOLD_1</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Category
            </label>
            <select
              name="cat_id"
              value={formData.cat_id}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            >
              <option value="">Select Category</option>
              <option value="FOODS">FOODS</option>
              <option value="HOBBIES">HOBBIES</option>
              <option value="HOUSEHOLD">HOUSEHOLD</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              State
            </label>
            <select
              name="state_id"
              value={formData.state_id}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            >
              <option value="">Select State</option>
              <option value="CA">California</option>
              <option value="TX">Texas</option>
              <option value="WI">Wisconsin</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Price ($)
            </label>
            <input
              type="number"
              name="sell_price"
              value={formData.sell_price}
              onChange={handleChange}
              step="0.01"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="2.99"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Forecast Days
            </label>
            <select
              name="days_ahead"
              value={formData.days_ahead}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value={7}>7 days</option>
              <option value={14}>14 days</option>
              <option value={28}>28 days</option>
            </select>
          </div>
        </div>

        <div className="space-y-3 pt-4">
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Generating...
              </div>
            ) : (
              'Generate Forecast'
            )}
          </button>

          <button
            type="button"
            onClick={loadSampleData}
            className="w-full bg-gray-100 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Load Sample Data
          </button>
        </div>
      </form>
    </div>
  );
};

export default PredictionForm;