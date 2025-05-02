import React from 'react';
import { User } from 'lucide-react';



const StudentProfile = ({ 
  studentId, 
  name, 
  imageUrl 
}) => {
  return (
    <div className="flex items-center gap-3">
      <div className="w-10 h-10 bg-gray-100 border border-gray-200 rounded-md overflow-hidden flex items-center justify-center">
        {imageUrl ? (
          <img src={imageUrl} alt={name} className="w-full h-full object-cover" />
        ) : (
          <User size={20} className="text-gray-400" />
        )}
      </div>
      <div>
        <p className="font-medium text-gray-800">{name}</p>
        <p className="text-sm text-gray-500">{studentId}</p>
      </div>
    </div>
  );
};

export default StudentProfile;