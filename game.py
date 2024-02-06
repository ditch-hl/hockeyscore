from enum import Enum

import pygame

from config import PERIOD_LENGTH_IN_MINUTES

class GameState(Enum):
    PREGAME = 1
    PLAYING = 2
    BETWEEN_PERIODS = 3
    GOAL = 4
    GAME_OVER = 5

class Game:
    def __init__(self):
        self.game_time = 0
        self.game_state = GameState.PREGAME
        self.home_score = 0
        self.visitor_score = 0
        self.period = 0
        self.last_tick = pygame.time.get_ticks()
        self.tick_accum = 0
        self.state_time = 0
        self.animation = None
        self.gif_pack = None

        self.new_game()

    def new_game(self):
        self.game_time = PERIOD_LENGTH_IN_MINUTES * 60
        self.home_score = 0
        self.visitor_score = 0
        self.period = 0
        self.state_time = 0
        self.game_state = GameState.PREGAME
        self.animation = None

    def get_time_readout(self):
        minutes = int(self.game_time / 60)
        seconds = self.game_time % 60

        return f'{str(minutes).zfill(2)}:{str(seconds).zfill(2)}'

    def tick(self):
        current_tick = pygame.time.get_ticks()
        self.tick_accum += current_tick - self.last_tick
        self.last_tick = current_tick

        if self.tick_accum >= 1000:
            self.tick_accum = 0

            if self.game_state == GameState.PLAYING:
                self.game_time -= 1
                if self.game_time == 0:
                    self.period -= 1
                    if self.period == 0:
                        self.game_state = GameState.GAME_OVER

                    else:
                        self.game_state = GameState.BETWEEN_PERIODS
            elif self.game_state in [GameState.GOAL, GameState.BETWEEN_PERIODS]:
                self.state_time -= 1
                if self.state_time == 0:
                    self.game_state = GameState.PLAYING

