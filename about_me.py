import curses

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

def about_me(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()
    stdscr.keypad(True)  # Enable keypad mode

    # Initialize color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)  # About Me Box
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Button Normal
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)  # Button Selected

    # Screen dimensions
    screen_height, screen_width = stdscr.getmaxyx()

    # Define dimensions and positions
    # About Me box
    about_box_height = 10
    about_box_width = 50
    about_box_y = 2
    about_box_x = (screen_width - about_box_width) // 2

    # Button
    button_y = about_box_y + about_box_height + 2
    button_x = (screen_width - 10) // 2
    selected_button = 0  # Index of the selected button

    # About Me text
    about_text = [
        "This is the About Me screen.",
        "Here you can find information about the game",
        "and its developer.",
        "Feel free to explore and enjoy the game!"
    ]

    while True:
        stdscr.clear()
        
        # Draw About Me box
        draw_box(stdscr, about_box_y, about_box_x, about_box_height, about_box_width, 1)
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(about_box_y + 1, about_box_x + (about_box_width - 12) // 2, "About Me")
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
        
        # Draw About Me text
        stdscr.attron(curses.color_pair(1))
        for i, line in enumerate(about_text):
            if i >= about_box_height - 2:  # Ensure text doesn't overflow the box
                break
            stdscr.addstr(about_box_y + 2 + i, about_box_x + 2, line)
        stdscr.attroff(curses.color_pair(1))
        
        # Draw "Back" button
        draw_button(stdscr, button_y, button_x, "Back", selected_button == 0, 3 if selected_button == 0 else 2)

        stdscr.refresh()
        key = stdscr.getch()

        # Handle button selection
        if key in [curses.KEY_ENTER, 10, 13]:  # Enter key
            if selected_button == 0:  # "Back" button pressed
                return  # Return to the main screen
        elif key == ord('q'):  # Exit on 'q'
            break

if __name__ == "__main__":
    curses.wrapper(about_me)