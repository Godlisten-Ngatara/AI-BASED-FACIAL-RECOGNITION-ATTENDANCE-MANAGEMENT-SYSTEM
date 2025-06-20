import StudentProfilePage from "@/pages/StudentProfilePage";
import { useAuth } from "../auth/AuthContext";
import TeacherProfilePage from "@/pages/TeacherProfilePage";

const ProfileRouter = () => {
  const { user } = useAuth();
  if (!user) return null;
  return user.role === "student" ? <StudentProfilePage /> : <TeacherProfilePage />;
};

export default ProfileRouter;
