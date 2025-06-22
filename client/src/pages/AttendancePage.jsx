import React, { useState } from "react";
import { Pencil, Save, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import useFetch from "@/hooks/useFetch.js";
import Spinner from "@/components/ui/spinner";

const ITEMS_PER_PAGE = 10;

// Column mapping: field → label
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
  const { data, loading, error } = useFetch(
    "http://localhost:8002/api/v1/attendance"
  );
  const [currentPage, setCurrentPage] = useState(1);
  const [editingRow, setEditingRow] = useState(null);
  const [formState, setFormState] = useState({});

  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const paginatedData = data?.records?.slice(startIndex, startIndex + ITEMS_PER_PAGE) || [];
  const totalPages = Math.ceil((data?.records?.length || 0) / ITEMS_PER_PAGE);

  const handleEdit = (row) => {
    setEditingRow(row.id);
    setFormState(row);
  };

  const handleCancel = () => {
    setEditingRow(null);
    setFormState({});
  };

  const handleSave = () => {
    // This assumes you eventually add an API update call
    setEditingRow(null);
    setFormState({});
  };

  const handleChange = (e, field) => {
    setFormState({ ...formState, [field]: e.target.value });
  };

  console.log(data)
  if (loading) return <Spinner/>;
  if (error) return <p>Error loading data: {error.message}</p>;
  if (!data) return <p>No data found.</p>;

  return (
    
      <div>
        <table className="min-w-full table-auto border text-sm">
          <thead className="bg-gray-100">
            <tr>
              {columns.map((col) => (
                <th key={col.key} className="p-2 border">
                  {col.label}
                </th>
              ))}
              <th className="p-2 border">Actions</th>
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((row) => (
              <tr key={row.id} className="text-center">
                {columns.map(({ key }) => (
                  <td key={key} className="p-2 border">
                    {editingRow === row.id && key !== "id" ? (
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
                <td className="p-2 border flex justify-center gap-2">
                  {editingRow === row.id ? (
                    <>
                      <Button onClick={handleSave} size="icon">
                        <Save size={16} />
                      </Button>
                      <Button onClick={handleCancel} variant="destructive" size="icon">
                        <X size={16} />
                      </Button>
                    </>
                  ) : (
                    <Button onClick={() => handleEdit(row)} size="icon">
                      <Pencil size={16} />
                    </Button>
                  )}
                </td>
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
