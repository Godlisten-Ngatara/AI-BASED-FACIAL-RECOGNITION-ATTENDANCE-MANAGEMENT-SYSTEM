import React from "react";
import { motion } from "framer-motion";

const Spinner = () => {
    const message = "Processing your request.."
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-white/80 backdrop-blur-sm">
      <div className="flex flex-col items-center space-y-4">
        {/* Spinner */}
        <div className="relative">
          {/* Outer ring */}
          <div className="h-16 w-16 animate-spin rounded-full border-4 border-gray-200"></div>
          {/* Inner spinning ring */}
          <div className="absolute inset-0 h-16 w-16 animate-spin rounded-full border-4 border-transparent border-t-blue-500 border-r-blue-500"></div>
          {/* Center dot */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="h-2 w-2 animate-pulse rounded-full bg-blue-500"></div>
          </div>
        </div>

        {/* Loading text */}
        <div className="text-center">
          <p className="text-lg font-medium text-gray-700 animate-pulse">
            {message}
          </p>
          <div className="mt-2 flex space-x-1 justify-center">
            <div className="h-1 w-1 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
            <div className="h-1 w-1 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
            <div className="h-1 w-1 bg-blue-500 rounded-full animate-bounce"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Spinner;
