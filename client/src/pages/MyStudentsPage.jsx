import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";
import useFetch from "@/hooks/useFetch.js";
import Spinner from "@/components/ui/spinner";
import handleDownloadCSV from "@/hooks/useDownload";

const ITEMS_PER_PAGE = 10;

const columns = [
  { key: "seq", label: "ID" }, // sequential index
  { key: "full_name", label: "Full Name" },
  { key: "regno", label: "Reg No" },
  { key: "programme_name", label: "Programme" },
  { key: "year_of_study", label: "YoS" },
  { key: "attendance_rate", label: "Attendance Rate" },
];

export default function MyStudentsPage({ data, loading, error }) {
  const [selectedCourseId, setSelectedCourseId] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    // Auto-select first course if available
    if (data?.data?.length && selectedCourseId === null) {
      setSelectedCourseId(data.data[0].course.course_id);
    }
  }, [data, selectedCourseId]);

  if (loading) return <Spinner />;
  if (error) return <p>Error loading data: {error.message}</p>;
  if (!data?.data?.length) return <p>No data found.</p>;

  // Find the selected course object
  const selectedCourse = data.data.find(
    (item) => item.course.course_id === selectedCourseId
  );

  // Safely compute studentsWithAttendance
  const studentsWithAttendance = (selectedCourse?.students || []).map(
    (student) => {
      const attendance = student.attendance || [];
      const total = attendance.length;
      const present = attendance.filter(
        (a) => a.status === "present" || a.status === "late"
      ).length;

      const attendance_rate =
        total > 0 ? `${((present / total) * 100).toFixed(1)}%` : "N/A";

      return {
        ...student,
        attendance_rate,
      };
    }
  );
  const filteredStudents = studentsWithAttendance.filter((student) => {
    const query = searchQuery.toLowerCase();
    return (
      student.full_name.toLowerCase().includes(query) ||
      student.regno.toLowerCase().includes(query)
    );
  });

  // Pagination
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const paginatedData = filteredStudents.slice(
    startIndex,
    startIndex + ITEMS_PER_PAGE
  );
  const totalPages = Math.ceil(studentsWithAttendance.length / ITEMS_PER_PAGE);

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        {/* Course Select Dropdown */}
        <div>
          <label htmlFor="course-select" className="mr-2 font-medium">
            Select Course:
          </label>
          <select
            id="course-select"
            value={selectedCourseId || ""}
            onChange={(e) => {
              setSelectedCourseId(Number(e.target.value));
              setCurrentPage(1); // Reset pagination on change
            }}
            className="border border-gray-300 rounded px-2 py-1"
          >
            {data.data.map(({ course }) => (
              <option key={course.course_id} value={course.course_id}>
                {course.title} ({course.course_code})
              </option>
            ))}
          </select>
        </div>

        <div className="relative w-64">
          <Input
            placeholder="Search by name or reg no"
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value);
              setCurrentPage(1); // Reset to first page when searching
            }}
            className="w-64 rounded-full border-gray-800 pl-10"
          />

          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
        </div>

        {/* CSV Download */}
        <Button
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          onClick={() => handleDownloadCSV(filteredStudents, columns)}
          disabled={!studentsWithAttendance.length}
        >
          Download CSV
        </Button>
      </div>

      {/* Table */}
      <table className="min-w-full table-auto border text-sm">
        <thead className="bg-gray-100">
          <tr>
            {columns.map((col) => (
              <th key={col.key} className="p-2 border text-left">
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {paginatedData.map((row, index) => {
            const sequentialId = startIndex + index + 1;
            return (
              <tr key={sequentialId} className="text-center">
                {columns.map(({ key }) => (
                  <td key={key} className="p-2 border">
                    {key === "seq" ? sequentialId : row[key] || "-"}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>

      {/* Pagination Controls */}
      <div className="flex justify-between items-center mt-4">
        <Button
          onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
          disabled={currentPage === 1}
        >
          Prev
        </Button>
        <span>
          Page {currentPage} of {totalPages || 1}
        </span>
        <Button
          onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
          disabled={currentPage === totalPages}
        >
          Next
        </Button>
      </div>
    </div>
  );
}
