import serial, time, msvcrt

PORT = "COM8"
BAUD = 115200
TIMEOUT = 0.3

ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)

def send_hex(frame):
    print("TX:", frame)
    ser.write(bytes.fromhex(frame))
    ser.flush()
    time.sleep(0.05)

# Переводим моторы в velocity loop
send_hex("01 A0 00 00 00 00 00 00 00 9E")
send_hex("02 A0 00 00 00 00 00 00 00 6B")
send_hex("03 A0 00 00 00 00 00 00 00 CF")
send_hex("04 A0 00 00 00 00 00 00 00 98")

print("Управление: W=вперёд, S=назад, Q=стоп, ESC=выход")

try:
    while True:
        if msvcrt.kbhit():                 # ждём нажатие
            key = msvcrt.getch().decode().lower()

            if key == "w":
                # вперёд (+100 rpm)
                send_hex("01 64 00 64 00 00 00 00 00 4F")
                send_hex("02 64 FF 9C 00 00 00 00 00 6F")
                send_hex("03 64 00 64 00 00 00 00 00 1E")
                send_hex("04 64 FF 9C 00 00 00 00 00 9C")
                print(">>> Вперёд")

            elif key == "s":
                # назад (-100 rpm)
                send_hex("01 64 FF 9C 00 00 00 00 00 9A")
                send_hex("02 64 00 64 00 00 00 00 00 BA")
                send_hex("03 64 FF 9C 00 00 00 00 00 CB")
                send_hex("04 64 00 64 00 00 00 00 00 49")
                print("<<< Назад")

            elif key == "q":
                # стоп
                send_hex("01 64 00 00 00 00 00 00 00 50")
                send_hex("02 64 00 00 00 00 00 00 00 A5")
                send_hex("03 64 00 00 00 00 00 00 00 01")
                send_hex("04 64 00 00 00 00 00 00 00 56")
                print("=== Стоп ===")

            elif key == chr(27):   # ESC
                print("Выход...")
                break

finally:
    ser.close()
