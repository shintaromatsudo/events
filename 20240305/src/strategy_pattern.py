from typing import Protocol
from pydantic import BaseModel
from enum import Enum, auto


class Color(Enum):
    RED = auto()
    BLUE = auto()
    YELLOW = auto()


class ColorPattern(Enum):
    PURPLE = {Color.RED, Color.BLUE}
    ORANGE = {Color.RED, Color.YELLOW}
    GREEN = {Color.BLUE, Color.YELLOW}


class ColorDuck(Protocol):
    def mix_color(self):
        pass


class Red(BaseModel, frozen=True):
    with_color: Color

    def mix_color(self):
        return ColorPattern({Color.RED, self.with_color}).name


class Blue(BaseModel, frozen=True):
    with_color: Color

    def mix_color(self):
        return ColorPattern({Color.BLUE, self.with_color}).name


class Yellow(BaseModel, frozen=True):
    with_color: Color

    def mix_color(self):
        return ColorPattern({Color.YELLOW, self.with_color}).name


class Mixer:
    def __init__(self, color: Color):
        self._color = color

    def mix_color(self):
        return self._color.mix_color()


red_blue = Red(with_color=Color.BLUE)
print(Mixer(red_blue).mix_color())
