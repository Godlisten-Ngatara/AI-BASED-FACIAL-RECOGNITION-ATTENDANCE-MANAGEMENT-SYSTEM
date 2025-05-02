import React from 'react';
import { RefreshCw, Download, Settings, FileSpreadsheet } from 'lucide-react';



const ActionButtons = ({ 
  onExport, 
  onRefresh,
  showSettings = false
}) => {
  return (
    <div className="flex gap-2">
      {onExport && (
        <button 
          onClick={onExport}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
        >
          <Download size={16} />
          <span>Export</span>
        </button>
      )}
      
      {onRefresh && (
        <button 
          onClick={onRefresh}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
        >
          <RefreshCw size={16} />
          <span>Refresh</span>
        </button>
      )}

      {showSettings && (
        <button className="p-2 text-gray-500 hover:bg-gray-100 rounded-md transition-colors">
          <Settings size={20} />
        </button>
      )}
    </div>
  );
};

export default ActionButtons;