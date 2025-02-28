# Terminal TypeXtream Documentation

## Overview
Terminal TypeXtream is a terminal-based typing test application built using Python and the `curses` library. It provides an engaging way for users to improve their typing skills by offering different typing test categories, real-time feedback, and a persistent leaderboard for tracking progress.

## Dependencies
- `curses`: For handling the terminal-based user interface.
- `json`: For storing and retrieving leaderboard data.
- `random`: For generating random word selections.
- `time`: For calculating typing speed.
- `about_me`: A custom module that displays information about the game.
- `game`: A custom module that contains the core typing test functionality.

## File Structure
- **Main Script**: Initializes the application and handles the UI.
- **Modules**:
  - `game.py`: Contains the typing test logic.
  - `leaderboard.json`: Stores the leaderboard data.

## Features
- **Typing Test**: Users can select categories such as words, strings, or alphanumeric strings to test their typing speed.
- **Real-time Feedback**: Displays correct and incorrect inputs as users type.
- **Leaderboard**: Scores are saved and can be viewed later.
- **User-Friendly UI**: Uses `curses` to create an interactive text-based interface.
- **Menu System**: Allows users to navigate between the test, leaderboard, about section, and exit options.

## Functions

### `draw_box(stdscr, y, x, height, width, color_pair)`
Draws a rectangular box on the screen.

**Parameters**:
- `stdscr`: The main window object for `curses`.
- `y`, `x`: Coordinates of the top-left corner of the box.
- `height`, `width`: Dimensions of the box.
- `color_pair`: Color scheme for the box.

---

### `draw_button(stdscr, y, x, label, selected, color_pair)`
Draws a button with a given label and highlights it if selected.

**Parameters**:
- `stdscr`: The main window object for `curses`.
- `y`, `x`: Coordinates of the button.
- `label`: Text displayed on the button.
- `selected`: Boolean flag indicating if the button is selected.
- `color_pair`: Color scheme for the button.

---

### `clear_leaderboard()`
Clears the leaderboard by overwriting `leaderboard.json` with an empty list.

---

### `load_leaderboard()`
Loads the leaderboard data from `leaderboard.json`.

**Returns**:
- A list of dictionaries containing `username` and `wpm` values.

---

### `save_leaderboard(leaderboard)`
Saves the leaderboard to `leaderboard.json`.

**Parameters**:
- `leaderboard`: A list of user scores.

---

### `show_leaderboard(stdscr)`
Displays the leaderboard in the terminal using `curses`.

**Parameters**:
- `stdscr`: The window object for displaying output.

---

### `choose_words(category)`
Retrieves a set of words based on the selected category.

**Parameters**:
- `category`: The word category (e.g., words, string, alphanumeric_string).

**Returns**:
- A list of randomly selected words.

---

### `typing_test(stdscr, username)`
Runs the typing test.

**Parameters**:
- `stdscr`: The window object for output.
- `username`: The player’s name.

**Functionality**:
- Displays a randomly chosen set of words.
- Tracks user input and compares it to the target text.
- Calculates WPM and updates the leaderboard.

---

### `post_test_menu(stdscr, username)`
Displays post-test options such as replaying the test or viewing the leaderboard.

**Parameters**:
- `stdscr`: The window object for output.
- `username`: The player's name.

---

### `game_main(stdscr)`
Initializes the game, handling user navigation and game logic.

**Parameters**:
- `stdscr`: The window object for output.

**Functionality**:
- Prompts the user for their username.
- Displays the menu for starting the game, viewing the leaderboard, or quitting.

---

### `main(stdscr)`
The main function that sets up the user interface and navigation.

**Parameters**:
- `stdscr`: The main window object.

**Functionality**:
- Initializes `curses` settings (e.g., hiding cursor, enabling color pairs).
- Draws the welcome message and menu buttons.
- Handles user input to navigate and select options.

---

## Execution
To start the application, run:

```python
if __name__ == "__main__":
    curses.wrapper(main)
```

This ensures that `curses` initializes and restores the terminal settings properly upon exit.

## Key Variables
- `buttons`: Stores the menu options.
- `selected_button`: Tracks the currently selected button index.
- `leaderboard`: Stores user scores.
- `categories_words`: Maps categories to lists of words.
- `target_text`: The text that the user needs to type.
- `user_input`: Tracks what the user has typed so far.

## Conclusion
Terminal TypeXtream offers an engaging, text-based typing experience with a structured UI, leaderboard, and category-based challenges. The use of `curses` allows for a smooth, visually appealing interface while keeping the program lightweight and efficient for terminal users.


## Usage


```
git clone https://github.com/CyberHorizonX/TypeXtreme.git

cd TypeXtream

(right click in the folder and click on terminal)

Run the program : python main.py
```

