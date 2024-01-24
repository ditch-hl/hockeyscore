import os.path
import tempfile

import pygame.time
from PIL import GifImagePlugin
from PIL import Image

import config

GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS

FRAMERATE = 20  # frames per second
MS_PER_FRAME = 1000 / FRAMERATE


class Animation:
    def __init__(self, filename: str, im: pygame.Surface):
        self.im = im
        self.accum = 0
        self.last_tick = 0
        self.current_frame = 0
        self.n_frames = int(filename[:filename.find("_")])
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

        with tempfile.NamedTemporaryFile(prefix=f"{im.n_frames}_", suffix=".jpg", delete_on_close=False,
                                         dir=".") as outfile:
            spritesheet = spritesheet.resize(
                size=(int(im.size[0] * scale_factor * im.n_frames), int(im.size[1] * scale_factor)))
            spritesheet.save(outfile)
            filepath = outfile.file.name
            with open(filepath, mode="rb") as infile:
                spritesheet_im = pygame.image.load(infile)
                _, tail = os.path.split(outfile.file.name)

                return tail, spritesheet_im


if __name__ == '__main__':
    spritesheet = convert_gif_to_spritesheet(r"G:\Development\HockeyScoreboard\goal-hockey-goal.gif")
    print(spritesheet.name)
