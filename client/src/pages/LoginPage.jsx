// src/pages/Login.tsx

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/auth/AuthContext";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import login_pict from "../assets/login_img.png";
import usePost from "@/hooks/usePost";
import Spinner from "@/components/ui/spinner";

export default function LoginPage() {
  const { login, selectedRole } = useAuth();
  const navigate = useNavigate();
  const { postData, loading, error } = usePost();

  const [email, setEmail] = useState("");
  const [regno, setregno] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({
    identifier: "",
    password: "",
    general: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();

    const identifier = selectedRole === "instructor" ? email : regno;

    // Clear server error on new attempt
    setErrors((prev) => ({ ...prev, general: "" }));

    // Client-side validation
    const newErrors = {
      identifier:
        identifier.trim() === ""
          ? selectedRole === "instructor"
            ? "Email is required"
            : "Student ID is required"
          : "",
      password: password.trim() === "" ? "Password is required" : "",
      general: "",
    };

    setErrors(newErrors);

    if (newErrors.identifier || newErrors.password) return;

    const url =
      selectedRole === "instructor"
        ? "http://localhost:8002/api/v1/auth/instructor/login"
        : "http://localhost:8002/api/v1/auth/student/login";

    const payload =
      selectedRole === "instructor" ? { email, password } : { regno, password };

    const response = await postData(url, payload);

    if (response?.access_token) {
      login(response.access_token);
      setEmail("");
      setregno("");
      setPassword("");
      navigate("/main/dashboard");
    } else {
      setErrors((prev) => ({
        ...prev,
        general: error || "Invalid credentials. Please try again.",
      }));
    }
  };

  const identifierValue = selectedRole === "instructor" ? email : regno;
  const identifierLabel =
    selectedRole === "instructor" ? "Email Address" : "Student ID";
  const handleIdentifierChange = (e) =>
    selectedRole === "instructor"
      ? setEmail(e.target.value)
      : setregno(e.target.value);

  return (
    <div className="h-screen flex bg-blue-50">
      {loading && (
        <div className="absolute inset-0 bg-white/70 z-10 flex items-center justify-center rounded-md w-full">
          <Spinner />
        </div>
      )}
      {/* Left Image */}
      <div className="w-1/2 hidden md:flex items-center justify-center h-full">
        <img
          src={login_pict}
          alt="AI-FRAMS Illustration"
          className="w-full h-full object-cover"
        />
      </div>

      {/* Right Form */}
      <div className="w-full md:w-1/2 flex items-center justify-center p-8">
        <Card className="w-full max-w-md shadow-2xl bg-blue-50 border border-blue-100 relative">
          <CardContent className="space-y-6 p-6">
            <div className="text-center">
              <h1 className="text-2xl font-bold text-blue-900">Login</h1>
            </div>

            <form className="space-y-6" onSubmit={handleSubmit}>
              {/* Identifier Field */}
              <div className="relative">
                <Input
                  id="identifier"
                  type={selectedRole === "instructor" ? "email" : "text"}
                  value={identifierValue}
                  onChange={handleIdentifierChange}
                  placeholder=" "
                  className={`peer h-14 w-full rounded-md border ${
                    errors.identifier ? "border-red-500" : "border-gray-300"
                  } bg-white px-3 pt-4 pb-1 text-base placeholder-transparent focus:outline-none focus:ring-2 ${
                    errors.identifier
                      ? "focus:ring-red-500"
                      : "focus:ring-blue-500"
                  }`}
                />
                <label
                  htmlFor="identifier"
                  className={`absolute left-3 top-3 transition-all text-sm ${
                    errors.identifier ? "text-red-500" : "text-gray-500"
                  } peer-placeholder-shown:top-4 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-focus:top-2 peer-focus:text-sm peer-focus:${
                    errors.identifier ? "text-red-500" : "text-blue-500"
                  }`}
                >
                  {identifierLabel}
                </label>
                {errors.identifier && (
                  <p className="text-red-500 text-xs mt-1 ml-1">
                    {errors.identifier}
                  </p>
                )}
              </div>

              {/* Password Field */}
              <div className="relative">
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder=" "
                  className={`peer h-14 w-full rounded-md border ${
                    errors.password ? "border-red-500" : "border-gray-300"
                  } bg-white px-3 pt-4 pb-1 text-base placeholder-transparent focus:outline-none focus:ring-2 ${
                    errors.password
                      ? "focus:ring-red-500"
                      : "focus:ring-blue-500"
                  }`}
                />
                <label
                  htmlFor="password"
                  className={`absolute left-3 top-3 transition-all text-sm ${
                    errors.password ? "text-red-500" : "text-gray-500"
                  } peer-placeholder-shown:top-4 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-focus:top-2 peer-focus:text-sm peer-focus:${
                    errors.password ? "text-red-500" : "text-blue-500"
                  }`}
                >
                  Password
                </label>
                {errors.password && (
                  <p className="text-red-500 text-xs mt-1 ml-1">
                    {errors.password}
                  </p>
                )}
              </div>

              {/* Server Error */}
              {errors.general && (
                <div className="text-red-600 text-sm mb-2 text-center">
                  {errors.general}
                </div>
              )}

              {/* Submit */}
              <Button
                type="submit"
                className="w-full py-4 bg-blue-600 hover:bg-blue-700 transition-all duration-200 text-white text-lg font-semibold rounded-lg shadow-md"
              >
                Login
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
