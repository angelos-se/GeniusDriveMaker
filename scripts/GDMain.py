#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, subprocess
from MacDisk import *

def main():
    RPartName = 'GDMRsvd'
    # Spare space on disk will be named using string RPartName, this is also used to identify drives formatted using Genius Drive Maker

    # The following is just an example, disk0 is usually automatically ignored when booted from internal disk. If you have disk drives that you want to protect, add the name to IgnoreMediaList and the drive will be automatically excluded.
    IgnoreList = ['disk98', 'disk99']
    IgnoreMediaList = ['ADATA USB Flash Drive Media']

    # Part 0
    DiskUtil = MacDiskutil() # Required for most of diskutil operation
	# Includes version check during class initialization, defaults: (reqOSXVer='10.7.0', PyVer='2.7')

    # Part 1
    print 'Current working directory:', os.getcwd()

    DMGFileList = []
    for fileName in os.listdir(os.getcwd()):
        if '.dmg' in fileName[-4:].lower(): DMGFileList.append(fileName)
    if len(DMGFileList) == 0: sys.exit("No DMG found, running from the wrong directory?")
    DMGSizeDict = DiskUtil.getSizeForFiles(DMGFileList)
    print 'Found DMGs:', DMGSizeDict
    
    # Part 2
    DiskList = DiskUtil.getWholeDisks()
    IgnoreList.extend(DiskUtil.getInternalDisks())
    IgnoreList.extend(DiskUtil.getDiskByMediaName(IgnoreMediaList))
    IgnoreList.extend(DiskUtil.getAppleRAIDAll())
    # There are other options for RAID, see MacDisk module for details
    IgnoreList.extend(DiskUtil.getMountedImages())
    IgnoreList.extend(DiskUtil.getCoreStorageAllDisks())

    for disk in set(IgnoreList):
        if disk in DiskList: DiskList.remove(disk)

    DiskNameDict = DiskUtil.getMediaNameForList(DiskList).iteritems()

    for disk, MediaName in DiskNameDict:
        
        diskVolumeDict = DiskUtil.getVolumesForDisk(disk)
        print 'On', MediaName, '('+disk+') found volumes:', diskVolumeDict

        if not DiskUtil.diskHasVolume(disk, RPartName):
            print MediaName, '('+disk+') will be erased.'
            if not DiskUtil.diskHasVolume(disk, 'x'+RPartName):
                if 'yes' != raw_input('Proceed? (yes/NO) ').lower(): continue # #Prompt
            if not DiskUtil.diskHasVolume(disk, RPartName):
                subprocess.call(['diskutil', 'eraseDisk', 'JHFS+', RPartName, 'GPT', disk])
                diskVolumeDict = DiskUtil.getVolumesForDisk(disk)    
        
        for dmg in DMGFileList:
            if dmg[:-4] not in diskVolumeDict:
                if 'x'+dmg[:-4] in diskVolumeDict:
                    print '* x'+dmg[:-4], 'marked for erase & restore'
                    DiskUtil.EraseRestore(diskVolumeDict['x'+dmg[:-4]], dmg)
                    diskVolumeDict = DiskUtil.getVolumesForDisk(disk)
                else:
                    print '* Adding', dmg[:-4], 'to', MediaName, '('+disk+')'
                    DiskUtil.EraseResizeRestore(diskVolumeDict[RPartName], dmg, DMGSizeDict[dmg]*3, RPartName) # Using some very large partitons here… =_=||
                    diskVolumeDict = DiskUtil.getVolumesForDisk(disk)
            

if __name__ == "__main__": main()
