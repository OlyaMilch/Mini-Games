import pygame as pg
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien
from laser import Laser
from alien import MysteryShip
import random

'''
Class 'Game' serves as a container for all game elements such as spaceship, obstacles, aliens and game state.
Contains methods that control game logic: checking for collisions, updating the position of game objects, etc.
'''


class Game:
    def __init__(self, screen_width, screen_height, offset):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.spaceship_group = pg.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height, self.offset))
        self.obstacles = self.create_obstacles()
        self.aliens_group = pg.sprite.Group()  # Create aliens group
        self.create_aliens()
        self.aliens_direction = 1  # Alien direction
        self.alien_lasers_group = pg.sprite.Group()
        self.mystery_ship_group = pg.sprite.GroupSingle()
        self.lives = 3  # Spaceship HP
        self.run = True  # When the game ends it will be False

    # Equal placement of obstacles
    def create_obstacles(self):
        obstacle_width = len(grid[0]) * 3
        gap = (self.screen_width + self.offset - (4 * obstacle_width)) / 5
        obstacles = []
        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 100)
            obstacles.append(obstacle)
        return obstacles

    # Creating a mesh of aliens
    def create_aliens(self):
        for row in range(5):
            for column in range(11):
                x = 75 + column * 55  # Int its pixels
                y = 110 + row * 55

                # We put different alien models depending on the location
                if row == 0:
                    alien_type = 3
                elif row in (1, 2):
                    alien_type = 2
                else:
                    alien_type = 1

                alien = Alien(alien_type, x + self.offset / 2,
                              y)  # There are 3 variables here: the type of alien (its appearance) and coordinates: x, y
                self.aliens_group.add(alien)

    # Moving aliens
    def move_aliens(self):
        self.aliens_group.update(self.aliens_direction)

        # Aliens don't leave the screen (if at least 1 alien tries to go of screen, then all aliens change direction)
        alien_sprites = self.aliens_group.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width + self.offset / 2:
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= self.offset / 2:
                self.aliens_direction = 1
                self.alien_move_down(2)

    # Aliens drop down every time they hit the edges of the screen
    def alien_move_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    # Aliens are shooting (random alien shoots)
    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())  # Choice random alien
            laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height)
            self.alien_lasers_group.add(laser_sprite)

    # Mystery ship creation timers
    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))

    def check_for_collisions(self):
        # Spaceship
        if self.spaceship_group.sprite.lasers_group:
            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                if pg.sprite.spritecollide(laser_sprite, self.aliens_group,
                                           True):  # Spritecollide method detects sprite collisions. True mean object destruction
                    laser_sprite.kill()
                if pg.sprite.spritecollide(laser_sprite, self.mystery_ship_group,
                                           True):  # We do the same with the mysterious ship
                    laser_sprite.kill()

                # Damage to obstacles
                for obstacle in self.obstacles:  # We are going through because we have 4 obstacles
                    if pg.sprite.spritecollide(laser_sprite, obstacle.block_group, True):
                        laser_sprite.kill()

        # Alien lasers
        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                if pg.sprite.spritecollide(laser_sprite, self.spaceship_group,
                                           False):  # False because we don't want to immediately destroy the player's ship
                    laser_sprite.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over()

                # Alien lasers damage obstacles
                for obstacle in self.obstacles:  # We are going through because we have 4 obstacles
                    if pg.sprite.spritecollide(laser_sprite, obstacle.block_group, True):
                        laser_sprite.kill()

        # Collision of an alien ship with an obstacle
        if self.aliens_group:
            for alien in self.aliens_group:  # Get all aliens
                for obstacle in self.obstacles:  # Get all obstacles
                    pg.sprite.spritecollide(alien, obstacle.block_group, True)

                # Alien ship collides with player ship
                if pg.sprite.spritecollide(alien, self.spaceship_group, False):
                    self.game_over()

    def game_over(self):
        self.run = False  # Finish the game

    def reset(self):
        self.run = True
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.obstacles = self.create_obstacles()
