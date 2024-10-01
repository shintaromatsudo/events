from pydantic import BaseModel


class LowCohesionColor(BaseModel):
    color: str

    def mix_color(self, color1, color2):
        print(f"Mixing {color1} and {color2}...")


class HighCohesionColor(BaseModel):
    color1: str
    color2: str

    def mix_color(self):
        print(f"Mixing {self.color1} and {self.color2}...")
