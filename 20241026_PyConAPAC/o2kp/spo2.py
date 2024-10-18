from machine import SoftI2C, Pin, I2C
from time import sleep

from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM


class Spo2:
    def __init__(self):
        # I2C software instance
        i2c = SoftI2C(
                  sda=Pin(14),
                  scl=Pin(15),
                  freq=400000)

        self.sensor = MAX30102(i2c=i2c)

        # Scan I2C bus to ensure that the sensor is connected
        if self.sensor.i2c_address not in i2c.scan():
            print("Sensor not found.")
            return
        elif not (self.sensor.check_part_id()):
            # Check that the targeted sensor is compatible
            print("I2C device ID not corresponding to MAX30102 or MAX30105.")
            return
        else:
            print("Sensor connected and recognized.")

        # It's possible to set up the sensor at once with the setup_sensor() method.
        # If no parameters are supplied, the default config is loaded:
        # Led mode: 2 (RED + IR)
        # ADC range: 16384
        # Sample rate: 400 Hz
        # Led power: maximum (50.0mA - Presence detection of ~12 inch)
        # Averaged samples: 8
        # pulse width: 411
        print("Setting up sensor with default configuration.", '\n')
        self.sensor.setup_sensor()

        # It is also possible to tune the configuration parameters one by one.
        # Set the sample rate to 400: 400 samples/s are collected by the sensor
        self.sensor.set_sample_rate(400)
        # Set the number of samples to be averaged per each reading
        self.sensor.set_fifo_average(8)
        # Set LED brightness to a medium value
        self.sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
        
        self.ir_list = []
        self.red_list = []

        sleep(1)


    def get_data(self):
        self.sensor.check()
        
        ir = 0
        red = 0

        if self.sensor.available():
            ir = self.sensor.pop_ir_from_storage()
            red = self.sensor.pop_red_from_storage()
            self.ir_list.append(ir)
            self.red_list.append(red)
            if len(self.ir_list) > 10:
                del self.ir_list[0]
            if len(self.red_list) > 10:
                del self.red_list[0]

        return ir, red

    def get_spo2(self, ir, red):
        return round(red / ir * 100, 3)


if __name__ == "__main__":
    s = Spo2()
    while True:
        ir, red = s.get_data()
        if ir is None or red is None:
            continue
        spo2 = s.get_spo2(ir, red)
        print('SpO2:', spo2, 'IR:', ir, 'Red:', red)
        sleep(1)
        