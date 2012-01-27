# This script require you have py2exe installed

from distutils.core import setup
import py2exe, sys, os

setup(
options = {'py2exe': {'bundle_files': 1,'compressed': 1, 'optimize': 2}}, 
windows = [{'script':'HotelKilo.py', 'icon_resources': [(1, '..\icons\hooker.ico')] }],
zipfile = None,
)