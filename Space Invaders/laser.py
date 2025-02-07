import pygame as pg

'''
Objects associated with both the player laser and the alien laser
'''


class Laser(pg.sprite.Sprite):
    def __init__(self, position, speed, screen_height):
        super().__init__()
        self.image = pg.Surface((4, 15))  # Instead of a sprite we use a drawn laser (little rectangle)
        self.image.fill('#f06419')
        self.rect = self.image.get_rect(
            center=position)  # Determines where on the screen the laser will appear when it is first created
        self.speed = speed
        self.screen_height = screen_height

    # Laser movement
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            self.kill()  # Destroys a laser that goes beyond the playing field
