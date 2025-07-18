import { createContext, useContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(undefined); // { name: "Dr.Daudi", role: "instructor" }
  const [selectedRole, setSelectedRole] = useState(null);
  useEffect(() => {
    const stored = JSON.parse(localStorage.getItem("user"));
    const role = localStorage.getItem("selectedRole");
    if (stored) {
      setUser(stored);
    } else {
      setUser(null);
    }
    if (role) setSelectedRole(role);
  }, []);

  useEffect(() => {
    if (selectedRole) {
      localStorage.setItem("selectedRole", selectedRole);
    }
  }, [selectedRole]);

  const login = (token) => {
    const decoded = jwtDecode(token);
    const userInfo = {
      id: decoded.sub,
      email: decoded.email,
      name: decoded.name,
    };

    setUser(userInfo);
    localStorage.setItem("user", JSON.stringify(userInfo));
    localStorage.setItem("token", token);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("user");
    localStorage.removeItem("token");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        selectedRole,
        setSelectedRole,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
