import React, { useState } from 'react';
import { Search, X } from 'lucide-react';
import DateRangePicker from '../components/DaterangePicker';
import ActionButtons from '../components/ActionButton';
import AttendanceStatus from '../components/AttendanceStatus';

const StudentWiseView = () => {
  const [studentId, setStudentId] = useState('1534779298');
  const [startDate, setStartDate] = useState('2023-08-03');
  const [endDate, setEndDate] = useState('2023-08-10');
  const [courseName, setCourseName] = useState('');

  // Mock data
  const studentData = {
    id: '1534779298',
    name: 's1',
    class: 'class1',
    image: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII='
  };

  const attendanceData = [
    { courseName: 'course11', courseTime: '19:40-20:00', courseDate: '2023/08/09 Wednesday', courseTeacher: 't11', classroom: 'classroom11', attendance: 'Absent', capturedPicture: '--' },
    { courseName: 'course10', courseTime: '19:20-19:30', courseDate: '2023/08/09 Wednesday', courseTeacher: 't10', classroom: 'classroom10', attendance: 'Absent', capturedPicture: '--' },
    { courseName: 'course9', courseTime: '19:00-19:10', courseDate: '2023/08/09 Wednesday', courseTeacher: 't9', classroom: 'classroom9', attendance: 'Absent', capturedPicture: '--' },
    { courseName: 'course8', courseTime: '18:40-18:50', courseDate: '2023/08/09 Wednesday', courseTeacher: 't8', classroom: 'classroom8', attendance: 'Absent', capturedPicture: '--' },
  ];

  const handleExport = () => {
    alert('Exporting data...');
  };

  const handleRefresh = () => {
    alert('Refreshing data...');
  };

  const clearStudentId = () => {
    setStudentId('');
  };

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div>
          <label htmlFor="student" className="block mb-1 font-medium">
            Student <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <input
              id="student"
              type="text"
              value={studentId}
              onChange={(e) => setStudentId(e.target.value)}
              className="w-full pl-3 pr-10 py-2 border border-gray-300 rounded-md"
              placeholder="Enter student ID"
            />
            {studentId && (
              <button 
                onClick={clearStudentId}
                className="absolute right-3 top-1/2 -translate-y-1/2"
              >
                <X size={16} className="text-gray-400 hover:text-gray-600" />
              </button>
            )}
          </div>
        </div>

        <div>
          <label htmlFor="course" className="block mb-1 font-medium">
            Course Name
          </label>
          <input
            id="course"
            type="text"
            value={courseName}
            onChange={(e) => setCourseName(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
            placeholder="Enter course name"
          />
        </div>
      </div>

      <div className="flex justify-between items-center flex-wrap gap-4 mb-6">
        <div>
          <label className="block mb-1 font-medium">Course Date</label>
          <DateRangePicker
            startDate={startDate}
            endDate={endDate}
            onStartDateChange={setStartDate}
            onEndDateChange={setEndDate}
          />
        </div>
      </div>

      {studentId && (
        <>
          <div className="bg-white shadow-sm border border-gray-200 rounded-md overflow-hidden mb-6">
            <table className="min-w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th className="px-4 py-3 bg-gray-50 text-left text-sm font-semibold text-gray-700">Name</th>
                  <th className="px-4 py-3 bg-gray-50 text-left text-sm font-semibold text-gray-700">Student No.</th>
                  <th className="px-4 py-3 bg-gray-50 text-left text-sm font-semibold text-gray-700">Class Name</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="px-4 py-3 text-sm text-gray-900">{studentData.name}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{studentData.id}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{studentData.class}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="flex justify-end mb-4">
            <ActionButtons 
              onExport={handleExport} 
              onRefresh={handleRefresh} 
            />
          </div>

          <div className="bg-white shadow-sm border border-gray-200 rounded-md overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th className="px-4 py-3 bg-gray-50 text-left text-sm font-semibold text-gray-700">Course Name</th>
                  <th className="px-4 py-3 bg-gray-50 text-left text-sm font-semibold text-gray-700">Course Time</th>
                  <th className="px-4 py-3 bg-gray-50 text-left text-sm font-semibold text-gray-700">Course Date</th>
                  <th className="px-4 py-3 bg-gray-50 text-left text-sm font-semibold text-gray-700">Course Teacher</th>
                  <th className="px-4 py-3 bg-gray-50 text-left text-sm font-semibold text-gray-700">Classroom</th>
                  <th className="px-4 py-3 bg-gray-50 text-left text-sm font-semibold text-gray-700">Attendance</th>
                  <th className="px-4 py-3 bg-gray-50 text-left text-sm font-semibold text-gray-700">Captured Picture</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {attendanceData.map((record, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm text-gray-900">{record.courseName}</td>
                    <td className="px-4 py-3 text-sm text-gray-900">{record.courseTime}</td>
                    <td className="px-4 py-3 text-sm text-gray-900">{record.courseDate}</td>
                    <td className="px-4 py-3 text-sm text-gray-900">{record.courseTeacher}</td>
                    <td className="px-4 py-3 text-sm text-gray-900">{record.classroom}</td>
                    <td className="px-4 py-3 text-sm">
                      <AttendanceStatus status={record.attendance } />
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900">{record.capturedPicture}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      <div className="mt-8 bg-green-50 border border-green-100 rounded-lg p-6 text-center">
        <h2 className="text-xl font-semibold text-green-800 mb-2">Student-wise Attendance</h2>
        <p className="text-green-700">It is easy to search dedicated student's all attendance</p>
      </div>
    </div>
  );
};

export default StudentWiseView;