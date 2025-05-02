import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';


const WeekNavigation = ({
  currentWeek,
  term,
  onPrevWeek,
  onNextWeek,
  onCurrentWeek
}) => {
  return (
    <div className="flex items-center gap-3">
      <button
        onClick={onPrevWeek}
        className="p-1 rounded-full hover:bg-gray-100 transition-colors"
      >
        <ChevronLeft size={20} />
      </button>
      
      <div className="flex gap-2">
        <select 
          className="py-1 px-3 border border-gray-300 rounded-md text-sm bg-white"
          value={term}
        >
          <option>2023-2023 / SUMMER</option>
          <option>2023-2023 / FALL</option>
          <option>2023-2023 / SPRING</option>
        </select>
        
        <select 
          className="py-1 px-3 border border-gray-300 rounded-md text-sm bg-white"
          value={currentWeek}
        >
          <option>Week 5/08/07-08/13</option>
          <option>Week 6/08/14-08/20</option>
          <option>Week 7/08/21-08/27</option>
        </select>
      </div>
      
      <button
        onClick={onNextWeek}
        className="p-1 rounded-full hover:bg-gray-100 transition-colors"
      >
        <ChevronRight size={20} />
      </button>
      
      <button
        onClick={onCurrentWeek}
        className="py-1 px-3 text-sm border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
      >
        Current Week
      </button>
    </div>
  );
};

export default WeekNavigation;