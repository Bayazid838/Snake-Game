from tkinter import *
import random
import pygame

GAME_WIDTH = 800
GAME_HEIGHT = 600
SPEED = 120
SPACE_SIZE = 50
BODY_PARTS = 3
snake_colors = ["Red", "Blue", "Green", "White", "Yellow", "Purple", "Orange", "Cyan", "Pink", "#00FF00"]
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self, color):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.color = color

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, snake_coordinates):
        while True:
            x = int(random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE)
            y = int(random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE)
            if [x, y] not in snake_coordinates:
                break

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    if not pause:
        x, y = snake.coordinates[0]

        if direction == "up":
            y -= SPACE_SIZE
        elif direction == "down":
            y += SPACE_SIZE
        elif direction == "left":
            x -= SPACE_SIZE
        elif direction == "right":
            x += SPACE_SIZE

        snake.coordinates.insert(0, (x, y))

        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=snake.color)
        snake.squares.insert(0, square)

        if x == food.coordinates[0] and y == food.coordinates[1]:
            global score
            score += 1
            label.config(text="Score:{}".format(score), fg="#00FF00")
            canvas.delete("food")
            food = Food(snake.coordinates)
            pygame.mixer.Sound.play(eat_sound)
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

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    global restart_button, highscore

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 - 50,
                      font=('consolas', 70), text="GAME OVER...", fill="red", tag="game_over")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 100,
                      font=('consolas', 10), text="Developed By Bayazid Bostami Sinha", fill="grey", tag="dev")
    pygame.mixer.Sound.play(game_over_sound)
    print("You scored " + str(score) + " pts!")

    if score > highscore:
        highscore = score

    print("Highscore: ", highscore)
    print()
    print("GAME OVER")
    print()

    restart_button = Button(window, text="RESTART GAME", command=restart_game, font=("Arial", 18), fg="#00FF00", bg="#e2fE34", activeforeground="#00FF00",
                            activebackground="black")
    restart_button.place(relx=0.5, rely=0.6, anchor=CENTER)

def restart_game():
    global snake, food, score, direction, restart_button, SNAKE_COLOR

    restart_button.destroy()

    canvas.delete(ALL)

    score = 0
    direction = 'down'
    SNAKE_COLOR = random.choice(snake_colors)
    pause = False

    label.config(text="Score:{}".format(score), fg="#00FF00")
    

    snake = Snake(SNAKE_COLOR)
    food = Food(snake.coordinates)

    next_turn(snake, food)

def pause_game(event):
    global pause
    pause = not pause
    if not pause:
        next_turn(snake, food)

window = Tk()
window.title("Snake game")
window.resizable(False, False)

pygame.mixer.init()
eat_sound = pygame.mixer.Sound("food_eating_sound.mp3")
game_over_sound = pygame.mixer.Sound("game_over.mp3")
background_music = pygame.mixer.Sound("breakfast.mp3")

score = 0
direction = 'down'
highscore = 0
restart_button = None
SNAKE_COLOR = random.choice(snake_colors)
pause = False

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()
#photo = PhotoImage(file='banner.png')
#banner_label = Label(window,
              #text=label,
              #font=('Arial',40,'bold'),
              #image=photo)
#banner_label.pack()
pygame.mixer.Sound.play(background_music)


canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

window.bind('<a>', lambda event: change_direction('left'))
window.bind('<d>', lambda event: change_direction('right'))
window.bind('<w>', lambda event: change_direction('up'))
window.bind('<s>', lambda event: change_direction('down'))
window.bind('<p>', pause_game)

snake = Snake(SNAKE_COLOR)
food = Food(snake.coordinates)
print("If you have any feedback regarding this product you may cantact the developer (Bayazid) anytime you want. Contact:- notbayazid@gmail.com")
next_turn(snake, food)

window.mainloop()