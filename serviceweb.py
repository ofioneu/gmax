import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import logging
import subprocess 


pathexe = r"C:\\Users\\Fabio Martins\\Desktop\\GMAC\\dist\\app.exe"
logging.basicConfig(
    filename = 'C:\maximus\GMAX\\Temp\\service.log',
    level = logging.DEBUG, 
    format = '[hello-service] %(levelname)-7.7s %(message)s'
)

class HelloWorldSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "GMAX"
    _svc_display_name_ = "GMAX"
    
    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.stop_event = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logging.info('Stopping service ...')
        self.stop_requested = True

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_,'')
        )
        self.main()

    def main(self):
        logging.info(' ** Hello PyWin32 World ** ')
        # Simulate a main loop
        for i in range(0,1):
            if self.stop_requested:
                logging.info('A stop signal was received: Breaking main loop ...')
                break
            time.sleep(5)
            subprocess.Popen([pathexe])  
               
            logging.info("Hello at %s" % time.ctime())
        return

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(HelloWorldSvc)