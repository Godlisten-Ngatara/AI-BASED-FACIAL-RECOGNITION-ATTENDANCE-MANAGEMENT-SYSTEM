import React, { useState, useMemo } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { addDays, subDays, format, isAfter, isBefore, parseISO } from "date-fns";

const mockImages = [
  {
    id: 1,
    url: "https://placekitten.com/400/300",
    timestamp: "2025-06-18T10:15:00Z",
  },
  {
    id: 2,
    url: "https://placekitten.com/401/300",
    timestamp: "2025-06-19T14:30:00Z",
  },
  {
    id: 3,
    url: "https://placekitten.com/402/300",
    timestamp: "2025-06-20T09:45:00Z",
  },
  {
    id: 4,
    url: "https://res.cloudinary.com/dpfswdpgr/image/upload/v1750437751/captured_images/capture_20250620_194230.jpg",
    timestamp: "2025-06-20T20:00:00Z",
  },
  // add more as needed
];

export default function CapturedImagesGallery() {
  // Default date range: last 7 days
  const [startDate, setStartDate] = useState(subDays(new Date(), 7));
  const [endDate, setEndDate] = useState(new Date());

  // Filter images within the selected date range
  const filteredImages = useMemo(() => {
    return mockImages.filter(({ timestamp }) => {
      const time = parseISO(timestamp);
      return (
        (isAfter(time, startDate) || format(time, "yyyy-MM-dd") === format(startDate, "yyyy-MM-dd")) &&
        (isBefore(time, endDate) || format(time, "yyyy-MM-dd") === format(endDate, "yyyy-MM-dd"))
      );
    });
  }, [startDate, endDate]);

  return (
    <div className="max-w-7xl mx-auto p-4">
      <h1 className="text-2xl font-semibold mb-6 text-center">Captured Images</h1>

      <div className="flex justify-center space-x-4 mb-8">
        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="start-date">
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

      {filteredImages.length === 0 ? (
        <p className="text-center text-gray-500">No images found for the selected date range.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {filteredImages.map(({ id, url, timestamp }) => (
            <div
              key={id}
              className="border rounded overflow-hidden shadow hover:shadow-lg transition-shadow duration-300"
            >
              <img
                src={url}
                alt={`Captured at ${format(parseISO(timestamp), "PPpp")}`}
                className="w-full h-48 object-cover"
                loading="lazy"
              />
              <div className="p-2 bg-gray-50 text-center text-sm text-gray-700 font-mono">
                {format(parseISO(timestamp), "PPP p")}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
