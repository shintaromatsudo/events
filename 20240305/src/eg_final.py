from typing import Final

# fruit = "cherry"
# print(fruit)

fruit: Final = "apple"
fruit = "banana"


def print_fruit(fruit) -> None:
    fruit = "cherry"
    print(fruit)


fruit: Final = "apple"
print_fruit(fruit)
