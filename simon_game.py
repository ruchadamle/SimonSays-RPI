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
            user_input = self.button_controller.get_button_press()
            if user_input != expected_color:
                print(f"Game Over! Your score: {self.score}")
                return False
        return True

    def play(self):
        """Runs the main game loop."""
        print("Welcome to Simon Says! Repeat the LED sequence correctly to score points.")
        
        while True:
            difficulty = input("Choose difficulty (easy/medium/hard): ").strip().lower()
            if difficulty in ["easy", "medium", "hard"]:
                self.led_controller.set_difficulty(difficulty)
                break
            print("Invalid difficulty! Please choose easy, medium, or hard.")

        print(f"\nStarting game on {difficulty} difficulty...\n")
        self.led_controller.start_sequence()

        try:
            while True:
                self.sequence.append(random.choice(self.colors))
                print("Watch the sequence:")
                
                for color in self.sequence:
                    self.led_controller.flash_led(color)
                
                if not self.get_user_input():
                    self.led_controller.game_over_flash()
                    break
                
                self.score += 1
                print(f"Correct! Score: {self.score}\n")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nGame exited.")
        finally:
            self.led_controller.cleanup()

if __name__ == "__main__":
    led_pins = {"r": 17, "g": 18, "b": 22}
    button_pins = {"r": 23, "g": 24, "b": 25} 

    led_controller = LEDController(led_pins)
    button_controller = ButtonController(button_pins)
    game = SimonGame(led_controller, button_controller)
    game.play()
