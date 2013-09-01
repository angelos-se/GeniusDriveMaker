#!/usr/bin/python
import os, sys, subprocess, pickle
from MacDisk import *

def main():
    DMGFileList = []

    IgnoreList = []

    # Part 0
    DiskUtil = MacDiskutil()
	# Includes version check during class initialization, defaults: (reqOSXVer='10.7.0', PyVer='2.7')

    # Part 1
    print 'Current working directory: ', os.getcwd()
    for fileName in os.listdir(os.getcwd()):
        if '.dmg' in fileName[-4:].lower(): DMGFileList.append(fileName)
    print 'Found DMGs: ', DMGFileList
    
    # Part 2
    DiskList = DiskUtil.getWholeDisks()
#    print 'All disks: ', DiskList # Debug use
    IgnoreList.extend(DiskUtil.getInternalDisks())
    IgnoreList.extend(DiskUtil.getAppleRAIDAll())
    # There are other options for RAID, see MacDisk module for details
    IgnoreList.extend(DiskUtil.getMountedImages())
    IgnoreList.extend(DiskUtil.getCoreStorageAllDisks())
    
    for disk in set(IgnoreList): DiskList.remove(disk)
    
    print 'Valid disks:'
    DiskNameList = DiskUtil.getMediaNameForList(DiskList)
    for key, value in DiskNameList.iteritems():
        print key, ": ", value 

if __name__ == "__main__": main()