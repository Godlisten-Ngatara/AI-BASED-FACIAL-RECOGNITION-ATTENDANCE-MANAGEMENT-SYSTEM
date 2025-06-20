// components/ProfilePage.tsx
import React from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Pencil } from "lucide-react";
import user_icon from "../assets/icons/user.png";
const StudentProfilePage = () => {
  return (
    <div className="flex flex-col gap-6 p-6 w-full ">
      {/* Top Header */}

      {/* Profile Name Section */}
      <div className="flex items-center gap-4 mb-0">
        <img src={user_icon} alt="Profile" className="w-16 h-16 rounded-full" />
        <h3 className="text-lg font-medium text-blue-900">Godlisten</h3>
      </div>

      {/* Form */}
      <form onSubmit={(e) => e.preventDefault()}>
        <Card className="bg-[#e9f8fe] shadow-[0_20px_50px_rgba(0,0,0,0.5)] rounded-2xl">
          <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4 p-6">
           {[
  ["First Name", "firstName"],
  ["Surname", "surname"],
  ["Email", "email"],
  ["Phone Number", "phoneNumber"],
  ["Date of Birth", "dob"],
  ["Degree Programme", "degreeProgramme"],
  ["Registration Number", "regNumber"],
  ["Department", "department"],
].map(([label, name]) => (
  <div key={name} className="flex flex-col gap-1">
    <label htmlFor={name} className="text-sm text-gray-700">
      {label}
    </label>
    <div className="relative">
      <Input
        id={name}
        name={name}
        placeholder={label}
        type={name=='dob'?'date':'text'}
        className="pr-10 p-5 bg-[#e9f8fe] focus:bg-white border-gray-300" // extra padding on the right for the icon space
      />
      <div className="absolute right-3 top-[-13px] transform -translate-y-1/2 cursor-pointer">
        <Pencil className="w-4 h-4 text-gray-500" />
      </div>
    </div>
  </div>
))}


          </CardContent>
        </Card>

        {/* Save Button */}
        <div className="w-full flex justify-center mt-8">
          <Button
            type="submit"
            className="bg-blue-900 hover:bg-blue-700 text-white text-lg px-10 py-6 rounded-xl w-full cursor-pointer"
          >
            Save Changes
          </Button>
        </div>
      </form>
    </div>
  );
};

export default StudentProfilePage;
