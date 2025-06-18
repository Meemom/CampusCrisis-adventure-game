"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations

# Standard library imports
import json
import time
from typing import Optional
from dataclasses import dataclass

# Project-specific imports
from additional_functions import typewriter_effect
from game_entities import Location, Item, Score, Moves
from proj1_event_logger import Event, EventList

# Global constants for text colors
RED = "\033[31m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
RESET = "\033[0m"


@dataclass
class GameState:
    """Represents the current state of the game, tracking the player's score and remaining moves.

    Instance Attributes:
        - score: A Score object that tracks the player's current score.
        - moves: A Moves object that tracks the number of remaining moves the player can make.

    Representation Invariants:
        - self.score >= 0
        - self.moves >= 0
    """
    score: Score
    moves: Moves


@dataclass
class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: The ID of the player's current location.
        - ongoing: A boolean indicating if the game is ongoing (True) or ended (False).
        - score: A Score object that tracks the player's current score.
        - moves: A Moves object that tracks the remaining number of moves the player can make.
        - inventory: A list of Item objects representing the player's collected items.
        - game_state: A GameState object that manages the overall game state, including
          score and remaining moves.

    Representation Invariants:
        - self.current_location_id in self._locations
        - self._locations != {}
        - self._items != []
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.
    #   - _game_log: an EventList object that keeps track of all the player's actions in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    _game_log: EventList
    inventory: list[Item]
    current_location_id: int
    ongoing: bool
    game_state: GameState

    def __init__(self, game_data_file: str, initial_location_id: int, moves: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)
        self._game_log = EventList()
        self.inventory = []

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing
        self.game_state = GameState(score=Score(), moves=Moves(moves))

    # Handle choices in game menu
    def handle_menu_choice(self, menu_choice: str, adventure_game: AdventureGame) -> bool:
        """Handle user menu choices and return whether the game should continue."""
        if menu_choice == "look":
            print(self.get_location().long_description)  # Show current location's full description
        elif menu_choice == "inventory":
            adventure_game.get_inventory()  # Show the inventory contents
        elif menu_choice == "score":
            print(f"{YELLOW}\033[1mCURRENT SCORE: {self.game_state.score}\033[0m{RESET}")
        elif menu_choice == "undo":
            adventure_game.undo_move()  # Undo the last move
        elif menu_choice == "log":
            adventure_game.log()  # Show all events in the game log
        elif menu_choice == "quit":
            self.quit_game()  # End the game
        elif menu_choice == "moves":
            print(f"{RED}\033[1mMOVES LEFT: {self.game_state.moves}\033[0m{RESET}")
        elif menu_choice == "drop":
            adventure_game.remove_from_inventory(location)  # Drop the given item
        else:
            print("Please choose a valid option.")
            return True
        return False

    # Menu Helper Functions
    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return the Location object associated with the provided location ID."""
        if loc_id is None:
            return self._locations[self.current_location_id]
        else:
            return self._locations[loc_id]

    def add_event_to_log(self, current_location: Location,
                         action_choice: Optional[str] = None, event_item: Optional[Item] = None) -> None:
        """Add a new event to the game log based on the player's actions."""
        if event_item is not None:  # Log an item action (pick up or drop)
            self._game_log.add_event(Event(id_num=current_location.id_num, description=None, item=event_item,
                                           next_command=action_choice))
        else:  # Log a location change (movement)
            self._game_log.add_event(Event(id_num=current_location.id_num, description=location.long_description,
                                           next_command=action_choice, item=None))

    def get_inventory(self) -> None:
        """Prints all the items (name and description) currently in the player's inventory."""
        if not self.inventory:
            print("There are currently no items in your inventory.")
        else:
            print("The following items are in your inventory: \n")
            for inv_item in self.inventory:
                cleaned_description = inv_item.description.replace("\n", " ")  # Remove new lines in description
                print(f"- {inv_item.name}: {cleaned_description}")

    def remove_from_inventory(self, current_location: Location, curr_item: Optional[Item] = None) -> None:
        """Remove an item from the inventory and drop it at the current location.

        1. If item is None, then the function is being called by the player from the menu choices.
        2. If item is not None, then the function is being called from the undo function.
        """
        if curr_item is not None:
            # Check if item exists in the inventory
            if not any(inv_item.name == curr_item.name for inv_item in self.inventory):
                print(f"{curr_item.name} is not in the inventory.")
                return

            # Item exists in inventory, so remove it and add it to the location
            self.inventory.remove(curr_item)
            location.items.append(curr_item)
            self.add_event_to_log(current_location=location, event_item=curr_item)
            print(f"{curr_item.name} has been dropped at the location.")

        elif curr_item is None:  # Ask Player for the item to drop
            response = input("What is the name of the item you would like to drop at this location? ").strip().lower()

            # Find the item instance in inventory
            item_to_remove = next((inv_item for inv_item in self.inventory if inv_item.name.lower() == response), None)

            if item_to_remove is not None:
                # Remove item from inventory and add it to location
                self.inventory.remove(item_to_remove)  # Remove the correct instance
                current_location.items.append(item_to_remove)  # Add the item to the location
                self.add_event_to_log(current_location=location, event_item=item_to_remove)  # Log the event
                print(f"{item_to_remove.name} has been dropped at the location.")
            else:
                print("Item not found in inventory.")  # Notify the player if the item is not in inventory

    def undo_move(self) -> None:
        """Undo the last move made by the player."""
        if self._game_log.is_empty():
            print("No actions to undo.")
            return

        last_event = self._game_log.last  # Get the last event
        print(f"Last event: {last_event}")  # Debugging line

        if last_event.item is None:  # Undo location movement
            if last_event.prev is not None:
                self.current_location_id = last_event.prev.id_num
                # Ensure we are correctly setting the location back before calling `get_location`
                previous_location = self.get_location(self.current_location_id)
                print(f"You are moved back to {previous_location.name}.")
            else:
                print("No previous location to return to.")

        else:
            if last_event.item in self.inventory:  # Undo item pickup (Drop the item to the current location)
                self.remove_from_inventory(location, last_event.item)
                self.get_location().items.append(last_event.item)
                print(f"Dropped {last_event.item.name} back at {self.get_location().name}.")
            else:  # Undo item drop (Pick the item back up)
                self.get_location(last_event.id_num).items.remove(last_event.item)
                self.inventory.append(last_event.item)
                print(f"Picked {last_event.item.name} back up.")

        self._game_log.last = last_event.prev

        self.game_state.moves.increase(1)  # Increase the number of moves left
        print(f"{YELLOW}\033[1mEARNED POINTS: +{1}\033[0m")

    def log(self) -> None:
        """Display all events in the game log."""
        self._game_log.display_events()

    def quit_game(self) -> None:
        """Quit the game and display the score."""
        print(f"{RED}Thanks for playing! Your score was: {self.game_state.score}{RESET}")
        self.ongoing = False

    def handle_non_menu_choice(self, nonmenu_choice: str, current_location: Location) -> None:
        """Handle non-menu choices based on location-specific commands.

        Preconditions:
            - a pickup action has a command that leads to None.
            - a "special" action is a command that leads to None and its location is in location_commands
        """

        # A mapping of a location id to its specific function to handle special actions in the location
        location_commands = {
            3: (location.location_3_commands, [nonmenu_choice, self.inventory]),
            5: (location.sublocation_5_commands, [nonmenu_choice, self.game_state.moves, self.game_state.score,
                                                  self.inventory]),
            6: (location.sublocation_6_commands, [nonmenu_choice, self.game_state.moves, self.game_state.score,
                                                  self.inventory]),
            8: (location.location_8_commands, [nonmenu_choice, self.game_state.moves, self.inventory,
                                               self.game_state.score]),
            11: (location.sublocation_11_commands, [nonmenu_choice]),
            12: (location.sublocation_12_commands, [nonmenu_choice, self.game_state.moves, self.inventory,
                                                    self.game_state.score])
        }

        # Check if the choice is a valid command
        valid_choice = current_location.available_commands[nonmenu_choice]

        if valid_choice is None:
            if self.current_location_id not in location_commands:  # PICK UP
                pickup = current_location.handle_pickup_item(nonmenu_choice, self.inventory)
                if pickup:  # Log only if an item was actually picked up
                    self.add_event_to_log(current_location, nonmenu_choice, pickup)
            else:  # SPECIAL ACTION
                func, args = location_commands[self.current_location_id]
                func(*args)  # Call the function with arguments

                self.add_event_to_log(current_location, nonmenu_choice)

                # log if this wasn't a pickup action
                if self.current_location_id in location_commands:
                    self.add_event_to_log(current_location, nonmenu_choice)

        else:  # CHANGE LOCATION
            new_location_id = location.available_commands.get(nonmenu_choice)
            if new_location_id is not None:
                self.current_location_id = new_location_id

                # If location-specific functions exist, call them
                if self.current_location_id in location_commands:
                    func, args = location_commands[self.current_location_id]
                    func(*args)

                self.add_event_to_log(current_location, nonmenu_choice)

            # Mark the location as visited and decrease moves
            current_location.visited = True  # Mark the new location as visited
            self.game_state.moves.decrease(1)  # Decrease the moves

    # Assign each location object an list of Item objects, if it has any.
    def assign_location_items(self, locations: dict[int, Location], items: list[Item]) -> None:
        """Assign each Location object to an Items object."""
        # Create a dictionary mapping the item.id_num to the corresponding Item object
        dict_items = {item.id_num: item for item in items}

        # Iterate over each location and assign the items based on id_num
        for loc in locations.values():
            if loc.items:  # Check if loc.items is not None or empty
                # Replace item ids with the corresponding Item objects in a single step
                loc.items = [dict_items[item_id] for item_id in loc.items if item_id in dict_items]

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations
        mapping each game location's ID to a Location object, and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id_num'], loc_data['name'], loc_data['brief_description'],
                                    loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'], loc_data['visited'],
                                    loc_data['sub_locations'])
            locations[loc_data['id_num']] = location_obj

        items = []
        for item_data in data['items']:  # Go through each element associated with the 'items' key in the file
            item_object = Item(item_data['name'], item_data['id_num'], item_data['description'],
                               item_data['start_position'], item_data['target_position'])
            items.append(item_object)

        return locations, items


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    # Ask for the player's name at the start of the game
    player_name = None
    while not player_name:
        player_name = input("What is your name, adventurer? ").strip()
        if not player_name:
            print("Please enter a valid name!")

    # while True:
    #     player_name = input("What is your name, adventurer? ").strip()
    #     if player_name:
    #         break
    #     print("Please enter a valid name!")

    MAX_MOVES = 35
    WINNING_ITEM_COUNT = 4

    # Initialize the game
    game = AdventureGame('game_data.json', 1, MAX_MOVES)  # Load data, set initial location ID to 1
    game.assign_location_items(game._locations, game._items)

    # Define menu options available at each location
    menu = ["look", "inventory", "score", "undo", "log", "quit", "moves", "drop"]

    choice = None

    # Track the first location
    first_location_id = game.current_location_id
    first_location = game.get_location(first_location_id)

    # Print a welcome message to the player
    def start_game(playername: str) -> None:
        """Initiate the welcome dialogue of the game."""
        print(f"{MAGENTA}\033[1mWELCOME TO THE CS QUEST, {playername.upper()}!\033[0m{RESET}")
        input("Press Enter to start game...")

        print("The clock is ticking—you’ve only got a few hours left to finish your CS project "
              "before the 4 PM deadline, and things aren’t looking great.")

        print("\nAfter a quick nap (because, let’s be real, you \033[3mdefinitely\033[0m needed it),"
              " you wake up in a panic. ")

        print("\nYour \033[1mT-Card, USB drive, laptop charger, and your lucky UofT mug\033[0m "
              "are nowhere to be found.")

        print("\nYour project, your grade, and your friendship with your partner are all on the line.")

        print("\nYou’re in your dorm at University College, "
              "but you’ll need to venture out into campus to "
              "track down what’s missing—before time runs out.")

        print("\nCan you recover everything in time and finish your project? "
              f"\n\n{RED}\033[1mREMEMBER!{RESET}\033[0m {RED}To win the game, you must find all the target items "
              f"and return them to your dorm to click{RESET} {RED}\033[1m'SUBMIT PROJECT'\033[0m{RESET}"
              "\n\nIt’s crunch time, and the pressure is on!")

        input(f"{MAGENTA}\n\033[1mPress Enter when you're ready!\033[0m{RESET}")

    start_game(player_name)

    while game.ongoing:

        location = game.get_location()  # Get current location

        game.add_event_to_log(location, choice)

        # Show location description depending on whether it's been visited before.
        if location.visited:
            if location.brief_description != "":
                print(f"{BLUE}\n{location.brief_description}{RESET}")
        else:
            print(f"{BLUE}\n{location.long_description}{RESET}")

        time.sleep(1)

        # Display possible actions at this location
        print(f"{MAGENTA}\nWhat now? Remember to choose wisely!{RESET}")
        print("Available actions: look, inventory, score, undo, log, quit, moves, drop")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input(f"{MAGENTA}\nEnter action: {RESET}").strip().lower()
        while choice not in [cmd.lower() for cmd in location.available_commands] and choice not in menu:
            print(
                f"Available commands: {list(location.available_commands.keys())}")
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").strip().lower()

        print("========")
        print(f"{MAGENTA}You decided to: {choice}{RESET}")
        if choice in menu:
            if not game.handle_menu_choice(choice, game):
                pass  # Exit the while loop
        else:
            game.handle_non_menu_choice(choice, location)

        # Add score each time an item is brought to its target position
        for item in game.inventory:
            if item.target_position == game.current_location_id:
                game.game_state.score.increase(2)

        if first_location and first_location.items is not None:
            correctly_placed_items = sum(
                1 for loc_item in first_location.items if loc_item.target_position == first_location_id)

            # Winning condition: Check if all target items have been correctly placed
            if correctly_placed_items == WINNING_ITEM_COUNT:
                submit = input("Finally, type 'SUBMIT PROJECT' to finalize: ").strip().upper()
                if submit == "SUBMIT PROJECT":
                    print(f"{RED}\033[1mCONGRATULATIONS! You've placed all the items correctly and"
                          f"won the game with {game.game_state.score} points and with"
                          f"{game.game_state.moves}! Well played!\033[0m{RESET}")
                    game.ongoing = False  # End the game
                else:
                    print("You need to type 'SUBMIT PROJECT' exactly to submit!")

        # Losing condition: Check if moves have run out
        if game.game_state.moves.moves <= 0:
            typewriter_effect(f"{RED}\033[1mGAME OVER! You ran out of moves. Please try again!\033[0m{RESET}")
            game.ongoing = False  # End the game

    print(f"{RED}\033[1mGAME HAS ENDED.\033[0m{RESET}")
