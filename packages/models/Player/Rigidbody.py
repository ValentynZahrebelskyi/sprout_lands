from abc import ABC
from typing import List

import pygame as pg

from packages import models
from packages.enums import Direction
from packages.utils.images import find_images_by_direction as fibd


class Rigidbody(ABC, pg.sprite.Sprite):
    """
    Rigidbody is a class that is responsible for
    the movement of the player.
    """

    def __init__(self, speed: float) -> None:
        pg.sprite.Sprite.__init__(self)
        device = models.Device()

        x, y = device.get_display()

        # return the path to the spritesheet
        self.__filename = "Basic Charakter Spritesheet/Basic_Charakter_Spritesheet"

        # return default properties of the player
        self.__current_direction = Direction.DOWN
        self.__player_pos = pg.Vector2(x / 2, y / 2)
        self.__current_sprite = 0.0
        self.__is_move = False
        self.__speed = speed

        # return a list of images by direction (up, down, left, right) based on idleness
        self.__sprites_idle_up = fibd(self.__filename, Direction.UP)
        self.__sprites_idle_down = fibd(self.__filename, Direction.DOWN)
        self.__sprites_idle_left = fibd(self.__filename, Direction.LEFT)
        self.__sprites_idle_right = fibd(self.__filename, Direction.RIGHT)

        # return a list of images by direction (up, down, left, right) based on movement
        self.__sprites_move_up = fibd(
            self.__filename, Direction.UP, range(3, 5))
        self.__sprites_move_down = fibd(
            self.__filename, Direction.DOWN, range(3, 5))
        self.__sprites_move_left = fibd(
            self.__filename, Direction.LEFT, range(3, 5))
        self.__sprites_move_right = fibd(
            self.__filename, Direction.RIGHT, range(3, 5))

        # return a list of keys that are responsible for the movement of the player
        self.__direction_up_keys: List[bool] = []
        self.__direction_down_keys: List[bool] = []
        self.__direction_left_keys: List[bool] = []
        self.__direction_right_keys: List[bool] = []
        self.__all_direction_keys: List[bool] = []

        # get the rectangle object that has the dimensions
        self.image = self.__sprites_idle_down[int(self.__current_sprite)]
        # return the rectangle object of the image
        self.rect = self.image.get_rect()

    def update(self, diff: float) -> None:
        """
        Update the player:
        - handle the animation of the player based on the current sprite and direction
        - handle the movement of the player based on the pressed keys
        """
        self.animation()
        self.movement(diff)

    def animation(self):
        """Handles the animation of the player based on the current sprite."""
        self.rect.center = self.__player_pos
        self.__current_sprite += self.__speed * 0.1

        # reset the animation if the current sprite is greater than the length of the list
        if self.__current_sprite >= len(self.__sprites_idle_down):
            self.__current_sprite = 0.0

        # handle the player animation based on the direction and movement or idleness
        if self.__current_direction == Direction.UP and not self.__is_move:
            self.image = self.__sprites_idle_up[int(self.__current_sprite)]
        elif self.__current_direction == Direction.DOWN and not self.__is_move:
            self.image = self.__sprites_idle_down[int(self.__current_sprite)]
        elif self.__current_direction == Direction.LEFT and not self.__is_move:
            self.image = self.__sprites_idle_left[int(self.__current_sprite)]
        elif self.__current_direction == Direction.RIGHT and not self.__is_move:
            self.image = self.__sprites_idle_right[int(self.__current_sprite)]
        elif self.__current_direction == Direction.UP and self.__is_move:
            self.image = self.__sprites_move_up[int(self.__current_sprite)]
        elif self.__current_direction == Direction.DOWN and self.__is_move:
            self.image = self.__sprites_move_down[int(self.__current_sprite)]
        elif self.__current_direction == Direction.LEFT and self.__is_move:
            self.image = self.__sprites_move_left[int(self.__current_sprite)]
        elif self.__current_direction == Direction.RIGHT and self.__is_move:
            self.image = self.__sprites_move_right[int(self.__current_sprite)]

    def movement(self, diff: float) -> None:
        """Handles the movement of the player."""
        keys = pg.key.get_pressed()

        self.__direction_up_keys = [
            keys[pg.K_w],
            keys[pg.K_UP]
        ]
        self.__direction_down_keys = [
            keys[pg.K_s],
            keys[pg.K_DOWN]
        ]
        self.__direction_left_keys = [
            keys[pg.K_a],
            keys[pg.K_LEFT]
        ]
        self.__direction_right_keys = [
            keys[pg.K_d],
            keys[pg.K_RIGHT]
        ]
        self.__all_direction_keys = [
            *self.__direction_up_keys,
            *self.__direction_down_keys,
            *self.__direction_left_keys,
            *self.__direction_right_keys
        ]

        # handle the player idle animation
        if any(self.__direction_up_keys):
            self.__current_direction = Direction.UP
            self.__player_pos.y -= diff
        if any(self.__direction_down_keys):
            self.__current_direction = Direction.DOWN
            self.__player_pos.y += diff
        if any(self.__direction_left_keys):
            self.__current_direction = Direction.LEFT
            self.__player_pos.x -= diff
        if any(self.__direction_right_keys):
            self.__current_direction = Direction.RIGHT
            self.__player_pos.x += diff

        # handle the player movement animation
        if any(self.__all_direction_keys):
            self.toggle_move(True)
        else:
            self.toggle_move(False)

    def toggle_move(self, is_move: bool) -> None:
        self.__is_move = is_move
