from tkinter import *
from tkinter import colorchooser
import random
from idlelib.tooltip import Hovertip

# Constants
width_game = 700  # Screen width
height_game = 700  # Screen height
snake_parts = 3  # Starting blocks of a snake
font = ('Consolas', 20)  # Label font settings

# Variables

speed = 70  # Default speed (change once each 100ms)
snake_color = '#0099ff'  # All colors can be customized
food_color = '#d61cbd'
background_color = '#000000'
font = ('Consolas', 20)  # Label font settings


# Object - Snake

class Snake():

    def __init__(self):
        self.length = snake_parts
        self.coordinates = []  # Draw a new square
        self.squares = []  # Delete square objects

        for i in range(snake_parts):  # List with coordinates of snake blocks (start)
            self.coordinates.append([0, 0])

        # For each item in the list - draw a square and add this object to a list of squares
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + space_size.get(), y + space_size.get(), fill=snake_color,
                                             tag='snake')
            self.squares.append(square)


class Food():

    def __init__(self):
        x_coords = random.randint(0, int(width_game / space_size.get()) - 1) * space_size.get()
        y_coords = random.randint(0, int(height_game / space_size.get()) - 1) * space_size.get()
        self.coordinates = [x_coords, y_coords]  # Create a new food object                                                              # To make deletion easier
        canvas.create_rectangle(x_coords, y_coords, x_coords + space_size.get(), y_coords + space_size.get(),
                                fill=food_color, tag='food')


# Main function


def next_turn(snake, food):
    global direction
    global new_direction

    # Change the direction of the snake
    if new_direction.get() == 'up' and direction != 'down': direction = 'up'
    if new_direction.get() == 'down' and direction != 'up': direction = 'down'
    if new_direction.get() == 'right' and direction != 'left': direction = 'right'
    if new_direction.get() == 'left' and direction != 'right': direction = 'left'

    # Snake head coordinates
    x, y = snake.coordinates[0]
    if direction == 'up':
        y -= space_size.get()
    elif direction == 'down':
        y += space_size.get()
    elif direction == 'left':
        x -= space_size.get()
    elif direction == 'right':
        x += space_size.get()

    # Update coordinates of the snake head
    snake.coordinates.insert(0, (x, y))

    # Create a new snake head
    global snake_color
    square = canvas.create_rectangle(x, y, x + space_size.get(), y + space_size.get(), fill=snake_color)
    snake.squares.insert(0, square)  # Update the snake's list of body-part

    # If the coordinates of the food and the coordinates of the head coincide, the snake will increase
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        global speed
        score += 1
        if speed > 60: speed -= 1  # Change snakes speed
        score_label.config(text='Score: {}'.format(score))

        canvas.delete('food')
        food = Food()

    # Tail-block of the snake is deleted each turn when food is not eaten
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

        # When a collision occurs, the game ends. You can start new game
    if collisions_check(snake) == False:
        game_over()
    else:
        window.after(speed, next_turn, snake, food)


# Secondary functions


def collisions_check(snake):
    x, y = snake.coordinates[0]
    if x < 0 or y < 0 or y >= height_game or x >= width_game:
        return False
    for body_part in snake.coordinates[1:]:
        if body_part == (x, y):
            return False


def game_over():  # Unlock the reset button and clear the field.
    global score
    score_label.config(text='Game over! Your score: {}'.format(score))
    start_button.config(state=NORMAL)
    space_size_chooser.config(state=NORMAL)
    snake_color_button.config(state=NORMAL)
    food_color_button.config(state=NORMAL)
    background_color_button.config(state=NORMAL)


def game_start():  # Reset game and block all launcher buttons
    global score
    global direction
    global speed
    canvas.delete('all')  # Clean all
    score = 0
    direction = 'down'
    new_direction.set('down')  # Avoid the bug with the death of the snake at the start
    speed = 90
    food = Food()
    snake = Snake()  # Create a new snake
    start_button.config(state=DISABLED)
    space_size_chooser.config(state=DISABLED)
    snake_color_button.config(state=DISABLED)
    food_color_button.config(state=DISABLED)
    background_color_button.config(state=DISABLED)
    score_label.config(text='Score: {}'.format(score))
    next_turn(snake, food)


# Customization


def new_snake_color():
    global snake_color
    x = colorchooser.askcolor(title='Pick snake color')[1]
    snake_color = x
    snake_color_button.config(bg=x)

def new_food_color():
    global food_color
    x = colorchooser.askcolor(title='Pick food color')[1]
    food_color = x
    food_color_button.config(bg=x)


def new_background_color():
    global background_color
    canvas.config(bg=colorchooser.askcolor(title='Pick background color')[1])


def new_space_size():
    global space_size
    space_size.set(space_size_chooser.get())


# Window (game launcher)


window = Tk()  # A Tk object is created, which is the main game window
window.title('Snake!')
window.resizable(False, False)  # Window resizing blocked
space_size = IntVar(window)  # The playing field cell is stored here
space_size.set(35)
new_direction = StringVar(window)  # Variable to store the current direction of the snake's movement
new_direction.set('down')


# Launcher settings


frame = Frame(window)
background_color_button = Button(frame, text='Background color', width=15, command=new_background_color)
background_color_button.pack(side=LEFT)
tip_bkg_clr = Hovertip(background_color_button, 'Change a new background color', hover_delay=500)

snake_color_button = Button(frame, text='Snake color', width=15, command=new_snake_color, bg=snake_color)
snake_color_button.pack(side=LEFT)
tip_snake_clr = Hovertip(snake_color_button, 'Change a new snake color', hover_delay=500)

food_color_button = Button(frame, text='Food color', width=15, command=new_food_color, bg=food_color)
food_color_button.pack(side=LEFT)
tip_food_clr = Hovertip(food_color_button, 'Change a new food color', hover_delay=500)



space_size_chooser = OptionMenu(frame, space_size, *[10, 25, 35, 50, 70])
space_size_chooser.pack(side=LEFT)
tip_sschooser = Hovertip(space_size_chooser,'Change the space size', hover_delay=500)

frame.pack()


# Start the game


start_button = Button(window, text='Start the game', command=game_start)
start_button.pack()
tip_bkg_clr = Hovertip(start_button, 'Lets go!', hover_delay=1000)
score_label = Label(window, font=font, text='You will succeed! ^-^')
score_label.pack()

canvas = Canvas(window, bg=background_color, width=width_game, height=height_game)
canvas.pack()


# Game window placement settings


window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Stretching and placing a window

# You can change the key bindings
window.bind("<w>", lambda x: new_direction.set('up'))
window.bind("<a>", lambda x: new_direction.set('left'))
window.bind("<s>", lambda x: new_direction.set('down'))
window.bind("<d>", lambda x: new_direction.set('right'))
window.bind("<Up>", lambda x: new_direction.set('up'))
window.bind("<Left>", lambda x: new_direction.set('left'))
window.bind("<Down>", lambda x: new_direction.set('down'))
window.bind("<Right>", lambda x: new_direction.set('right'))

window.mainloop()  # Keeps the game window open and commits changes :)
