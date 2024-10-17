from spo2 import Spo2
from display import Display

s = Spo2()
d = Display()
while True:
    red, ir = s.get_data()
    spo2 = s.get_spo2(red, ir)
    print('SpO2:', spo2, 'Red:', red, 'IR:', ir)
    d.show('SpO2; %d Red: %d IR: %d' % (spo2, red, ir))
