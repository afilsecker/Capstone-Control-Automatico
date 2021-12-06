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
            'set_vels': self.set_vels,
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
        self.serial = Serial(port=self.ruta, baudrate=115200)
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()
        self.closed = False
        Thread(target=self.listen, daemon=False, name="listen serial")

    def reset(self):
        self.closed = True
        self.serial.close()
        self.server_buffer = deque()
        self.start_serial()

    def listen(self):
        while not self.closed:
            if self.serial.in_waiting > 0:
                line = self.serial.readline().decode('UTF-8')
                print(line[:-1])

    def send_capstone(self, envio):
        with self.lock:
            self.motores_pipe.send(envio)

    def set_vels(self, vel_A: int, vel_B: int):
        self.start_time = time()
        initial_bit = pow(2, 7)
        if vel_A >= 0:
            initial_bit += pow(2, 0)
        if vel_B >= 0:
            initial_bit += pow(2, 1)
        initial_bit = int.to_bytes(initial_bit, 1, 'big')
        self.serial.write(initial_bit)
        vel_A_bit = int.to_bytes(abs(vel_A), 1, 'big')
        self.serial.write(vel_A_bit)
        vel_B_bit = int.to_bytes(abs(vel_B), 1, 'big')
        self.serial.write(vel_B_bit)
        print('send_time = {:<6.2f} ms'.format(
            (time() - self.start_time) * 1000))


def motores_process(motores_pipe, lock_send):
    Motores(motores_pipe, lock_send)


if __name__ == '__main__':
    conn1, conn2 = Pipe()
    lock = Lock()
    Process(target=motores_process, daemon=False, args=(conn1, lock),
            name="proceso motores").start()
    vel_A = 0
    vel_B = -255
    sleep(2)
    while True:
        conn2.send(['set_vels', {'vel_A': vel_A, 'vel_B': vel_B}])
        vel_A += 1
        if vel_A > 255:
            vel_A = -255
        vel_B += 1
        if vel_B > 255:
            vel_B = -255
        sleep(0.1)
