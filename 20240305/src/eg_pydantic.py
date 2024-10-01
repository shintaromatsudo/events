from pydantic import BaseModel, model_validator
from enum import Enum, auto
from typing import Literal


class Color(Enum):
    RED = auto()
    BLUE = auto()
    YELLOW = auto()


class MixedColor(Enum):
    GREEN = auto()
    PURPLE = auto()
    ORANGE = auto()


class ColorPattern(Enum):
    PURPLE = {Color.RED, Color.BLUE}
    ORANGE = {Color.RED, Color.YELLOW}
    GREEN = {Color.BLUE, Color.YELLOW}


class MixColor(BaseModel, frozen=True):
    color1: Color
    color2: Color

    @model_validator(mode="before")
    @classmethod
    def validate_secret(cls, d: dict) -> dict:
        if d["color1"] == d["color2"]:
            raise ValueError("must be different colors")
        return d

    # def mix_color(self) -> MixedColor:
    #     if {Color.RED, Color.BLUE} == {self.color1, self.color2}:
    #         return MixedColor.PURPLE
    #     if {Color.RED, Color.YELLOW} == {self.color1, self.color2}:
    #         return MixedColor.ORANGE
    #     return MixedColor.GREEN

    def mix_color(self) -> Literal["PURPLE", "ORANGE", "GREEN"]:
        return ColorPattern({self.color1, self.color2}).name


print(MixColor(color1=Color.RED, color2=Color.BLUE).mix_color())

mix = MixColor(color1=Color.RED, color2=Color.BLUE)
mix2 = MixColor(color1=Color.RED, color2="BLUE")
mix3 = MixColor(color1=Color.RED, color2=Color.GOLD)
mix4 = MixColor(color1=Color.RED, color2=Color.RED)
mix5 = MixColor(color1=Color.RED, color2=None)

mix.color1 = Color.YELLOW
