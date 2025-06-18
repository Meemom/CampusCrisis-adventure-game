"""
CSC111 Project 1: Text Adventure Game - Additional Functions

This module provides supplementary functions for the text adventure game,
which can be accessed by the main game file (adventure.py).

"""
import time
import sys


# typewriter effect function
def typewriter_effect(text: str, speed: float = 0.01) -> None:
    """Print the given text character by character with a delay, simulating a typewriter effect."""
    for letter in text:
        sys.stdout.write(letter)  # Print the letter without newline
        sys.stdout.flush()  # Ensure the letter gets printed immediately
        time.sleep(speed)  # A pause before printing the next letter

    print()


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
