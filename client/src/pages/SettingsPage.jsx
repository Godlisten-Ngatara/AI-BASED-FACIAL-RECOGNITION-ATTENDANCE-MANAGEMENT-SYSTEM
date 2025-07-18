import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select"
import { Pencil } from "lucide-react"

export default function SettingsPage() {
  return (
    <div className="flex-1  p-8 min-h-screen mb-0">
    
      {/* Form Card */}
      <div 
      style={{ boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)' }}
      className="flex justify-around flex-wrap bg-white ml p-6 rounded-xl  gap-0">
        <div className="flex-1 min-w-[280px]">
          <Button className="bg-[#003e82] text-white text-lg mb-4 px-6 py-6 rounded-lg w-full">
            Change Password
          </Button>

          <div className="space-y-4 w-90">
            {[
              { label: "Email", placeholder: "Email" },
              { label: "New Password", placeholder: "New Password" },
              { label: "Confirm Password", placeholder: "Confirm Password" },
            ].map(({ label, placeholder }) => (
              <div key={label}>
                <Label className="flex justify-between items-center text-[#003e82]">
                  {label}
                  <span className="text-sm text-gray-500 flex items-center gap-1 cursor-pointer">
                    <Pencil className="w-3 h-3" /> Edit
                  </span>
                </Label>
                <Input placeholder={placeholder} className="bg-white border border-gray-300 p-5" />
              </div>
            ))}
          </div>
        </div>

        {/* Notification Settings */}
        <div className="flex-1 min-w-[220px] mt-12 ml-15 bg-[#003e82]  rounded-xl p-4 text-white flex flex-col justify-center h-45">
          <h3 className="text-sm font-medium mb-2 text-center">Allow/ Mute Notifications</h3>
          <Select>
            <SelectTrigger className="bg-white text-black rounded-md w-full">
              <SelectValue placeholder="Allow" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="allow">Allow</SelectItem>
              <SelectItem value="mute">Mute</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Footer Button */}
      <div className="mt-10 mb-0 flex justify-center w-full">
        <Button className="bg-[#003e82] text-white px-12 py-3 text-2xl rounded-md w-full p-8">
          Update Settings
        </Button>
      </div>

    </div>
  )
}
