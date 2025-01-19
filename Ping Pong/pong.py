import sys
import pygame as pg
import random


# When receiving a point, the ball resets in the middle of the screen
def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.x = screen_width / 2 - 10
    ball.y = random.randint(10, 100)
    ball_speed_x *= random.choice([-1, 1])  # Randomly changes the speed of the ball
    ball_speed_y *= random.choice([-1, 1])


# A point is awarded when the ball touches the edge of the enemy field
def point_won(winner):
    global cpu_points, player_points

    if winner == 'cpu':
        cpu_points += 1
    if winner == 'player':
        player_points += 1

    reset_ball()


# Change the ball positions
def animate_ball():
    global ball_speed_x, ball_speed_y  # Thanks to global, we can use objects declared later
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball does not go out of screen
    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1

    if ball.right >= screen_width:
        point_won('cpu')

    if ball.left <= 0:
        point_won('player')

    if ball.colliderect(player) or ball.colliderect(cpu):  # Collision between ball with racket
        ball_speed_x *= -1


def animate_player():
    player.y += player_speed

    # The racket does not go out of screen
    if player.top <= 0:
        player.top = 0

    if player.bottom >= screen_height:
        player.bottom = screen_height


def animate_cpu():
    global cpu_speed
    cpu.y += cpu_speed  # The computer moves the racket, focusing in the center of the ball

    if ball.centery <= cpu.centery:
        cpu_speed = -6
    if ball.centery >= cpu.centery:
        cpu_speed = 6

    # The racket does not go beyond the screen
    if cpu.top <= 0:
        cpu.top = 0
    if cpu.bottom >= screen_height:
        cpu.bottom = screen_height


# Basic game setup

pg.init()  # Initialization

# Playing field size
screen_width = 1280
screen_height = 800

# Creating game display
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Ping Pong')

clock = pg.time.Clock()

ball = pg.Rect(0, 0, 30, 30)  # (x, y, width, height)
ball.center = (screen_width / 2, screen_height / 2)  # Move object 'ball' to the center of the screen

cpu = pg.Rect(0, 0, 20, 100)  # AI racket
cpu.centery = screen_height / 2  # Move object to the center of the screen

player = pg.Rect(0, 0, 20, 100)  # Player's racket
player.midright = (screen_width, screen_height / 2)

ball_speed_x = 6
ball_speed_y = 6
player_speed = 0
cpu_speed = 6

cpu_points, player_points = 0, 0

score_font = pg.font.Font(None, 100)  # "None" is default font

# Game loop settings

# Checks for events
while True:
    for event in pg.event.get():  # Gets all events
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()  # Will stop the loop and exit the game if the game launcher is closed

        # The player takes control of the racket
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                player_speed = -6  # Changing the speed of a player's racket
            if event.key == pg.K_DOWN:
                player_speed = 6
        if event.type == pg.KEYUP:  # When the player releases the buttons, the racket does not move
            if event.key == pg.K_UP:
                player_speed = 0
            if event.key == pg.K_DOWN:
                player_speed = 0

    # Change the positions of the game objects
    animate_ball()
    animate_player()
    animate_cpu()

    # Draw the game objects
    screen.fill('#030302')  # Clear the previous location of the ball and rackets

    cpu_score_surface = score_font.render(str(cpu_points), True, '#f7f0f0')
    player_score_surface = score_font.render(str(player_points), True, '#f7f0f0')
    screen.blit(cpu_score_surface, (screen_width / 4, 20))  # Will display earned points
    screen.blit(player_score_surface, (3 * screen_width / 4, 20))

    pg.draw.aaline(screen, '#f7f0f0', (screen_width / 2, 0),
                   (screen_width / 2, screen_height))  # Divides the field in half
    pg.draw.ellipse(screen, '#f7f0f0', ball)  # .ellipse makes an object shaped like a circle
    pg.draw.rect(screen, '#f7f0f0', cpu)  # Draw the racket
    pg.draw.rect(screen, '#f7f0f0', player)  # Draw second racket

    # Update the display
    pg.display.update()
    clock.tick(60)  # fps
