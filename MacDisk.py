#!/usr/bin/python
import os, sys, subprocess, pickle
import xml.etree.ElementTree as plist

class UnexpectedOutput(Exception): pass
class OSVerCheck(Exception): pass
class PythonVerCheck(Exception): pass
class DiskutilMissing(Exception): pass
class CLIError(Exception): pass

class MacDiskutil(object):
    'A partial interface of Mac diskutil for Python'
    
    def __init__(self, reqOSXVer='10.7.0', PyVer='2.7'):
        '''Initialization of class also perform version check for OS X and Python'''
        try: osxVerNum = subprocess.check_output("sw_vers | grep 10. | awk '{ FS = \" \" } ; { print $2 }'", shell=True).strip().split('.')
        except: raise CLIError()
        else:
            try: osxVer = int(osxVerNum[1]) >= int(reqOSXVer.split('.')[1]) and int(osxVerNum[2]) >= int(reqOSXVer.split('.')[2])
            except: osxVer = False
            
        try:
            subprocess.check_output(['which', 'which'])
            try: haveDiskutil = 'diskutil' in subprocess.check_output(['which', 'diskutil'])
            except: haveDiskutil = False
        except: osxVer = False
        
        pyVer27 = sys.version_info[0] == 2 and sys.version_info[1] >= 7
    
        if os.uname()[0] != 'Darwin' or not osxVer: raise OSVerCheck()
        elif not haveDiskutil: raise DiskutilMissing()
        elif not pyVer27: raise PythonVerCheck()

    def getWholeDisks(self):
    	WholeDisks = []
        try: output = subprocess.check_output(['diskutil', 'list', '-plist'])
        except: raise
        else:
            try: 
                DiskPlist = plist.fromstring(output)
            except: raise
            else:
            	if DiskPlist[0][6].text != 'WholeDisks':
            	    raise UnexpectedOutput()
        for disk in DiskPlist[0][7]: WholeDisks.append(disk.text)
        return WholeDisks