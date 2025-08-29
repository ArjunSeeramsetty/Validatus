import React from 'react';
import { ChevronRightIcon, HomeIcon } from '@heroicons/react/24/outline';

interface BreadcrumbItem {
  level: string;
  name: string;
  path: string;
}

interface Props {
  breadcrumb: BreadcrumbItem[];
  onNavigate: (targetIndex?: number) => void;
}

export const NavigationBreadcrumb: React.FC<Props> = ({ breadcrumb, onNavigate }) => {
  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center space-x-2 py-3">
          {breadcrumb.map((item, index) => (
            <React.Fragment key={index}>
              {index > 0 && (
                <ChevronRightIcon className="h-5 w-5 text-gray-400" />
              )}
              <button
                onClick={() => onNavigate(index)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  index === breadcrumb.length - 1
                    ? 'text-blue-600 bg-blue-50 cursor-default'
                    : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50 cursor-pointer'
                }`}
              >
                {index === 0 ? (
                  <HomeIcon className="h-4 w-4" />
                ) : (
                  <span className="capitalize">{item.level}</span>
                )}
                <span className="max-w-xs truncate">{item.name}</span>
              </button>
            </React.Fragment>
          ))}
        </div>
      </div>
    </nav>
  );
};
