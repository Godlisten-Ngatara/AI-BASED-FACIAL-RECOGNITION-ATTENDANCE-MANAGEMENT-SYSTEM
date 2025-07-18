
export default function Sidebar() {
  return (
    <aside className="h-screen w-64 bg-white border-r flex flex-col items-center py-6 shadow">
      {/* Logo */}
      <div className="mb-4">
        <img src="/logo.png" alt="Company Logo" className="h-12 w-12" />
      </div>

      {/* Company Name */}
      <h1 className="text-lg font-bold text-blue-600 mb-8">AI-FRAMS</h1>

      {/* Navigation Menu */}
      <nav className="w-full px-4 space-y-3 text-sm">
        {["Dashboard", "My Profile", "My Classes", "Attendance", "Records", "Notifications", "Settings"].map((item) => (
          <a
            key={item}
            href="#"
            className="block px-3 py-2 rounded-md hover:bg-blue-100 hover:text-blue-700 transition"
          >
            {item}
          </a>
        ))}
      </nav>
    </aside>
  );
}
