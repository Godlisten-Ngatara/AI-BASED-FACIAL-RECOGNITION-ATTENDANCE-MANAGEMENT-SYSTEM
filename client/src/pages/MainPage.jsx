import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import logo from "../assets/udsm_logo.png";
import user_icon from "../assets/icons/user.png";
import dashboard_icon_active from "../assets/icons/dashboard_active.png";
import dashboard_icon from "../assets/icons/dashboard.png";
import profile_icon from "../assets/icons/profile.png";
import profile_icon_active from "../assets/icons/profile_active.png";
import classes_icon from "../assets/icons/classes.png";
import classes_icon_active from "../assets/icons/classes_active.png";
import students_icon from "../assets/icons/students.png";
import students_icon_active from "../assets/icons/students_active.png";
import attendance_icon from "../assets/icons/attendance.png";
import attendance_icon_active from "../assets/icons/attendance_active.png";
import notifications_icon from "../assets/icons/notifications.png";
import notifications_icon_active from "../assets/icons/notifications_active.png";
import settings_icon from "../assets/icons/settings.png";
import settings_icon_active from "../assets/icons/settings_active.png";
import logout_icon from "../assets/icons/logout.png";
import TeacherDashboardPage from "./TeacherDashboardPage";
import { Search } from "lucide-react";
import TeacherProfilePage from "./TeacherProfilePage";
import StudentDashboardPage from "./StudentDashboardPage";
import StudentProfilePage from "./StudentProfilePage";
import TeacherNotificationPage from "./TeacherNotificationPage";
import StudentNotificationPage from "./StudentNotificationPage";
import { useAuth } from "@/auth/AuthContext";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import MyStudentsPage from "./MyStudentsPage";
import SettingsPage from "./SettingsPage";
import AttendanceTable from "./AttendancePage";
import CapturedImagesGallery from "./CapturedImagesPage";
const menuItems = [
  {
    id: "dashboard",
    label: "Dashboard",
    icon: dashboard_icon,
    activeIcon: dashboard_icon_active,
  },
  {
    id: "profile",
    label: "My Profile",
    icon: profile_icon,
    activeIcon: profile_icon_active,
  },
  // {
  //   id: "classes",
  //   label: "My Classes",
  //   icon: classes_icon,
  //   activeIcon: classes_icon_active,
  // },
  {
    id: "students",
    label: "My Students",
    icon: students_icon,
    activeIcon: students_icon_active,
  },
  {
    id: "attendance",
    label: "Attendance Records",
    icon: attendance_icon,
    activeIcon: attendance_icon_active,
  },
  // {
  //   id: "notifications",
  //   label: "Notifications",
  //   icon: notifications_icon,
  //   activeIcon: notifications_icon_active,
  // },
  // {
  //   id: "settings",
  //   label: "Settings",
  //   icon: settings_icon,
  //   activeIcon: settings_icon_active,
  // },
  {
    id: "images",
    label: "Captured Images",
    icon: settings_icon,
    activeIcon: settings_icon_active,
  },
];
const getLabelById = (id) => {
  const menuItem = menuItems.find((item) => item.id === id);
  return menuItem ? menuItem.label : null; // Return label if found, else null
};

export default function MainPage() {
  const [active, setActive] = useState("dashboard");
  const { user, selectedRole } = useAuth();
  const storedRole = localStorage.getItem("selectedRole");
  // Access role
  const role = user?.role;
  const renderContent = () => {
    switch (active) {
      case "dashboard":
        return storedRole == "student" ? (
          <StudentDashboardPage />
        ) : (
          <TeacherDashboardPage />
        );
      case "profile":
        return storedRole == "student" ? (
          <StudentProfilePage />
        ) : (
          <TeacherProfilePage />
        );
      case "attendance":
        return <AttendanceTable />;
      case "notifications":
        return storedRole == "student" ? (
          <StudentNotificationPage />
        ) : (
          <TeacherNotificationPage />
        );
      case "students":
        return <MyStudentsPage />;
      case "settings":
        return <SettingsPage />;
      case "images":
        return storedRole == "student" ? "" : <CapturedImagesGallery />;
      default:
        return <div className="text-blue-900 text-xl">{active} content</div>;
    }
  };

  // logout functionality
  const { logout } = useAuth();
  const navigate = useNavigate();
  const handleLogout = () => {
    logout(); // Clear user context and localStorage
    navigate("/"); // Redirect to login or home page
  };

  // Filter menu items based on role
  const filteredMenuItems = menuItems.filter((item) => {
    // Show 'My Students' only for instructors
    if (item.id === "students" && storedRole !== "instructor") {
      return false;
    }
    return true;
  });
  return (
    <div className="flex min-h-screen font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-[#002366] text-white flex flex-col items-start px-4 ">
        
        <div className="fixed top-6">
          <img src={logo} alt="Logo" className="w-16 h-16 mb-6 mx-auto" />
          <h1 className="text-xl font-bold text-center w-full mb-8">
            AI-FRAMS
          </h1>

          <nav className="flex flex-col gap-2 w-full">
            {filteredMenuItems.map((item) => (
              <button
                key={item.id}
                onClick={() => setActive(item.id)}
                className={`flex items-center gap-3 px-4 py-2 text-left w-full transition-all duration-200 ${
                  active === item.id
                    ? "bg-blue-50 text-blue-900 rounded-tr-3xl rounded-br-3xl"
                    : "hover:bg-blue-800"
                }`}
              >
                <img
                  src={active === item.id ? item.activeIcon : item.icon}
                  alt="icon"
                  className="w-5 h-5"
                />
                <span>{item.label}</span>
              </button>
            ))}
          </nav>
        </div>

        <button
          onClick={handleLogout}
          className="mt-auto flex items-center gap-2 px-6 py-2 text-white fixed bottom-2"
        >
          <img src={logout_icon} alt="logout icon" className="w-5 h-5" /> Logout
        </button>
      </aside>

      {/* Main Content */}
      <main className="flex-1 bg-blue-50 ">
        <div className="flex justify-between items-center  pt-6 pb-0 px-20">
          <h2 className="text-2xl font-bold text-blue-900">
            {getLabelById(active)}
          </h2>

          <div className="relative w-64">
            <Input
              placeholder="Search Here"
              className="w-64 rounded-full border-gray-800 pl-10"
            />
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          </div>
          <div className="flex justify-between items-center gap-2 text-blue-900">
            <img
              src={user_icon}
              alt="Dr.Daudi"
              className="w-10 h-10 rounded-full"
            />
            <h1>{storedRole == "student" ? "Godlisten" : "Dr.Daudi"}</h1>
          </div>
        </div>
        <div className="pt-6 pb-0 px-20">{renderContent()}</div>

        {/* <footer className=" fixed bottom-0 right-0 w-full text-center text-sm text-white bg-[#002366] py-1">
          © 2025 All Rights Reserved
        </footer> */}
      </main>
    </div>
  );
}
