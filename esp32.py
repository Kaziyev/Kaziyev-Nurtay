import serial
import time
import json

PORT = "COM8"       # порт ESP32
BAUD = 115200
TIMEOUT = 0.5

ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)

def send_json(cmd: dict):
    """Отправка JSON-команды на ESP32"""
    frame = json.dumps(cmd) + "\n"   # переводим словарь в JSON + \n
    print("TX:", frame.strip())
    ser.write(frame.encode("utf-8"))
    ser.flush()
    time.sleep(0.1)

    send_json({"T":10010,"id":1,"cmd":50,"act":3})