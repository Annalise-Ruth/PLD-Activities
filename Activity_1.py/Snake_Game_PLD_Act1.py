from tkinter import *
import random

#Constants
GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#9FDDA4"
FOOD_COLOR = "#E0889F"
BACKGROUND_COLOR = "#99DFEC"

#Snake and Food 
class Snake:
    
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])

        for x_axis, y_axis in self.coordinates:
            square = canvas.create_rectangle(x_axis, y_axis, x_axis + SPACE_SIZE, y_axis + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    
    def __init__(self):

        x_axis = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y_axis = random.randint(0, (GAME_HEIGHT / SPACE_SIZE)-1) * SPACE_SIZE

        self.coordinates = [x_axis, y_axis]

        canvas.create_oval(x_axis, y_axis, x_axis + SPACE_SIZE, y_axis + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

#Direction and Collisions
def next_turn(snake, food):
    
    x_axis, y_axis = snake.coordinates[0]

    if direction == "up":
        y_axis -= SPACE_SIZE
    elif direction == "down":
        y_axis += SPACE_SIZE  
    elif direction == "left":
        x_axis -= SPACE_SIZE
    elif direction == "right":
        x_axis += SPACE_SIZE

    snake.coordinates.insert(0, (x_axis, y_axis))

    square = canvas.create_rectangle(x_axis, y_axis, x_axis + SPACE_SIZE, y_axis + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x_axis == food.coordinates[0] and y_axis == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    
    else:
        window.after(SPEED, next_turn, snake, food)
    
def change_direction(new_direction):
    
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction
    
def check_collisions(snake):
    
    x_axis, y_axis = snake.coordinates[0]

    if x_axis < 0 or x_axis >= GAME_WIDTH:
        print("GAME OVER")
        return True
    elif y_axis < 0 or y_axis >= GAME_HEIGHT:
        print("GAME OVER")
        return True
    
    for body_part in snake.coordinates[1:]:
        if x_axis == body_part[0] and y_axis == body_part[1]:
            print ("GAME OVER")
            return True
        
    return False

def game_over():
   
   canvas.delete(ALL)
   canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas',70), text="GAME OVER", fill="#E0889F", tag="gameover")

#Window
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_axis = int((screen_width/2) - (window_width/2))
y_axis = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x_axis}+{y_axis}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
