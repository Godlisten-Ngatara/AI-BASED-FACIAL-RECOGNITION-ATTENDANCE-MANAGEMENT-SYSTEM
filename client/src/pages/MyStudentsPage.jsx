import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

export default function MyStudentsPage() {
  const students = Array(10).fill({
    name: "Godlisten Ngatara",
    regNumber: "2021-04-0889",
    programme: "Bsc.CEIT",
    year: 4,
  });

  return (
    <div className="w-full bg-blue-50 min-h-screen p-6">
   

      <Card className="overflow-x-auto  p-0 rounded-none shadow-none border-none">
        <table className="min-w-full divide-y divide-gray-300">
          <thead className="bg-blue-800 text-white">
            <tr>
              <th className="text-left px-6 py-3 text-m font-semibold">Student Name</th>
              <th className="text-left px-6 py-3 text-m font-semibold">Reg.Number</th>
              <th className="text-center px-6 py-3 text-m font-semibold">Programme</th>
              <th className="text-center px-6 py-3 text-m font-semibold">Year of Study</th>
            </tr>
          </thead>
          <tbody className="bg-blue-50 text-blue-900 divide-y divide-blue-200">
            {students.map((student, index) => (
              <tr key={index}>
                <td className="px-6 py-4 text-sm">{student.name}</td>
                <td className="px-6 py-4 text-sm">{student.regNumber}</td>
                <td className="px-6 py-4 text-sm text-center">{student.programme}</td>
                <td className="px-6 py-4 text-sm text-center">{student.year}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>

    </div>
  )
}
