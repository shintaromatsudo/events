from machine import Pin, SPI
import ssd1306
import time

spi_port = 0
MOSI = 19     # blue   3
CLK = 18      # yellow 4
CS = 22       # orange 5
DC = 21       # green  6
RST = 20      # white  7 #NB MISO not used

WIDTH = 128
HEIGHT = 64

spi = SPI(
    spi_port,
    baudrate=40000000,
    mosi=Pin(MOSI),
    sck=Pin(CLK))

oled = ssd1306.SSD1306_SPI(WIDTH,HEIGHT,
    spi,
    dc=Pin(DC),
    res=Pin(RST),
    cs=Pin(CS),
    external_vcc=False
    )

# Clear the oled display in case it has junk on it.
oled.fill(0)

while True:
    for i in range(2):
        for x in range(80):
            oled.fill(i)
            oled.text("Hello PyCon APAC 2024", int(145 - x*4), 6, 1-i)

            oled.text('Yogyakarta, Indonesia', int(145 - x*4), 26, 1-i)
            oled.text(' 25th-27th Oct, 2024', int(145 - x*4), 46, 1-i)

            # Finally update the oled display so the text is displayed
            oled.show()
            time.sleep(0.1)
