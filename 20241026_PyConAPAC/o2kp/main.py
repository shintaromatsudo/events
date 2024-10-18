from time import sleep

from spo2 import Spo2
from display import Display


s = Spo2()
d = Display()

spo2_0 = "SpO2:-%"
spo2_1 = "SpO2:-%"
spo2_2 = "SpO2:-%"
spo2_3 = "SpO2:-%"
spo2_4 = "SpO2:-%"

while True:
    ir, red = s.get_data()
    if ir < 1000 or red < 1000:
        spo2 = "-"
    else:
        spo2 = s.get_spo2(ir, red)
    print("SpO2:", spo2, "IR:", ir, "Red:", red)
    
    spo2_4 = spo2_3
    spo2_3 = spo2_2
    spo2_2 = spo2_1
    spo2_1 = spo2_0
    spo2_0 = f"SpO2:{spo2}%"
    
    d.show(
        spo2_0,
        spo2_1,
        spo2_2,
        spo2_3,
        spo2_4,
    )
    
    sleep(1)