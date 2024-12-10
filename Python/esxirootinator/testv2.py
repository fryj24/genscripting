import subprocess
import argparse
import tarfile
import os

def run_command(command):
    try:
        subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return None

    except subprocess.CalledProcessError as e:
        return e.stderr.strip()

def mount_partition(disk_path, mount_path):
    if not os.path.exists(mount_path):
        os.makedirs(mount_path)

    else:
        if not os.path.ismount(mount_path):
            os.makedirs(mount_path)
        else:
            return "Folder already contains a mount!"

    err = run_command(["mount", disk_path, mount_path])
    if err is not None:
        return err

def unmount_partition(mount_path):
    if os.path.ismount(mount_path):
        err = run_command(["umount", mount_path])
        if err is not None:
            return err

def extract_shadow(mount_path, temp_dir):
    try:
        with tarfile.open(mount_path + "/state.tgz", "r:gz") as tar:
            tar.extract("/local.tgz", temp_dir+"/local.tgz")

        with tarfile.open(temp_dir+"/local.tgz", "r:gz") as tar:
            tar.extract("/etc/shadow", temp_dir+"/shadow")
        
        return None

    except Exception as err:
        return err

def pack_shadow(mount_path, temp_dir):
    try:
        with tarfile.open(temp_dir+"/local.tgz", "rw:gz") as tar:
            tar.add(temp_dir+"/shadow", "/etc/shadow")
        
        with tarfile.open(mount_path + "/local.gz", "rw:gz") as tar:
            tar.add(temp_dir+"/local.tgz", "/local.tgz")
        
        return None

    except:
        return "Packing Shadow File Failed"

def modify_shadow():
    pass


def main():
    parser = argparse.ArgumentParser(description="If you are locked out, then I unlock your root")
    parser.add_argument("disk_path", type = str, help="Path to the VMware disk: IE: `/dev/sda5`")
    parser.add_argument("mnt_path", type = str, default="/tmp/vmw", help="Path to the VMware disk: IE: `/dev/sda5`")
    parser.add_argument("temp_dir", type = str, default="/tmp/vmw-unpack", help="Temp dir for unpacking file that will be cleaned at the end of the run")
    args = parser.parse_args()

    try:
        err = mount_partition(args.disk_path, args.mnt_path)
        if err is not None:
            print(err)
            raise(err)
        
        err = extract_shadow(args.mnt_path, args.temp_dir)
        if err is not None:
            print(err)
            raise(err)

    except:
        print("Failed!")

    finally:
        err = unmount_partition(args.mnt_path)
        if err is not None:
            print(err)


main()