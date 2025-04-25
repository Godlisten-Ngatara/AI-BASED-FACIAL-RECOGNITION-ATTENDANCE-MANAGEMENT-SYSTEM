import uuid
import socket
from onvif import ONVIFCamera

class CameraError(Exception):
    class Camera:
        def __init__(self, ip, user, password):
            try:
                self._mycam = ONVIFCamera(ip, 8080, user, password, no_cache = True)
            except:
                raise CameraError("Could not Connect to camera. Verify credentials and ONVIF support")
            self._camera_media = self._mycam.create_media_service()
            self._camera_media_profie = self._camera_media.GetProfiles()[0]
            
           
            
        
        @property
        def hostname(self) -> str:
            resp = self._mycam.devicemgmt.GetHostname()
            return resp.Name
        
        @property
        def date(self) -> str:

            datetime = self._mycam.devicemgmt.GetSystemDateAndTime()
            return datetime.UTCDateTime.Date
        
        @property
        def is_ptz(self) -> bool:

            resp = self._mycam.devicemgmt.GetCapabilities()
            return bool(resp.PTZ)
        
    

