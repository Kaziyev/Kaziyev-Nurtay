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
set_id2 = "AA 55 53 01 00 00 00 00 00 CB"

print("Устанавливаем ID=2...")
for _ in range(5):
    send_hex(set_id2)

time.sleep(0.5)  # пауза, чтобы мотор сохранил новый ID

# === 2. Переводим мотор с ID=2 в режим velocity loop ===
send_hex("01 A0 00 00 00 00 00 00 00 9E")
 
# === 3. Запускаем мотор ID=2 на +100 rpm ===
send_hex("01 64 00 64 00 00 00 00 00 4F")
print("Мотор (ID=2) крутится 2 секунды...")
time.sleep(2)

# === 4. Останавливаем мотор ID=2 ===
send_hex("01 64 00 00 00 00 00 00 00 50")
print("Мотор остановлен.")

ser.close()