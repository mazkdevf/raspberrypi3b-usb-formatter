import time
import board
import neopixel
import os
import RPi.GPIO as GPIO
import sys


# Configure the LED strip
LED_COUNT = 7        # Number of LEDs in the strip
LED_PIN = board.D18   # GPIO pin connected to the LED strip
LED_BRIGHTNESS = 0.5  # LED brightness (0 to 1)

INPUT_USB_PORT = "/usb1/1-1/1-1.5/1-1.5:1.0/host0/target0:0:0/0:0:0:0/block/sda"
OUTPUT_USB_PORT = "/usb1/1-1/1-1.4/1-1.4:1.0/host0/target0:0:0/0:0:0:0/block/sda"

LED_ERROR = 1
LED_DONE = 2
LED_BUSY = 3
LED_NONE = 4
LED_DEFAULT = 6

# Initialize the LED strip
pixels = neopixel.NeoPixel(
    LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False)


def set_led_color(led_index, red, green, blue):
    """
    Set the color of a specific LED in the strip.

    :param led_index: Index of the LED (0 to LED_COUNT-1).
    :param red: Red value (0 to 255).
    :param green: Green value (0 to 255).
    :param blue: Blue value (0 to 255).
    """
    pixels[led_index] = (red, green, blue)
    pixels.show()


def clear_leds():
    """Clear all LEDs in the strip (turn off)."""
    pixels.fill((0, 0, 0))
    pixels.show()


def ledState(state):
    if state == LED_ERROR:
        # Red color for error
        for led_index in range(LED_COUNT):
            set_led_color(led_index, 255, 0, 0)
    elif state == LED_DONE:
        # Green color for done
        for led_index in range(LED_COUNT):
            set_led_color(led_index, 0, 255, 0)
    elif state == LED_BUSY:
        # Yellow color for busy
        for led_index in range(LED_COUNT):
            set_led_color(led_index, 255, 255, 0)
    elif state == LED_DEFAULT:
        # Blue color by default
        for led_index in range(LED_COUNT):
            set_led_color(led_index, 0, 0, 255)
    else:
        # Blue color by default
        for led_index in range(LED_COUNT):
            set_led_color(led_index, 0, 0, 255)


def isBlockDeviceExist(usbPath):
    for filename in os.listdir("/sys/block/"):
        if filename.startswith("sd"):
            stream = os.popen("udevadm info -p /sys/block/" +
                              filename + " --query=env")
            output = stream.read()
            if output.find(usbPath) >= 0:
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
    if os.system("mkfs.exfat " + blockDevice + " -n USB") != 0:
        print("mkfs.exfat..")
        return True
    return False


def cloneUsb(inputDevice, outputDevice):
    if os.system("dd if=" + inputDevice + " of=" + outputDevice + " bs=16M"):
        print("dd failed..")
        return True
    return False


def isModeFormat():
    # Implement the check for the mode (format/clone) based on the USB port (uncomment this part)
    return True


def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # GPIO pins for LEDs
    GPIO.setup(18, GPIO.OUT)

    # GPIO pin for USB connection detection
    GPIO.setup(23, GPIO.IN)


if __name__ == "__main__":
    setup_gpio()

    ledState(LED_NONE)

    try:
        while True:
            blockOutputDevice = None
            blockInputDevice = None

            while isModeFormat() and blockOutputDevice is None or not isModeFormat() and (blockOutputDevice is None or blockInputDevice is None):
                time.sleep(1)
                blockOutputDevice = isBlockDeviceExist(OUTPUT_USB_PORT)
                blockInputDevice = isBlockDeviceExist(INPUT_USB_PORT)

            if blockOutputDevice is not None:
                ledState(LED_BUSY)
                error = None
                if isModeFormat():
                    error = formatUsb(blockOutputDevice)
                else:
                    error = cloneUsb(blockInputDevice, blockOutputDevice)

                if error:
                    ledState(LED_ERROR)
                else:
                    ledState(LED_DONE)

            while blockOutputDevice is not None:
                time.sleep(1)
                blockOutputDevice = isBlockDeviceExist(OUTPUT_USB_PORT)

            # Set LED state to LED_NONE when USB stick is disconnected after formatting
            if isModeFormat() and blockOutputDevice is None:
                ledState(LED_DEFAULT)

    except KeyboardInterrupt:
        # Turn off LEDs and exit gracefully if Ctrl+C is pressed
        clear_leds()
        GPIO.cleanup()
