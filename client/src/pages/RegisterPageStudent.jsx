
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Card, CardContent } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import register_pict from '../assets/register.png'
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/auth/AuthContext";

export default function RegisterPageStudent() {

    const navigate = useNavigate();
   const { setSelectedRole ,selectedRole} = useAuth();

  
  const handleRegister = (role) => {
    // Store only the role (you can extend this later)
    // login({ role });
    setSelectedRole(role)
    navigate("/login");
  };
  return (
    <div className="min-h-screen flex bg-blue-50">
      {/* Left Image Section */}
      <div className="w-1/2 hidden md:flex items-center justify-center">
        <img
          src={register_pict} // Put your image in /public
          alt="Register Illustration"
          className="w-[400px]  object-contain"
        />
      </div>

      {/* Right Form Section */}
      <div className="w-full md:w-1/2 flex items-center justify-center p-8">
        <Card className="w-full max-w-2xl p-6 shadow-2xl rounded-xl border border-gray-200 bg-blue-50">
          <CardContent className="space-y-6">
            <div className="text-center">
              <h1 className="text-2xl font-bold text-blue-900">Sign Up</h1>
            </div>

            <form className="grid grid-cols-1 md:grid-cols-2 gap-4 text-gray-700">
              <div>
                <Label className='mb-2 '>First Name</Label>
                <Input placeholder="First Name" className='bg-white py-6' />
              </div>
              <div>
                <Label className='mb-2 '>Second Name</Label>
                <Input placeholder="Second Name" className='bg-white py-6' />
              </div>
              <div>
                <Label className='mb-2'>Surname</Label>
                <Input placeholder="Surname" className='bg-white py-6'/>
              </div>
               <div>
                <Label className='mb-2'>Date of Birth</Label>
                <Input type="date" placeholder='Date of Birth' className='bg-white py-6'/>
              </div>
                <div>
                <Label className='mb-2'>Registration Number</Label>
                <Input type='text' placeholder="Registration Number" className='bg-white py-6' />
              </div>
              <div>
                <Label className='mb-2'>Degree Programme</Label>
                <Input type='text' placeholder="Degree Programme" className='bg-white py-6'/>
              </div>

                <div>
                <Label className='mb-2'>Email</Label>
                <Input type="email" placeholder="Email" className='bg-white py-6' />
              </div>

              <div>
                <Label className='mb-2'>Phone Number</Label>
                <Input placeholder="Phone Number" className='bg-white py-6' />
              </div>
              
              <div>
                <Label className='mb-2'>Enter Password</Label>
                <Input type="password" placeholder="Password" className='bg-white py-6' />
              </div>
              <div>
                <Label className='mb-2'>Re-enter Password</Label>
                <Input type="password" placeholder="Confirm Password"className='bg-white py-6' />
              </div>

              <div className="col-span-1 md:col-span-2 flex items-center  justify-center gap-2">
                <Checkbox id="terms" />
                <Label htmlFor="terms" className="text-sm">
                  Agree to Terms and Conditions
                </Label>
              </div>

              <div className="col-span-1 md:col-span-2 flex justify-center">
                <Button onClick={() => handleRegister("student")}
                   className="bg-blue-600 hover:bg-blue-700 text-white px-30 py-5 rounded ">
                  Sign Up
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
