import NotificationList from "@/components/NotificationList";
import user_icon from "../assets/icons/user.png";


const TeacherNotificationPage = () => {

    return (
         <div className="flex flex-col gap-6 p-6 w-full ">

             {/* Profile Name Section */}
                  <div className="flex items-center gap-4 mb-0">
                    <img src={user_icon} alt="Profile" className="w-16 h-16 rounded-full" />
                    <h3 className="text-lg font-medium text-blue-900">DR. DAUDI</h3>
                  </div>

                  <NotificationList/>
                   <button
        className="w-full bg-[#002366] hover:bg-[#0033a0] text-white text-xl font-medium py-4 rounded-lg transition-colors duration-200 cursor-pointer"
      >
        Clear Notifications
      </button>
         </div>
    );
}

export default TeacherNotificationPage;