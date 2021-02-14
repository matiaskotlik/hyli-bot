from io import BytesIO

from aiohttp.client import ClientSession
from PIL import Image

from utils import run_in_executor


def get_frames(spritesheet, width: int, height: int, sheet_width: int):
    return [
        spritesheet.crop(
            (i * width, 0, (i + 1) * width, height)).convert('RGBA')
        for i in range(sheet_width // width)
    ]


class Petpet:
    default_frame_offsets = [  # xywh
        [0, 0, 0, 0],
        [-4, 12, 4, -12],
        [-12, 18, 12, -18],
        [-8, 12, 4, -12],
        [-4, 0, 0, 0]
    ]

    def __init__(self,
                 session: ClientSession,
                 squish: float = 1.25,
                 scale: float = 0.875,
                 fps: int = 14,
                 sprite_x: float = 14,
                 sprite_y: float = 20,
                 frame_offsets: list[list[int]] = None,
                 spritesheet_path: str = 'template.png'):
        self.session = session
        self.squish = squish
        self.scale = scale
        self.fps = fps
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        self.frame_offsets = frame_offsets or self.default_frame_offsets

        self.sprite_width = 112
        self.sprite_height = 112
        self.sprite_size = (self.sprite_width, self.sprite_height)
        self.base_frame = Image.new('RGBA', self.sprite_size,
                                    (255, 255, 255, 255))  # TODO blocking
        self.spritesheet = Image.open(spritesheet_path)  # TODO blocking
        self.frames = get_frames(self.spritesheet, self.sprite_width,
                                 self.sprite_height, self.spritesheet.width)

    def get_sprite_offset(self, idx: int):
        offset = self.frame_offsets[idx]
        return [
            self.sprite_x + offset[0] * (self.squish * 0.4),
            self.sprite_y + offset[1] * (self.squish * 0.9),
            (self.sprite_width + offset[2] * self.squish) * self.scale,
            (self.sprite_height + offset[3] * self.squish) * self.scale
        ]

    @run_in_executor
    def save_gif(self, out, frames: list[Image.Image]):
        if frames:
            frames[0].save(out, 'GIF', save_all=True, append_images=frames[1:],
                           duration=(1 / self.fps) * 1000, loop=0)
        else:
            raise ValueError('Need a valid frame to save')

    @run_in_executor
    def make_frames(self, image) -> list[Image.Image]:
        image_frame_count = getattr(image, "n_frames", 1)
        converted = False
        if image_frame_count == 1:
            converted = True
            image = image.convert('RGBA')

        frames = []
        frame_count = len(self.frames)
        for i, template_frame in enumerate(self.frames):
            frame = self.base_frame.copy()

            percentage = i / (frame_count - 1)
            seek = int(percentage * (image_frame_count - 1))
            if seek:
                image.seek(seek)

            image_frame = image.copy()
            if not converted:
                image_frame = image_frame.convert('RGBA')

            x, y, w, h = self.get_sprite_offset(i)
            image_frame = image_frame.resize((int(w), int(h)))

            frame.paste(image_frame, (int(x), int(y)))
            frame = Image.alpha_composite(frame, template_frame)

            frames.append(frame)
        return frames

    async def download_image(self, url: str):
        async with self.session.get(url) as res:
            return BytesIO(await res.read())

    @run_in_executor
    def open_image(self, fp) -> Image.Image:
        return Image.open(fp)

    async def petify(self, url: str, out):

        try:
            fp = await self.download_image(url)
        except Exception as e:
            raise Exception(f'Failed to download image from url {url}') from e

        try:
            image = await self.open_image(fp)
            frames = await self.make_frames(image)
            await self.save_gif(out, frames)
        except Exception as e:
            raise Exception(f'Failed to generate petpet from {url}') from e
