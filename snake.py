import curses
import time
from random import randint

# Setup screen
stdscr = curses.initscr()
curses.curs_set(0)  # Hide cursor
sh, sw = stdscr.getmaxyx()  # Get screen height and width
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)  # Enable keypad input
w.timeout(100)  # Set screen update timeout

# Start color functionality
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake color
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Food color
curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Background color

# Initial snake position and food
snake = [
    [sh // 2, sw // 4],
    [sh // 2, sw // 4 - 1],
    [sh // 2, sw // 4 - 2]
]
food = [sh // 2, sw // 2]
w.addch(food[0], food[1], curses.ACS_PI, curses.color_pair(2))  # Food represented by π

# Initial direction
direction = 'RIGHT'

# Function to display Game Over message
def game_over():
    msg = "Game Over!"
    w.clear()  # Clear the screen to make sure the message is visible
    w.addstr(sh // 2, (sw // 2) - len(msg) // 2, msg, curses.color_pair(3))  # Center the message
    w.refresh()  # Refresh the screen to update it with the message
    time.sleep(3)

 # Delay for 2 seconds to allow the player to see the message

  

# Main game loop
while True:
    key = w.getch()

    # Exit game on ESC
    if key == 27:
        break

    if key == curses.KEY_RIGHT and direction != 'LEFT':
        direction = 'RIGHT'
    elif key == curses.KEY_LEFT and direction != 'RIGHT':
        direction = 'LEFT'
    elif key == curses.KEY_UP and direction != 'DOWN':
        direction = 'UP'
    elif key == curses.KEY_DOWN and direction != 'UP':
        direction = 'DOWN'

    # Calculate new head position
    head = snake[0]
    if direction == 'RIGHT':
        new_head = [head[0], head[1] + 1]
    elif direction == 'LEFT':
        new_head = [head[0], head[1] - 1]
    elif direction == 'UP':
        new_head = [head[0] - 1, head[1]]
    elif direction == 'DOWN':
        new_head = [head[0] + 1, head[1]]

    # Check for game over conditions
    if (
        new_head in snake or
        new_head[0] in [0, sh] or
        new_head[1] in [0, sw]
    ):
        game_over()  # Display Game Over message
        curses.endwin()  # Clean up and end the game
        quit()  # Exit the game

    # Add new head to snake
    snake.insert(0, new_head)

    # Check if snake eats food
    if new_head == food:
        food = None
        while food is None:
            nf = [randint(1, sh - 2), randint(1, sw - 2)]
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI, curses.color_pair(2))  # Add food with color
    else:
        # Remove tail if no food eaten
        tail = snake.pop()
        w.addch(tail[0], tail[1], ' ', curses.color_pair(3))  # Clear tail with background color

    # Draw the snake
    w.addch(new_head[0], new_head[1], curses.ACS_CKBOARD, curses.color_pair(1))  # Snake with color
