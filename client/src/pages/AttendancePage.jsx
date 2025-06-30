import React, { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import { Pencil, Save, X, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import useFetch from "@/hooks/useFetch.js";
import Spinner from "@/components/ui/spinner";
import handleDownloadCSV from "@/hooks/useDownload";

const ITEMS_PER_PAGE = 10;

const columns = [
  { key: "id", label: "ID" },
  { key: "regno", label: "Reg No" },
  { key: "full_name", label: "Full Name" },
  { key: "programme_name", label: "Programme" },
  { key: "title", label: "Course" },
  { key: "year_of_study", label: "YoS" },
  { key: "recorded_date", label: "Recorded At" },
  { key: "status", label: "Attendance Status" },
];

export default function AttendanceTable() {
  const storedRole = localStorage.getItem("selectedRole");

  const endpoint =
    storedRole === "instructor"
      ? "http://localhost:8002/api/v1/attendance/instructor"
      : "http://localhost:8002/api/v1/attendance/student";

  const { data, error, loading } = useFetch(endpoint);
  const [currentPage, setCurrentPage] = useState(1);
  const [editingRow, setEditingRow] = useState(null);
  const [formState, setFormState] = useState({});
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  // Filter records based on date range
  const filteredData =
    data?.records?.filter((rec) => {
      const recordDate = new Date(rec.recorded_date);
      return (
        (!startDate || recordDate >= startDate) &&
        (!endDate || recordDate <= endDate)
      );
    }) || [];

  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const paginatedData = filteredData.slice(
    startIndex,
    startIndex + ITEMS_PER_PAGE
  );
  const totalPages = Math.ceil(filteredData.length / ITEMS_PER_PAGE);

  const handleEdit = (row) => {
    setEditingRow(row.id);
    setFormState(row);
  };

  const handleCancel = () => {
    setEditingRow(null);
    setFormState({});
  };

  const handleSave = () => {
    setEditingRow(null);
    setFormState({});
  };

  const handleChange = (e, field) => {
    setFormState({ ...formState, [field]: e.target.value });
  };

  useEffect(() => {
    if (data?.records?.length) {
      const dates = data.records
        .map((rec) => new Date(rec.recorded_date))
        .filter((d) => !isNaN(d));

      if (dates.length > 0) {
        const minDate = new Date(Math.min(...dates));
        const maxDate = new Date(Math.max(...dates));
        setStartDate(minDate);
        setEndDate(maxDate);
      }
    }
  }, [data]);

  if (loading) return <Spinner />;
  if (error) return <p>Error loading data: {error.message}</p>;
  if (!data) return <p>No data found.</p>;

  return (
    <div>
      <div className="mb-2">Filter by date:</div>
      <div className="w-full flex justify-between items-center gap-4 mb-2">
        <div className="flex gap-x-2">
          <DatePicker
            id="start-date"
            selected={startDate}
            onChange={(date) => {
              setStartDate(date);
              setCurrentPage(1);
            }}
            selectsStart
            startDate={startDate}
            endDate={endDate}
            maxDate={endDate}
            className="border rounded px-3 py-2 border-gray-800"
          />
          <DatePicker
            selected={endDate}
            onChange={(date) => {
              setEndDate(date);
              setCurrentPage(1);
            }}
            selectsEnd
            startDate={startDate}
            endDate={endDate}
            minDate={startDate}
            className="border rounded px-3 py-2 border-gray-800"
          />
        </div>

        {storedRole === "instructor" && (
          <div className="relative w-64">
            <Input
              placeholder="Search Here"
              className="w-64 rounded-full border-gray-800 pl-10"
            />
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          </div>
        )}

        <div>
          <Button
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
            onClick={() => handleDownloadCSV(filteredData, columns)}
          >
            Download CSV
          </Button>
        </div>
      </div>

      <table className="min-w-full table-auto border text-sm">
        <thead className="bg-gray-100">
          <tr>
            {columns.map((col) => (
              <th key={col.key} className="p-2 border">
                {col.label}
              </th>
            ))}
            {storedRole === "instructor" && (
              <th className="p-2 border">Actions</th>
            )}
          </tr>
        </thead>
        <tbody>
          {paginatedData.map((row) => (
            <tr key={row.id} className="text-center">
              {columns.map(({ key }) => (
                <td key={key} className="p-2 border">
                  {editingRow === row.id &&
                  storedRole === "instructor" &&
                  key !== "id" ? (
                    <input
                      type="text"
                      value={formState[key] || ""}
                      onChange={(e) => handleChange(e, key)}
                      className="w-full border rounded p-1"
                    />
                  ) : (
                    row[key]
                  )}
                </td>
              ))}
              {storedRole === "instructor" && (
                <td className="p-2 border flex justify-center gap-2">
                  {editingRow === row.id ? (
                    <>
                      <Button onClick={handleSave} size="icon">
                        <Save size={16} />
                      </Button>
                      <Button
                        onClick={handleCancel}
                        variant="destructive"
                        size="icon"
                      >
                        <X size={16} />
                      </Button>
                    </>
                  ) : (
                    <Button onClick={() => handleEdit(row)} size="icon">
                      <Pencil size={16} />
                    </Button>
                  )}
                </td>
              )}
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
