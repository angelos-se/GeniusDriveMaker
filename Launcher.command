#!/bin/bash
##################################################################
# Wrapper script for GeniusDriveMaker
# This script and accompanying python script is written by @angelos_se at his
# personal time. Latest version of this script may be obtained at:
# https://github.com/angelos-se/GeniusDriveMaker
##################################################################
echo "Genius Drive Maker:"
echo "Entering admin password at the following prompt may delete all data in"
echo "all attached drives, press Control-C or close window to cancel."
echo "Please check working directory below before proceeding."
pwd
sudo -k
sudo python ../scripts/GDMain.py