# At the top of my script you will find -

## vmware_dir = "/mnt/sda5" #<<<<<<<<<<<<<<CHANGE ME HERE

You absolutely must set the correct number after "sda" disk device number that relates to your VMWare OS disk first prior to running the script.

To do so see steps below, credit to the article I formulated this scrip based on and its respective author Kevin Soltow:
https://www.starwindsoftware.com/blog/forgot-esxi-root-password-no-problems-4-ways-reset/

1. In the terminal su to root
2. now run fdisk to list out all devices with a grep filter down to /dev/sda only ---
Example: fdisk –l | grep /dev/sda
3. In the output find the two disks "usually /dev/sda5"  for "Microsoft basic data"
4. Taking note of which "sda" disk numbers are "Microsoft basic data" ls each one to find if it contains a "/etc/shadow" file within if so that is the disk you need!
Example: ls -l /etc/ | grep shadow


Special thanks to my colleague Diego Torres for sparking my interst in creating this script and collaborating on its success.