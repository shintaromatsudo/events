from machine import Pin, I2C
import time
from max30102 import MAX30102  # ライブラリを使用する

# I2Cの初期化
i2c = I2C(1, scl=Pin(9), sda=Pin(8), freq=400000)

# MAX30102センサーの初期化
max30102 = MAX30102(i2c=i2c)

# データの読み取り
while True:
    # 心拍数と酸素飽和度を読み取る
    heart_rate, spo2 = max30102.read()

    # データを表示
    print("Heart Rate: ", heart_rate, " SpO2: ", spo2)

    time.sleep(1)
