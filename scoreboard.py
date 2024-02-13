import sys

import pygame.font
from gpiozero import Button
from pygame.locals import *

import gifs
from config import GAME_TIME_POSITION, HOME_SCORE_POSITION, VISITOR_SCORE_POSITION, PERIOD_NUMBER_POSITION, \
    LCD_BACKGROUND_COLOR, SCREEN_RESOLUTION, LCD_TEXT_COLOR
from game import Game, GameState, button
from gifs import Animation

pygame.init()
pygame.font.init()

time_font = pygame.font.Font(r"digital-7.monoitalic.ttf", size=111)
count_font = pygame.font.Font(r"digital-7.monoitalic.ttf", size=150)

DISPLAYSURF = pygame.display.set_mode(SCREEN_RESOLUTION)
DISPLAYSURF.fill((0, 0, 0))
pygame.display.set_caption("Hockey Scoreboard")
#pygame.display.toggle_fullscreen()

# Reusable surfaces
score_background_surf = count_font.render("00", False, LCD_BACKGROUND_COLOR, (0, 0, 0))
game_time_background_surf = time_font.render("00:00", False, LCD_BACKGROUND_COLOR, (0, 0, 0))
game_time_background_rect = game_time_background_surf.get_rect()
game_time_background_rect.center = GAME_TIME_POSITION

period_background_surf = count_font.render("0", False, LCD_BACKGROUND_COLOR, (0, 0, 0))
period_background_rect = period_background_surf.get_rect()
period_background_rect.center = PERIOD_NUMBER_POSITION

background = pygame.image.load(r"ScoreboardTemplate.png")
DISPLAYSURF.blit(background, background.get_rect())

game = Game()
game.game_state = GameState.PREGAME
game.gif_pack = gifs.GifPack()
game.gif_pack.load_gifs()

# spritesheet_filename, gif_spritesheet = gifs.convert_gif_to_spritesheet(r"zamboni.gif")
# animation = Animation(spritesheet_filename, gif_spritesheet)

# animation.start()

def draw_game_time():
    DISPLAYSURF.blit(game_time_background_surf, game_time_background_rect)

    game_time = time_font.render(game.get_time_readout(), False, LCD_TEXT_COLOR)
    game_time_rect = game_time.get_rect()
    game_time_rect.center = GAME_TIME_POSITION
    DISPLAYSURF.blit(game_time, game_time_rect)


def draw_home_score():
    score_background_rect = score_background_surf.get_rect()
    score_background_rect.center = HOME_SCORE_POSITION
    DISPLAYSURF.blit(score_background_surf, score_background_rect)
    home_score_surf = count_font.render("12", False, LCD_TEXT_COLOR)
    home_score_rect = home_score_surf.get_rect()
    home_score_rect.center = HOME_SCORE_POSITION
    DISPLAYSURF.blit(home_score_surf, home_score_rect)


def draw_visitor_score():
    score_background_rect = score_background_surf.get_rect()
    score_background_rect.center = VISITOR_SCORE_POSITION
    DISPLAYSURF.blit(score_background_surf, score_background_rect)
    visitor_score_surf = count_font.render("09", False, LCD_TEXT_COLOR)
    visitor_score_rect = visitor_score_surf.get_rect()
    visitor_score_rect.center = VISITOR_SCORE_POSITION
    DISPLAYSURF.blit(visitor_score_surf, visitor_score_rect)


def draw_period():
    DISPLAYSURF.blit(period_background_surf, period_background_rect)
    period_surf = count_font.render(str(game.period), False, LCD_TEXT_COLOR)
    period_rect = period_surf.get_rect()
    period_rect.center = PERIOD_NUMBER_POSITION
    DISPLAYSURF.blit(period_surf, period_rect)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    game.tick()

    DISPLAYSURF.fill((0, 0, 0))
    if game.animation is None:
        # blit the background image
        DISPLAYSURF.blit(background, background.get_rect())

        # draw the various readouts
        draw_game_time()
        draw_home_score()
        draw_visitor_score()
        draw_period()
    else:
        game.animation.draw(game.animation.centered_pos, DISPLAYSURF)
        game.animation.tick()

    pygame.display.update()
