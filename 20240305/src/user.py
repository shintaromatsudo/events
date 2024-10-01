from pydantic import BaseModel
from enum import Enum


class Language(Enum):
    FRENCH = "Bonjour"
    JAPANESE = "こんにちは"


class User(BaseModel):
    name: str
    language: Language


class LowCohesionGreeter(BaseModel):
    user: User

    def greet(self, greeting, name) -> str:
        return greeting + " from " + name


class TightCouplingGreeter(BaseModel):
    user: User

    def greet(self) -> str:
        return self.user.language.value + " from " + self.user.name


class LooseCouplingGreeter(BaseModel):
    greeting: str
    user_name: str

    def greet(self) -> str:
        return self.greeting + " from " + self.user_name


user = User(name="Shintaro", language=Language.JAPANESE)
t_greeter = Greeter(user=user)
print(t_greeter.greet())
l_greeter = LooseCouplingGreeter(greeting=user.language.value, user_name=user.name)
print(l_greeter.greet())
