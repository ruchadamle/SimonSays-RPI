import RPi.GPIO as GPIO
import time

class ButtonController:
    def __init__(self, button_pins):
        """
        Initializes the ButtonController with a dictionary of button pins.
        
        Args:
        button_pins (dict): A dictionary mapping button color keys (r, g, b) to GPIO pin numbers.
        """
        self.button_pins = button_pins
        GPIO.setmode(GPIO.BCM)
        # Configures the pins to take input
        # Enables internal pull-up resistors to avoid situations where button floats between HIGH and LOW
        GPIO.setup(list(self.button_pins.values()), GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_button_press(self):
        """
        Waits for a button press and returns the corresponding color key.
        
        Returns:
        str: The key representing the button pressed ('r', 'g', 'b').
        """
        while True:
            for color, pin in self.button_pins.items():
              # Button pressed
                if GPIO.input(pin) == GPIO.LOW:
                    # Short delay
                    time.sleep(0.3) 
                    return color
