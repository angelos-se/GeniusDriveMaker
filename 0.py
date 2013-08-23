#!/usr/bin/python
import os, sys, subprocess

# Part 0
uname = os.uname()
DEVNULL = open(os.devnull, 'wb')
haveDiskutil = not subprocess.call(['which', 'diskutil'], stdout=DEVNULL, stderr=subprocess.STDOUT)
pyver27 = sys.version_info[0] == 2 and sys.version_info[1] >= 7
DMGList = []
DiskList = []

if uname[0] != 'Darwin':
	print 'Not Darwin! Are you really running this on OS X?'
	sys.exit(1)
elif not haveDiskutil:
	print 'Diskutil not found...'
	sys.exit(2)
elif not pyver27:
	print 'Python version too old or too new...'
	sys.exit(3)
else:
	print 'Good, we are on Darwin, found Disk Utility and have Python 2.7 or better!'

# Part 1
print 'Current working directory is: ', os.getcwd()
for fileName in os.listdir(os.getcwd()):
	if '.dmg' in fileName[-4:].lower():
		DMGList.append(fileName)
print 'Found DMGs: ', DMGList

# Part 2
import xml.etree.ElementTree as plist
DiskPlist = plist.parse('Disks.plist').getroot() # Hard coded temporarily
if DiskPlist[0][6].text != 'WholeDisks':
	print 'Diskutil generated unexpected output, exiting...'
	sys.exit(4)
for disk in DiskPlist[0][7]:
	DiskList.append(disk.text)
print 'Found disks: ', DiskList