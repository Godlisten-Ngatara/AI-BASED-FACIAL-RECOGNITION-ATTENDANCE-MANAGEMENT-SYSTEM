// import React, { useState } from "react";
import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import teaching_image from "../assets/teaching.jpg";
import studets_icon from "../assets/icons/students.png";
import graph1_icon from "../assets/icons/graph_1.png";
import graph2_icon from "../assets/icons/graph_2.png";
import graph3_icon from "../assets/icons/graph_3.png";
import useFetch from "@/hooks/useFetch";
import AttendanceTrendChart from "@/components/ui/chart";
import Spinner from "@/components/ui/spinner";
export default function TeacherDashboardPage() {
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const first_name = user.name;
  const { data, loading } = useFetch("http://localhost:8002/api/v1/courses");
  const [selectedCourseId, setSelectedCourseId] = useState(null);
  const [startAt, setStartAt] = useState("08:00");
  const [endAt, setEndAt] = useState("10:00");
  const [isCanceled, setIsCanceled] = useState(false);
  const [showSessionModal, setShowSessionModal] = useState(false);
  const [scheduleLoading, setLoading] = useState(false);
  const [sessionMessage, setSessionMessage] = useState(""); // for success or error messages

  useEffect(() => {
    if (data?.data?.length && selectedCourseId === null) {
      setSelectedCourseId(data.data[0].course.course_id);
    }
  }, [data, selectedCourseId]);

  const selectedCourseData = data?.data.find(
    (item) => item.course.course_id === selectedCourseId
  );
  const total_students = selectedCourseData?.students?.length ?? 0;
  const handleSessionAdjust = async () => {
    setLoading(true);
    setSessionMessage("");
    try {
      const payload = {
        is_canceled: isCanceled,
        ...(isCanceled
          ? {}
          : { start_at: `${startAt}:00`, end_at: `${endAt}:00` }),
      };
      const endpoint = isCanceled
        ? `http://localhost:8002/api/v1/courses/${selectedCourseId}/cancel-session`
        : `http://localhost:8002/api/v1/courses/${selectedCourseId}/reschedule-session`;
      const res = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const result = await res.json();
      if (res.ok) {
        setSessionMessage(
          isCanceled
            ? "✅ Session successfully canceled."
            : "✅ Session successfully rescheduled."
        );
        setTimeout(() => {
          setShowSessionModal(false);
          setSessionMessage("");
        }, 1500);
      } else {
        setSessionMessage(`❌ ${result.detail || "Failed to adjust session."}`);
      }
    } catch (err) {
      console.error(err);
      setSessionMessage("❌ Error adjusting session.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Spinner />;
  return (
    <>
      <Card className="bg-blue-900 text-white mb-6">
        <CardContent className="flex justify-between items-center p-6">
          <h3 className="font-large text-3xl">Hello Dr. {first_name} 👋</h3>
          <span className="text-3xl font-large">Welcome to AI-FRAMS</span>
        </CardContent>
      </Card>
      {/* Course Selection Dropdown */}
      {data?.data?.length > 1 && (
        <div className="mb-6 flex justify-between">
          <label
            htmlFor="course-select"
            className="block mb-1 text-lg font-medium text-blue-900"
          >
            Select Course
          </label>
          <select
            id="course-select"
            value={selectedCourseId || ""}
            onChange={(e) => setSelectedCourseId(Number(e.target.value))}
            className="w-full max-w-md border border-gray-300 px-4 py-2 rounded focus:outline-none focus:ring focus:ring-blue-500"
          >
            {data.data.map(({ course }) => (
              <option key={course.course_id} value={course.course_id}>
                {course.title} ({course.course_code})
              </option>
            ))}
          </select>
          <button
            onClick={() => setShowSessionModal(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 cursor-pointer"
          >
            Reschedule / Cancel Session
          </button>
        </div>
      )}

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
                <h2 className="text-2xl font-bold">
                  {selectedCourseData?.course?.title}
                </h2>
                <h2 className="text-2xl font-bold">
                  {selectedCourseData?.course?.course_code}
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
          <AttendanceTrendChart courseId={selectedCourseId} />
        </div>
        {showSessionModal && (
          <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
            <div className="bg-white p-6 rounded-xl w-[400px] shadow-lg cursor-default relative">
              <h2 className="text-xl font-bold text-blue-900 mb-4">
                Adjust Session
              </h2>

              <label className="block mb-2 font-semibold text-sm text-gray-700">
                Start Time
              </label>
              <input
                type="time"
                value={startAt}
                onChange={(e) => setStartAt(e.target.value)}
                className="w-full border rounded p-2 mb-4"
                disabled={isCanceled || scheduleLoading}
              />

              <label className="block mb-2 font-semibold text-sm text-gray-700">
                End Time
              </label>
              <input
                type="time"
                value={endAt}
                onChange={(e) => setEndAt(e.target.value)}
                className="w-full border rounded p-2 mb-4"
                disabled={isCanceled || scheduleLoading}
              />

              <label className="flex items-center mb-4">
                <input
                  type="checkbox"
                  checked={isCanceled}
                  onChange={() => setIsCanceled(!isCanceled)}
                  className="mr-2"
                  disabled={scheduleLoading}
                />
                Cancel this session
              </label>

              {sessionMessage && (
                <div
                  className={`text-sm mb-4 ${
                    sessionMessage.startsWith("✅")
                      ? "text-green-600"
                      : "text-red-600"
                  }`}
                >
                  {sessionMessage}
                </div>
              )}

              <div className="flex justify-end gap-2">
                <button
                  onClick={() => setShowSessionModal(false)}
                  className="text-sm text-gray-600"
                  disabled={scheduleLoading}
                >
                  Cancel
                </button>
                <button
                  onClick={handleSessionAdjust}
                  className="bg-blue-600 text-white px-4 py-2 rounded flex items-center justify-center min-w-[120px]"
                  disabled={scheduleLoading}
                >
                  {scheduleLoading ? <Spinner size="sm" /> : "Save Changes"}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
}
