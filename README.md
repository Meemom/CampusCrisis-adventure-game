# Campus Crisis: A Text Adventure Game

## Overview
**Campus Crisis** is an engaging text-based adventure game where you play as a university student racing against time to complete your CS project before the 4 PM deadline. After waking up from a much-needed nap, you discover that four essential items are missing: your **T-Card, USB drive, laptop charger, and lucky UofT mug**. With only 35 moves to spare, you must navigate the University College campus, recover your lost items, and return them to your dorm before time runs out!

## Game Objective
Find all four target items scattered across campus and return them to your dorm room. Once all items are correctly placed, type **'SUBMIT PROJECT'** to win the game. But beware—if you run out of moves before completing your mission, it's game over!

## How to Play

### Starting the Game
1. Run the main game file (`adventure.py`)
2. Enter your name when prompted
3. Read the introduction carefully—it sets the scene for your adventure
4. Press Enter to begin your quest

### Game Controls
At each location, you'll have access to these commands:

**Menu Commands (available everywhere):**
- `look` - View the full description of your current location
- `inventory` - Check what items you're carrying
- `score` - Display your current score
- `moves` - See how many moves you have left
- `undo` - Reverse your last action
- `drop` - Drop an item at your current location
- `log` - View a history of your actions
- `quit` - Exit the game

**Location-Specific Actions:**
- Each location offers unique actions (e.g., "go north", "pick up item", "examine object")
- Available actions are displayed when you enter a location

### Scoring System
- Earn **+2 points** each time you bring an item to its target location
- Gain **+1 point** when you undo a move
- Your final score reflects your efficiency and success

### Winning Conditions
✅ Collect all 4 target items  
✅ Return them to your dorm (starting location)  
✅ Type **'SUBMIT PROJECT'** to finalize your submission  

### Losing Conditions
❌ Running out of moves (you have 35 total)  
❌ Failing to collect all items before time expires

## Game Features

### Strategic Exploration
Navigate through multiple campus locations, each with its own unique description and available actions. Some locations contain special interactive elements that require specific commands.

### Inventory Management
Manage your collected items strategically. You can pick up items, drop them at different locations, and use the undo feature if you make a mistake.

### Event Logging
The game automatically tracks all your actions. Use the `log` command to review your journey and help plan your next moves.

### Time Pressure
With only 35 moves available, every decision counts. Plan your route carefully and avoid unnecessary backtracking to maximize your chances of success.

## Installation & Requirements
```python
# Required Python version: 3.7+
# Required modules: json, time, typing, dataclasses

# To run the game:
python game_manager.py
```

## Credits
This game was created as part of CSC111 at the University of Toronto St. George campus.
