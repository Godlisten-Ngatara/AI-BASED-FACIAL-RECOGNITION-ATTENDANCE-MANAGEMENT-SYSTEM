import { useAuth } from "../auth/AuthContext";
import StudentNotificationPage from "@/pages/StudentNotificationPage";
import TeacherNotificationPage from "@/pages/TeacherNotificationPage";

const NotificationsRouter = () => {
  const { user } = useAuth();
  if (!user) return null;
  return user.role === "student" ? <StudentNotificationPage /> : <TeacherNotificationPage />;
};

export default NotificationsRouter;
