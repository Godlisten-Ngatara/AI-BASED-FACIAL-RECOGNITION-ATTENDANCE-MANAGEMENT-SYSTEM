import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  FaUserCheck,
  FaChartLine,
  FaCalendarCheck,
  FaLock,
} from "react-icons/fa";
import landing_background from "../assets/landing_background.jpg";
import logo from "../assets/udsm_logo.png";
import scan_landing from "../assets/icons/scan_landing.png";
import security_landing from "../assets/icons/security_landing.png";
import real_time_landing from "../assets/icons/real-time_landing.png";
import calendar_landing from "../assets/icons/calendar_landing.png";
import { useAuth } from "../auth/AuthContext";
import { useNavigate } from "react-router-dom";

export default function LandingPage() {
//   const { login } = useAuth();
  const navigate = useNavigate();
  const { setSelectedRole } = useAuth();
  const handleRoleLogin = (role) => {
    // Store only the role (you can extend this later)
    // login({ role });
    localStorage.setItem("selectedRole", role)
    setSelectedRole(role);
    navigate("/login");
  };
  return (
    <div className="relative min-h-screen overflow-hidden p-4">
      {/* Full-page background image with gradient fade */}
      <div className="absolute inset-0 z-0 ">
        <img
          src={landing_background}
          alt="Lecture Hall Background"
          className="w-full h-full object-cover"
        />
      </div>

      {/* Foreground content */}
      <div className="relative z-10 flex flex-col items-center px-4 text-white text-center">
        {/* Logo & Heading */}
        <img src={logo} alt="AI-FRAMS Logo" className="w-20 mt-10 mb-0" />
        <h1 className="font-bold mb-7">AI-FRAMS</h1>

        <h1 className="text-1xl md:text-5xl font-bold max-w-4xl mb-5">
          AI-Based Facial Recognition Students Attendance Management System
        </h1>
        <p className="italic text-lg mt-2 mb-2">
          "Experience smart, secure, and effortless attendance tracking"
        </p>

        <div className="w-150 h-0.5 bg-white mx-auto mt-0 mb-10" />

        {/* Features container */}
        <div className="w-full max-w-7xl bg-cyan-600  shadow-lg p-8 grid grid-cols-1 md:grid-cols-4 gap-6 mb-8 mx-8">
          <Card className="bg-cyan-600 text-white text-center border-none shadow-none w-50">
            <CardContent className="flex flex-col items-center p-4">
              <img src={scan_landing} alt="" className="mb-2 w-15 h-15" />
              <h3 className="text-lg font-bold">Facial Recognition</h3>
              <p className="text-sm font-semibold">
                Fast and accurate student identification.
              </p>
            </CardContent>
          </Card>

          <Card className="bg-cyan-600 text-white text-center border-none shadow-none w-50">
            <CardContent className="flex flex-col items-center p-4">
              <img src={real_time_landing} alt="" className="mb-2 w-15 h-15" />
              <h3 className="text-lg font-bold">Real-Time Reports</h3>
              <p className="text-sm font-semibold">
                Track attendance trends easily.
              </p>
            </CardContent>
          </Card>

          <Card className="bg-cyan-600 text-white text-center border-none shadow-none w-54">
            <CardContent className="flex flex-col items-center p-4">
              <img src={calendar_landing} alt="" className="mb-2 w-15 h-15" />
              <h3 className="text-lg font-bold">
                Automatic Attendance Logging
              </h3>
              <p className="text-sm font-semibold">No manual effort needed.</p>
            </CardContent>
          </Card>

          <Card className="bg-cyan-600 text-white text-center border-none shadow-none w-54">
            <CardContent className="flex flex-col items-center p-4">
              <img src={security_landing} alt="" className="mb-2 w-15 h-15" />
              <h3 className="text-lg font-bold">Secure & Role-Based</h3>
              <p className="text-sm font-semibold">
                Access different dashboards for instructors and students.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Buttons */}
        <div className="flex flex-col md:flex-row gap-4 mb-5">
          <Button
            onClick={() => handleRoleLogin("student")}
            className="bg-cyan-600 text-white hover:bg-cyan-500 px-6 py-2"
          >
            Login as Student
          </Button>
          <Button
            onClick={() => handleRoleLogin("instructor")}
            className="bg-cyan-600 text-white hover:bg-cyan-500 px-6 py-2"
          >
            Login as Instructor
          </Button>
        </div>
      </div>
    </div>
  );
}
