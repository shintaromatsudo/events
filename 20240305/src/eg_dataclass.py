from dataclasses import dataclass

from enum import Enum, auto


@dataclass(frozen=True)
class Fruit:
    name: str
    color: str
    price: float
    count: int

    def total_price(self) -> float:
        return self.price * self.count


apple = Fruit("apple", "red", 100.0, 10)
print(apple.price)
print(apple.total_price())
# apple.price = 200.0
# print(apple.price)


def print_fruit(fruit: Fruit) -> None:
    fruit.name = "cherry"
    print(fruit.name)


class Color(Enum):
    RED = auto()
    BLUE = auto()
    YELLOW = auto()


class MixedColor(Enum):
    GREEN = auto()
    PURPLE = auto()
    ORANGE = auto()


@dataclass(frozen=True)
class MixColor:
    color1: Color
    color2: Color

    def mix_color(self) -> Color | MixedColor:
        if self.color1 == Color.RED and self.color2 == Color.BLUE:
            return MixedColor.PURPLE
        if self.color1 == Color.RED and self.color2 == Color.YELLOW:
            return MixedColor.ORANGE
        if self.color1 == Color.BLUE and self.color2 == Color.YELLOW:
            return MixedColor.GREEN

        return self.color1

    def __post_init__(self):
        if self.color1 == self.color2:
            raise ValueError("color1 and color2 must be different")


def change_color(color: Color) -> None:
    color = Color.BLUE
    print(color)
    return color


mixing_color = MixColor(Color.RED, Color.BLUE)
print(mixing_color.mix_color())
new_color = change_color(mixing_color.color1)
