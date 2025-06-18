"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

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
from proj1_event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str], moves: int) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id, moves)

        # Add first event
        # Hint: self._game.get_location() gives you back the current location
        initial_location = self._game.get_location()
        first_event = Event(id_num=initial_location.id_num,
                            description=initial_location.long_description,
                            prev=None)
        self._events.add_event(first_event)

        # Generate the remaining events based on the commands and initial location
        # Hint: Call self.generate_events with the appropriate arguments
        self.generate_events(commands, initial_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """

        for command in commands:
            if command in current_location.available_commands:
                next_location_id = current_location.available_commands[command]
                next_location = self._game.get_location(next_location_id) if next_location_id is not None else None

                if next_location:
                    new_event = Event(
                        id_num=next_location.id_num,
                        description=next_location.long_description,
                        next_command=command
                    )

                    self._events.add_event(new_event, command)
                    current_location = next_location

                else:  # command leads to None (no location) i.e. picking up or dropping items
                    new_event = Event(
                        id_num=current_location.id_num,
                        description="No valid next location",
                        next_command=command
                    )
                    self._events.add_event(new_event, command)

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east"])
        >>> sim.get_id_log()
        [1, 2]

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east", "go east", "buy coffee"])
        >>> sim.get_id_log()
        [1, 2, 3, 3]
        """

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    MAX_MOVES = 35

    # A list of commands that represent a path to win the game
    # These commands can be executed in order to successfully complete the game.
    win_walkthrough = [
        "look at desk", "pickup note", "pickup phone", "return to dorm", "search cabinet",
        "pickup starbucks receipt", "go outside", "go east", "go to second floor", "go outside", "go west",
        "find coach carter", "go outside", "go east", "go to second floor", "go to starbucks", "talk to the barista",
        "go to common room", "ask the librarian", "go to first floor", "go outside", "go north",
        "go to the lost and found", "go to cssu lounge", "eavesdrop on the students", "check table light",
        "go to the lost and found", "unlock door", "go outside", "go outside", "go south", "drop", "drop", "drop",
        "drop"]

    # A list of location IDs that correspond to the player's journey through the game.
    expected_log = [1, 9, 9, 9, 1, 10, 10, 2, 3, 3, 2, 8, 8, 2, 3, 3, 2, 7, 12, 11, 11, 11, 12, 12, 7, 2, 1]

    sim = AdventureGameSimulation('game_data.json', 1, win_walkthrough, MAX_MOVES)
    assert expected_log == sim.get_id_log()

    # A list of commands that will lead to a 'game over' state due to the player exhausting all attempts at a puzzle.
    # This simulates a scenario where too many moves are made, resulting in failure.
    lose_demo = [
        'look at desk', 'pickup note', 'return to dorm', 'search cabinet', 'pickup starbucks receipt',
        'return to dorm', 'moves', 'go outside', 'go east', 'go to second floor', 'go to second floor',
        'go outside', 'go west', 'find coach carter', 'find coach carter', 'go outside',
        'go west', 'find coach carter', 'find coach carter', 'go outside', 'go east', 'go to second floor',
        'go to second floor', 'go to starbucks', 'talk to the barista', 'inventory', 'talk to the barista'
    ]

    # The expected sequence of locations visited in the "lose" scenario.
    expected_log = [1, 9, 9, 1, 10, 10, 1, 2, 3, 3, 3, 2, 8, 8, 8, 2, 8, 8, 8, 2, 3, 3, 3]
    sim = AdventureGameSimulation('game_data.json', 1, lose_demo, MAX_MOVES)
    assert expected_log == sim.get_id_log()

    # A demo of checking the player's inventory.
    inventory_demo = ["look at desk", "pickup note", "pickup phone", "inventory", "drop", "inventory"]
    expected_log = [1, 9, 9, 9]
    sim = AdventureGameSimulation('game_data.json', 1, inventory_demo, MAX_MOVES)
    assert expected_log == sim.get_id_log()

    # A demo of checking the player's score during the game.
    scores_demo = ["look at desk", "pickup phone", "return to dorm", "go outside", "go west",
                   "find coach carter", "score"]
    expected_log = [1, 9, 9, 1, 2, 8, 8]
    sim = AdventureGameSimulation('game_data.json', 1, scores_demo, MAX_MOVES)
    assert expected_log == sim.get_id_log()

    # typewriter effect
    enhancement1_demo = [
        "go outside", "go west", "find coach carter"
    ]
    expected_log = [1, 2, 8, 8]
    sim = AdventureGameSimulation('game_data.json', 1, enhancement1_demo, MAX_MOVES)
    assert expected_log == sim.get_id_log()

    # A demo showcasing the interdependent puzzles: Treadmill Puzzle, Mug Puzzle, and Connections Puzzle.
    # These puzzles are interconnected and cannot be solved individually without progressing through each part.
    enhancement2_demo = ["look at desk", "pickup note", "pickup phone", "return to dorm", "search cabinet",
                         "pickup starbucks receipt", "go outside", "go east", "go to second floor", "go outside",
                         "go west", "find coach carter", "go outside", "go east", "go to second floor",
                         "go to starbucks", "talk to the barista", "go to common room", "ask the librarian"]
    expected_log = [1, 9, 9, 9, 1, 10, 10, 2, 3, 3, 2, 8, 8, 2, 3, 3]
    sim = AdventureGameSimulation('game_data.json', 1, enhancement1_demo, MAX_MOVES)
    assert expected_log == sim.get_id_log()

    # A demo for solving the Caesar Cipher puzzle.
    # The player must complete specific tasks in sequence to unlock the cipher solution.
    enhancement3_demo = [
        "go outside", "go north", "go to the lost and found", "go to cssu lounge",
        "eavesdrop on the students", "check table light", "go to the lost and found", "unlock door"
    ]
    expected_log = [1, 2, 7, 12, 11, 11, 11, 12, 12]
    sim = AdventureGameSimulation('game_data.json', 1, enhancement3_demo, MAX_MOVES)
    assert expected_log == sim.get_id_log()
