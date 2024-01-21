import sys

import pygame
import pygame.font
from pygame.locals import *

from game import Game

pygame.init()
pygame.font.init()

time_font = pygame.font.Font(r"G:\Development\HockeyScoreboard\digital-7.monoitalic.ttf", size=111)
count_font = pygame.font.Font(r"G:\Development\HockeyScoreboard\digital-7.monoitalic.ttf", size=150)

DISPLAYSURF = pygame.display.set_mode((800, 480))
DISPLAYSURF.fill((255, 255, 255))
pygame.display.set_caption("Hockey Scoreboard")

background = pygame.image.load("G:\Development\HockeyScoreboard\ScoreboardTemplate.png")
DISPLAYSURF.blit(background, background.get_rect())

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    game.tick()

    # blit the background image
    DISPLAYSURF.blit(background, background.get_rect())

    # render the game time
    game_time = time_font.render(game.get_time_readout(), False, (255, 0, 0), (0, 0, 0))

    game_time_rect = game_time.get_rect()
    game_time_rect.center = (397, 118)
    DISPLAYSURF.blit(game_time, game_time_rect)

    # render the home score
    home_score_surf = count_font.render("12", False, (255, 0, 0), (0, 0, 0))

    home_score_rect = home_score_surf.get_rect()
    home_score_rect.center = (130, 238)
    DISPLAYSURF.blit(home_score_surf, home_score_rect)

    # render the visitor score
    visitor_score_surf = count_font.render("09", False, (255, 0, 0), (0, 0, 0))

    visitor_score_rect = visitor_score_surf.get_rect()
    visitor_score_rect.center = (655, 238)
    DISPLAYSURF.blit(visitor_score_surf, visitor_score_rect)

    # render the period
    period_surf = count_font.render("2", False, (255, 0, 0), (0, 0, 0))

    period_rect = period_surf.get_rect()
    period_rect.center = (397, 355)
    DISPLAYSURF.blit(period_surf, period_rect)


    pygame.display.update()
