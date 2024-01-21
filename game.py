import pygame

from config import PERIOD_LENGTH_IN_MINUTES


class Game:
    def __init__(self):
        self.game_time = 0
        self.home_score = 0
        self.visitor_score = 0
        self.period = 0
        self.last_tick = pygame.time.get_ticks()
        self.tick_accum = 0

        self.new_game()

    def new_game(self):
        self.game_time = PERIOD_LENGTH_IN_MINUTES * 60
        self.home_score = 0
        self.visitor_score = 0
        self.period = 0

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
            self.game_time -= 1
