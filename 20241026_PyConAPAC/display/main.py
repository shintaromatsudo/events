# Waveshare 0.96inch OLED Module via SPI (SSD1315)
# Available in White, Blue or Yellow & Blue
# Tony Goodhew 2 June 2023 - for thepihut.com

# Connect Red to 3.3V and Black to GND
from machine import Pin, SPI
import ssd1306
import time

# Uses SPI port 0
spi_port = 0
MOSI = 19     # blue   3
CLK = 18      # yellow 4
CS = 22       # orange 5
DC = 21       # green  6
RST = 15      # white  7 #NB MISO not used

WIDTH = 128
HEIGHT = 64

spi = SPI(
    spi_port,
    baudrate=40000000,
    mosi=Pin(MOSI),
    sck=Pin(CLK))
print(spi) # Not essential - comment out

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

# oled.fill(0)
#
# oled.text("Hello Misa!!", 5, 6, 1)
# oled.text('Sara', 5, 16, 1)
# oled.text('Reiri', 5, 26, 1)
# oled.text('WS 0.96" OLED', 5, 46, 1)
# oled.text("SSD1315 SPI", 5, 56, 1)
#
# oled.show()
