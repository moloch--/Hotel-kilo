import sys
buildservice = True
if '--no-service' in sys.argv[1:]:
        buildservice = False
        sys.argv = [k for k in sys.argv if k != '--no-service']
        print sys.argv
        
from distutils.core import setup
import os
import py2exe
import glob
import shutil
 
sys.path.insert(0,os.getcwd())
 
def get_files(dir):
        # dig looking for files
        dir1 = os.walk(dir)
        scanning = True
        filenames = []
 
        while(scanning):
                try: 
                        (dirpath, dirnames, files) = dir1.next()
                        filenames.append([dirpath, tuple(files)])
                except:
                        scanning = False
        return filenames
 
DESCRIPTION = 'place_holder'
NAME = 'name'

class Target:
        def __init__(self,**kw):
                        self.__dict__.update(kw)
                        self.version        = "1.00.00"
                        self.compay_name    = "Microsoft Software"
                        self.copyright      = "(c) 2001"
                        self.name           = NAME
                        self.description    = DESCRIPTION
 
my_com_server_target = Target(
                description    = DESCRIPTION,
                service = ["service_module"],
                modules = ["service_module"],
                create_exe = True,
                create_dll = True)
 
if not buildservice:
        setup(
            name = NAME ,
            description = DESCRIPTION,
            version = '1.00.00',
            console = ['hotelService.py'],
                zipfile=None,
                options = {
                                "py2exe":{"packages":"encodings",
                                        "includes":"win32com,win32service,win32serviceutil,win32event",
                                        'dll_excludes': [ "mswsock.dll", "powrprof.dll" ],
                                        'bundle_files': 1,
                                        'compressed': 1,
                                        "optimize": '2'
                                        },
                                },
        )
else:
        setup(
            name = NAME,
            description = DESCRIPTION,
            version = '1.00.00',
                service = [{'modules':["HotelService"], 'cmdline':'pywin32'}],
                zipfile=None,
                options = {
                                "py2exe":{"packages":"encodings",
                                        "includes":"win32com,win32service,win32serviceutil,win32event",
                                        'dll_excludes': [ "mswsock.dll", "powrprof.dll" ],
                                        'bundle_files': 1,
                                        'compressed': 1,
                                        "optimize": '2'
                                        },
                                },
        )
 