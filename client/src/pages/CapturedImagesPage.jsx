import React, { useState, useMemo } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { subDays, format, isAfter, isBefore, parseISO } from "date-fns";
import useFetch from "@/hooks/useFetch";
import Spinner from "@/components/ui/spinner";

export default function CapturedImagesGallery() {
  const { data, error, loading } = useFetch(
    "http://localhost:8002/api/v1/attendance/instructor"
  );
  const [startDate, setStartDate] = useState(subDays(new Date(), 7));
  const [endDate, setEndDate] = useState(new Date());
  const [selectedCourse, setSelectedCourse] = useState("All");

  const records = data?.records || [];

  const courseOptions = useMemo(() => {
    const titles = records.map((r) => r.title).filter(Boolean);
    return ["All", ...Array.from(new Set(titles))];
  }, [records]);

  const filteredImages = useMemo(() => {
    return records.filter(
      ({ recorded_date, recorded_time, captured_image, title }) => {
        if (!recorded_date || !recorded_time || !captured_image) return false;

        const time = parseISO(recorded_date);
        const dateInRange =
          (isAfter(time, startDate) ||
            format(time, "yyyy-MM-dd") === format(startDate, "yyyy-MM-dd")) &&
          (isBefore(time, endDate) ||
            format(time, "yyyy-MM-dd") === format(endDate, "yyyy-MM-dd"));

        const courseMatches =
          selectedCourse === "All" || title === selectedCourse;

        return dateInRange && courseMatches;
      }
    );
  }, [startDate, endDate, records, selectedCourse]);

  if (loading) return <Spinner />;
  if (error)
    return <p className="text-red-500 text-center">Error loading data</p>;

  return (
    <div className="max-w-7xl mx-auto p-4">
      <h1 className="text-2xl font-semibold mb-6 text-center">
        Captured Images
      </h1>

      <div className="flex justify-center space-x-4 mb-8">
        <div>
          <label
            className="block text-sm font-medium mb-1"
            htmlFor="start-date"
          >
            Start Date
          </label>
          <DatePicker
            id="start-date"
            selected={startDate}
            onChange={(date) => setStartDate(date)}
            selectsStart
            startDate={startDate}
            endDate={endDate}
            maxDate={endDate}
            className="border rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-400"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="end-date">
            End Date
          </label>
          <DatePicker
            id="end-date"
            selected={endDate}
            onChange={(date) => setEndDate(date)}
            selectsEnd
            startDate={startDate}
            endDate={endDate}
            minDate={startDate}
            maxDate={new Date()}
            className="border rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-400"
          />
        </div>
      </div>
      <div className="mb-2">
        <label
          className="block text-sm font-medium mb-1"
          htmlFor="course-filter"
        >
          Course
        </label>
        <select
          id="course-filter"
          value={selectedCourse}
          onChange={(e) => setSelectedCourse(e.target.value)}
          className="border rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-400"
        >
          {courseOptions.map((title) => (
            <option key={title} value={title}>
              {title}
            </option>
          ))}
        </select>
      </div>

      {filteredImages.length === 0 ? (
        <p className="text-center text-gray-500">
          No images found for the selected date range.
        </p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {filteredImages.map((record) => (
            <div
              key={record.id}
              className="border rounded overflow-hidden shadow hover:shadow-lg transition-shadow duration-300"
            >
              <img
                src={record.captured_image}
                alt={`Captured for ${record.full_name}`}
                className="w-full h-48 object-cover"
                loading="lazy"
              />
              <div className="p-2 bg-gray-50 text-center text-sm text-gray-700">
                <div className="text-xs">{record.title}</div>
                <div className="text-xs text-gray-500">
                  {record.recorded_date && record.recorded_time
                    ? format(
                        parseISO(
                          `${record.recorded_date}T${record.recorded_time}`
                        ),
                        "PPP p"
                      )
                    : "Invalid date"}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
