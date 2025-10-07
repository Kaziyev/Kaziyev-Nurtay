import serial, time

PORT = "COM8"      # укажи свой порт
BAUD = 115200
TIMEOUT = 0.3

ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)

def send_hex(frame):
    """Отправка HEX-кадра"""
    print("TX:", frame)
    ser.write(bytes.fromhex(frame))
    ser.flush()
    time.sleep(0.05)

# === 1. Меняем ID с 1 на 2 (только один мотор должен быть подключен!) ===
# Формат: AA 55 53 <NEW_ID> 00 00 00 00 00 CS
# Для ID=2 это:
set_id2 = "AA 55 53 03 00 00 00 00 00 A5"

print("Устанавливаем ID=2...")
for _ in range(5):
    send_hex(set_id2)

time.sleep(0.5)  # пауза, чтобы мотор сохранил новый ID

# === 2. Переводим мотор с ID=2 в режим velocity loop ===
send_hex("03 A0 00 00 00 00 00 00 00 CF")
 
# === 3. Запускаем мотор ID=2 на +100 rpm ===
send_hex("03 64 00 64 00 00 00 00 00 1E")
print("Мотор (ID=2) крутится 2 секунды...")
time.sleep(2)

# === 4. Останавливаем мотор ID=2 ===
send_hex("03 64 00 00 00 00 00 00 00 01")
print("Мотор остановлен.")

ser.close()
