from tkinter import *
import random
import pygame

# Configuration Constants
GAME_WIDTH, GAME_HEIGHT = 900, 700
SPEED, SPACE_SIZE, BODY_PARTS = 115, 50, 3
snake_colors = ["Red", "Blue", "Green", "White", "Yellow", "Purple", "Orange", "Cyan", "Pink", "#00FF00"]
FOOD_COLOR, BACKGROUND_COLOR = "#FF0000", "#000000"

# Sound initialization
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("food_eating_sound.mp3")
game_over_sound = pygame.mixer.Sound("game_over.mp3")
background_music = pygame.mixer.Sound("breakfast.mp3")

class Snake:
    def __init__(self, color):
        self.color = color
        self.body_size = BODY_PARTS
        self.coordinates = [[0, 0] for _ in range(BODY_PARTS)]
        self.squares = [canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=color, tag="snake")
                        for x, y in self.coordinates]

    def move(self, x, y):
        self.coordinates.insert(0, [x, y])
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color)
        self.squares.insert(0, square)

    def shrink(self):
        del self.coordinates[-1]
        canvas.delete(self.squares[-1])
        del self.squares[-1]

class Food:
    def __init__(self, snake_coordinates):
        self.coordinates = self.randomize_position(snake_coordinates)
        canvas.create_oval(self.coordinates[0], self.coordinates[1],
                           self.coordinates[0] + SPACE_SIZE, self.coordinates[1] + SPACE_SIZE, 
                           fill=FOOD_COLOR, tag="food")

    @staticmethod
    def randomize_position(snake_coordinates):
        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            if [x, y] not in snake_coordinates:
                return [x, y]

class Game:
    def __init__(self):
        self.window = Tk()
        self.window.title("Snake Game")
        self.window.resizable(False, False)

        self.score = 0
        self.highscore = 0
        self.round_number = 1
        self.direction = 'down'
        self.restart_button = None
        self.game_loop_id = None

        self.label = Label(self.window, text="Score: 0", font=('consolas', 40), fg="#00FF00")
        self.label.pack()

        global canvas
        canvas = Canvas(self.window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        canvas.pack()

        self.window.update()
        self.center_window()

        pygame.mixer.Sound.play(background_music, loops=-1)

        print("Contact the developer (Bayazid) at notbayazid@gmail.com for feedback.")
        
        self.reset_game()

    def reset_game(self):
        if self.restart_button:
            self.restart_button.destroy()
        if self.game_loop_id:
            self.window.after_cancel(self.game_loop_id)

        self.score = 0
        self.direction = 'down'
        self.label.config(text="Score: 0", fg="#00FF00")
        canvas.delete("all")

        SNAKE_COLOR = random.choice(snake_colors)
        self.snake = Snake(SNAKE_COLOR)
        self.food = Food(self.snake.coordinates)

        self.window.bind('<a>', lambda event: self.change_direction('left'))
        self.window.bind('<d>', lambda event: self.change_direction('right'))
        self.window.bind('<w>', lambda event: self.change_direction('up'))
        self.window.bind('<s>', lambda event: self.change_direction('down'))

        if self.round_number > 1:
            print("--------")

        print(f"Round {self.round_number}")
        self.round_number += 1
        self.next_turn()

    def game_over(self):
        if self.game_loop_id:
            self.window.after_cancel(self.game_loop_id)

        canvas.delete("all")
        canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 50, font=('consolas', 70),
                           text="GAME OVER...", fill="red", tag="game_over")
        canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - -0.5, font=('consolas', 20),
                           text="Game Developed By Bayazid", fill="grey", tag="developer")

        pygame.mixer.Sound.play(game_over_sound)

        if self.score > self.highscore:
            self.highscore = self.score

        print(f"Game Over! Your score: {self.score}")
        print(f"High Score: {self.highscore}")

        self.restart_button = Button(self.window, text="RESTART GAME", command=self.reset_game,
                                     font=("Arial", 18), fg="#00FF00", bg="#e2fE34")
        self.restart_button.place(relx=0.5, rely=0.65, anchor=CENTER)

    def center_window(self):
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def next_turn(self):
        x, y = self.snake.coordinates[0]
        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        self.snake.move(x, y)

        if [x, y] == self.food.coordinates:
            self.score += 1
            self.label.config(text=f"Score: {self.score}", fg="#00FF00")
            canvas.delete("food")
            self.food = Food(self.snake.coordinates)
            pygame.mixer.Sound.play(eat_sound)
        else:
            self.snake.shrink()

        if self.check_collisions():
            self.game_over()
        else:
            self.game_loop_id = self.window.after(SPEED, self.next_turn)

    def change_direction(self, new_direction):
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        elif new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction

    def check_collisions(self):
        x, y = self.snake.coordinates[0]
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True
        if any(x == part[0] and y == part[1] for part in self.snake.coordinates[1:]):
            return True
        return False

if __name__ == "__main__":
    game = Game()
    game.window.mainloop()
