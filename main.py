import os
import time
import threading
import subprocess

def get_connected_usb_devices():
    lsblk_cmd = "lsblk -o NAME,TYPE,RM | grep disk | awk '{print $1}'"
    output = subprocess.check_output(lsblk_cmd, shell=True, universal_newlines=True)
    usb_list = set(output.strip().split('\n'))
    return usb_list

def unmount_usb(device):
    try:
        unmount_cmd = f"udisksctl unmount -b /dev/{device}"
        subprocess.run(unmount_cmd, shell=True, check=True)
    except Exception as e:
        print(f"Error unmounting USB device {device}: {e}")

def format_usb(device):
    try:
        format_cmd = f"sudo parted /dev/{device} mktable msdos mkpart primary fat32 1MiB 100% set 1 boot on"
        subprocess.run(format_cmd, shell=True, check=True)
        format_fs_cmd = f"sudo mkfs.vfat -n 'USB' /dev/{device}"
        subprocess.run(format_fs_cmd, shell=True, check=True)
        print(f"Formatting USB device: {device}")
    except Exception as e:
        print(f"Error formatting USB device {device}: {e}")

def on_format_button_click(device):
    user_response = input(f"Do you want to format {device}? (yes/no): ").strip().lower()
    if user_response == "yes":
        unmount_usb(device)
        format_usb(device)
    else:
        print("Formatting process canceled.")

def monitor_usb():
    connected_usb_devices = get_connected_usb_devices()

    while True:
        new_usb_devices = get_connected_usb_devices()

        for device in new_usb_devices - connected_usb_devices:
            print(f"USB device inserted: {device}")

            on_format_button_click(device)

        for device in connected_usb_devices - new_usb_devices:
            print(f"USB device disconnected: {device}")

        connected_usb_devices = new_usb_devices
        time.sleep(2)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script needs to be runned with SUDO.")
        exit(1)

    print("Raspberry PI 3 B USB Formattor :D")
    monitor_usb()
