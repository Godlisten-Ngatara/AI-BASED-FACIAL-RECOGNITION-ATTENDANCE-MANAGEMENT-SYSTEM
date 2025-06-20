// DashboardRouter.jsx
import StudentDashboardPage from "@/pages/StudentDashboardPage";
import { useAuth } from "../auth/AuthContext";
import TeacherDashboardPage from "@/pages/TeacherDashboardPage";

const DashboardRouter = () => {
  const { user } = useAuth();

  if (!user) return null;

  if (user.role === "student") {
    return <StudentDashboardPage />;
  } else if (user.role === "instructor") {
    return <TeacherDashboardPage />;
  } else {
    return <div>Unauthorized</div>;
  }
};

export default DashboardRouter;
