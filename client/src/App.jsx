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
import { AuthProvider } from "./auth/AuthContext";
import LoginPage from "./pages/LoginPage";
import RegisterPageInstructor from "./pages/RegisterPageInstructor";
import MainPage from "./pages/MainPage";
import RegisterPageStudent from "./pages/RegisterPageStudent";
import LandingPage from "./pages/LandingPage";

const ProtectedRoute = ({ children }) => {
  const { user } = useAuth();
  return user ? children : <Navigate to="/" />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register/student" element={<RegisterPageStudent />} />
          <Route path="/register/instructor" element={<RegisterPageInstructor />} />

          <Route
            path="/main/*"
            element={
              <ProtectedRoute>
                <MainPage />
              </ProtectedRoute>
            }
          />

          {/* Redirect logged-in users to main page by default */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Navigate to="/main/dashboard" />
              </ProtectedRoute>
            }
          />

          {/* Fallback route for non-logged in users */}
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
