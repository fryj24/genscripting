import subprocess
import os
import re

#Assign some values = to variable strings and create pre req folders

vmware_disk = "/dev/sda5" #<<<<<<<<<<<<<<CHANGE ME HERE!!! PLEASE VERIFY AND CHANGE THE NUMBER IF NEEDED!
#      Example sda6, sda7 and so on. Refer to readme file on github, you need to know this beforehand and 
#      it needs to be the correct disk to work.
vmware_mount = "/mnt/vmw"
temp_dir = "/temp"

#create the vmw mount point folder in /mnt
result = subprocess.run(["mkdir", vmware_mount], capture_output=True, text=True)

#mounts vmware disk to vmware mountpoint
result = subprocess.run(["mount", vmware_disk, vmware_mount], capture_output=True, text=True)

# Now we need a temporary folder to work with here we check for "/temp" first in the below defined function with an if/else.
            #the folder temp can exist already on your bootable environment, we wont delete it; do this later on your own!

def create_directory_if_needed (directory_path):
    """Checking if temporary directory exist."""
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        print(f"Directory '{directory_path}' created successfully.")
    else:
        print(f"Directory '{directory_path}' already exists.")

# sets the temporary directory to create and call the above defined function
directory_to_create = temp_dir
create_directory_if_needed(directory_to_create)

#extract state tgz into temporary folder then extract local tgz file within temporary location
result = subprocess.run(["tar", "-xf", "/mnt/vmw/state.tgz", "–C", "/temp/"], capture_output=True, text=True)
result = subprocess.run(["tar", "-xf", "/temp/local.tgz", "–C", "/temp/"], capture_output=True, text=True)

#work magic on the shadow file using re to read file lines to look for root :: and clear in between then write the change

# Path to the shadow file
shadow_file_path = '/temp/etc/shadow'

# Read the file, modify it, and write back
with open(shadow_file_path, 'r') as file:
    lines = file.readlines()

# Prepare the new content by modifying the line with 'root'
with open(shadow_file_path, 'w') as file:
    for line in lines:
        # Check if the line starts with 'root' and modify the part between the first two colons
        if line.startswith('root:'):
            # Use regex to replace the part between the colons with empty string
            line = re.sub(r'(?<=^root:)[^:]+(?=:)', '', line)
        # Write back to the file
        file.write(line)

print(f"Successfully edited {shadow_file_path}.")

#move shadow back into archive and copy state gz back into VMWare OS disk after merging changes then unmount hammertime
result = subprocess.run(["tar", "-czf", "/temp/local.tgz", "/temp/local/etc"], capture_output=True, text=True)
result = subprocess.run(["tar", "-czf", "/temp/state.tgz", "/temp/local.tgz"], capture_output=True, text=True)
result = subprocess.run(["mv", "-czf", "/temp/state.tgz", "/mnt/vmw"], capture_output=True, text=True)
result = subprocess.run(["umount", "/mnt/vmw"], capture_output=True, text=True)

# Print the output
print(result.stdout)

print(f"That's it, reboot now into EXSi (dont forget to dismount your temporary bootable! then F2 at VMWare DCUI to set a root password. Initial F2 FYI no root password to get in until password is set.)")