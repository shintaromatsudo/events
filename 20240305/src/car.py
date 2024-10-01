from pydantic import BaseModel
from typing import Final


class Fuel(BaseModel, frozen=True):
    amount: float


class Car(BaseModel, frozen=True):
    name: str
    fuel: Fuel

    def add_fuel(self, fuel: Fuel) -> "Car":
        return Car(name=self.name, fuel=Fuel(amount=self.fuel.amount + fuel.amount))

    def bad_add_fuel(self, fuel: Fuel) -> None:
        self.fuel.amount += fuel.amount


fuel: Final = Fuel(amount=100.0)
toyota_car: Final = Car(name="Toyota", fuel=fuel)
tesla_car: Final = Car(name="Tesla", fuel=fuel)
print(toyota_car.fuel.amount)
print(tesla_car.fuel.amount)
new_fuel: Final = Fuel(amount=50.0)
toyota_added_fuel_car: Final = toyota_car.add_fuel(new_fuel)
print(toyota_added_fuel_car.fuel.amount)
print(tesla_car.fuel.amount)
# toyota_car.bad_add_fuel(new_fuel)
# tesla_car.bad_add_fuel(new_fuel)
toyota_car.fuel.amount += 50.0
print(toyota_added_fuel_car.fuel.amount)
print(tesla_car.fuel.amount)
