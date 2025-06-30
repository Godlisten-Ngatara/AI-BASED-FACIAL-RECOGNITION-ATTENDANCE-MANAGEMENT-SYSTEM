const handleDownloadCSV = (data, columns) => {
  if (!Array.isArray(data) || data.length === 0) return;

  const csvRows = [];

  // Add CSV headers
  csvRows.push(columns.map(col => `"${col.label}"`).join(","));

  // Add each row
  data.forEach(row => {
    const values = columns.map(col => `"${row[col.key] ?? ""}"`);
    csvRows.push(values.join(","));
  });

  const csvContent = csvRows.join("\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", "attendance_records.csv");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
export default handleDownloadCSV