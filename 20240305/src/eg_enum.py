from enum import Enum


class Color(Enum):
    RED = "RED"
    BLUE = "BLUE"
    YELLOW = "YELLOW"


class MixedColor(Enum):
    GREEN = "GREEN"
    PURPLE = "PURPLE"
    ORANGE = "ORANGE"


def mix_color(color1: Color, color2: Color) -> MixedColor:
    if {Color.RED, Color.BLUE} == {color1, color2}:
        return MixedColor.PURPLE
    if {Color.RED, Color.YELLOW} == {color1, color2}:
        return MixedColor.ORANGE
    if {Color.BLUE, Color.YELLOW} == {color1, color2}:
        return MixedColor.GREEN


print(mix_color(Color.BLUE, Color.RED))
print(mix_color(Color("RED"), None))
