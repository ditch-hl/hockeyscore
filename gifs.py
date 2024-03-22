import os.path
import random
import tempfile

import pygame.time
from PIL import GifImagePlugin
from PIL import Image

import config

GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS

FRAMERATE = 20  # frames per second
MS_PER_FRAME = 1000 / FRAMERATE


class GifPack:
    def __init__(self):
        self.home_goal = []
        self.visitor_goal = []
        self.between_periods = []
        self.game_over = []

    def load_gifs(self):
        self.home_goal = load_gifs_from_directory("gifs/home_goal")
        self.visitor_goal = load_gifs_from_directory("gifs/visitor_goal")
        self.between_periods = load_gifs_from_directory("gifs/between_periods")
        self.game_over = load_gifs_from_directory("gifs/game_over")

        loaded_gif_paths = [path for path, surf in self.home_goal]
        loaded_gif_paths.extend([path for path, surf in self.visitor_goal])
        loaded_gif_paths.extend([path for path, surf in self.between_periods])
        loaded_gif_paths.extend([path for path, surf in self.game_over])

        clear_gifs(loaded_gif_paths)


def load_gifs_from_directory(dir) -> list[tuple[str, pygame.Surface]]:
    result: list[tuple[str, pygame.Surface | pygame.SurfaceType]] = []
    for filepath in os.listdir(dir):
        if filepath.lower().endswith(".gif"):
            gif_im = Image.open(os.path.join(dir, filepath))
            jpg_filepath = os.path.join("./jpgs", f'{gif_im.n_frames}_{filepath[:filepath.rindex(".")]}.jpg')
            if not os.path.exists(jpg_filepath):
                print(f"Generating new gif spritesheet: {jpg_filepath}")
                jpg_filepath, gif_surf = convert_gif_to_spritesheet(os.path.join(dir, filepath))
                result.append((os.path.join("./jpgs", jpg_filepath), gif_surf))
            else:
                print(f"Found existing gif spritesheet: {jpg_filepath}")
                gif_surf = pygame.image.load(jpg_filepath)
                result.append((jpg_filepath, gif_surf))

    return result


def clear_gifs(loaded_gifs: list[str]):
    for filepath in os.listdir("./jpgs"):
        full_path = os.path.join("./jpgs", filepath)
        if filepath.lower().endswith("jpg") and full_path not in loaded_gifs:
            print(f"Removing unneeded gif spritesheet: {full_path}\n")
            os.remove(full_path)


class Animation:
    def __init__(self, filename: str, im: pygame.Surface):
        self.im = im
        self.accum = 0
        self.last_tick = 0
        self.current_frame = 0

        _, img_name = os.path.split(filename)
        self.n_frames = int(img_name[:img_name.find("_")])
        self.size = (self.im.get_size()[0] / self.n_frames, self.im.get_size()[1])

        self.centered_pos = (
            config.SCREEN_RESOLUTION[0] / 2 - self.size[0] / 2, config.SCREEN_RESOLUTION[1] / 2 - self.size[1] / 2)

    def reset(self):
        self.accum = 0
        self.last_tick = 0
        self.current_frame = 0

    def start(self):
        self.reset()
        self.last_tick = pygame.time.get_ticks()

    def tick(self):
        current_tick = pygame.time.get_ticks()
        self.accum += current_tick - self.last_tick
        self.last_tick = current_tick

        if self.accum >= MS_PER_FRAME:
            self.accum = 0
            self.current_frame = (self.current_frame + 1) % self.n_frames

    def draw(self, position: tuple[int, int], surf: pygame.Surface):
        area = pygame.Rect(self.current_frame * self.size[0], 0, self.size[0], self.size[1])
        surf.blit(self.im, position, area=area)


def pick_gif(gif_list: list[tuple[str, pygame.Surface]]):
    if not gif_list:
        return None

    gif_path, gif_surf = gif_list[random.randrange(start=0, stop=len(gif_list))]
    return Animation(gif_path, gif_surf)


def convert_gif_to_spritesheet(gif_filepath: str) -> [str, pygame.Surface]:
    with Image.open(gif_filepath) as im:
        print(f"{im.n_frames} frames")
        print(f"Size is {im.size}")

        width_difference = abs(im.size[0] - config.SCREEN_RESOLUTION[0])
        height_difference = abs(im.size[1] - config.SCREEN_RESOLUTION[1])

        scale_factor = config.SCREEN_RESOLUTION[0] / (im.size[0])
        if height_difference < width_difference:
            scale_factor = config.SCREEN_RESOLUTION[1] / (im.size[1])

        print(f"Scaling gif {scale_factor}\n")

        spritesheet_size = (im.size[0] * im.n_frames, im.size[1])

        spritesheet = Image.new("RGB", spritesheet_size)

        print(f"Spritesheet size is {spritesheet_size}")

        for frame in range(im.n_frames):
            im.seek(frame)
            spritesheet.paste(im, (frame * im.size[0], 0))

        _, gif_tail = os.path.split(gif_filepath)

        outfile = open(f'./jpgs/{im.n_frames}_{gif_tail[:gif_tail.rindex(".")]}.jpg', "w+b")
        spritesheet = spritesheet.resize(
            size=(int(im.size[0] * scale_factor * im.n_frames), int(im.size[1] * scale_factor)))
        spritesheet.save(outfile)

        filepath = outfile.name
        outfile.close()
        print(filepath)
        with open(filepath, mode="r+b") as infile:
            spritesheet_im = pygame.image.load(infile)
            _, tail = os.path.split(filepath)

            return tail, spritesheet_im

# if __name__ == '__main__':
#    spritesheet = convert_gif_to_spritesheet(r"G:\Development\HockeyScoreboard\goal-hockey-goal.gif")
#    print(spritesheet.name)
