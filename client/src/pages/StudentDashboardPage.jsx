import { Card, CardContent } from "@/components/ui/card";
import teaching_image from "../assets/teaching.jpg";
import classes_icon from "../assets/icons/classes.png";
import graph1_icon from "../assets/icons/graph_1.png";
import useFetch from "@/hooks/useFetch";

export default function StudentDashboardPage() {
  const { data, loading } = useFetch(
    "http://localhost:8002/api/v1/attendance/student"
  );

  const courses = data?.courses ?? [];

  return (
    <div className="flex flex-col gap-6 p-6 w-full">
      {/* Welcome Banner */}
      <div className="bg-blue-900 text-white p-4 rounded-2xl text-xl font-semibold flex justify-between items-center">
        <span>Hello Godlisten 👋</span>
        <span>Welcome to AI-FRAMS</span>
      </div>

      {/* Courses + Lectures and Tutorials */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* My Courses (spans 2 columns) */}
        <div className="relative md:col-span-2 rounded-2xl overflow-hidden">
          {/* Background image */}
          <div
            className="absolute inset-0 bg-cover bg-center"
            style={{ backgroundImage: `url(${teaching_image})` }}
          ></div>

          {/* Overlay */}
          <div className="absolute inset-0 bg-black/50"></div>

          {/* Foreground content */}
          <div className="relative z-10 p-4 text-white">
            <h3 className="text-lg font-semibold mb-3">My Courses</h3>
            <div className="grid grid-cols-2 gap-4">
              {courses.map((course) => (
                <Card
                  key={course.id}
                  className="bg-[#002366] text-white rounded-xl border-[#002366]"
                >
                  <CardContent>
                    <div className="text-xl font-bold">
                      {course.course_code}
                    </div>
                    <div className="text-sm font-semibold">{course.title}</div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>

        {/* Lectures and Tutorials */}
        <div className="flex flex-col gap-4">
          <Card className="bg-blue-500 text-white rounded-xl">
            <CardContent>
              <div className="text-xl font-bold mb-2">
                Total Number of Lectures
              </div>
              <div className="flex items-center justify-between">
                <div className="text-5xl font-extrabold">8</div>
                <img src={classes_icon} alt="classes" className="w-8 h-8" />
              </div>
            </CardContent>
          </Card>
          <Card className="bg-blue-500 text-white rounded-xl">
            <CardContent>
              <div className="text-xl font-bold mb-2">
                Total Number of Tutorials
              </div>
              <div className="flex items-center justify-between">
                <div className="text-5xl font-extrabold">4</div>
                <img src={classes_icon} alt="classes" className="w-8 h-8" />
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Average Attendance */}
      <div>
        <h3 className="text-4xl font-semibold text-blue-900 mb-4">
          Average Attendance
        </h3>
        <div className="grid grid-cols-4 gap-6">
          {[
            {
              day: " TE412",
              percent: "61%",
              color: "bg-blue-900",
              icon: graph1_icon,
            },
            {
              day: "CS432",
              percent: "57%",
              color: "bg-blue-900",
              icon: graph1_icon,
            }, // We'll simulate this
            {
              day: "CS411",
              percent: "77%",
              color: "bg-blue-900",
              icon: graph1_icon,
            },
            {
              day: "CS444",
              percent: "67%",
              color: "bg-blue-900",
              icon: graph1_icon,
            },
          ].map((item, index) => (
            <Card
              key={index}
              className={`${item.color} text-white bg-blue-500`}
            >
              <CardContent>
                <div className="flex items-center justify-between w-full">
                  {/* Left side: Day */}
                  <p className="text-2xl">{item.day}</p>

                  {/* Right side: Icon + Percent */}
                  <div className="flex flex-col items-center">
                    <img src={item.icon} alt="icon" className="w-8 h-8 mb-1" />
                    <h2 className="text-3xl font-bold">{item.percent}</h2>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
