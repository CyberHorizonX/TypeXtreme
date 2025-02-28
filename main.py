import curses
import json
from about_me import about_me  # Import the about_me function
from game import game_main #Import the game function

def draw_box(stdscr, y, x, height, width, color_pair):
    """Draw a box with the given dimensions and color."""
    stdscr.attron(curses.color_pair(color_pair))
    stdscr.addstr(y, x, '+' + '-' * (width - 2) + '+')
    for i in range(y + 1, y + height - 1):
        stdscr.addstr(i, x, '|' + ' ' * (width - 2) + '|')
    stdscr.addstr(y + height - 1, x, '+' + '-' * (width - 2) + '+')
    stdscr.attroff(curses.color_pair(color_pair))

def draw_button(stdscr, y, x, label, selected, color_pair):
    """Draw a button with the given label, highlighting if selected."""
    if selected:
        stdscr.attron(curses.color_pair(color_pair) | curses.A_BOLD | curses.A_REVERSE)
    else:
        stdscr.attron(curses.color_pair(color_pair))
    stdscr.addstr(y, x, '[' + label + ']')
    stdscr.attroff(curses.color_pair(color_pair) | curses.A_BOLD | curses.A_REVERSE)

def clear_leaderboard():
    with open("leaderboard.json", 'w') as file:
        json.dump([], file)  # Empty leaderboard


def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()
    stdscr.keypad(True)  # Enable keypad mode

    # Initialize color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)  # Welcome Box
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Message Box
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Button Normal
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)  # Button Selected

    # Screen dimensions
    screen_height, screen_width = stdscr.getmaxyx()

    # Define dimensions and positions
    # Welcome box
    welcome_box_height = 3
    welcome_box_width = 50
    welcome_box_y = 2
    welcome_box_x = (screen_width - welcome_box_width) // 2

    # Message box
    message_box_height = 12
    message_box_width = 70
    message_box_y = welcome_box_y + welcome_box_height + 2
    message_box_x = (screen_width - message_box_width) // 2

    # Buttons
    button_y = message_box_y + message_box_height + 2
    button_x_start = (screen_width - 60) // 2
    buttons = ["Start", "Quit", "About Me", "Clear Leaderboard"]
    button_positions = [button_x_start, button_x_start + 12, button_x_start + 24, button_x_start + 40]
    selected_button = 0  # Index of the selected button

    # Message text
    message_text = [
        "Get ready to test your speed, accuracy, and focus.",
        "Whether you're here to improve your typing skills or just have",
        "some fun, we're thrilled to have you.",
        "Let’s see how fast those fingers can fly!",
        "Feel free to tweak it to match the tone and style of your game.",
        "Encouraging phrases:",
        "- Every keystroke brings you closer to greatness!",
        "- Challenge yourself and beat your personal best!",
        "- The keyboard is your playground—let’s play!"
    ]

    # Ensure each line fits within the message box
    max_line_length = message_box_width - 4  # Account for borders and padding
    wrapped_text = []
    for line in message_text:
        if len(line) > max_line_length:
            # Split the line into chunks that fit within the box
            for i in range(0, len(line), max_line_length):
                wrapped_text.append(line[i:i + max_line_length])
        else:
            wrapped_text.append(line)

    while True:
        stdscr.clear()
        
        # Draw welcome box
        draw_box(stdscr, welcome_box_y, welcome_box_x, welcome_box_height, welcome_box_width, 1)
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(welcome_box_y + 1, welcome_box_x + (welcome_box_width - 28) // 2, "Welcome to the Typing Game")
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
        
        # Draw message box
        draw_box(stdscr, message_box_y, message_box_x, message_box_height, message_box_width, 2)
        stdscr.attron(curses.color_pair(2))
        for i, line in enumerate(wrapped_text):
            if i >= message_box_height - 2:  # Ensure text doesn't overflow the box
                break
            stdscr.addstr(message_box_y + 1 + i, message_box_x + 2, line)
        stdscr.attroff(curses.color_pair(2))
        
        # Draw buttons with selection highlight
        for i, button in enumerate(buttons):
            draw_button(stdscr, button_y, button_positions[i], button, selected_button == i, 4 if selected_button == i else 3)

        stdscr.refresh()
        key = stdscr.getch()

        # Navigate between buttons
        if key in [curses.KEY_LEFT, curses.KEY_RIGHT]:
            selected_button = (selected_button + (1 if key == curses.KEY_RIGHT else -1)) % 4  # Adjusted for 4 buttons
        elif key in [curses.KEY_ENTER, 10, 13]:  # Enter key
            if selected_button == 0:  # "Start" button
                game_main(stdscr)
            elif selected_button == 1:  # "Quit" button
                break
            elif selected_button == 2:  # "About Me" button
                about_me(stdscr)
            elif selected_button == 3:  # "Clear Leaderboard" button
                clear_leaderboard()
                stdscr.addstr(button_y + 2, button_x_start, "Leaderboard Cleared!", curses.color_pair(2))
                stdscr.refresh()
                curses.napms(1000)  # Pause for 1 second

        elif key == ord('q'):  # Exit on 'q'
            break

if __name__ == "__main__":
    curses.wrapper(main)