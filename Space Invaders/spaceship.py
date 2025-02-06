import pygame as pg
from laser import Laser

'''
Creation of a spaceship under player control
'''


# Sprite allows to use the image in the game, provides tools for managing groups of objects, collisions and state updates.
class Spaceship(pg.sprite.Sprite):
    def __init__(self, screen_width, screen_height, offset):
        super().__init__()  # We inherit everything from class Spaceship
        self.offset = offset
        self.screen_width = screen_width  # We pass information about the size of the game window to the spaceship object
        self.screen_height = screen_height
        self.image = pg.image.load("Images/spaceship.png")  # Loading an image from a folder
        self.rect = self.image.get_rect(midbottom=((self.screen_width + self.offset) / 2,
                                                   self.screen_height))  # Create a rectangle to store the location of the spaceship
        self.speed = 6
        self.lasers_group = pg.sprite.Group()  # Group of all lasers
        self.laser_ready = True
        self.laser_time = 0  # Shows how much time has passed since the last shot
        self.laser_delay = 300  # Laser firing speed control

    # Moving player spaceship
    def get_user_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pg.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pg.K_SPACE] and self.laser_ready:
            self.laser_ready = False
            laser = Laser(self.rect.center, 5, self.screen_height)  # The player's ship fires when SPACE is pressed
            self.lasers_group.add(laser)
            self.laser_time = pg.time.get_ticks()

    def update(self):
        self.get_user_input()
        self.constrain_movement()
        self.lasers_group.update()
        self.recharge_laser()

    # Spaceship does not go beyond the playing field
    def constrain_movement(self):
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width  # If the spaceship goes beyond the window, move it back
        if self.rect.left < self.offset:
            self.rect.left = self.offset

    # Makes the shot short rather than endless
    def recharge_laser(self):
        if not self.laser_ready:
            current_time = pg.time.get_ticks()
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True

    # All game objects with full HP will appear in their places
    def reset(self):
        self.rect = self.image.get_rect(midbottom=((self.screen_width + self.offset) / 2, self.screen_height))
        self.lasers_group.empty()  # Removes all shots from the screen
