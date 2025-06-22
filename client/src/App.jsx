import "./App.css";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { useAuth } from "./auth/AuthContext";
import DashboardRouter from "./routers/DashboardRouter";
import ProfileRouter from "./routers/ProfileRouter";
import NotificationsRouter from "./routers/NotificationsRouter";
import LoginPage from "./pages/LoginPage";
import RegisterPageInstructor from "./pages/RegisterPageInstructor";
import MainPage from "./pages/MainPage";
import RegisterPageStudent from "./pages/RegisterPageStudent";
import LandingPage from "./pages/LandingPage";
import NotFoundPage from "./components/ui/NotFound";
import Spinner from "./components/ui/spinner";

const ProtectedRoute = ({ children }) => {
  const { user } = useAuth();

  if (user === undefined) return <Spinner />;

  return user ? children : <Navigate to="/login" replace />;
};

function App() {
  const { user } = useAuth();

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={user ? <Navigate to="/main/dashboard" /> : <LandingPage />}
        />
        <Route
          path="/main/*"
          element={
            <ProtectedRoute>
              <MainPage />
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register/student" element={<RegisterPageStudent />} />
        <Route path="/register/instructor" element={<RegisterPageInstructor />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
}

export default App;
