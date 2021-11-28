import json
from serial import Serial
from collections import deque
from multiprocessing.connection import Connection
from multiprocessing import Pipe, Lock, Process
from threading import Thread
from time import sleep, time
import numpy as np


class Motores:
    def __init__(self, motores_pipe: Connection, lock):
        self.lock = lock
        self.lock_serial = Lock()
        self.motores_pipe = motores_pipe
        with open('parametros.json', 'r') as f:
            diccionario = json.load(f)
            self.__dict__.update(diccionario['motores'])

        self.generar_diccionario_acciones()
        Thread(target=self.handle_capstone, name='handle_capstone').start()
        self.start_serial()

    def generar_diccionario_acciones(self):
        self.action_dict = {
            "send": self.send,
            'reset': self.reset
        }

    def handle_capstone(self):
        while True:
            recibido = self.motores_pipe.recv()
            if isinstance(recibido, str):
                print(f"recibido: {recibido}")

            elif isinstance(recibido, list):
                if recibido[1] is not None:
                    self.action_dict[recibido[0]](**recibido[1])

                else:
                    self.action_dict[recibido[0]]()

    def start_serial(self):
        self.serial = Serial(self.ruta, self.baudrate, timeout=self.timeout)
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()
        self.closed = False
        Thread(target=self.listen, daemon=False, name="listen serial").start()

    def reset(self):
        self.closed = True
        self.serial.close()
        self.server_buffer = deque()
        self.start_serial()

    def listen(self):
        while not self.closed:
            try:
                if self.serial.in_waiting > 0:
                    line = self.serial.readline().decode(self.encoding).rstrip()
                    print(line)
            except OSError:
                pass

    def send_capstone(self, envio):
        with self.lock:
            self.motores_pipe.send(envio)

    def send(self, msg: str):
        self.start_time = time()
        self.serial.write((msg + '\n').encode(self.encoding))
        print('1msg = {:<6}| send_time = {:<6.2f} ms'.format(
            msg, (time() - self.start_time) * 1000))


def motores_process(motores_pipe, lock_send):
    Motores(motores_pipe, lock_send)


if __name__ == '__main__':
    conn1, conn2 = Pipe()
    lock = Lock()
    Process(target=motores_process, daemon=True, args=(conn1, lock),
            name="proceso motores").start()
    prev_time = time()
    sleep(1)
    vel_a = - 700
    vel_b = 0
    sleep_time = 1000
    mag = 100
    dir_a = mag
    dir_b = mag
    while True:
        if vel_a == 0:
            vel_r_a = 0
        else:
            vel_r_a = vel_a + 100 * np.sign(vel_a)
        if vel_b == 0:
            vel_r_b = 0
        else:
            vel_r_b = vel_b + 100 * np.sign(vel_b)
        envio_1 = ['send', {'msg': f'A{vel_r_a}'}]
        envio_2 = ['send', {'msg': f'B{vel_r_b}'}]
        conn2.send(envio_1)
        sleep(sleep_time / 1000 / 2)
        conn2.send(envio_2)
        sleep(sleep_time / 1000 / 2)
        # print(f'A{vel_r_a}, B{vel_r_b}, interval = {(time() - prev_time) * 1000:.1f}')
        prev_time = time()
        vel_a = vel_a + dir_a
        vel_b = vel_b + dir_b
        if vel_a > 700:
            vel_a = 700
            dir_a = - mag
        if vel_a < - 700:
            vel_a = - 700
            dir_a = mag
        if vel_b > 700:
            vel_b = 700
            dir_b = - mag
        if vel_b < - 700:
            vel_b = - 700
            dir_b = mag
