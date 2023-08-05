import time
import board
import neopixel

# Configure the LED strip
LED_COUNT = 7        # Number of LEDs in the strip
LED_PIN = board.D18   # GPIO pin connected to the LED strip
LED_BRIGHTNESS = 0.5  # LED brightness (0 to 1)

# Initialize the LED strip
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False)

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

def lerp_color(color1, color2, t):
    """
    Linear interpolation between two colors.

    :param color1: Starting color (r, g, b).
    :param color2: Ending color (r, g, b).
    :param t: Interpolation parameter (0 to 1).
    :return: Interpolated color (r, g, b).
    """
    r = int(color1[0] + t * (color2[0] - color1[0]))
    g = int(color1[1] + t * (color2[1] - color1[1]))
    b = int(color1[2] + t * (color2[2] - color1[2]))
    return (r, g, b)

if __name__ == "__main__":
    try:
        # Clear all LEDs first
        clear_leds()

        # Color cycle: red (255, 0, 0), green (0, 255, 0), blue (0, 0, 255)
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        num_colors = len(colors)
        duration = 0.5  # Duration of each color transition (in seconds)

        while True:
            for i in range(num_colors):
                color1 = colors[i]
                color2 = colors[(i + 1) % num_colors]

                for t in range(100):
                    # Interpolate between the two colors
                    interp_color = lerp_color(color1, color2, t / 100.0)

                    # Set the first 10 LEDs to the interpolated color
                    for led_index in range(min(LED_COUNT, 10)):
                        set_led_color(led_index, *interp_color)

                    # Delay to create a smoother transition
                    time.sleep(duration / 100)

        # This part will never be reached, as the loop is infinite
        # but you can still add other code here if needed.

    except KeyboardInterrupt:
        # Turn off LEDs and exit gracefully if Ctrl+C is pressed
        clear_leds()
