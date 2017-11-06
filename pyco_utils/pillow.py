# from wand.image import Image
from enum import Enum
from PIL import Image


class ImageSuffix(Enum):
    crop = '_crop.'
    resize = '_resize.'
    avatar = '_avatar.'
    thumbnail = '_thumb.'


def crop_square(image, output=''):
    if output == '':
        output = image.filename.replace('.', ImageSuffix.crop.value)
    w, h = image.size
    m = min(w, h)
    box = (0, 0, m, m)
    c = image.crop(box)
    c.save(output)
    return c


def thumbnail(file, output='', width=64, height=64):
    with Image.open(file) as f:
        if output == '':
            output = f.filename.replace('.', ImageSuffix.thumbnail.value)
        crop_square(f)
        f.thumbnail((width, height))
        f.save(output)


def resize(file, output='', width=64, height=64):
    with Image.open(file) as f:
        if output == '':
            output = f.filename.replace('.', ImageSuffix.resize.value)
        m = f.resize((width, height))
        # out <PIL.Image.Image image mode=P size=64x64 at 0x1066133C8>
        m.save(output)


def gen_avatar(file, w=64, h=64, output=''):
    with Image.open(file) as f:
        fw, fh = f.size
        output = f.filename.replace('.', ImageSuffix.avatar.value)
        m = min(fw, fh)
        box = (0, 0, m, m)
        image = f.crop(box)
        image.thumbnail((w, h))
        image.save(output)
        print(output)

