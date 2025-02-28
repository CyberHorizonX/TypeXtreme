import random
import time
import json
import curses

def load_leaderboard():
    try:
        with open("leaderboard.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_leaderboard(leaderboard):
    with open("leaderboard.json", 'w') as file:
        json.dump(leaderboard, file, indent=2)

def show_leaderboard(stdscr):
    leaderboard = load_leaderboard()

    stdscr.clear()
    stdscr.addstr(0, 0, "Leaderboard:", curses.A_BOLD)

    if not leaderboard:
        stdscr.addstr(2, 0, "No records found!", curses.A_DIM)
    else:
        for i, entry in enumerate(leaderboard, start=1):
            stdscr.addstr(i + 1, 2, f"{i}. {entry['username']}: {entry['wpm']} WPM")

    stdscr.addstr(len(leaderboard) + 3, 0, "Press any key to return...")
    stdscr.refresh()
    stdscr.getch()

def choose_words(category):
    categories_words = {
        "animals": ["dog", "cat", "elephant", "giraffe", "lion", "tiger", "zebra", "kangaroo"],
        "fruits": ["apple", "banana", "orange", "grape", "kiwi", "mango", "strawberry"],
        "countries": ["USA", "Canada", "Brazil", "Japan", "Germany", "Australia", "India", "France"],
        "colors": ["red", "blue", "green", "yellow", "purple", "orange", "black", "white"],
        "vehicles": ["car", "bus", "bicycle", "motorcycle", "truck", "airplane", "train", "boat"],
        "sports": ["soccer", "basketball", "tennis", "swimming", "volleyball", "cricket", "rugby", "badminton"],
        "professions": ["doctor", "engineer", "teacher", "artist", "lawyer", "chef", "nurse", "pilot"],
        "planets": ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
        "musical_instruments": ["guitar", "piano", "violin", "drums", "flute", "trumpet", "saxophone", "cello"],
        "shapes": ["circle", "square", "triangle", "rectangle", "oval", "hexagon", "pentagon", "star"],
        "clothing": ["shirt", "pants", "dress", "jacket", "hat", "shoes", "scarf", "gloves"],
        "beverages": ["water", "coffee", "tea", "juice", "soda", "milk", "smoothie", "lemonade"]
    }

    if category == "words":
        return random.choices(categories_words[random.choice(list(categories_words.keys()))], k=10)
    elif category == "string":
        return ["".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=random.randint(3, 7))) for _ in range(20)]
    elif category == "alphanumeric_string":
        return ["".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=random.randint(3, 7))) for _ in range(20)]
    return []

def typing_test(stdscr, username):
    stdscr.clear()
    stdscr.addstr(0, 0, "Select a category:", curses.A_BOLD)
    stdscr.addstr(1, 0, "1. Words")
    stdscr.addstr(2, 0, "2. String")
    stdscr.addstr(3, 0, "3. Alphanumeric String")
    stdscr.refresh()

    category_choice = stdscr.getch()
    category = {ord('1'): "words", ord('2'): "string", ord('3'): "alphanumeric_string"}.get(category_choice, None)
    if category is None:
        return

    words = choose_words(category)
    target_text = " ".join(words).rstrip()  # Remove trailing spaces
    user_input = [" "] * len(target_text)

    stdscr.clear()
    stdscr.addstr(0, 0, "Get ready! The test starts in 3 seconds...", curses.A_BOLD)
    stdscr.refresh()
    time.sleep(3)

    stdscr.clear()
    stdscr.addstr(0, 0, target_text, curses.A_BOLD)
    stdscr.refresh()

    start_time, cursor_x = None, 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, target_text, curses.A_BOLD)

        for i, char in enumerate(user_input):
            if char == target_text[i]:
                stdscr.addstr(1, i, char, curses.color_pair(1))
            elif char != " ":
                stdscr.addstr(1, i, char, curses.color_pair(2))
            else:
                stdscr.addstr(1, i, "_")

        if start_time:
            elapsed_time = max(time.time() - start_time, 1)
            correct_chars = sum(1 for i in range(cursor_x) if user_input[i] == target_text[i])
            wpm = (correct_chars / 5) / (elapsed_time / 60)
            stdscr.addstr(3, 0, f"WPM: {wpm:.2f}")

        stdscr.move(1, cursor_x)
        stdscr.refresh()
        key = stdscr.getch()

        if key == 27:  # Escape key
            return
        elif key in (curses.KEY_BACKSPACE, 127, 8) and cursor_x > 0:
            cursor_x -= 1
            user_input[cursor_x] = " "
        elif 32 <= key <= 126 and cursor_x < len(target_text):  # Only allow valid characters
            if start_time is None:
                start_time = time.time()
            user_input[cursor_x] = chr(key)
            cursor_x += 1

        if "".join(user_input) == target_text:
            elapsed_time = time.time() - start_time
            wpm = (len(target_text) / 5) / (elapsed_time / 60)
            leaderboard = load_leaderboard()
            leaderboard.append({"username": username, "wpm": round(wpm, 2)})
            leaderboard = sorted(leaderboard, key=lambda x: x["wpm"], reverse=True)[:10]
            save_leaderboard(leaderboard)
            post_test_menu(stdscr, username)
            return

def post_test_menu(stdscr, username):
    stdscr.clear()
    stdscr.addstr(0, 0, "Test Completed!", curses.A_BOLD)
    stdscr.addstr(1, 0, "1. Try Again")
    stdscr.addstr(2, 0, "2. Main Menu")
    stdscr.addstr(3, 0, "3. Exit")
    stdscr.refresh()

    while True:
        choice = stdscr.getch()
        if choice == ord('1'):
            typing_test(stdscr, username)
            break
        elif choice == ord('2'):
            game_main(stdscr)
            break
        elif choice == ord('3'):
            return

def game_main(stdscr):
    curses.curs_set(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to Terminal TypeXtream!", curses.A_BOLD)
    stdscr.addstr(1, 0, "Enter your username: ")
    stdscr.refresh()

    username = ""
    while True:
        key = stdscr.getch()
        if key == 10:
            break
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            username = username[:-1]
        else:
            username += chr(key)

        stdscr.addstr(1, 20, " " * 50)
        stdscr.addstr(1, 20, username)
        stdscr.refresh()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Options:", curses.A_BOLD)
        stdscr.addstr(1, 0, "1. Start Typing Test")
        stdscr.addstr(2, 0, "2. Show Leaderboard")
        stdscr.addstr(3, 0, "3. Back")
        stdscr.refresh()

        choice = stdscr.getch()
        if choice == ord('1'):
            typing_test(stdscr, username)
        elif choice == ord('2'):
            show_leaderboard(stdscr)
        elif choice == ord('3'):
            return

if __name__ == "__main__":
    curses.wrapper(game_main)
