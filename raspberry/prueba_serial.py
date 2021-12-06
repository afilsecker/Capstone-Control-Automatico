import serial
from threading import Thread
import time


arduino_serial = serial.Serial(port="/dev/ttyS0", baudrate=115200, timeout=0.1)
arduino_serial.reset_input_buffer()
arduino_serial.reset_output_buffer()

vel = 1
start_time = 0


def send(vel, s):
    s = time.time()
    b = int.to_bytes(vel, 1, byteorder='big')
    arduino_serial.write(b)


def recieve(start_time):
    while True:
        if arduino_serial.in_waiting > 0:
            c = arduino_serial.read()
            print(f"looped {c} on {time.time() - start_time}")


Thread(target=recieve, daemon=True, args=(start_time,)).start()

while True:
    send(vel, start_time)
    vel += 1
    if vel > 255:
        vel = 1
    time.sleep(0.01)
