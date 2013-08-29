#!/usr/bin/python
import os, sys, subprocess, pickle
from MacDisk import *

def main():
    DMGList = []
    DiskList = []
    RAIDList = []
    RAIDSetList = []
    MountedDMGList = []

    IgnoreList = ['disk0']

    # Part 0

	
    #else: print 'Good, we are on Darwin, found Disk Utility and have Python 2.7 or better!'

    # Part 1
    print 'Current working directory is: ', os.getcwd()
    for fileName in os.listdir(os.getcwd()):
        if '.dmg' in fileName[-4:].lower(): DMGList.append(fileName)
    print 'Found DMGs: ', DMGList
    
    # Part 2
    
    DiskList = MacDisk.getWholeDisks()
    
    try:
        output = subprocess.check_output("diskutil ar list | grep Online | grep disk | awk '{ FS = \" \" } ; { print $2 }'", shell=True).split()
    except:
        print 'Cannot get Apple RAID Disks...'
        sys.exit(6)
    else: 
        for RAIDDisk in output:
            RAIDList.append(RAIDDisk[:RAIDDisk.rfind('s')])
        #print 'Disks in RAID: ', RAIDList
    
    try:
        output =  subprocess.check_output('diskutil ar list | grep "Device Node" | awk \'{ print $3 }\'', shell=True).split()
    except:
        print 'Cannot get Apple RAID Sets...'
        sys.exit(7)
    else: 
        for RAIDSet in output:
            if 'disk' in RAIDSet : RAIDSetList.append(RAIDSet)

    try:
         output = subprocess.check_output('mount | grep "mounted by apple"', shell=True).split()
    except:
        output = ""
    else:
        for MountedDMG in output:
            if '/dev/disk' in MountedDMG: MountedDMGList.append(MountedDMG[5:MountedDMG.rfind('s')])
        #print 'Mounted images: ', MountedDMGList
    
    for disk in IgnoreList: DiskList.remove(disk)
    for disk in RAIDList: DiskList.remove(disk)
    for disk in RAIDSetList: DiskList.remove(disk)
    for disk in MountedDMGList: DiskList.remove(disk)
    print 'Found disks: ', DiskList

if __name__ == "__main__": main()