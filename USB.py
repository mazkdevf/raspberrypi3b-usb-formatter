import os
import time
import sys

#from gpiozero import LED

INPUT_USB_PORT = sys.argv[1]  # "/usb2/2-2/1-2:1.0/"
OUTPUT_USB_PORT = sys.argv[2]  # "/usb1/1-2/1-2:1.0/"
RED_LED_GPIO = sys.argv[3]
GREEN_LED_GPIO = sys.argv[4]
BUTTON_GPIO = sys.argv[5]

LED_ERROR = 1
LED_DONE = 2
LED_BUSY = 3
LED_NONE = 4
#ledRed = LED(RED_LED_GPIO)
#ledGreen = LED(GREEN_LED_GPIO)
#button = Button(BUTTON_GPIO)


def ledState(state):
    print("set led state")
    # if state == LED_ERROR:
    # ledRed.on()
    # ledGreen.off()
    # if state == LED_DONE:
    # ledRed.off()
    # ledGreen.on()
    # if state == LED_BUSY:
    # ledRed.on()
    # ledGreen.on()
    # if state == LED_NONE:
    # ledRed.off()
    # ledGreen.off()


def isBlockDeviceExist(usbPath):
    for filename in os.listdir("/sys/block/"):
        if filename.startswith("sd"):
            stream = os.popen("udevadm info -p /sys/block/" +
                              filename + " --query=env")
            output = stream.read()
            if output.find(usbPath) >= 0:
                # print(output)
                print("----->" + filename)
                return "/dev/"+filename
    return None


def formatUsb(blockDevice):
    if os.system("wipefs -a " + blockDevice) != 0:
        print("wipefs failed..")
        return True
    if os.system("parted " + blockDevice + " mklabel gpt mkpart primary 0% 100% --script") != 0:
        print("parted failed..")
        return True
    if os.system("mkfs.exfat " + blockDevice + " -n UsbTikku") != 0:
        print("mkfs.exfat..")
        return True
    return False


def formatUsb(blockDevice):
    if os.system("wipefs -a " + blockDevice) != 0:
        print("wipefs failed..")
        return True
    if os.system("parted " + blockDevice + " mklabel gpt mkpart primary 0% 100% --script") != 0:
        print("parted failed..")
        return True
    if os.system("mkfs.exfat " + blockDevice + " -n UsbTikku") != 0:
        print("mkfs.exfat..")
        return True
    return False


def cloneUsb(inputDevice, outputDevice):
    if os.system("dd if=" + inputDevice + " of=" + outputDevice + " bs=16M"):
        print("dd failed..")
        return True
    return False


def isModeFormat():
    # return button.is_pressed
    return True


print("input usb = " + INPUT_USB_PORT)
print("input usb = " + OUTPUT_USB_PORT)
print("red gpio = " + RED_LED_GPIO)
print("green gpio = " + GREEN_LED_GPIO)
print("button gpio = " + BUTTON_GPIO)


while True:
    blockOutputDevice = None
    blockInputDevice = None

    ledState(LED_NONE)

    while isModeFormat() == True and blockOutputDevice == None or isModeFormat() == false and (blockOutputDevice == None or blockInputDevice == None):
        time.sleep(5)
        blockOutputDevice = isBlockDeviceExist(OUTPUT_USB_PORT)
        blockInputDevice = isBlockDeviceExist(INPUT_USB_PORT)

    if blockDevice != None:
        ledState(LED_BUSY)
        error = None
        if isModeFormat() == True:
            error = formatUsb(blockOutputDevice)
        else:
            error = cloneUsb(blockInputDevice, blockOutputDevice)

        if error:
            ledState(LED_ERROR)
        else:
            ledState(LED_DONE)

    while blockDevice != None:
        time.sleep(5)
        blockOutputDevice = isBlockDeviceExist(OUTPUT_USB_PORT)
