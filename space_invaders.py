# space invaders

import turtle
import os
import math
import random

# set up the screen
main_screen = turtle.Screen()
main_screen.bgcolor("black")
main_screen.title("space invaders")
main_screen.bgpic("space_invaders_background.gif")

# register shapes
turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")

# draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# set the score to 0
score = 0

# draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: %s" % score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

difficulty = int(input("Please choose difficulty: \n"
                   "1. Easy\n"
                   "2. Medium\n"
                   "3. Hard\n"))
global enemyspeed
if difficulty == 3:
    enemyspeed = 8
elif difficulty == 2:
    enemyspeed = 5
elif difficulty == 1:
    enemyspeed = 2
else:
    print("Please try again.")

# choose a number of enemies
number_of_enemies = 5
# create empty list of enemies
enemies = []
# add enemies to the list
for i in range(number_of_enemies):
    # create the enemy turtle
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 200)
    enemy.setposition(x, y)

# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

playerspeed = 0

# create player bullet
bullet = turtle.Turtle()  # create turtle object
bullet.color("yellow")  # color
bullet.shape("triangle")  # shape
bullet.penup()  # don't draw line
bullet.speed(0)  # draw speed
bullet.setheading(90)  # make triangle face up
bullet.shapesize(0.5, 0.5)  # size of bullet
bullet.hideturtle()  # hide the object beginning of the game

bulletspeed = 20

# define bullet state
# ready - ready to fire
# fire - bullet is firing
bulletstate = "ready"


# move the player left and right
def move_left():
    global playerspeed
    playerspeed = -5


def move_right():
    global playerspeed
    playerspeed = 5


def stop_player():
    global playerspeed
    playerspeed = 0


def fire_bullet():
    # declare bullsetstate as a global if it needs changed
    global bulletstate
    if bulletstate == "ready":
        os.system("afplay laser.wav&")  # sound only works for Mac
        bulletstate = "fire"
        # move the bullet to just above the player
        x = player.xcor()
        y = player.ycor() + 10  # +10 for position just above the player
        bullet.setposition(x, y)
        bullet.showturtle()


def is_collision(t1, t2):
    distance = math.sqrt(pow(t1.xcor() - t2.xcor(), 2) + pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


# create keyboard binding
turtle.listen()
turtle.onkeypress(move_left, "Left")
turtle.onkeypress(move_right, "Right")
turtle.onkeypress(fire_bullet, "space")
turtle.onkeyrelease(stop_player, "Left")
turtle.onkeyrelease(stop_player, "Right")

# create main game loop
while True:
    # move the player
    player.setx(player.xcor() + playerspeed)

    for enemy in enemies:
        # move the enemy
        enemy.setx(enemy.xcor() + enemyspeed)

        # move the enemy back and down
        if enemy.xcor() > 280:
            # move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # change enemy direction
            enemyspeed *= -1

        if enemy.xcor() < -280:
            for e in enemies:
                # move all enemies down
                y = e.ycor()
                y -= 40
                e.sety(y)
            # change enemy direction
            enemyspeed *= -1

        # check for collision between bullet and enemy
        if is_collision(bullet, enemy):
            os.system("afplay explosion.wav&")
            # Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)  # to avoid collision with anything while resetting
            # reset the enemy
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
            # update the score
            score += 10
            scorestring = "Score: %s" % score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

        if is_collision(player, enemy):
            os.system("afplay explosion.wav&")
            player.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            break

    # move the bullet
    if bulletstate == "fire":  # makes code more efficient
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # check bullet to see if it has gone to top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"
