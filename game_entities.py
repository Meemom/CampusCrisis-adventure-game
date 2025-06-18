"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
# Standard library imports
import time
import random
from typing import Optional
from dataclasses import dataclass

# Local module imports
from additional_functions import typewriter_effect

# Global variables for text colors
RED = "\033[31m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
RESET = "\033[0m"


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: The name of the item.
        - id_num: A unique integer id of the item.
        - description: A brief description of the functions or properties of the item.
        - start_position: The initial location ID where the item is found.
        - target_position: The target location ID for the item, or None if not specified.
    """

    name: str
    id_num: int
    description: str
    start_position: int
    target_position: Optional[int] = None

    def __init__(self, name: str, id_num: int, description: str, start_position: int,
                 target_position: Optional[int] = None) -> None:
        """Initializes a new item."""
        self.name = name
        self.id_num = id_num
        self.description = description
        self.start_position = start_position
        self.target_position = target_position


@dataclass
class Score:
    """A class to track the player's score in the adventure game.

    Instance Attributes:
        - score: An integer representing the current score of the player.

    Representation Invariants:
        - score >= 0
    """
    score: int

    def __init__(self) -> None:
        """Initialize the score to 0."""
        self.score = 0

    def increase(self, amount: int) -> None:
        """Increase the score by a given amount (must be non-negative)."""
        if amount > 0:
            self.score += amount

    def decrease(self, amount: int) -> None:
        """Decrease the score by a given amount (must not drop below 0)."""
        if amount > 0:
            self.score = max(0, self.score - amount)


@dataclass
class Moves:
    """A class to track the number of moves.

    Instance Attributes:
        - moves: An integer representing the number of moves the player has left.

    Representation Invariants:
        - moves >= 0
    """
    moves: int

    def __init__(self, num: int) -> None:
        """Initialize an instance of Moves with a given number of moves."""
        self.moves = num

    def increase(self, amount: int) -> None:
        """Increase the moves by a given amount (must be non-negative)."""
        if amount > 0:
            self.moves += amount
            print(f"{YELLOW}\033[1;33mMOVES EARNED: +{amount}\033[0m{RESET}")

    def decrease(self, amount: int) -> None:
        """Decrease the moves by a given amount (must not drop below 0)."""
        if amount > 0:
            self.moves = max(0, self.moves - amount)


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: A unique integer id for this location
        - name: A string that represents the name of this location.
        - brief_description: A short description displayed if the location has been visited before, or None if it
                            is unnecessary.
        - long_description: A detailed description displayed upon the player's first visit.
        - available_commands: a mapping of available commands at this location to
                            the location executing that command would lead to, or None if it does not change
                            the player's location.
        - items: a list of Item objects present at this location, or None if this location has no items.
        - visited: A flag indicating whether the player has previously visited this location.
        - sub_locations: A list of IDs representing sublocations within this location, or None if this location
                        has no sublocations.

    Representation Invariants:
        - long_description != ''
    """
    id_num: int
    name: str
    brief_description: str
    long_description: str
    available_commands: dict[str, Optional[int]] = None
    items: Optional[list[Item]] = None
    visited: bool = False
    sub_locations: Optional[list[int]] = None

    def __init__(self, location_id: int = 0, name: str = "", brief_description: str = "", long_description: str = "",
                 available_commands: Optional[dict[str, Optional[int]]] = None,
                 items: Optional[list[Item]] = None, visited: bool = False,
                 sub_locations: Optional[list[int]] = None) -> None:
        """Initialize a new location."""

        self.id_num = location_id
        self.name = name
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = available_commands
        self.items = items
        self.visited = visited
        self.sub_locations = None

    def handle_pickup_item(self, choice: str, inventory: list[Item]) -> Optional[Item]:
        """Handle item pickups at this location."""
        print(f"{YELLOW}Handling pickup for choice: {choice}{RESET}")

        # Find the matching item by exact name
        item = next((matching_item for matching_item in self.items if matching_item.name in choice), None)

        if not item:
            print("No such item found here.")
            return None

        # Check if the inventory already has an item with the same name
        if any(inv_item.name == item.name for inv_item in inventory):
            print(f"You already have {item.name} in your inventory.")
            return None

        # Find the exact instance in self.items and remove it safely
        stored_item = next((stored for stored in self.items if stored.name == item.name), None)

        if stored_item:
            self.items.remove(stored_item)  # Remove item from location
            inventory.append(stored_item)  # Add the item to inventory
            typewriter_effect(f"{YELLOW}Added {stored_item.name} to your inventory.{RESET}")
            typewriter_effect(f"{stored_item.description}")
            return stored_item  # Return the picked-up item to update game log

        return None

    def location_3_commands(self, choice: str, inventory: list[Item]) -> None:
        """Handle available commands at location 3: ROBARTS COMMONS and its sublocations.

        Preconditions:
            - self.id_num == 3
        """
        if choice == "go to second floor":
            if not any(item.id_num == 1 for item in inventory):  # Check if T-Card is in inventory
                typewriter_effect("Oh no! Seems like you need your T-Card to get in."
                                  "\nDo you remember where you last left it?\n")
                time.sleep(1)

                available_commands = ", ".join(self.available_commands.keys())
                print(f"Available commands: {available_commands}")
                self.available_commands[choice] = 4
                return  # Exit early if no T-Card
            else:  # Update the location that this choice leads to
                self.id_num = 4

    def sublocation_5_commands(self, choice: str, moves: Moves, score: Score, inventory: list[Item]) -> None:
        """Handle available commands at sublocation 5: Starbucks.

        Preconditions:
            - self.id_num == 5
        """
        if choice == "talk to the barista":
            puzzle = MugPuzzle()
            if puzzle.barista_dialogue(moves):
                lucky_mug = self.items.pop()
                inventory.append(lucky_mug)
                print(f"{YELLOW}Added to inventory: \033[3m{lucky_mug.description}\033[0m{RESET}")
                score.increase(10)
                print(f"{YELLOW}\033[1mEARNED POINTS: +{10}\033[0m")
                return

    def sublocation_6_commands(self, choice: str, moves: Moves, score: Score, inventory: list[Item]) -> None:
        """Handle available commands at sublocation 6: Robarts Common Room and its sublocations.

        Preconditions:
            - self.id_num == 6
        """
        if choice != "ask the librarian":
            return  # If the choice is something else, do nothing

        while True:  # Allow multiple attempts if the player fails
            puzzle = ConnectionsPuzzle()
            success = puzzle.play_game(moves)

            if success:
                score.increase(10)
                print(f"{YELLOW}\033[1mEARNED POINTS: +{10}\033[0m")
                puzzle.roommate_dialogue()
                laptop_charger = self.items.pop()
                inventory.append(laptop_charger)
                return  # Exit function if successful

            print("Librarian: A noble effort, but the puzzle remains unsolved. Perhaps another attempt?")
            retry = input("\nWould you like to try again? (yes/no) ").strip().lower()

            if retry == "no":
                print("Librarian: Didn't think you'd give up so easily. Let me know if you change your mind.")
                return  # Exit function if the player refuses to retry

            if retry != "yes":
                print("Librarian: Please answer with 'yes' or 'no'.")

    def location_8_commands(self, choice: str, moves: Moves, inventory: list[Item], score: Score) -> None:
        """Handle available commands at location 8: Hart House Fitness Centre.

        Preconditions:
            - self.id_num == 8"""
        if choice == "find coach carter":
            # Create the puzzle instance here, no need to store it as an attribute of Location8
            puzzle = TreadmillPuzzle()

            # Pass the state between method calls
            success = puzzle.coach_challenge(moves)

            if success:
                t_card = self.items.pop()
                inventory.append(t_card)
                print(f"{YELLOW}Added to inventory: \033[3m{t_card.description}\033[0m{RESET}")
                score.increase(10)
                print(f"{YELLOW}\033[1mEARNED POINTS: +{10}\033[0m")
                moves.decrease(1)

    def sublocation_11_commands(self, choice: str) -> None:
        """Handle available commands at sublocation 11: CSSU Lounge."""
        if choice == "eavesdrop on the students":
            typewriter_effect("\033[3mAs you pass a group of students, you overhear a conversation that "
                              "catches your attention.\033[0m")
            typewriter_effect("\nStudent 1: I don’t know if I’m cut out for this. First year feels like such a mess. "
                              "\nThere are too many possibilities... I’m not even sure what I want anymore."
                              "\nIt’s like I’m stuck in this whirlwind of uncertainty.")
            typewriter_effect("\nStudent 2: Isn’t that how it always goes?  "
                              "\nWe’re not living in the world of binary where there are only two truths: 0s and 1s."
                              "\nThere will always be uncertainties in our everyday life. "
                              "\nJust accept it and ride with it.\n")
        elif choice == "check table light":
            typewriter_effect("A table lamp flickers beside you, its light switching on and off in an unusual rhythm."
                              "\nAfter watching for a few moments, a pattern begins to emerge:"
                              "\nOn.")
            time.sleep(0.5)

            typewriter_effect("\nOff.")
            time.sleep(0.5)

            typewriter_effect("\nOn.")
            time.sleep(0.5)

            typewriter_effect("\nOff.")
            time.sleep(0.5)

            typewriter_effect("\nOff.")
            time.sleep(0.5)

    def sublocation_12_commands(self, choice: str, moves: Moves, inventory: list[Item], score: Score) -> None:
        """Handle available commands at sublocation 12: Lost and Found."""
        if choice == "unlock door":
            shift_key = 20
            encrypted_message = f"{RED}BYFFI QILFX{RESET}"
            puzzle = CaesarCipher(shift_key, encrypted_message)
            success = puzzle.unlock_door(moves)

            if success:
                usb_drive = self.items.pop()
                inventory.append(usb_drive)
                print(f"{YELLOW}Added to inventory: \033[3m{usb_drive.description}\033[0m{RESET}")
                score.increase(15)
                print(f"{YELLOW}\033[1mEARNED POINTS: +{15}\033[0m")
                moves.decrease(1)

                typewriter_effect("Great job! Go on with your adventure!")
                input("Press Enter to continue...")


