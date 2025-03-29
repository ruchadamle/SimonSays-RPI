# Import necessary libraries
# Importing library to control GPIO pins on Pi to control LEDs
import RPi.GPIO as GPIO
# Importing time to add delays when flashing the LEDs
import time
# Importing random to randomly choose which LED to light up
import random

# Class that controls the LEDs
class LEDController:
    def __init__(self, pins):
        """
        Initializes the LEDController with a dictionary of LED pins.
        
        Parameters:
        pins (dict): A dictionary mapping LED color keys (r, g, b) to GPIO pin numbers.
        """
        self.led_pins = pins
        GPIO.setmode(GPIO.BCM)
        # Set up the specified pins as output
        GPIO.setup(list(self.led_pins.values()), GPIO.OUT)
        # Default difficulty level
        # Difficulty level determines how long the pins stay on
        self.difficulty = "medium"
        # LEDs blink for a shorter duration on harder modes
        self.duration_map = {"easy": 1.0, "medium": 0.5, "hard": 0.25}

    def set_difficulty(self, difficulty):
        """
        Sets the difficulty level, adjusting LED flash duration accordingly.
        
        Parameters:
        difficulty (str): The difficulty level (easy, medium, or hard).
        """
        self.difficulty = difficulty.lower()
        
    def flash_led(self, color):
        """
        Flashes the LED of the specified color for a duration based on the selected difficulty level.
        
        Parameters:
        color (str): The key representing the LED color (r, g, b).
        """
        duration = self.duration_map.get(self.difficulty, 0.5)
        # Turn the LED on
        GPIO.output(self.led_pins[color], GPIO.HIGH)
        # Keep the LED on according to the chosen difficulty level
        time.sleep(duration)
        # Turn off the LED
        GPIO.output(self.led_pins[color], GPIO.LOW)
        # Short delay before the next LED flashes
        time.sleep(0.3)

    def cleanup(self):
        """
        Cleans up the GPIO pins, resetting them to their default state.
        """
        GPIO.cleanup()

# Class that controls the game logic
class SimonGame:
    """
        Initializes the SimonGame with an LED controller.
        
        Parameters:
        led_controller (LEDController): An instance of LEDController to manage LED flashing.
    """
    def __init__(self, led_controller):
        # Instance of LED Controller to control the LEDs
        self.led_controller = led_controller
        # The sequence of colors to be remembered by the player
        self.sequence = []
        # The player's score
        self.score = 0
        # Creates a list of the LED color names
        self.colors = list(self.led_controller.led_pins.keys())

    def get_user_input(self):
        """
        Prompts the user to input the sequence of colors.
        
        Returns:
        bool: True if the user correctly repeats the sequence, False if not.
        """
        print("Enter the sequence using 'r' (red), 'g' (green), 'b' (blue). Press Enter after each input.")

        # Iterate through the expected sequence
        for expected_color in self.sequence:
            while True:
                # Prompt user to enter the color
                user_input = input("Color: ").strip().lower()
                # Check if the input is valid
                if user_input in self.colors:
                    # If user input does not match expected color
                    if user_input != expected_color:
                        # End the game and print the user's score
                        print(f"Game Over! Your score: {self.score}")
                        return False
                    break
                else:
                    # If user does not input r/g/b, remind them and keep asking until
                    # a proper input is given
                    print("Invalid input! Use 'r', 'g', or 'b'.")
        return True

    def play(self):
        """
        Runs the main game loop, where the player must repeat an increasingly long sequence of LED flashes.
        """
        
        print("Welcome to Simon Says! Repeat the LED sequence correctly to score points.")
        
        # Get difficulty level from user
        while True:
            difficulty = input("Choose difficulty (easy/medium/hard): ").strip().lower()
            if difficulty in ["easy", "medium", "hard"]:
                # Set the chosen difficulty
                self.led_controller.set_difficulty(difficulty)
                break
            else:
                # If improper input is given, ask user to choose again
                print("Invalid difficulty! Please choose easy, medium, or hard.")

        print(f"\nStarting game on {difficulty} difficulty...\n")

        try:
            while True:
                # Add a random color ot the sequence
                self.sequence.append(random.choice(self.colors))

                print("Watch the sequence:")
                # Flash each color in the sequence
                for color in self.sequence:
                    self.led_controller.flash_led(color)

                # If user does not enter sequence properly, end game
                if not self.get_user_input():
                    break

                # If user provides proper input, add 1 to the score
                self.score += 1
                # Display a message with the updated score
                print(f"Correct! Score: {self.score}\n")
                # Pause before starting the next round
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nGame exited.")
        finally:
            self.led_controller.cleanup()

if __name__ == "__main__":
    # Define the GPIO pin numbers for the LEDs
    led_pins = {"r": 17, "g": 18, "b": 22}
    # Create an instance of the LED Controller
    led_controller = LEDController(led_pins)
    # Create an instance of the SimonGame using the LED controller
    game = SimonGame(led_controller)
    # Start the game
    game.play()
