import React, { useState } from 'react';
import { Search, School, Users, Settings, ChevronLeft, ChevronRight } from 'lucide-react';
import WeekNavigation from '../components/WeekNavigation';
import ActionButtons from '../components/ActionButton';

const ClassWiseView = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [currentWeek, setCurrentWeek] = useState('Week 5/08/07-08/13');
  const [currentTerm, setCurrentTerm] = useState('2023-2023 / SUMMER');
  const [selectedClass, setSelectedClass] = useState('class1');

  // Mock data
  const classList = [
    { id: 'all', name: 'all' },
    { id: 'class1', name: 'class1' },
    { id: 'class2', name: 'class2' },
    { id: 'class3', name: 'class3' },
    { id: 'class4', name: 'class4' },
    { id: 'class5', name: 'class5' },
    { id: 'test', name: 'test' },
    { id: 'testclass', name: 'testclass' },
  ];

  const scheduleData = [
    { 
      section: 'course1',
      days: [
        { day: 'Monday', date: '08/07', course: 'course1', teacher: 't1', students: 2 },
        { day: 'Tuesday', date: '08/08', course: 'course1', teacher: 't1', students: 2 },
        { day: 'Wednesday', date: '08/09', course: 'course1', teacher: 't1', students: 2 },
        { day: 'Thursday', date: '08/10', course: 'course1', teacher: 't1', students: 2 },
        { day: 'Friday', date: '08/11', course: 'course1', teacher: 't1', students: 2 },
        { day: 'Saturday', date: '08/12', course: 'course12', teacher: 't12', students: 2 },
        { day: 'Sunday', date: '08/13', course: 'course1', teacher: 't1', students: 2 },
      ]
    },
    { 
      section: 'course1',
      days: [
        { day: 'Monday', date: '08/07', course: 'course1', teacher: 't1', students: 2 },
        { day: 'Tuesday', date: '08/08', course: 'course1', teacher: 't1', students: 2 },
        { day: 'Wednesday', date: '08/09', course: 'course1', teacher: 't1', students: 2 },
        { day: 'Thursday', date: '08/10', course: 'course1', teacher: 't1', students: 2 },
        { day: 'Friday', date: '08/11', course: 'course1', teacher: 't1', students: 2 },
        { day: 'Saturday', date: '08/12', course: 'course12', teacher: 't12', students: 2 },
        { day: 'Sunday', date: '08/13', course: 'course1', teacher: 't1', students: 2 },
      ]
    }
  ];

  const handleExport = () => {
    alert('Exporting data...');
  };

  const handleRefresh = () => {
    alert('Refreshing data...');
  };

  const handlePrevWeek = () => {
    alert('Navigate to previous week');
  };

  const handleNextWeek = () => {
    alert('Navigate to next week');
  };

  const handleCurrentWeek = () => {
    alert('Navigate to current week');
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6 flex-wrap gap-4">
        <div className="relative w-full max-w-xs">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search for app or class name..."
            className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md"
          />
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
        </div>
        
        <div className="text-sm text-gray-700 font-medium">
          Number of Class Students: <span className="font-bold">2</span>
        </div>
        
        <WeekNavigation
          currentWeek={currentWeek}
          term={currentTerm}
          onPrevWeek={handlePrevWeek}
          onNextWeek={handleNextWeek}
          onCurrentWeek={handleCurrentWeek}
        />
      </div>

      <div className="flex items-start gap-6 flex-wrap md:flex-nowrap">
        <div className="w-full md:w-64 bg-white shadow-sm rounded-lg overflow-hidden">
          <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
            <div className="flex items-center gap-2 text-gray-700 font-medium">
              <School size={16} />
              <span>Hikvision Testing</span>
            </div>
            <div className="text-sm text-gray-500">School of T1</div>
          </div>
          
          <div className="overflow-y-auto max-h-[400px]">
            {classList.map(cls => (
              <button
                key={cls.id}
                className={`w-full px-4 py-3 text-left flex items-center gap-2 hover:bg-gray-50 transition-colors border-b border-gray-100 ${
                  selectedClass === cls.id ? 'bg-red-50' : ''
                }`}
                onClick={() => setSelectedClass(cls.id)}
              >
                <Users size={16} className={selectedClass === cls.id ? 'text-red-500' : 'text-gray-500'} />
                <span className={selectedClass === cls.id ? 'text-red-600 font-medium' : 'text-gray-700'}>
                  {cls.name}
                </span>
              </button>
            ))}
          </div>
        </div>
        
        <div className="flex-1">
          <div className="flex justify-end mb-4 gap-2">
            <ActionButtons 
              onExport={handleExport} 
              onRefresh={handleRefresh}
              showSettings={true} 
            />
          </div>
          
          <div className="bg-white shadow-sm rounded-lg overflow-x-auto">
            <table className="min-w-full border-collapse">
              <thead>
                <tr>
                  <th className="bg-gray-600 text-white px-4 py-3 text-left font-medium">Section</th>
                  <th className="bg-gray-600 text-white px-4 py-3 text-center font-medium">
                    <div>Monday</div>
                    <div className="text-xs font-normal">08/07</div>
                  </th>
                  <th className="bg-gray-600 text-white px-4 py-3 text-center font-medium">
                    <div>Tuesday</div>
                    <div className="text-xs font-normal">08/08</div>
                  </th>
                  <th className="bg-gray-600 text-white px-4 py-3 text-center font-medium">
                    <div>Wednesday</div>
                    <div className="text-xs font-normal">08/09</div>
                  </th>
                  <th className="bg-gray-600 text-white px-4 py-3 text-center font-medium">
                    <div>Thursday</div>
                    <div className="text-xs font-normal">08/10</div>
                  </th>
                  <th className="bg-gray-600 text-white px-4 py-3 text-center font-medium">
                    <div>Friday</div>
                    <div className="text-xs font-normal">08/11</div>
                  </th>
                  <th className="bg-gray-600 text-white px-4 py-3 text-center font-medium">
                    <div>Saturday</div>
                    <div className="text-xs font-normal">08/12</div>
                  </th>
                  <th className="bg-gray-600 text-white px-4 py-3 text-center font-medium">
                    <div>Sunday</div>
                    <div className="text-xs font-normal">08/13</div>
                  </th>
                </tr>
              </thead>
              <tbody>
                {scheduleData.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    <td className="border px-4 py-2">{row.section}</td>
                    {row.days.map((day, dayIndex) => (
                      <td key={dayIndex} className="border p-2 bg-green-50">
                        <div className="flex flex-col items-center">
                          <div className="text-sm font-medium">{day.course}</div>
                          <div className="text-xs text-gray-500">{day.teacher}</div>
                          <div className="flex items-center gap-1 mt-1">
                            <Users size={14} className="text-red-500" />
                            <span className="text-xs">{day.students}</span>
                          </div>
                        </div>
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="mt-8 bg-green-50 border border-green-100 rounded-lg p-6 text-center">
        <h2 className="text-xl font-semibold text-green-800 mb-2">Class-wise Attendance</h2>
      </div>
    </div>
  );
};

export default ClassWiseView;