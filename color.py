'''
    https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
'''

from typing import Any


class Color:

    class Code:
        white = 252
        green = 34
        yellow = 172
        lightgray = 248
        darkgray = 242

    end = '\033[0m'

    @staticmethod
    def start(color):
        c = _color_code(color)
        return f'\033[{c}m'


class ColoredPrinter(object):
    def __init__(self, color, text=None):
        self._color = color
        self._text = text

    def __call__(self, text):
        return colored_string(self._color, text)

    def __str__(self) -> str:
        return self(self._text)


def colored_string(color, text):
    c = _color_code(color)
    return f'\033[{c}m{text}{Color.end}'


def _color_code(color):
    color_parts = color.strip().replace(' ', '').lower().split('/')
    if len(color_parts) == 1:
        color_parts.append('')

    foreground = getattr(Color.Code, color_parts[0], '')
    if foreground:
        foreground = f'38;5;{foreground}'
    background = getattr(Color.Code, color_parts[1], '')
    if background:
        background = f'48;5;{background}'

    f = foreground
    if background:
        if f:
            f = f + ';'
        f = f + background

    return f


if __name__ == '__main__':
    import os
    os.system('color')

    print(colored_string("White /  Green/s", "white on green"))
    print(colored_string("Yellow/Green   ", "yellow on green"))
    print(colored_string("Green", "green on black"))
    print(colored_string("/Green", "default on green"))
    print()
    print(f'{Color.start("Yellow/Green")}yellow on green{Color.end}')
