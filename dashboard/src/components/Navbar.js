import React from 'react';
import { BellIcon, UserCircleIcon } from '@heroicons/react/24/outline';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <h1 className="text-2xl font-bold text-gray-900">
                <span className="text-blue-600">AI</span> Forecasting
              </h1>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-sm text-gray-600">Model Active</span>
            </div>
            
            <div className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium">
              5.41% MAPE
            </div>
            
            <button className="p-2 text-gray-400 hover:text-gray-500">
              <BellIcon className="h-6 w-6" />
            </button>
            
            <button className="p-2 text-gray-400 hover:text-gray-500">
              <UserCircleIcon className="h-8 w-8" />
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;