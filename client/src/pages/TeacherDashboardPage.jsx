// import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import teaching_image from "../assets/teaching.jpg";
import studets_icon from "../assets/icons/students.png";
import graph1_icon from "../assets/icons/graph_1.png";
import graph2_icon from "../assets/icons/graph_2.png";
import graph3_icon from "../assets/icons/graph_3.png";
import useFetch from "@/hooks/useFetch";
import AttendanceTrendChart from "@/components/ui/chart";
export default function TeacherDashboardPage() {
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const first_name = user.name;
  const { data } = useFetch("http://localhost:8002/api/v1/courses");
  const total_students = data?.data?.students?.length ?? 0;
  return (
    <>
      <Card className="bg-blue-900 text-white mb-6">
        <CardContent className="flex justify-between items-center p-6">
          <h3 className="font-large text-3xl">Hello Dr. {first_name} 👋</h3>
          <span className="text-3xl font-large">Welcome to AI-FRAMS</span>
        </CardContent>
      </Card>

      <div className="flex w-full gap-6 mb-6">
        {/* First card - 3/4 width */}
        <div className="w-3/4 bg-white rounded-xl shadow-lg overflow-hidden">
          <div
            className="h-96 w-full bg-cover bg-center relative p-6 text-white"
            style={{ backgroundImage: `url(${teaching_image})` }}
          >
            <div className="absolute inset-0 bg-blue-900/60 z-0 rounded-xl" />
            <div className="relative z-10 flex flex-col justify-between h-full">
              <div>
                <h4 className="text-md">Course Name</h4>
                <h2 className="text-2xl font-bold">
                  {data?.data?.course?.title}
                </h2>
                <h4 className="text-md">Course Code </h4>
                <h2 className="text-2xl font-bold">
                  {data?.data?.course?.course_code}
                </h2>
              </div>
            </div>
          </div>
        </div>

        {/* Second card - 1/4 width */}
        <div className="w-1/4">
          <Card className="bg-cyan-600 text-white h-96 p-6 flex flex-col justify-between">
            <div>
              <p className="text-left text-3xl">
                Total Number of
                <br />
                Students
              </p>
            </div>

            <div className="flex justify-center">
              <h1 className="text-8xl font-bold">{total_students}</h1>
            </div>

            <div className="flex justify-end">
              <img src={studets_icon} alt="icon" className="w-15 h-15" />
            </div>
          </Card>
        </div>
      </div>

      <div className="mb-2">
        <h3 className="text-4xl font-semibold text-blue-900 mb-4">
          Average Attendance
        </h3>
        <div className="mt-2">
          {/* {[
            {
              day: "Monday",
              percent: "67%",
              color: "bg-blue-900",
              icon: graph1_icon,
            },
            {
              day: "Tuesday",
              percent: "50%",
              color: "bg-blue-900",
              icon: graph2_icon,
            }, // We'll simulate this
            {
              day: "Friday",
              percent: "80%",
              color: "bg-blue-900",
              icon: graph3_icon,
            },
          ].map((item, index) => (
            <Card key={index} className="bg-blue-900 text-white">
              <CardContent className="p-4">
                <div className="flex items-center justify-between w-full p-4">
                  <p className="text-2xl">{item.day}</p>

                  <div className="flex flex-col items-center">
                    <img
                      src={item.icon}
                      alt="icon"
                      className="w-10 h-10 mb-1"
                    />
                    <h2 className="text-5xl font-bold">{item.percent}</h2>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))} */}
          <AttendanceTrendChart/>
        </div>
      </div>
    </>
  );
}
