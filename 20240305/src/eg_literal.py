from typing import Literal

Color = Literal["RED", "BLUE", "YELLOW"]
MixedColor = Literal["GREEN", "PURPLE", "ORANGE"]


def mix_color(color1: Color, color2: Color) -> MixedColor | None:
    if {"RED", "BLUE"} == {color1, color2}:
        return "PURPLE"
    if {"RED", "YELLOW"} == {color1, color2}:
        return "ORANGE"
    if {"BLUE", "YELLOW"} == {color1, color2}:
        return "GREEN"

    return None


mix_color("RED", "BLUE")
mix_color("ORANGE", "PURPLE")


def mix_color(color1: str, color2: str) -> str | None:
    if {"RED", "BLUE"} == {color1, color2}:
        return "PURPLE"
    if {"RED", "YELLOW"} == {color1, color2}:
        return "ORANGE"
    if {"BLUE", "YELLOW"} == {color1, color2}:
        return "GREEN"

    return None
