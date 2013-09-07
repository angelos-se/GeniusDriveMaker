#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, subprocess, pickle
from MacDisk import *

def main():
    RPartName = 'Reserved'
    DMGFileList = []

#    IgnoreList = ['disk3']
    IgnoreList = []

    # Part 0
    DiskUtil = MacDiskutil()
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
    for disk, volName in DiskNameDict:
        print volName, '('+disk+') will be erased:', not DiskUtil.diskHasVolume(disk, RPartName)
        if 'yes' != raw_input('Proceed? (yes/NO) ').lower(): sys.exit(1)
        if not DiskUtil.diskHasVolume(disk, RPartName):
            subprocess.call('diskutil eraseDisk JHFS+ ' + RPartName + ' GPT ' + disk, shell=True)
        
        print DiskUtil.getVolumeForDisk(disk)
        	

if __name__ == "__main__": main()
