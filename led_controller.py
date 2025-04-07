import RPi.GPIO as GPIO
import time

class LEDController:
    def __init__(self, pins):
        """
        Initializes the LEDController with a dictionary of LED pins.
        
        Args:
        pins (dict): A dictionary mapping LED color keys (r, g, b) to GPIO pin numbers.
        """
        self.led_pins = pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(list(self.led_pins.values()), GPIO.OUT)
        # Default game difficulty is medium
        self.difficulty = "medium"
        # Light flashes for a longer duration on easy mode, shorter duration on hard
        self.duration_map = {"easy": 1.0, "medium": 0.5, "hard": 0.25}

    def set_difficulty(self, difficulty):
        """Sets the difficulty level, adjusting LED flash duration accordingly."""
        self.difficulty = difficulty.lower()
        
    def flash_led(self, color):
        """Flashes the LED for the set duration."""
        duration = self.duration_map.get(self.difficulty, 0.5)
        GPIO.output(self.led_pins[color], GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.led_pins[color], GPIO.LOW)
        time.sleep(0.3)

    def start_sequence(self):
        """Performs a countdown sequence in red, green, blue order."""
        # Light up LEDs sequentially and keep them on
        for color in ["r", "g", "b"]:
            GPIO.output(self.led_pins[color], GPIO.HIGH)
            time.sleep(0.5)
        time.sleep(0.3)
        
        # Turn all the LEDs off
        for pin in self.led_pins.values():
            GPIO.output(pin, GPIO.LOW)
        # At the end, turn off all LEDs to avoid confusion between starting sequence
        # and the start of the game
        time.sleep(1.0)

    def game_over_flash(self):
        """Flashes all LEDs simultaneously for a 'Game Over' effect."""
        # Flash the LEDS 3 times
        for i in range(3):
            for pin in self.led_pins.values():
                GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.3)
            for pin in self.led_pins.values():
                GPIO.output(pin, GPIO.LOW)
            time.sleep(0.3)

    def cleanup(self):
        """Cleans up the GPIO pins."""
        GPIO.cleanup()
