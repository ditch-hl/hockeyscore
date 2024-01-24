import os.path
import tempfile
import time

import pygame.time
from PIL import Image
from PIL import GifImagePlugin

GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS

FRAMERATE = 10 # frames per second
MS_PER_FRAME = 1000 / FRAMERATE
class Animation:
    def __init__(self, filename: str, im: pygame.Surface):
        self.im = im
        self.accum = 0
        self.last_tick = 0
        self.current_frame = 0
        self.n_frames = int(filename[:filename.find("_")])
        self.size = (self.im.get_size()[0] / self.n_frames, self.im.get_size()[1])

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


def convert_gif_to_spritesheet(gif_filepath: str) -> [str, pygame.Surface]:
    with Image.open(gif_filepath) as im:
        print(f"{im.n_frames} frames")
        print(f"Size is {im.size}")
        spritesheet_size = (im.size[0] * im.n_frames, im.size[1])

        spritesheet = Image.new("RGB", spritesheet_size)

        print(f"Spritesheet size is {spritesheet_size}")

        for frame in range(im.n_frames):
            im.seek(frame)
            spritesheet.paste(im, (frame * im.size[0], 0))

        with tempfile.NamedTemporaryFile(prefix=f"{im.n_frames}_", suffix=".png", delete_on_close=False, dir=".") as outfile:
            spritesheet.save(outfile)
            filepath = outfile.file.name
            with open(filepath, mode="rb") as infile:
                spritesheet_im = pygame.image.load(infile)
                _, tail = os.path.split(outfile.file.name)

                return tail, spritesheet_im


if __name__ == '__main__':
    spritesheet = convert_gif_to_spritesheet(r"G:\Development\HockeyScoreboard\goal-hockey-goal.gif")
    print(spritesheet.name)
