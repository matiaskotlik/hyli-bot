from PIL import Image, ImageSequence
import requests
import sys


class Petpet:
    def __init__(self,
                 squish: float = 1.25,
                 scale: float = 0.875,
                 fps: int = 14,
                 sprite_x: float = 14,
                 sprite_y: float = 20):
        self.squish = squish
        self.scale = scale
        self.fps = fps
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y

        self.sprite_width = 112
        self.sprite_height = 112
        self.spritesheet = Image.open('template.png')
        self.frames = [
            self.spritesheet.crop(
                (i * self.sprite_width, 0, (i + 1) * self.sprite_width,
                 self.sprite_height)).convert('RGBA')
            for i in range(self.spritesheet.width // self.sprite_width)
        ]
        self.frame_offsets = [  # xywh
            [0, 0, 0, 0], [-4, 12, 4, -12], [-12, 18, 12, -18],
            [-8, 12, 4, -12], [-4, 0, 0, 0]
        ]

        self.base_frame = Image.new('RGBA', self.sprite_size,
                                    (255, 255, 255, 255))

    def get_sprite_offset(self, idx: int):
        offset = self.frame_offsets[idx]
        return [
            self.sprite_x + offset[0] * (self.squish * 0.4),
            self.sprite_y + offset[1] * (self.squish * 0.9),
            (self.sprite_width + offset[2] * self.squish) * self.scale,
            (self.sprite_height + offset[3] * self.squish) * self.scale
        ]

    @property
    def sprite_size(self):
        return (self.sprite_width, self.sprite_height)

    def save_gif(self, out, frames):
        if frames:
            frames[0].save(out, 'GIF',
                           save_all=True,
                           append_images=frames[1:],
                           duration=(1 / self.fps) * 1000,
                           loop=0)
        else:
            raise ValueError('Need a valid frame')

    def petify(self, url: str, out):
        try:
            image = Image.open(requests.get(url, stream=True).raw)
        except Exception:
            print(f'Failed to download image from url {url}', file=sys.stderr)
            return

        try:
            image = image.convert('RGBA')
            frames = []
            frame_count = len(self.frames)
            for i, template_frame in enumerate(self.frames):
                frame = self.base_frame.copy()

                image_frame = image.copy()
                x, y, w, h = self.get_sprite_offset(i)
                image_frame.thumbnail((w, h))

                frame.paste(image_frame, (int(x), int(y)))
                frame = Image.alpha_composite(frame, template_frame)

                frames.append(frame)

            self.save_gif(out, frames)
        except Exception as e:
            print(f'Failed to generate petpet image', file=sys.stderr)
            raise e
