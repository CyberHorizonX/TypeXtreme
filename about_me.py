import curses
import textwrap

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
    about_box_height = 25
    about_box_width = 80
    about_box_y = 2
    about_box_x = (screen_width - about_box_width) // 2

    # Button
    button_y = about_box_y + about_box_height + 2
    button_x = (screen_width - 10) // 2
    selected_button = 0  # Index of the selected button

    # About Me text
    about_text = '''
    Hello there! I'm the creator of TypeXtream, a project born from my passion for programming and problem-solving. I've always been fascinated by how technology can make learning more engaging, and this typing test is my way of bringing that idea to life. With TypeXtream, I wanted to go beyond just a basic typing speed test—I aimed to create something that challenges users while also keeping the experience smooth and enjoyable.

    This project features different test modes, including word-based, string-based, and alphanumeric challenges, along with a countdown timer, real-time error tolerance, and a visually appealing curses-based UI. The goal? To provide an exciting typing experience that helps users improve their speed and accuracy without feeling restricted by traditional typing tests.

    I have a strong interest in cybersecurity, back-end developement and problem-solving, and I’m always eager to explore new ideas. Whether it's competitive programming, ethical hacking, or system automation, I enjoy diving deep into the technical world. TypeXtream is just one of the many projects I’ve worked on, and I plan to keep refining it while also developing more creative tools in the future.

    If you're using TypeXtream, I hope you find it helpful, fun, and a great way to challenge yourself. Keep typing, keep improving, and most importantly—enjoy the process!
    '''

    # Wrap the text to fit within the box
    wrapped_text = textwrap.fill(about_text, width=about_box_width - 4)
    wrapped_lines = wrapped_text.split('\n')

    while True:
        stdscr.clear()
        
        # Draw About Me box
        draw_box(stdscr, about_box_y, about_box_x, about_box_height, about_box_width, 1)
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(about_box_y + 1, about_box_x + (about_box_width - 12) // 2, "About Me")
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
        
        # Draw About Me text
        stdscr.attron(curses.color_pair(1))
        for i, line in enumerate(wrapped_lines):
            if i >= about_box_height - 4:  # Ensure text doesn't overflow the box
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