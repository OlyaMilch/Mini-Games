import pygame as pg
import sys
from game import Game
import random

# Initial application setup
pg.init()

# Game window
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

font = pg.font.Font(None, 40)
level_surface = font.render('LEVEL 01', False, '#F2F22F')
game_over_surface = font.render('GAME OVER', False, '#F2F22F')

screen = pg.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET))  # Creating a game window
pg.display.set_caption('Space Invaders')

clock = pg.time.Clock()

'''
A "group" is a container that displays and processes multiple sprites.
It provides functions for collision detection, update, processing and rendering.
'''

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

shoot_laser = pg.USEREVENT  # "Userevent" is used to create user events
pg.time.set_timer(shoot_laser, 300)  # Adjusting the frequency of alien shots

mystery_ship = pg.USEREVENT + 1
pg.time.set_timer(mystery_ship, random.randint(4000, 8000))

# Game loop

# Handling game events
while True:
    for event in pg.event.get():  # Retrieves all events within the game
        if event.type == pg.QUIT:  # Exits the game when you press the cross button
            pg.quit()
            sys.exit()
        if event.type == shoot_laser and game.run:
            game.alien_shoot_laser()

        if event.type == mystery_ship and game.run:
            game.create_mystery_ship()
            pg.time.set_timer(mystery_ship, random.randint(4000, 8000))  # Random spawn time

        # Restart the game when pressing SPACE
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and game.run is False:
            game.reset()

    # Updating
    if game.run:
        game.spaceship_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collisions()

    # Drawing
    screen.fill('#102022')
    pg.draw.rect(screen, "#F2F22F", (10, 10, 780, 780),
                 2, 0, 60, 60,
                 60, 60)  # Game frame
    pg.draw.line(screen, "#F2F22F", (25, 730), (775, 730), 3)  # A piece of the screen where we see HP

    if game.run:
        screen.blit(level_surface, (570, 740, 50, 50))
    else:
        screen.blit(game_over_surface, (570, 740, 50, 50))

    # HP display
    x = 50
    for life in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (x, 745))
        x += 50

    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)  # Drawing sprites from spaceship_group
    for obstacle in game.obstacles:
        obstacle.block_group.draw(screen)
    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.mystery_ship_group.draw(screen)

    pg.display.update()  # Draws all changes on the screen
    clock.tick(60)  # Fps
