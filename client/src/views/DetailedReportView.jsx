import React, { useState } from 'react';
import { ChevronLeft } from 'lucide-react';
import ActionButtons from '../components/ActionButton';
import AttendanceStatus from '../components/AttendanceStatus';

const DetailedReportView = () => {
  const [showCourseInfo, setShowCourseInfo] = useState(true);

  // Mock data
  const courseInfo = {
    name: 'course1',
    time: '00:15-00:35',
    date: '2023/08/07 Monday',
    teacher: 't1',
    className: 'class1',
    classroom: 'classroom1',
    attendanceRate: '0.0% (0/2)'
  };

  const studentData = [
    { 
      profilePicture: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=', 
      name: 's1', 
      studentNo: '1534779298', 
      attendance: 'Absent', 
      capturedPicture: '--' 
    }
  ];

  const handleExport = () => {
    alert('Exporting data...');
  };

  const handleAttendanceCorrection = () => {
    alert('Opening attendance correction...');
  };

  const toggleCourseInfo = () => {
    setShowCourseInfo(!showCourseInfo);
  };

  return (
    <div>
      <button 
        onClick={toggleCourseInfo}
        className="flex items-center gap-1 text-blue-600 hover:underline mb-6"
      >
        <ChevronLeft size={16} />
        {showCourseInfo ? 'Hide' : 'Show'} Course Information
      </button>

      {showCourseInfo && (
        <div className="bg-green-50 border border-green-100 rounded-lg mb-6 overflow-hidden">
          <table className="min-w-full">
            <thead>
              <tr>
                <th className="px-4 py-3 bg-green-100 text-left text-sm font-semibold text-green-800">Course Name</th>
                <th className="px-4 py-3 bg-green-100 text-left text-sm font-semibold text-green-800">Course Time</th>
                <th className="px-4 py-3 bg-green-100 text-left text-sm font-semibold text-green-800">Course Teacher</th>
                <th className="px-4 py-3 bg-green-100 text-left text-sm font-semibold text-green-800">Class Name</th>
                <th className="px-4 py-3 bg-green-100 text-left text-sm font-semibold text-green-800">Classroom</th>
                <th className="px-4 py-3 bg-green-100 text-left text-sm font-semibold text-green-800">Attendance Rate</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="px-4 py-3 text-sm text-gray-800">{courseInfo.name}</td>
                <td className="px-4 py-3 text-sm text-gray-800">
                  <div>{courseInfo.time}</div>
                  <div>{courseInfo.date}</div>
                </td>
                <td className="px-4 py-3 text-sm text-gray-800">{courseInfo.teacher}</td>
                <td className="px-4 py-3 text-sm text-gray-800">{courseInfo.className}</td>
                <td className="px-4 py-3 text-sm text-gray-800">{courseInfo.classroom}</td>
                <td className="px-4 py-3 text-sm text-gray-800">{courseInfo.attendanceRate}</td>
              </tr>
            </tbody>
          </table>
        </div>
      )}

      <div className="flex gap-4 mb-6">
        <button 
          onClick={handleAttendanceCorrection}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
        >
          Attendance Correction
        </button>
        
        <button 
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
        >
          Leave
        </button>
        
        <ActionButtons onExport={handleExport} />
      </div>

      <div className="bg-white shadow-sm border border-gray-200 rounded-md overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th className="px-4 py-3 bg-gray-50">
                <input type="checkbox" className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
              </th>
              <th className="px-4 py-3 bg-gray-50 text-left text-sm font-semibold text-gray-700">Profile Picture</th>
              <th className="px-4 py-3 bg-gray-50 text-left text-sm font-semibold text-gray-700">Student Name</th>
              <th className="px-4 py-3 bg-gray-50 text-left text-sm font-semibold text-gray-700">Student No.</th>
              <th className="px-4 py-3 bg-gray-50 text-left text-sm font-semibold text-gray-700">Attendance Result</th>
              <th className="px-4 py-3 bg-gray-50 text-left text-sm font-semibold text-gray-700">Captured Picture</th>
            </tr>
          </thead>
          <tbody>
            {studentData.map((student, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="px-4 py-3">
                  <input type="checkbox" className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                </td>
                <td className="px-4 py-3">
                  <div className="w-12 h-12 bg-gray-100 border border-gray-200 rounded-md overflow-hidden">
                    <img src={student.profilePicture} alt={student.name} className="w-full h-full object-cover" />
                  </div>
                </td>
                <td className="px-4 py-3 text-sm text-gray-900">{student.name}</td>
                <td className="px-4 py-3 text-sm text-gray-900">{student.studentNo}</td>
                <td className="px-4 py-3 text-sm">
                  <AttendanceStatus status={student.attendance} />
                </td>
                <td className="px-4 py-3 text-sm text-gray-900">{student.capturedPicture}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-8 bg-green-50 border border-green-100 rounded-lg p-6 text-center">
        <h2 className="text-xl font-semibold text-green-800 mb-2">Detailed Attendance Report</h2>
      </div>
    </div>
  );
};

export default DetailedReportView;