# PUZZLE CLASSES
@dataclass
class TreadmillPuzzle:
    """A Treadmill Puzzle where the player has to run for an exact amount of time (10 seconds) to retrieve their T-Card.

    Instance Attributes:
        - max_attempts: An integer representing the maximum number of attempts at solving the puzzle.
        - found_coach_carter: A boolean value that tracks whether the player has already found coach carter.

    Representation Invariants:
        - max_attempts > 0
    """
    max_attempts: int

    def __init__(self) -> None:
        """Initialize a new Treadmill Puzzle"""
        self.max_attempts = 3  # the player has 3 tries to win the game

    def coach_challenge(self, moves: Moves) -> bool:
        """Initiate a dialogue from Coach Carter to initiate the puzzle."""

        typewriter_effect("\nCoach Carter: Well, well, well... I knew you'd be showing up sooner or later."
                          "\nLooking for your T-Card, huh?")
        time.sleep(1)

        typewriter_effect("\n\n\033[3mYou give a determined nod, hoping not to face much trouble.\033[0m")
        time.sleep(1)

        typewriter_effect("\nCoach Carter: Haha, you think I'm just going to hand it over that easily? "
                          "Nah, not on my watch.")
        time.sleep(1)

        typewriter_effect("\nYou’ve been slacking off lately. I can’t have that on my team. "
                          "Time to prove yourself!")
        time.sleep(1)

        typewriter_effect("\nLet’s see if you've got the speed and precision of a true athlete.")
        time.sleep(1)

        typewriter_effect("\nI’m setting up a little challenge. You’re going to run for exactly 10 seconds."
                          f"\nRun too long or too short, and you’re out! You’ve got {self.max_attempts} tries. ")
        time.sleep(1)

        typewriter_effect("\nReady to prove your worth?")
        time.sleep(1)

        input("\nPress Enter to begin your challenge...")

        return self.treadmill_game(moves)

    def treadmill_game(self, moves: Moves) -> bool:
        """Starts the treadmill puzzle where the player has to "run" exactly 10 seconds."""
        tries_left = self.max_attempts

        while tries_left > 0:
            print(f"\nYou have {tries_left} tries left!")
            print("\nGreat! Press Enter after I say 'Go', and try to press Enter again exactly when 10 seconds hit!")
            time.sleep(2)

            typewriter_effect("Ready...")
            time.sleep(0.5)

            typewriter_effect("Set...")
            time.sleep(0.5)

            typewriter_effect("Go!")
            time.sleep(0.5)

            # Wait for the player to press Enter to start the timing
            input("\nPress Enter to start timing...")  # Timing starts here
            start_time = time.time()

            # Wait for the player to press Enter after 10 seconds
            input("\nPress Enter after exactly 10 seconds...")

            end_time = time.time()
            elapsed_time = round(end_time - start_time, 2)

            if 9.2 <= elapsed_time <= 10.8:
                typewriter_effect("\nCoach Carter: 'Whoa! Exactly 10 seconds?! You’re a natural!'")
                typewriter_effect("Coach Carter: 'Well done, you've earned your T-Card back!'")

                return True  # Return success and updated state
            else:
                typewriter_effect(f"\nCoach Carter: 'Oops! You were {elapsed_time - 10:.2f} seconds off... "
                                  f"Not quite there.'")
                tries_left -= 1
                moves.decrease(2)
                print(f"{RED}\033[1mMOVES DECREASED: -{2}\033[0m{RESET}")

        typewriter_effect("\nCoach Carter: 'You’ve used all your tries... Better luck next time!'")
        return False  # Return failure with unchanged state


