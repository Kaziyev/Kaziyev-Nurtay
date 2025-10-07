#define UNICODE
#define _UNICODE
#include <windows.h>
#include <iostream>
#include <conio.h>   // для _kbhit и _getch
#include <string>

using namespace std;

HANDLE hSerial;

// отправка hex-строки
void send_hex(const string& frame) {
    // убираем пробелы
    string cleaned;
    for (char c : frame) {
        if (c != ' ') cleaned.push_back(c);
    }

    size_t len = cleaned.size() / 2;
    char* buffer = new char[len];
    for (size_t i = 0; i < len; i++) {
        string byteString = cleaned.substr(i * 2, 2);
        buffer[i] = (char) strtol(byteString.c_str(), nullptr, 16);
    }

    DWORD bytesWritten;
    WriteFile(hSerial, buffer, len, &bytesWritten, nullptr);
    FlushFileBuffers(hSerial);

    cout << "TX: " << frame << endl;

    delete[] buffer;
    Sleep(50); // пауза как в Python
}

int main() {
    // открываем порт COM8
    hSerial = CreateFile(
        L"COM8",
        GENERIC_READ | GENERIC_WRITE,
        0,
        nullptr,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        nullptr
    );

    if (hSerial == INVALID_HANDLE_VALUE) {
        cerr << "Ошибка открытия COM8" << endl;
        return 1;
    }

    // задаём параметры порта
    DCB dcbSerialParams = {0};
    dcbSerialParams.DCBlength = sizeof(dcbSerialParams);

    if (!GetCommState(hSerial, &dcbSerialParams)) {
        cerr << "Ошибка GetCommState" << endl;
        return 1;
    }

    dcbSerialParams.BaudRate = CBR_115200;
    dcbSerialParams.ByteSize = 8;
    dcbSerialParams.StopBits = ONESTOPBIT;
    dcbSerialParams.Parity   = NOPARITY;

    if (!SetCommState(hSerial, &dcbSerialParams)) {
        cerr << "Ошибка SetCommState" << endl;
        return 1;
    }

    cout << "Управление: W=вперёд, S=назад, Q=стоп, ESC=выход\n";

    // Переводим моторы в velocity loop
    send_hex("01 A0 00 00 00 00 00 00 00 9E");
    send_hex("02 A0 00 00 00 00 00 00 00 6B");
    send_hex("03 A0 00 00 00 00 00 00 00 CF");
    send_hex("04 A0 00 00 00 00 00 00 00 98");

    while (true) {
        if (_kbhit()) {
            char key = tolower(_getch());

            if (key == 'w') {
                send_hex("01 64 00 64 00 00 00 00 00 4F");
                send_hex("02 64 FF 9C 00 00 00 00 00 6F");
                send_hex("03 64 00 64 00 00 00 00 00 1E");
                send_hex("04 64 FF 9C 00 00 00 00 00 9C");
                cout << ">>> Вперёд\n";
            } else if (key == 's') {
                send_hex("01 64 FF 9C 00 00 00 00 00 9A");
                send_hex("02 64 00 64 00 00 00 00 00 BA");
                send_hex("03 64 FF 9C 00 00 00 00 00 CB");
                send_hex("04 64 00 64 00 00 00 00 00 49");
                cout << "<<< Назад\n";
            } else if (key == 'q') {
                send_hex("01 64 00 00 00 00 00 00 00 50");
                send_hex("02 64 00 00 00 00 00 00 00 A5");
                send_hex("03 64 00 00 00 00 00 00 00 01");
                send_hex("04 64 00 00 00 00 00 00 00 56");
                cout << "=== Стоп ===\n";
            } else if (key == 27) { // ESC
                cout << "Выход...\n";
                break;
            }
        }
    }

    CloseHandle(hSerial);
    return 0;
}
