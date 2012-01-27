# ===============================================
#  Filename: hkPim.py
#     About: Main module for Hotel-Kilo 
# ===============================================

import sys
from HkNetcode import UDPListenServer, TCPListenServer

__version__ = '0.2'

def banner():
    ''' Banners are awesome '''
    print '\t ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ '
    print '\t||H |||o |||t |||e |||l |||- |||K |||i |||l |||o ||'
    print '\t||__|||__|||__|||__|||__|||__|||__|||__|||__|||__||'
    print '\t|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|'
    print '\t~~~~~~~~~~~ d0t.Mayhem  Proudly Presents ~~~~~~~~~~\n'
    
def help():
    ''' Displays a helpful message to stdout '''
    banner()
    print 'Hotel Kilo: Post Intercept Module - v%s' % __version__
    print 'Usage:\n\tPim.py [mode] [options]'
    print 'Mode:'
    print '\t--tcp............................Use TCP listen server'
    print '\t--udp............................Use UDP listen server'
    print 'Options:'
    print '\t--port [number]..................Set port number'
    print '\t--shift..........................Display shift key presses'
    print '\t--file...........................Save data to log file'
    print '\t--help...........................Display this message'

if __name__ == '__main__':
    displayShift = '--shift' in sys.argv
    fileOutput = '--file' in sys.argv
    if '--help' in sys.argv:
        help()
        sys.exit()
    if '--port' in sys.argv:
        try:
            port = int(sys.argv[sys.argv.index('--port') + 1])
        except:
            print 'Error: %s is not a valid port, or is already in use!' % sys.argv[sys.argv.index('--port') + 1]
            sys.exit()
    else:
        port = 2600 # Default port number
    if '--udp' in sys.argv:
        banner()
        udp = UDPListenServer()
        udp.port = port
        udp.createBroadcastSocket()
        udp.start()
    elif '--tcp' in sys.argv:
        banner()
        tcp = TCPListenServer()
        tcp.port = port
        tcp.createTcpSocket('')
        tcp.start()
    else:
        print '\n [!] PEBKAC: You must select the listen server mode, see --help'

'''
0 1 0
0 0 1
1 1 1
'''