@dataclass
class MugPuzzle:
    """A puzzle where the player has to solve a deduction riddle to find their lucky UofT mug."""

    def barista_dialogue(self, moves: Moves) -> bool:
        """Initiates a dialogue with the player and the Starbucks Barista."""

        typewriter_effect("You approach the counter, hoping the barista remembers you..."
                          "\nIt seems like you might be missing something from your last visit."
                          "\n(Hint: Try asking about your \033[1mMUG\033[0m specifically!)")

        time.sleep(1)

        typewriter_effect("\nBarista: 'Oh hey! I remember you! You were here pretty late yesterday. "
                          "\nDid you need help with something?'")

        while True:
            player_response = input("Enter your question: ").strip().lower()

            if 'mug' in player_response:
                typewriter_effect("\nBarista: Oh! You’re looking for a mug? That sounds familiar... "
                                  "I might be able to help!"
                                  "\nBut first, can you give me your order number for confirmation?")
                break
            else:
                typewriter_effect("\nBarista: Hmm... I don't think I can help with that. "
                                  "Are you sure you're asking about the right thing?")
                moves.decrease(1)
                print(f"{RED}\033[1mMOVES DECREASED: -{1}\033[0m{RESET}")

        attempts = 3
        while attempts > 0:
            order_number = input("Please type in your order number: ").strip()

            if order_number == "7069":
                typewriter_effect("\nBarista: Got it! Your mug should be here... but there’s just one problem.")
                typewriter_effect("\nBarista: You see, I have a bit of a habit of mixing things up, "
                                  "and now the mugs are all jumbled. \nCan you help me figure out which one is yours?")
                break
            else:
                attempts -= 1
                moves.decrease(1)
                print(f"{RED}\033[1mMOVES DECREASED: -{1}\033[0m{RESET}")
                if attempts > 0:
                    typewriter_effect(f"\nBarista: Oops, that doesn’t seem right. You have {attempts} attempts left.")
                else:
                    typewriter_effect("\nBarista: Hmm... I don’t think I can help without the right number. "
                                      "Maybe check your receipt and come back?")
                    return False

        # Ask if they want to solve the puzzle
        while True:
            player_answer = input("What do you say? (Answer yes/no): ").strip().lower()
            if player_answer == "no":
                typewriter_effect("\nBarista: Well... looks like your mug is on its own adventure!")
                return False  # Return False if the player refuses to play
            elif player_answer == "yes":
                return self.solve_mug_puzzle(moves)  # Return True if they solve the puzzle
            else:
                typewriter_effect("\nBarista: Hmm, I didn’t quite get that. "
                                  "Please answer with 'yes' or 'no'! Let’s try again: ")

        return False

    def solve_mug_puzzle(self, moves: Moves) -> bool:
        """Plays a puzzle where the player deducts which one is their lucky mug.
        Returns True if the player solves it correctly, False otherwise.
        """
        clues = [
            "The person who ordered the espresso definitely doesn’t have the pink mug.",
            "The cat mug was used by the person who ordered latte.",
            "The person who has the UofT mug is not the one who ordered the cappuccino.",
            "The person who ordered vanilla latte definitely doesn’t have the green mug.",
            "Customer C didn’t get the cat mug.",
            "The pink mug belongs to the person who ordered the vanilla latte."
        ]

        correct_solution = {
            'A': 'cat',
            'B': 'green',
            'C': 'pink',
            'D': 'uoft'
        }

        print("\n\n\033[1mPUZZLE: Help the barista match customers with their mugs!\033[0m")
        time.sleep(1)

        typewriter_effect("You have to match the customers to the mugs. Here are the clues:")
        for clue in clues:
            print(f"- {clue}")
            time.sleep(1)

        attempts = 3  # Player gets 3 tries
        while attempts > 0:
            typewriter_effect(f"\nYou have {attempts} attempt(s) left.")
            typewriter_effect("Enter your guesses for each customer:")
            typewriter_effect("Options: Green, Pink, UofT, Cat")

            customer_a_mug = input("\nCustomer A (Latte): Which mug does Customer A get? ").strip().lower()
            customer_b_mug = input("Customer B (Cappuccino): Which mug does Customer B get? ").strip().lower()
            customer_c_mug = input("Customer C (Vanilla latte): Which mug does Customer C get? ").strip().lower()
            customer_d_mug = input("Customer D (Espresso): Which mug does Customer D get? ").strip().lower()

            guesses = {
                'A': customer_a_mug,
                'B': customer_b_mug,
                'C': customer_c_mug,
                'D': customer_d_mug
            }

            if guesses == correct_solution:
                typewriter_effect("\nBarista: 🎉 Congrats! You matched all the customers with their mugs correctly! "
                                  "You've found your mug!")
                return True  # Player wins

            typewriter_effect("\nBarista: oops! Some of your guesses were incorrect. Try again!")
            attempts -= 1
            moves.decrease(2)
            print(f"{RED}\033[1mMOVES DECREASED: -{2}\033[0m{RESET}")

        typewriter_effect("\nBarista: You've used all your attempts! Looks like your mug remains lost in the mix :(")
        return False  # Player loses


