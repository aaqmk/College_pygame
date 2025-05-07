import os
import sys

import pygame as pg


def load_image(image_path: str, colorkey=None) -> pg.Surface:
    """
    Функция, открывающая картинку по имени, расположенную в каталоге `/data/img`
     - `colorkey == None` - используем исходный альфа-канал
     - `colorkey as pygame.Color` - используем выбранный хромакей
     - `colorkey == -1` - используем в качестве хромакея цвет пикселя в левом верхнем углу

    :param image_path:  имя файла
    :param colorkey:    хромокей
    :return:            слой с изображением
    """
    fullname = os.path.join('data', 'img', image_path)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением {fullname} не найден!', file=sys.stderr)
        sys.exit(404)
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
