import time
import random
from led_controller import LEDController
from button_controller import ButtonController

class SimonGame:
    def __init__(self, led_controller, button_controller):
        """Initializes the SimonGame with LED and Button controllers."""
        self.led_controller = led_controller
        self.button_controller = button_controller
        self.sequence = []
        self.score = 0
        self.colors = list(self.led_controller.led_pins.keys())

    def get_user_input(self):
        """Waits for the user to input the sequence using physical buttons."""
        print("Press the buttons in the correct sequence!")
        
        for expected_color in self.sequence:
            # Check that the user input matches the expected input
            user_input = self.button_controller.get_button_press()
            if user_input != expected_color:
                # Print user's score at the end of the game
                print(f"Game Over! Your score: {self.score}")
                return False
        return True

    def play(self):
        """Runs the main game loop."""
        print("Welcome to Simon Says! Repeat the LED sequence correctly to score points.")
        
        while True:
            difficulty = input("Choose difficulty (easy/medium/hard): ").strip().lower()
            # Set difficulty to user's chosen difficulty
            if difficulty in ["easy", "medium", "hard"]:
                self.led_controller.set_difficulty(difficulty)
                break
            print("Invalid difficulty! Please choose easy, medium, or hard.")

        print(f"\nStarting game on {difficulty} difficulty...\n")
        # Flashes the LEDs in a starting pattern
        self.led_controller.start_sequence()

        try:
            while True:
                # Everytime this loop runs, add one to the sequence of colors
                self.sequence.append(random.choice(self.colors))
                print("Watch the sequence carefully:")

                # Flash the LEDs in the sequence of colors
                for color in self.sequence:
                    self.led_controller.flash_led(color)

                # If the user input is not correct, end the game
                if not self.get_user_input():
                    self.led_controller.game_over_flash()
                    break

                # If the user input is correct, add increment the score
                self.score += 1
                print(f"Correct! Score: {self.score}\n")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nGame exited.")
        finally:
            self.led_controller.cleanup()

if __name__ == "__main__":
    # Set up GPIO pins to be used
    led_pins = {"r": 17, "g": 18, "b": 22}
    button_pins = {"r": 23, "g": 24, "b": 25} 

    led_controller = LEDController(led_pins)
    button_controller = ButtonController(button_pins)
    game = SimonGame(led_controller, button_controller)
    game.play()
