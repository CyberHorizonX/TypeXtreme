import random
import time
import json
import curses

# Load leaderboard from file
def load_leaderboard():
    try:
        with open("leaderboard.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Display leaderboard
def show_leaderboard(stdscr):
    leaderboard = load_leaderboard()
    stdscr.clear()
    stdscr.addstr(0, 0, "Leaderboard:", curses.A_BOLD)
    for i, entry in enumerate(leaderboard, start=1):
        stdscr.addstr(i, 2, f"{i}. {entry['username']}: {entry['wpm']} WPM")
    stdscr.refresh()
    stdscr.getch()

# Save leaderboard to file
def save_leaderboard(leaderboard):
    with open("leaderboard.json", 'w') as file:
        json.dump(leaderboard, file, indent=2)

# Choose words based on category
def choose_words(category):
    categories_words = {
        "animals": ["dog", "cat", "elephant", "giraffe", "lion", "tiger", "zebra", "penguin", "kangaroo", "koala"],
        "fruits": ["apple", "banana", "orange", "grape", "watermelon", "kiwi", "strawberry", "mango", "pineapple", "peach"],
        "countries": ["USA", "Canada", "Japan", "India", "Brazil", "Australia", "Germany", "France", "Italy", "China"],
        "colors": ["red", "blue", "green", "yellow", "purple", "orange", "pink", "brown", "black", "white"],
        "vegetables": ["carrot", "broccoli", "spinach", "potato", "tomato", "cucumber", "bell pepper", "onion", "garlic", "celery"],
        "sports": ["football", "basketball", "soccer", "tennis", "golf", "baseball", "volleyball", "hockey", "swimming", "cycling"],
        "movies": ["action", "comedy", "drama", "horror", "sci-fi", "romance", "thriller", "fantasy", "animation", "documentary"],
        "technology": ["computer", "software", "internet", "keyboard", "mouse", "smartphone", "tablet", "laptop", "algorithm", "programming"],
        "musical_instruments": ["piano", "guitar", "violin", "trumpet", "drums", "flute", "saxophone", "clarinet", "bass guitar", "accordion"],
        "planets": ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto", "sun"],
        "weather": ["rain", "sunshine", "clouds", "wind", "storm", "snow", "hail", "fog", "thunder", "lightning"],
        "clothing": ["shirt", "pants", "dress", "jacket", "shoes", "hat", "socks", "gloves", "scarf", "tie"],
        "insects": ["ant", "bee", "butterfly", "dragonfly", "mosquito", "spider", "ladybug", "grasshopper", "beetle", "caterpillar"]
    }

    if category == "words":
        # Randomly select a sub-category
        sub_category = random.choice(list(categories_words.keys()))
        return categories_words[sub_category]
    elif category == "string":
        # Generate 150 random lowercase strings of length 2-7
        return ["".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=random.randint(2, 7))) for _ in range(150)]
    elif category == "alphanumeric_string":
        # Generate 150 random alphanumeric strings of length 2-7
        return ["".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=random.randint(2, 7))) for _ in range(150)]
    else:
        return []

# Typing test function
def typing_test(stdscr, username):
    stdscr.clear()
    stdscr.addstr(0, 0, "Select a category:", curses.A_BOLD)
    stdscr.addstr(1, 0, "1. Words")
    stdscr.addstr(2, 0, "2. String")
    stdscr.addstr(3, 0, "3. Alphanumeric String")
    stdscr.refresh()

    category_choice = stdscr.getch()
    if category_choice == ord('1'):
        category = "words"
    elif category_choice == ord('2'):
        category = "string"
    elif category_choice == ord('3'):
        category = "alphanumeric_string"
    else:
        stdscr.addstr(5, 0, "Invalid choice. Exiting.")
        stdscr.refresh()
        time.sleep(1)
        return

    words = choose_words(category)
    print(f'GENERATED-WORD', words)
    if not words:
        stdscr.addstr(5, 0, f"Error: No words found for category {category}.")
        stdscr.refresh()
        time.sleep(1)
        return

    stdscr.clear()
    stdscr.addstr(0, 0, "Get ready! The test starts in 3 seconds...", curses.A_BOLD)
    stdscr.refresh()
    for i in range(3, 0, -1):
        stdscr.addstr(1, 0, f"Starting in {i}...")
        stdscr.refresh()
        time.sleep(1)

    stdscr.clear()
    stdscr.addstr(0, 0, " ".join(words), curses.A_BOLD)
    stdscr.refresh()

    start_time = time.time()
    user_input = ""
    while True:
        key = stdscr.getch()
        if key == 10:  # Enter key
            break
        elif key == 127 or key == 8:  # Backspace
            user_input = user_input[:-1]
        else:
            user_input += chr(key)
        stdscr.addstr(2, 0, " " * 100)  # Clear previous input
        stdscr.addstr(2, 0, user_input)
        stdscr.refresh()

    end_time = time.time()
    time_taken = end_time - start_time

    # Allow minor mistakes (e.g., 1 character difference per word)
    correct_words = 0
    user_words = user_input.split()
    for i in range(min(len(words), len(user_words))):
        if words[i] == user_words[i]:
            correct_words += 1
        elif len(words[i]) == len(user_words[i]) and sum(1 for a, b in zip(words[i], user_words[i]) if a != b) <= 1:
            correct_words += 1

    wpm = int((correct_words / time_taken) * 60)

    stdscr.clear()
    stdscr.addstr(0, 0, "Test Results:", curses.A_BOLD)
    stdscr.addstr(1, 0, f"Words Typed: {correct_words}")
    stdscr.addstr(2, 0, f"Time Taken: {time_taken:.2f} seconds")
    stdscr.addstr(3, 0, f"Words Per Minute: {wpm} WPM", curses.A_BOLD)
    stdscr.refresh()
    stdscr.getch()

    # Update leaderboard
    leaderboard = load_leaderboard()
    leaderboard.append({"username": username, "wpm": wpm})
    leaderboard = sorted(leaderboard, key=lambda x: x["wpm"], reverse=True)[:10]
    save_leaderboard(leaderboard)

# Main function
def main(stdscr):
    curses.curs_set(1)  # Show cursor
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to Terminal Typing Master!", curses.A_BOLD)
    stdscr.addstr(1, 0, "Enter your username: ")
    stdscr.refresh()
    username = ""
    while True:
        key = stdscr.getch()
        if key == 10:  # Enter key
            break
        elif key == 127 or key == 8:  # Backspace
            username = username[:-1]
        else:
            username += chr(key)
        stdscr.addstr(1, 20, " " * 50)  # Clear previous input
        stdscr.addstr(1, 20, username)
        stdscr.refresh()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Options:", curses.A_BOLD)
        stdscr.addstr(1, 0, "1. Start Typing Test")
        stdscr.addstr(2, 0, "2. Show Leaderboard")
        stdscr.addstr(3, 0, "3. Exit")
        stdscr.refresh()

        choice = stdscr.getch()
        if choice == ord('1'):
            typing_test(stdscr, username)
        elif choice == ord('2'):
            show_leaderboard(stdscr)
        elif choice == ord('3'):
            stdscr.clear()
            stdscr.addstr(0, 0, "Exiting the program. Goodbye!", curses.A_BOLD)
            stdscr.refresh()
            time.sleep(1)
            break
        else:
            stdscr.addstr(5, 0, "Invalid choice. Please select a valid option.")
            stdscr.refresh()
            time.sleep(1)

if __name__ == "__main__":
    curses.wrapper(main)