#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, subprocess
from MacDisk import *

def main():
    RPartName = 'Reserved'
    DMGFileList = []

    IgnoreList = ['disk99']
    IgnoreMediaList = ['Hitachi HTS543216L9SA02 Media']

    # Part 0
    DiskUtil = MacDiskutil() # Required for most of diskutil operation
	# Includes version check during class initialization, defaults: (reqOSXVer='10.7.0', PyVer='2.7')

    # Part 1
    print 'Current working directory:', os.getcwd()

    for fileName in os.listdir(os.getcwd()):
        if '.dmg' in fileName[-4:].lower(): DMGFileList.append(fileName)
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
    
    for disk in set(IgnoreList): DiskList.remove(disk)

    DiskNameDict = DiskUtil.getMediaNameForList(DiskList).iteritems()

# Make shift solution
    """for disk in DiskNameList:
        cmdString = 'diskutil partitionDisk ' + disk + ' GPTFormat '
        for dmg in DMGFileList:
            cmdString += 'JHFS+ ' + dmg[:-4] + ' ' + str(DMGSizeDict[dmg] *1.5) + 'B '
        cmdString += 'JHFS+ Free 1B'
        print cmdString"""
    
    """sudo asr --source /Volumes/My\ Book\ VelociRaptor\ Duo/Users/apple/Desktop/Scripts/ASD/IMAGES/OS155.dmg --target /Volumes/OS155 --erase --noverify --noprompt"""
    
# Hopefully this is perm
    for disk, MediaName in DiskNameDict:
        
        diskVolumeDict = DiskUtil.getVolumesForDisk(disk)
        print 'On', MediaName, '('+disk+') found volumes:', diskVolumeDict
        
#        print MediaName, '('+disk+') will be erased:', not DiskUtil.diskHasVolume(disk, RPartName)
        if not DiskUtil.diskHasVolume(disk, RPartName):
            print MediaName, '('+disk+') will be erased.'
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
                    DiskUtil.EraseResizeRestore(diskVolumeDict[RPartName], dmg, DMGSizeDict[dmg]*2, RPartName)
                    diskVolumeDict = DiskUtil.getVolumesForDisk(disk)
            

if __name__ == "__main__": main()
