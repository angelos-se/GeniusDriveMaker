#!/usr/bin/python
import os, sys, subprocess, pickle
import xml.etree.ElementTree as plist

class UnexpectedOutput(Exception):
    pass
    
def __init__():
	return MacDisk

class MacDisk(object):
    'A partial interface of Mac diskutil for Python'
    
    def __init__(self):
        try: osxVerNum = subprocess.check_output("sw_vers | grep 10. | awk '{ FS = \" \" } ; { print $2 }'", shell=True).strip().split('.')
        except: osxVer = False
        else:
            try: osxVer = int(osxVerNum[1]) >= 7 and int(osxVerNum[2]) >= 0
            except: osxVer = False
    
        try:
            subprocess.check_output(['which', 'which'])
            try: haveDiskutil = 'diskutil' in subprocess.check_output(['which', 'diskutil'])
            except: haveDiskutil = False
        except: osxVer = False
        
        pyVer27 = sys.version_info[0] == 2 and sys.version_info[1] >= 7
    
        if os.uname()[0] != 'Darwin' or not osxVer:
            print 'Not OS X or version too old or missing UNIX tools...'
            sys.exit(1)
        elif not haveDiskutil:
            print 'Diskutil not found...'
            sys.exit(2)
        elif not pyVer27:
            print 'Python version too old or too new...'
            sys.exit(3)

    def getWholeDisks(self):
        try: output = subprocess.check_output(['diskutil', 'list', '-plist'])
        except: raise
        else:
            try: 
                DiskPlist = plist.fromstring(output)
            except: raise
            else: 
                #raise UnexpectedOutput()
                return []
        for disk in DiskPlist[0][7]: WholeDisks.append(disk.text)
        return WholeDisks