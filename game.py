from enum import Enum

import pygame
from gpiozero import Button

import gifs
from config import PERIOD_LENGTH_IN_MINUTES

button = Button(4, hold_time=3)
home_score_pin = Button(17, pull_up=False)


class GameState(Enum):
    PREGAME = 1
    PLAYING = 2
    BETWEEN_PERIODS = 3
    GOAL = 4
    GAME_OVER = 5
    PAUSED = 6


class Game:
    def __init__(self):
        self.game_time = 0
        self.game_state = GameState.PREGAME
        self.home_score = 0
        self.visitor_score = 0
        self.period = 1
        self.last_tick = pygame.time.get_ticks()
        self.tick_accum = 0
        self.blinker = False
        self.state_time = 0
        self.animation = None
        self.gif_pack = None
        button.when_held = lambda: self.new_game()
        home_score_pin.when_pressed = lambda: self.home_goal()

        self.new_game()

    def home_goal(self):
        if self.game_state == GameState.PLAYING:
            self.home_score += 1

    def visitor_goal(self):
        if self.game_state == GameState.PLAYING:
            self.visitor_score += 1

    def new_game(self):
        self.game_time = PERIOD_LENGTH_IN_MINUTES * 60
        self.home_score = 0
        self.visitor_score = 0
        self.period = 1
        self.state_time = 0
        self.game_state = GameState.PREGAME
        self.animation = None

    def get_time_readout(self):
        minutes = int(self.game_time / 60)
        seconds = self.game_time % 60

        if self.game_state == GameState.PREGAME:
            return '--:--'

        return f'{str(minutes).zfill(2)}:{str(seconds).zfill(2)}'

    def tick(self):
        current_tick = pygame.time.get_ticks()
        self.tick_accum += current_tick - self.last_tick
        self.last_tick = current_tick

        if button.is_pressed:
            if self.game_state == GameState.PREGAME:
                self.game_state = GameState.PLAYING
            elif self.game_state == GameState.PLAYING:
                self.game_state = GameState.PAUSED
            elif self.game_state == GameState.PAUSED:
                self.game_state = GameState.PLAYING
            elif self.game_state == GameState.BETWEEN_PERIODS:
                self.game_time = PERIOD_LENGTH_IN_MINUTES * 60
                self.animation = None
                self.game_state = GameState.PLAYING

        if self.tick_accum >= 1000:
            self.blinker = not self.blinker
            self.tick_accum = 0

            if self.game_state == GameState.PLAYING:
                self.game_time -= 1
                if self.game_time == 0:
                    if self.period == 3:
                        self.game_state = GameState.GAME_OVER
                    else:
                        self.period += 1
                        self.game_state = GameState.BETWEEN_PERIODS
                        self.state_time = 10
                        self.animation = gifs.pick_gif(self.gif_pack.between_periods)
            elif self.game_state in [GameState.GOAL]:
                self.state_time -= 1
                if self.state_time == 0:
                    self.animation = None
                    self.game_state = GameState.PLAYING
