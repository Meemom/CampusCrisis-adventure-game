"""CSC111 Project 1: Text Adventure Game - Event Logger

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

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
from dataclasses import dataclass
from typing import Optional
from game_entities import Item


@dataclass
class Event:
    """
    A node representing one event in an adventure game.

    Instance Attributes:
    - id_num: Integer id of this event's location
    - description: Long description of this event's location
    - next_command: String command which leads this event to the next event, None if this is the last game event
    - next: Event object representing the next event in the game, or None if this is the last game event
    - prev: Event object representing the previous event in the game, None if this is the first game event
    - item: an Item Object that is found at this event's location.
    """

    # NOTES:
    # This is proj1_event_logger (separate from the ex1 file). In this file, you may add new attributes/methods,
    # or modify the names or types of provided attributes/methods, as needed for your game.
    # If you want to create a special type of Event for your game that requires a different
    # set of attributes, you can create new classes using inheritance, as well.

    id_num: Optional[int]
    description: Optional[str]
    next_command: Optional[str] = None
    next: Optional[Event] = None
    prev: Optional[Event] = None
    item: Optional[Item] = None


class EventList:
    """
    A linked list of game events.

    Instance Attributes:
        - first: Event object representing the first event in the game, or None if the list is empty.
        - last: Event object representing the last event in the game, or None if the list is empty.

    Representation Invariants:
        - self.first is not None and self.last is not None
        - self.first.prev == None
        - self.last.next == None
    """
    first: Optional[Event]
    last: Optional[Event]

    def __init__(self) -> None:
        """Initialize a new empty event list."""

        self.first = None
        self.last = None

    def display_events(self) -> None:
        """Display all events in chronological order."""
        curr = self.first
        while curr:
            print(f"Location: {curr.id_num}, Command: {curr.next_command}")
            curr = curr.next

    def is_empty(self) -> bool:
        """Return whether this event list is empty."""

        return self.first is None

    def add_event(self, event: Event, command: str = None) -> None:
        """Add the given new event to the end of this event list.
        The given command is the command which was used to reach this new event, or None if this is the first
        event in the game.
        """
        # Hint: You should update the previous node's <next_command> as needed
        if self.first is None:  # if the list is empty, the given event is both the first and last.
            self.first = event
            self.last = event
        else:  # if the list is not empty, add the new event to the end of the event list.
            self.last.next = event
            event.prev = self.last

            # if command is not None, update the next_command of the previous last event.
            if command is not None:
                self.last.next_command = command

            self.last = event  # Update the last event to be the given new event.

    def remove_last_event(self) -> None:
        """Remove the last event from this event list.
        If the list is empty, do nothing."""

        # Hint: The <next_command> and <next> attributes for the new last event should be updated as needed
        if self.is_empty():  # If the list is empty, do nothing.
            return
        elif self.first == self.last:  # If there is only one event in the list.
            self.first = None
            self.last = None
        else:  # If there is more than one event in the list.
            self.last = self.last.prev
            self.last.next = None
            self.last.next_command = None

    def get_id_log(self) -> list[int]:
        """Return a list of all location IDs visited for each event in this list, in sequence."""

        id_log = []  # Initialize a new empy list.
        curr = self.first  # Set curr to the first event in the list.
        while curr is not None:
            id_log.append(curr.id_num)  # Append the current event's id_num to id_log
            curr = curr.next  # Move to the next event

        return id_log


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
