# ===============================================
#  Filename: TCPListenServer.py
#     About: Simple tcp listen server
# ===============================================
import sys
import socket
import traceback

from HkDisplay import HkDisplay

class TCPListenServer():
    ''' TCP Listen Server for Hotel Kilo '''
    host = ''
    port = 2600
    display = HkDisplay()
    
    def __init__(self, log=False):
        ''' TCP Listen Server constructor '''
        print '\n [*] Starting TCP listen server, press ctrl + break to exit...'
        if log:
            self.display.fileOuput = True
            print '\n [*] Saving data to log file (%s)' % self.display.fileOutputPath
        
    def createTcpSocket(self, url=''):
        ''' Creates a tcp socket for listening '''
        self.networkInterface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.networkInterface.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.networkInterface.bind((url, self.port))
    
    def start(self):
        ''' '''
        print '\n [*] Server is listening on port:', self.port
        while True:
            try: 
                self.networkInterface.listen(1)
                connection, sourceAddress = self.networkInterface.accept()
                print '\n [+] Connection from: ', sourceAddress
                while True:
                    data = connection.recv(1024)
                    self.display.printMessage(data)
            except KeyboardInterrupt:
                print '\n [!] User exit, closing remote connection.'
                connection.close()
                break
            except socket.error, cause:
                print '\n [-] Lost connection to hooker: %s' % cause
                pass
            except:
                pass
        
class UDPListenServer():
    ''' UDP Listen Server for Hotel Kilo '''
    
    networkInterface = ''
    oldAddress = ''
    port = 2600
    display = HkDisplay()
    
    def __init__(self, log=False):
        ''' '''
        print '\n [*] Starting UDP listen server, press ctrl + break to exit...'
        if log:
            self.display.fileOuput = True
            print '\n [*] Saving data to log file (%s)' % self.display.fileOutputPath

    def createBroadcastSocket(self):
        ''' Creates a broadcast socket on self.port (defaults to 2600) '''
        self.networkInterface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.networkInterface.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.networkInterface.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.networkInterface.bind(('', self.port))
        
    def start(self):
        ''' Create a listen server using "networkInterface" '''
        print '\n [*] Waiting for UDP hookers on port: %s' % self.port
        while True:
            try:
                message, address = self.networkInterface.recvfrom(8192)
                if str(address) != self.oldAddress:
                    self.display.newClient(address)
                    self.oldAddress = str(address)
                self.display.printMessage(message)
            except KeyboardInterrupt:
                print '\n [*] User exit requested, the listen server has been stopped.'
                sys.exit()
            except:
                traceback.print_exc()
                continue

# Test Code
if __name__ == '__main__':
    tcp = TCPListenServer()
    tcp.createTcpSocket('localhost')
    tcp.start()