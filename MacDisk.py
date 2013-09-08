#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, subprocess, pickle
import xml.etree.ElementTree as plist

class UnexpectedOutput(Exception): pass
class OSVerCheck(Exception): pass
class PythonVerCheck(Exception): pass
class DiskutilMissing(Exception): pass
class CLIError(Exception): pass
class InvalidParameter(Exception): pass

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
        try: output = subprocess.check_output(['diskutil', 'list'])
        except: raise
        else:
            for line in output.split('\n'):
                if line[0:5] == '/dev/': WholeDisks.append(line[5:].strip())
            return WholeDisks
        
    def getInternalDisks(self):
        InternalDisks = []
        for dev in self.getWholeDisks():
            try:
                output = subprocess.check_output('diskutil info ' + dev+ ' | grep "Internal:"', shell=True)
            except: raise
            else:
                if 'Yes' in output: InternalDisks.append(dev)
        return InternalDisks
        
    def getAppleRAIDDisks(self):
        RAIDDisks = []
        try:
            output = subprocess.check_output("diskutil ar list | grep Online | grep disk | awk '{ FS = \" \" } ; { print $2 }'", shell=True).split()
        except: raise
        else: 
            for RAIDDisk in output: RAIDDisks.append(RAIDDisk[:RAIDDisk.rfind('s')])
        return RAIDDisks

    def getAppleRAIDSets(self):
        RAIDSets = []
        try:
            output =  subprocess.check_output('diskutil ar list | grep "Device Node" | awk \'{ print $3 }\'', shell=True).split()
        except: raise
        else: 
            for RAIDSet in output:
                if 'disk' in RAIDSet : RAIDSets.append(RAIDSet)
        return RAIDSets
        
    def getAppleRAIDAll(self):
        RAIDAll = []
        RAIDAll.extend(self.getAppleRAIDDisks())
        RAIDAll.extend(self.getAppleRAIDSets())
    	return RAIDAll

    def getMountedImages(self):
        MountedDMGs = []
        for dev in self.getWholeDisks():
            try:
                output = subprocess.check_output('diskutil info ' + dev+ ' | grep "Protocol:"', shell=True)
            except: raise
            else:
                if 'Disk Image' in output: MountedDMGs.append(dev)
        return MountedDMGs

    def getCoreStorageAllDisks(self):
        CoreStorageAllDisks = []
        try:
            output = subprocess.check_output('diskutil cs list | grep Disk', shell=True).split('Disk:')
        except: output = ''
        else:
            for CSDisk in output:
                if 's' in CSDisk:
                    if CSDisk.find('s') == CSDisk.rfind('s'): CoreStorageAllDisks.append(CSDisk[CSDisk.find('disk'):].strip())
                    else: CoreStorageAllDisks.append(CSDisk[CSDisk.find('disk'):CSDisk.rfind('s')])
        return CoreStorageAllDisks

    def getMediaNameByDev(self, dev=""):
        try:
            output = subprocess.check_output('diskutil info ' + dev+ ' | grep "Media Name:"', shell=True)
        except: raise
        else:
            return output[output.find("Name:")+5:].strip()

    def getMediaNameForList(self, devList=[]):
        MediaNameDict = {}
        for dev in devList:
            MediaNameDict[dev] = self.getMediaNameByDev(dev)
        return MediaNameDict
    
    def getSizeForFile(self, fileName=''):
        if fileName == '':
            raise InvalidParameter()
        else:
            try:
                output = subprocess.check_output(['ls', '-al', fileName])
            except: raise
            else:
                return int(output.split()[4])
    
    def getSizeForFiles(self, fileList=[]):
        FileListDict = {}
        for fileName in fileList:
            FileListDict[fileName] = self.getSizeForFile(fileName)
        return FileListDict
        
    def getVolumeForDisk(self, diskName=''):
        VolumeList = {}
        try:
            output = subprocess.check_output(['diskutil', 'list', diskName])
        except: raise
        else:
            for line in output.split('\n'):
                if 'Apple_HFS' in line: VolumeList[line[33:57].strip()] = line[67:].strip()
            return VolumeList
    
    def diskHasVolume(self, diskName='', volName=''):
        if diskName == '' or volName == '':
            raise InvalidParameter()
        else:
            try:
                output = subprocess.check_output('diskutil list ' + diskName + ' | grep ' + volName, shell=True)
            except: return False
            else:
                if volName == output[33:57].strip(): return True
                else: return False
