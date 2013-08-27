#!/usr/bin/python
import os, sys, subprocess, pickle

def main():
    DMGList = []
    DiskList = []
    IgnoreList = ['disk0', 'disk2']

    # Part 0
    try: osxVerNum = subprocess.check_output("sw_vers | grep 10. | awk '{ FS = \" \" } ; { print $2 }'", shell=True).strip().split('.')
    except: osxVer = False
    else:
    	try: osxVer = int(osxVerNum[1]) >= 8 and int(osxVerNum[2]) >= 0
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
    #else: print 'Good, we are on Darwin, found Disk Utility and have Python 2.7 or better!'

    # Part 1
    print 'Current working directory is: ', os.getcwd()
    for fileName in os.listdir(os.getcwd()):
        if '.dmg' in fileName[-4:].lower(): DMGList.append(fileName)
    print 'Found DMGs: ', DMGList

    # Part 2
    import xml.etree.ElementTree as plist
    try: output = subprocess.check_output(['diskutil', 'list', '-plist'])
    except: output = ''
    else:
    	try: 
    		DiskPlist = plist.fromstring(output)
    	except:
    		print 'Unable to parse Diskutil output, exiting...'
        	sys.exit(4)
    	else: 
    		if DiskPlist[0][6].text != 'WholeDisks':
        		print 'Diskutil generated unexpected output, exiting...'
        		sys.exit(5)
	
	#DiskPlist = plist.parse('Disks.plist').getroot() # Hard coded temporarily	
	for disk in DiskPlist[0][7]: DiskList.append(disk.text)
	for disk in IgnoreList: DiskList.remove(disk)
	print 'Found disks: ', DiskList

if __name__ == "__main__": main()