import RPi.GPIO as GPIO
import time
import random

class LEDController:
    def __init__(self, pins):
        self.led_pins = pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(list(self.led_pins.values()), GPIO.OUT)
        self.difficulty = "medium"  # Default difficulty
        self.duration_map = {"easy": 1.0, "medium": 0.5, "hard": 0.25}

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty.lower()
        
    def flash_led(self, color):
        duration = self.duration_map.get(self.difficulty, 0.5)
        GPIO.output(self.led_pins[color], GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.led_pins[color], GPIO.LOW)
        time.sleep(0.3)

    def cleanup(self):
        GPIO.cleanup()

class SimonGame:
    def __init__(self, led_controller):
        self.led_controller = led_controller
        self.sequence = []
        self.score = 0
        self.colors = list(self.led_controller.led_pins.keys())

    def get_user_input(self):
        print("Enter the sequence using 'r' (red), 'g' (green), 'b' (blue). Press Enter after each input.")

        for expected_color in self.sequence:
            while True:
                user_input = input("Color: ").strip().lower()
                if user_input in self.colors:
                    if user_input != expected_color:
                        print(f"Game Over! Your score: {self.score}")
                        return False
                    break
                else:
                    print("Invalid input! Use 'r', 'g', or 'b'.")
        return True

    def play(self):
        print("Welcome to Simon Says! Repeat the LED sequence correctly to score points.")
        
        # Get difficulty level from user
        while True:
            difficulty = input("Choose difficulty (easy/medium/hard): ").strip().lower()
            if difficulty in ["easy", "medium", "hard"]:
                self.led_controller.set_difficulty(difficulty)
                break
            else:
                print("Invalid difficulty! Please choose easy, medium, or hard.")

        print(f"\nStarting game on {difficulty} difficulty...\n")

        try:
            while True:
                self.sequence.append(random.choice(self.colors))

                print("Watch the sequence:")
                for color in self.sequence:
                    self.led_controller.flash_led(color)

                if not self.get_user_input():
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
    led_controller = LEDController(led_pins)
    game = SimonGame(led_controller)
    game.play()
