from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


# def get_first_item(items: list[str]) -> str:
#     return items[0]


# def get_first_item(items: list[str | int]) -> str | int:
#     return items[0]


# def get_first_item(items: list[T]) -> T:
#     return items[0]


def get_first_item(items: Sequence[T]) -> T:
    return items[0]


# def get_first_item[T](items: list[T]) -> T:
#     return items[0]


print(get_first_item(["a", "b", "c"]))
print(get_first_item([1, 2, 3]))
print(get_first_item([[1, 2, 3], ["a", "b", "c"]]))
print(get_first_item("hello"))  # str
print(get_first_item((1, 2, 3)))  # tuple
