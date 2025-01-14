import pygame as pg
import sys
from game import Game
from colors import Colors


#  Initial application setup
pg.init()

# User window font
title_font = pg.font.Font(None, 40)  # None - is an embedded font
score_surface = title_font.render('Score :)', True, Colors.white)
next_surface = title_font.render('Next', True, Colors.white)
game_over_surface = title_font.render('GAME OVER', True, Colors.white)

score_rect = pg.Rect(320, 55, 170, 60)
next_rect = pg.Rect(320, 215, 170, 180)

screen = pg.display.set_mode((500, 620))  # Screen size: width and height
pg.display.set_caption('Tetris')

clock = pg.time.Clock()  # Frame rate control

GAME_UPDATE = pg.USEREVENT  # Creating custom events
pg.time.set_timer(GAME_UPDATE, 200)  # The game updates the block position every 200 milliseconds


game = Game()

# Event Handling
while True:
    for event in pg.event.get():  # Recognizes all events in a loop puts them in a list
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:  # Checking for key presses from the keyboard
            if game.game_over is True:
                game.game_over = False
                game.reset()  # Reset the game
            if event.key == pg.K_LEFT and game.game_over == False:  # K_LEFT is the left arrow on the keyboard
                game.move_left()  # Move the figure to the left
            if event.key == pg.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pg.K_DOWN and game.game_over == False:
                game.move_down()
                game.update_score(0, 1)
            if event.key == pg.K_UP and game.game_over == False:  # Using the "up" button we rotate the blocks
                game.rotate()
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()

    # Drawing
    score_value_surface = title_font.render(str(game.score), True, Colors.white)

    screen.fill('#070808')  # Stroke color of screen cells
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 180, 50, 50))

    if game.game_over is True:
        screen.blit(game_over_surface, (320, 450, 50, 50))

    pg.draw.rect(screen, Colors.light_green, score_rect, 0, 10)  # Draw the score window
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx,
                                                                  centery = score_rect.centery))
    pg.draw.rect(screen, Colors.light_green, next_rect, 0, 10)
    game.draw(screen)

    pg.display.update()  # First launch of the game
    clock.tick(60)  # The code inside the while will execute 60 times per second (fps)
