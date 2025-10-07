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
send_hex("01 A0 00 00 00 00 00 00 00 02")
send_hex("02 A0 00 00 00 00 00 00 00 6B")

print("Управление: W=вперёд, S=назад, Q=стоп, ESC=выход")

try:
    while True:
        if msvcrt.kbhit():                 # ждём нажатие
            key = msvcrt.getch().decode().lower()

            if key == "w":
                # вперёд (+100 rpm)
                send_hex("02 64 00 64 00 00 00 00 00 BA")
                send_hex("01 64 FF 9C 00 00 00 00 00 9A")
                print(">>> Вперёд")
                
            elif key == "f":
                # вперёд (+320 rpm)
                send_hex("02 64 01 4A 00 00 00 00 00 22")
                send_hex("01 64 FE B6 00 00 00 00 00 DE")
                print(">>> Вперёд")

            elif key == "s":
                # назад (-100 rpm)
                send_hex("02 64 FF 9C 00 00 00 00 00 6F")
                send_hex("01 64 00 64 00 00 00 00 00 4F")
                print("<<< Назад")
                

            elif key == "q":
                # стоп
                send_hex("02 64 00 00 00 00 00 00 00 A5")
                send_hex("01 64 00 00 00 00 00 00 00 50")
                print("=== Стоп ===")

            elif key == chr(27):   # ESC
                print("Выход...")
                break

finally:
    ser.close()
