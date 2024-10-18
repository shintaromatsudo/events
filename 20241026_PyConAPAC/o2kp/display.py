from machine import Pin, SPI
import ssd1306
import time

class Display:
    def __init__(self):
        # Uses SPI port 0
        spi_port = 0
        MOSI = 19     # blue   3
        CLK = 18      # yellow 4
        CS = 22       # orange 5
        DC = 21       # green  6
        RST = 20      # white  7

        WIDTH = 128
        HEIGHT = 64

        spi = SPI(
            spi_port,
            baudrate=40000000,
            mosi=Pin(MOSI),
            sck=Pin(CLK))

        self.oled = ssd1306.SSD1306_SPI(WIDTH,HEIGHT,
            spi,
            dc=Pin(DC),
            res=Pin(RST),
            cs=Pin(CS),
            external_vcc=False
            )

        self.oled.fill(0)

    def show(self, text_list):
        self.oled.fill(0)
        for i, t in enumerate(text_list):
            self.oled.text(t, 5, 6 + 10 * i, 1)
        self.oled.show()

    def show_demo(self):
        self.oled.fill(0)
        while True:
            for i in range(2):
                for x in range(80):
                    self.oled.fill(i)
                    self.oled.text("Hello PyCon APAC 2024", int(145 - x*4), 6, 1-i)

                    self.oled.text('Yogyakarta, Indonesia', int(145 - x*4), 26, 1-i)
                    self.oled.text(' 25th-27th Oct, 2024', int(145 - x*4), 46, 1-i)

                    # Finally update the oled display so the text is displayed
                    self.oled.show()
                    time.sleep(0.1)


if __name__ == "__main__":
    display = Display()
    display.show_demo()
