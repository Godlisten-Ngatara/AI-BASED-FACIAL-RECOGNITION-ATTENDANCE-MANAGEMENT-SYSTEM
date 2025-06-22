import useFetch from "@/hooks/useFetch";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { useMemo } from "react";

export default function AttendanceTrendChart() {
  const { data } = useFetch("http://localhost:8002/api/v1/attendance");

  // Prepare chart data
  const chart_data = useMemo(() => {
    if (!data?.records) return [];

    const grouped = {};

    data.records.forEach((record) => {
      const date = record.recorded_date;
      if (!grouped[date]) {
        grouped[date] = { present: 0, total: 0 };
      }

      grouped[date].total += 1;
      if (record.status === "present") {
        grouped[date].present += 1;
      }
    });

    // Convert and sort by date descending
    const sorted = Object.entries(grouped)
      .map(([date, { present, total }]) => ({
        date,
        attendance: Math.round((present / total) * 100),
      }))
      .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()) // newest first
      .slice(0, 5) // take latest 5
      .reverse(); // optional: show oldest to newest left to right

    return sorted;
  }, [data]);

  return (
    <div className="w-full h-96">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={
            chart_data.length > 0
              ? chart_data
              : [{ date: "N/A", attendance: 0 }]
          }
          margin={{ top: 20, right: 30, left: 0, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis domain={[0, 100]} tickFormatter={(tick) => `${tick}%`} />
          <Tooltip formatter={(value) => `${value}%`} />
          <Line
            type="monotone"
            dataKey="attendance"
            stroke="#8884d8"
            strokeWidth={2}
            dot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
