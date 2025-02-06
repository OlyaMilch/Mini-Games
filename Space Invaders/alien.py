import pygame as pg
import random

'''
The aliens move together first in one direction, then in the other (when they reach the edge of the screen)
Also, after each income to the end of the screen, the aliens descend a little lower to the player.
Aliens shoot and, when hit, cause damage to both the player and obstacles.
'''


class Alien(pg.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type  # We have 3 types of aliens, so we do it this way
        path = f"Images/alien_{type}.png"  # Path to all alien sprites (convenient to use when there are a lot of images!)
        self.image = pg.image.load(path)  # Every alien sprite is loaded
        self.rect = self.image.get_rect(topleft=(x, y))

    # Alien movement
    def update(self, direction):
        self.rect.x += direction

    # Create mystery alien


class MysteryShip(pg.sprite.Sprite):
    def __init__(self, screen_width, offset):
        super().__init__()
        self.screen_width = screen_width
        self.offset = offset
        self.image = pg.image.load("Images/mystery_ship.png")

        x = random.choice([self.offset / 2, self.screen_width + self.offset - self.image.get_width()])
        if x == self.offset / 2:
            self.speed = 3
        else:
            self.speed = -3

        self.rect = self.image.get_rect(topleft=(x, 40))

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > self.screen_width + self.offset / 2:
            self.kill()
        elif self.rect.left < self.offset / 2:
            self.kill()
