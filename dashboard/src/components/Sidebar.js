import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  HomeIcon,
  ChartBarIcon,
  CogIcon,
  CpuChipIcon,
  DocumentChartBarIcon
} from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Analytics', href: '/analytics', icon: ChartBarIcon },
  { name: 'Model Info', href: '/model', icon: CpuChipIcon },
  { name: 'Reports', href: '/reports', icon: DocumentChartBarIcon },
  { name: 'Settings', href: '/settings', icon: CogIcon },
];

const Sidebar = () => {
  const location = useLocation();

  return (
    <div className="w-64 bg-white shadow-sm h-screen">
      <div className="p-6">
        <nav className="space-y-2">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
                  isActive
                    ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <item.icon className="mr-3 h-5 w-5" />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;