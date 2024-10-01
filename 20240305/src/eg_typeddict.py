from typing import TypedDict, NotRequired


class FruitDict(TypedDict):
    name: str
    color: NotRequired[str]
    price: int
    count: int


apple: FruitDict = {"name": "apple", "price": 100.0, "count": "10"}
print(apple["price"])
apple["price"] = 200
print(apple["price"])
