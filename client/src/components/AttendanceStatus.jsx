import React from 'react';


const AttendanceStatus = ({ status }) => {
  let className = '';
  
  switch (status) {
    case 'Present':
      className = 'text-green-600';
      break;
    case 'Absent':
      className = 'text-red-500';
      break;
    case 'Late':
      className = 'text-amber-500';
      break;
    default:
      className = 'text-gray-500';
  }
  
  return (
    <span className={`font-medium ${className}`}>
      {status}
    </span>
  );
};

export default AttendanceStatus;