@dataclass
class ConnectionsPuzzle():
    """A Connections puzzle where the player has to guess word associations.

    Instance Attributes:
        - categories: A dictionary of 4 categories that maps to a list of 4 associating words.
        - words: A list that contains all the words in categories in order.
        - solved_categories: A set that tracks the categories solved by the player so far.
        - solved_words: A set representing the words that are already grouped in the right category.
        - max_attempts: An integer representing the maximum number of attempts at solving the puzzle.


    Representation Invariants:
        - self.categories != {}
        - self.words != []
        - self.max_attempts > 0
    """
    categories: dict[str, list[str]]
    words: list[str]
    solved_categories: set[str]
    solved_words: set[str]
    max_attempts: int

    def __init__(self) -> None:
        """Initialize a new Connections Puzzle."""
        # Word categories and their associated words
        self.categories = {
            "Two of a Kind": ["Binary", "Twin", "Pair", "Clone"],
            "97th Oscar Nominated Films": ["Conclave", "Wicked", "Anora", "Nosferatu"],
            "Having 8 of Something": ["Octopus", "Arachnids", "Octagon", "Medium pizza slices"],
            "One__": ["Way Ticket", "Size Fits All", "Night Stand", "Hit Wonder"]
        }

        self.words = [word for category in self.categories.values() for word in category]
        random.shuffle(self.words)  # Reorders the words to create the shuffled grid

        self.solved_categories = set()

        self.solved_words = set()

        self.max_attempts = 5

    def game_introduction(self) -> None:
        """Plays a dialogue from the librarian to introduce the Connections puzzle to the player."""

        typewriter_effect("\n\033[3mYou walk towards the Librarian, who eyes you with a sense of suspicion...\033[0m")

        typewriter_effect(
            "\n\nLibrarian: Ah, I see you're on a quest for something important. But not so fast."
            "\nAs a UofT student, I expect you to rise to my academic standards."
            "\nAs a wise man once said: 'Language is the thread that binds us "
            "together across time and space,'"
            "It connects us in ways words alone cannot explain.'"
            "\nSo here’s a challenge to sharpen your mind. I’ll give you 16 random words."
            "\nYour task? Group them into 4 categories based on their hidden connections."
            "\nSolve this, and you’ll be one step closer to the answer you seek."
        )
        time.sleep(1)

        input("\nPress Enter to begin..\n")

    def display_grid(self) -> None:
        """Displays the shuffled grid of 16 words (4x4), highlighting solved words."""
        typewriter_effect("\nHere's your shuffled grid of words:")
        time.sleep(1)
        for i in range(0, 16, 4):
            row = self.words[i:i + 4]
            row_display = [f"\033[1m{word}\033[0m" if word in self.solved_words else word for word in row]
            print(f"\n{row_display[0]:<20} {row_display[1]:<20} {row_display[2]:<20} {row_display[3]:<20}")
        print()

    def check_guess(self, guess: str) -> list:
        """Checks the player's guess and gives feedback."""
        correct_categories = []
        guessed_words = set(guess)

        for category, words in self.categories.items():
            if guessed_words == {word.lower() for word in words}:
                correct_categories.append(category)

        return correct_categories

    def play_game(self, moves: Moves) -> bool:
        """Runs the connections puzzle."""
        self.game_introduction()

        print("\033[1mHere is a reminder of how the game works!\033[0m")
        time.sleep(1)

        print("\nYour task is to group 4 words into categories.")
        time.sleep(1)

        print("\nYou have 5 guesses to figure out all the categories.")
        time.sleep(1)

        print("\nEach guess will be checked for one category at a time.")
        time.sleep(1)

        print("\nGood luck!")
        time.sleep(1.5)

        self.display_grid()

        attempts = 0
        remaining_words = self.words[:]

        while attempts < self.max_attempts and len(self.solved_categories) < len(self.categories):
            print("\nCurrent Words: ", ", ".join(sorted(remaining_words)))

            # Store the player's guess
            guess = input("\nEnter 4 words you think belong together, separated by commas: ").strip().lower().split(",")
            guess = [word.strip() for word in guess]

            # Check if guess is valid
            if len(guess) != 4 or not all(any(word.lower() == w.lower() for w in remaining_words) for word in guess):
                typewriter_effect("\nLibrarian: Hmm... That doesn't seem quite right. Try again.")
                continue

            # Check if the guess matches a category
            category_found = False
            for category, words in self.categories.items():
                if category not in self.solved_categories and set(guess) == set(word.lower() for word in words):
                    self.solved_categories.add(category)
                    self.solved_words.update(words)
                    remaining_words = [word for word in remaining_words if word not in words]
                    print(f"\nLibrarian: Well done! You discovered the category: {category}.\n")
                    category_found = True
                    break  # Stop checking other categories

            if not category_found:
                correct_guesses = sum(1 for word in guess if any(word in category_words
                                                                 for category_words in self.categories.values()))

                if correct_guesses == 3:
                    print("\nLibrarian: So close! One of your words is incorrect.")
                elif correct_guesses == 2:
                    print("\nLibrarian: Almost there! Two of your words are incorrect.")
                elif correct_guesses == 1:
                    print("\nLibrarian: Almost there! Three of your words are incorrect.")
                else:
                    print("\nLibrarian: Hmmm..that is not a category I had in mind. Try again!")

                time.sleep(2)

                attempts += 1
                moves.decrease(2)  # Deduct player's total number of moves by 2 for each attempt
                print(f"{RED}\033[1mMOVES DECREASED: -{2}\033[0m{RESET}")

            if len(self.solved_categories) == len(self.categories):
                print("Congratulations! You've solved all categories!")
                guess_room_number = self.guess_room_number(moves)
                if guess_room_number:
                    return True  # The player successfully completed the puzzle

            self.display_grid()

        print("Game Over! Better luck next time.")
        return False  # The player failed to complete the puzzle

    def guess_room_number(self, moves: Moves) -> bool:
        """Displays text for the player to guess the room number if they solve the Connections puzzle.

        Preconditions:
            - self.play_game() == True
        """
        typewriter_effect("\nHere are the solved categories: ")
        time.sleep(1)
        for category in self.solved_categories:
            print("-", category)

        typewriter_effect(
            "Librarian: Ah, sharper than I took you for at first glance!"
            "\nAs a small reward, I’ll give you a chance."
            "\nThese categories may seem scattered and wide,"
            "\nBut don’t be so quick to cast them aside."
            "\nArrange them numbers ascendingly, don’t let them stray—"
            "\nYour roommate’s location is hidden that way!"
        )

        while True:
            player_guess = input("\nWhich study room do you think your roommate is in? (hint: 2XXXXX) ")

            if player_guess.strip() == "212789":
                print("\nCorrect! Let's take our journey there!")
                return True
            else:
                print("\nNot quite there... Try again!")
                moves.decrease(1)

        return False

    def roommate_dialogue(self) -> None:
        """Initiate dialogue from roommate once player reaches the hidden study room."""

        # Inform player about the laptop charger
        typewriter_effect("Roommate: OMG! You finally made it! Here’s your laptop charger.")
        time.sleep(1)

        # Hint to player about Bahen Centre
        typewriter_effect(
            f"\nRoommate: I’ve been holed up in Robarts for hours, and honestly, I’m craving a change of scenery. "
            f"\nYou know, there’s this spot on campus where {BLUE}\033[1mB\033[0m{RESET}ooks and "
            f"late-night study sessions thrive, "
            f"\nwhere {BLUE}\033[1mA\033[0m{RESET}ll-nighters somehow feel a little less brutal, "
            f"and {BLUE}\033[1mH\033[0m{RESET}ackers are always on the go. "
            f"\nIt's one of the quietest, most focused places to be—ideal for someone like you, "
            f"always chasing the next big idea. "
            f"\nTrust me, you could lose yourself in there for hours. "
            f"\nThere’s this constant {BLUE}\033[1mE\033[0m{RESET}nergy, and the best part? "
            f"No Wi-Fi worries, just uninterrupted productivity. "
            f"\nIt feels like {BLUE}\033[1mN\033[0m{RESET}ever-ending inspiration. "
            f"\nHonestly, it's the kind of place you won’t miss once you know it’s there. You should check it out!"
        )


