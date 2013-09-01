#!/usr/bin/python
import os, sys, subprocess, pickle
from MacDisk import *

def main():
    DMGList = []
    RAIDSetList = []
    MountedDMGList = []

#    IgnoreList = [] # Debug use
    IgnoreList = ['disk0'] # Internal disk

    # Part 0
    DiskUtil = MacDiskutil()
	# Includes version check during class initialization, defaults: (reqOSXVer='10.7.0', PyVer='2.7')

    # Part 1
    print 'Current working directory: ', os.getcwd()
    for fileName in os.listdir(os.getcwd()):
        if '.dmg' in fileName[-4:].lower(): DMGList.append(fileName)
    print 'Found DMGs: ', DMGList
    
    # Part 2
    DiskList = DiskUtil.getWholeDisks()
#    print 'All disks: ', DiskList # Debug use
    RAIDDiskList = DiskUtil.getAppleRAIDDisks()
    RAIDSetList = DiskUtil.getAppleRAIDSets()
    MountedDMGList = DiskUtil.getMountedImages()
    CSDiskList = DiskUtil.getCoreStorageAllDisks()
    
    for disk in RAIDDiskList: IgnoreList.append(disk)
    for disk in RAIDSetList: IgnoreList.append(disk)
    for disk in MountedDMGList: IgnoreList.append(disk)
    for disk in CSDiskList: IgnoreList.append(disk)
    for disk in set(IgnoreList): DiskList.remove(disk)
    
    print 'Valid disks:'
    DiskNameList = DiskUtil.getMediaNameForList(DiskList)
    for key, value in DiskNameList.iteritems():
        print key, ": ", value 

if __name__ == "__main__": main()