import React from 'react';



const TabNavigation = ({ activeTab, setActiveTab }) => {
  return (
    <div className="bg-white rounded-lg overflow-hidden mb-6 shadow-sm">
      <div className="flex text-center">
        <button
          className={`flex-1 py-4 px-4 text-center transition-colors duration-200 ${
            activeTab === 'student' 
              ? 'bg-blue-50 text-blue-700 font-medium' 
              : 'text-gray-600 hover:bg-gray-50'
          }`}
          onClick={() => setActiveTab('student')}
        >
          Student-wise
        </button>
        <button
          className={`flex-1 py-4 px-4 text-center transition-colors duration-200 ${
            activeTab === 'class' 
              ? 'bg-blue-50 text-blue-700 font-medium' 
              : 'text-gray-600 hover:bg-gray-50'
          }`}
          onClick={() => setActiveTab('class')}
        >
          Class-wise
        </button>
        <button
          className={`flex-1 py-4 px-4 text-center transition-colors duration-200 ${
            activeTab === 'report' 
              ? 'bg-blue-50 text-blue-700 font-medium' 
              : 'text-gray-600 hover:bg-gray-50'
          }`}
          onClick={() => setActiveTab('report')}
        >
          Detailed Report
        </button>
      </div>
    </div>
  );
};

export default TabNavigation;