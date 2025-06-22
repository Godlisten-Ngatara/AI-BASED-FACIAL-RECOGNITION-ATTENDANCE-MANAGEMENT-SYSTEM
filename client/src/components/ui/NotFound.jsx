import React from "react";
import { useAuth } from "../../auth/AuthContext";
import { useNavigate } from "react-router-dom";

const NotFoundPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleRedirect = () => {
    navigate(user ? "/main/dashboard" : "/", { replace: true });
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center bg-gray-100 px-4">
      <h1 className="text-5xl font-bold text-gray-800 mb-4">404</h1>
      <p className="text-xl text-gray-600 mb-6">
        Oops! The page you're looking for doesn't exist.
      </p>
      <button
        onClick={handleRedirect}
        className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded shadow"
      >
        {user ? "Go to Dashboard" : "Go to Home"}
      </button>
    </div>
  );
};

export default NotFoundPage;