@dataclass
class CaesarCipher:
    """A puzzle where the player has to solve for a key to unlock the Lost and Found door.

    Instance Attributes:
        - shift_key: An integer representing the number of positions each letter is shifted in the cipher.
        - encrypted_message: A string containing the encrypted message using the Caesar cipher.
        - alphabet: A string containing the alphabet used for encryption and decryption.

    Representation Invariants:
        - 0 <= shift_key <= 25
    """
    shift_key: int
    alphabet: str
    encrypted_message: str

    def __init__(self, shift_key: int, encrypted_message: str) -> None:
        """Initialize a an instance of CaesarCipher."""
        self.shift_key = shift_key
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.encrypted_message = encrypted_message

    def encrypt(self, text: str) -> str:
        """Encrypt the given text using the Caesar Cipher."""
        encrypted_text = []
        for char in text.upper():
            if char in self.alphabet:
                new_index = (self.alphabet.index(char) + self.shift_key) % len(self.alphabet)
                encrypted_text.append(self.alphabet[new_index])
            else:
                encrypted_text.append(char)
        return ''.join(encrypted_text)

    def decrypt(self, text: str, shift: int) -> str:
        """Decrypt the given text using the Caesar Cipher."""
        decrypted_text = []
        for char in text.upper():
            if char in self.alphabet:
                new_index = (self.alphabet.index(char) - shift) % len(self.alphabet)
                decrypted_text.append(self.alphabet[new_index])
            else:
                decrypted_text.append(char)
        return ''.join(decrypted_text)

    def unlock_door(self, moves: Moves) -> bool:
        """Start the game where the player guesses the key to unlock the Lost and Found door."""

        attempts = 0  # player has 3 attempts
        while attempts < 3 and moves.moves > 0:
            try:
                # Prompt for the key
                guessed_key = int(input("Enter the key to unlock the door: "))
                decrypted_message = self.decrypt(self.encrypted_message, guessed_key)

                # Check if the decrypted message makes sense
                if "HELLO WORLD" in decrypted_message:
                    print(f"Congratulations! You've unlocked the Lost and Found. The message says: {decrypted_message}")
                    return True  # Exit the game after a correct answer
                else:
                    print("The decryption didn't work. Try again.")
                    attempts += 1
                    moves.decrease(1)  # Reduce the remaining moves for each attempt
                    print(f"{RED}\033[1mMOVES DECREASED: -{1}\033[0m{RESET}")
            except ValueError:
                print("Invalid input. Please enter a number.")

        if attempts == 3:
            print("Sorry, you've used all your attempts. Better luck next time.")
        else:
            print("Sorry, you've run out of moves. Better luck next time.")

        return False


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
