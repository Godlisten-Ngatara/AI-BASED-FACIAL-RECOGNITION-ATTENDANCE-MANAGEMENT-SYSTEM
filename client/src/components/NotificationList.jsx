import { Card, CardContent } from "@/components/ui/card"
import { Bell } from "lucide-react"
import notifications_icon_active from '../assets/icons/notifications_active.png'
const notifications = [
  { id: 1, message: "Your report has been submitted successfully.Your report has been submitted successfully.Your report has been submitted successfully.Your report has been submitted successfully." },
  { id: 2, message: "New comment on your post.New comment on your post.New comment on your post.New comment on your post.New comment on your post.New comment on your post." },
  { id: 3, message: "You have a meeting at 3:00 PM." },
  { id: 4, message: "System update completed." },
]

export default function NotificationList() {
  return (
    <div className="space-y-4">
      {notifications.map((notification) => (
        <Card key={notification.id} className='bg-[#e9f8fe] shadow-[0_20px_50px_rgba(0,0,0,0.5)] rounded-2xl'>
          <CardContent className="flex items-start space-x-4">
            <img src={notifications_icon_active} alt="icon" className="w-8 h-8" />
            <p className="text-sm text-gray-800">{notification.message}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
