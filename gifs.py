import tempfile
import time

from PIL import Image
from PIL import GifImagePlugin

GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS


def convert_gif_to_spritesheet(gif_filepath):
    with Image.open(gif_filepath) as im:
        print(f"{im.n_frames} frames")
        print(f"Size is {im.size}")
        spritesheet_size = (im.size[0] * im.n_frames, im.size[1])

        spritesheet = Image.new("RGB", spritesheet_size)

        print(f"Spritesheet size is {spritesheet_size}")

        for frame in range(im.n_frames):
            im.seek(frame)
            spritesheet.paste(im, (frame * im.size[0], 0))

        outfile = tempfile.NamedTemporaryFile(suffix=".png")
        spritesheet.save(outfile)

        return outfile


if __name__ == '__main__':
    spritesheet = convert_gif_to_spritesheet(r"G:\Development\HockeyScoreboard\goal-hockey-goal.gif")
    print(spritesheet.name)
