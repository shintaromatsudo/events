from time import sleep

from spo2 import Spo2
from display import Display


s = Spo2()
d = Display()

spo2_str_list = [
    "SpO2:-%",
    "SpO2:-%",
    "SpO2:-%",
    "SpO2:-%",
    "SpO2:-%",
]

while True:
    ir, red = s.get_data()
    if ir < 1000 or red < 1000:
        spo2 = "-"
    else:
        spo2 = s.get_spo2(ir, red)
    print("SpO2:", spo2, "IR:", ir, "Red:", red)

    spo2_str_list.insert(0, f"SpO2:{spo2}%")

    spo2_str_list = spo2_str_list[:5]

    d.show(spo2_str_list)

    sleep(1)
