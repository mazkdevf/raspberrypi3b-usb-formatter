import os
import time
import threading
import subprocess

def USBLaitteet():
    lsblk_cmd = "lsblk -o NAME,TYPE,RM | grep disk | awk '{print $1}'"
    output = subprocess.check_output(lsblk_cmd, shell=True, universal_newlines=True)
    usb_list = set(output.strip().split('\n'))
    return usb_list

def MountUSB(laite):
    try:
        unmount_cmd = f"udisksctl unmount -b /dev/{laite}"
        subprocess.run(unmount_cmd, shell=True, check=True)
    except Exception as e:
        print(f"Virhe irrottaessa USB-laitetta {laite}: {e}")

def FormatoiUSB(laite):
    try:
        format_cmd = f"sudo parted /dev/{laite} mktable msdos mkpart primary fat32 1MiB 100% set 1 boot on"
        subprocess.run(format_cmd, shell=True, check=True)
        format_fs_cmd = f"sudo mkfs.vfat -n 'USB' /dev/{laite}"
        subprocess.run(format_fs_cmd, shell=True, check=True)
        print(f"USB-laitteen alustus: {laite}")
    except Exception as e:
        print(f"Virhe alustettaessa USB-laitetta {laite}: {e}")

def UserInput(laite):
    user_response = input(f"Haluatko alustaa laitteen {laite}? (kyllä/ei): ").strip().lower()
    if user_response == "kyllä":
        MountUSB(laite)
        FormatoiUSB(laite)
    else:
        print("Alustusprosessi peruttu.")

def USBLooppi():
    liitetyt_usb_laitteet = USBLaitteet()

    while True:
        uudet_usb_laitteet = USBLaitteet()

        for laite in uudet_usb_laitteet - liitetyt_usb_laitteet:
            print(f"USB-laite liitetty: {laite}")

            UserInput(laite)

        for laite in liitetyt_usb_laitteet - uudet_usb_laitteet:
            print(f"USB-laite irrotettu: {laite}")

        liitetyt_usb_laitteet = uudet_usb_laitteet
        time.sleep(2)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Tämä skripti tulee ajaa SUDO-oikeuksilla.")
        exit(1)

    print("Raspberry PI 3B USB Alustaja :D")
    USBLooppi()
