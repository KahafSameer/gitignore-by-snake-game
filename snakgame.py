import turtle
import time
import random
import os

delay = 0.1

# Score
score = 0
high_score = 0

# Load high score from file
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        try:
            high_score = int(f.read())
        except:
            high_score = 0

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)  # Turns off the screen updates

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.hideturtle()
border_pen.goto(-300, -300)
border_pen.pendown()
for _ in range(4):
    border_pen.forward(600)
    border_pen.left(90)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# Pen for score
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 30, "normal"))

# Start screen pen
start_pen = turtle.Turtle()
start_pen.speed(0)
start_pen.color("white")
start_pen.penup()
start_pen.hideturtle()

# Game over pen
game_over_pen = turtle.Turtle()
game_over_pen.speed(0)
game_over_pen.color("white")
game_over_pen.penup()
game_over_pen.hideturtle()

# Game state
game_state = "start"  # start, playing, game_over

# Functions
def start_game():
    global game_state
    game_state = "playing"
    start_pen.clear()

def restart_game():
    global game_state, score, delay, segments
    game_state = "playing"
    game_over_pen.clear()
    head.goto(0, 0)
    head.direction = "stop"
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    score = 0
    delay = 0.1
    pen.clear()
    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 30, "normal"))

def quit_game():
    wn.bye()

def go_up():
    if game_state == "playing" and head.direction != "down":
        head.direction = "up"

def go_down():
    if game_state == "playing" and head.direction != "up":
        head.direction = "down"

def go_left():
    if game_state == "playing" and head.direction != "right":
        head.direction = "left"

def go_right():
    if game_state == "playing" and head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

def save_high_score():
    with open("highscore.txt", "w") as f:
        f.write(str(high_score))

# Keyboard bindings
wn.listen()
wn.onkeypress(start_game, "space")
wn.onkeypress(restart_game, "r")
wn.onkeypress(quit_game, "q")
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# Main game loop
while True:
    wn.update()

    if game_state == "start":
        start_pen.goto(0, 0)
        start_pen.write("Snake Game\n\nUse WASD to move\nEat red food to grow\n\nPress SPACE to start", align="center", font=("Courier", 24, "normal"))
        time.sleep(0.1)
        continue

    if game_state == "game_over":
        game_over_pen.goto(0, 0)
        game_over_pen.write("Game Over!\n\nScore: {}\nHigh Score: {}\n\nPress R to restart\nPress Q to quit".format(score, high_score), align="center", font=("Courier", 24, "normal"))
        time.sleep(0.1)
        continue

    # Check for a collision with the border
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        game_state = "game_over"
        save_high_score()

    # Check for a collision with the food
    if head.distance(food) < 20:
        # Move the food to a random spot
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("white")
        new_segment.penup()
        segments.append(new_segment)

        # Shorten the delay
        delay -= 0.001

        # Increase the score
        score += 10

        if score > high_score:
            high_score = score
            save_high_score()

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 30, "normal"))

    # Move the end segments first in reverse order
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            game_state = "game_over and you loss"
            save_high_score()

    time.sleep(delay)

wn.mainloop()
