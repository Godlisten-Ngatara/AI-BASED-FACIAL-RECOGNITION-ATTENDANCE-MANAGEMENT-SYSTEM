// src/pages/Login.tsx

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@radix-ui/react-label";
import { useAuth } from "@/auth/AuthContext";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import login_pict from "../assets/login_img.png";

export default function LoginPage() {
  const { selectedRole } = useAuth();

  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  // default role

  const [password, setPassword] = useState("");
  const storedRole = localStorage.getItem("selectedRole");

  const handleSubmit = (e) => {
    e.preventDefault();

    // if (!email || !password || !role) {
    //   setError("All fields are required.");
    //   return;
    // }

    const userData = {
      name: email.split("@")[0],
      email,
      storedRole,
    };

    // NOTE: You would normally verify password here (e.g. via API call)
    login(userData);
    navigate("/main/*");
  };

  const handleCreateAccount = () => {
    navigate(`/register/${selectedRole}`, { state: { selectedRole } });
  };
  return (
    <div className="h-screen flex  bg-blue-50">
      {/* Left Image Section */}
      <div className="w-1/2 hidden md:flex items-center justify-center h-full">
        <img
          src={login_pict} // Place your image in public folder
          alt="AI-FRAMS Illustration"
          className="w-full h-full object-cover"
        />
      </div>

      {/* Right Form Section */}
      <div className="w-full md:w-1/2 flex items-center justify-center p-8 ">
        <Card className="w-full max-w-md shadow-2xl bg-blue-50 border border-blue-100">
          <CardContent className="space-y-6 p-6">
            <div className="text-center">
              <h1 className="text-2xl font-bold text-blue-900">Login</h1>
              {/* <p className="text-sm text-gray-500">Login to Your Account</p> */}
            </div>

            <form className="space-y-4" onSubmit={handleSubmit}>
              <div>
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="bg-white py-6"
                />
              </div>

              <div>
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="bg-white py-6"
                />
              </div>

              <Button
                type="submit"
                className="w-full bg-blue-600 hover:bg-blue-700 py-5"
              >
                Login
              </Button>

              {/* <div className="text-center">
                <div className="mb-1">
                  <a href="#" className="text-m  hover:underline">
                    Forgot Password?{" "}
                    <span className="text-blue-600"> Reset Here</span>
                  </a>
                </div>

                <div>
                  <span>Dont Have an Account? </span>
                  <a
                    onClick={handleCreateAccount}
                    className="text-m  hover:underline"
                  >
                    <span className="text-blue-600"> Create Here</span>
                  </a>
                </div>
              </div> */}
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
