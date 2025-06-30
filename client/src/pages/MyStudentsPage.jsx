import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import useFetch from "@/hooks/useFetch.js";
import Spinner from "@/components/ui/spinner";

const ITEMS_PER_PAGE = 10;

const columns = [
  { key: "id", label: "ID" },
  { key: "full_name", label: "Full Name" },
  { key: "regno", label: "Reg No" },
  { key: "programme_name", label: "Programme" },
  { key: "year_of_study", label: "YoS" },
  { key: "attendance_rate", label: "Attendance Rate" },
];

export default function MyStudentsPage() {
  const { data, error, loading } = useFetch(
    "http://localhost:8002/api/v1/courses"
  );
  const [currentPage, setCurrentPage] = useState(1);

  if (loading) return <Spinner />;
  if (error) return <p>Error loading data: {error.message}</p>;
  if (!data) return <p>No data found.</p>;

  // Calculate attendance rate from student.attendance array
  const studentsWithAttendance = (data.data.students || []).map((student) => {
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
  });

  // Pagination
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const paginatedData = studentsWithAttendance.slice(
    startIndex,
    startIndex + ITEMS_PER_PAGE
  );
  const totalPages = Math.ceil(studentsWithAttendance.length / ITEMS_PER_PAGE);

  return (
    <div>
      <div className="flex justify-end mb-2">
        <Button
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          onClick={() => handleDownloadCSV(data, columns)}
        >
          Download CSV
        </Button>
      </div>
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
          {paginatedData.map((row) => (
            <tr key={row.id} className="text-center">
              {columns.map(({ key }) => (
                <td key={key} className="p-2 border">
                  {row[key] || "-"}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      <div className="flex justify-between items-center mt-4">
        <Button
          onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
          disabled={currentPage === 1}
        >
          Prev
        </Button>
        <span>
          Page {currentPage} of {totalPages}
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
