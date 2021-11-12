import cv2
import json
import time
from threading import Thread, Event, Lock
from collections import deque
import numpy as np


class Camera:
    def __init__(self, src=0):
        with open('parametros.json', 'r') as archivo:
            diccionario = json.load(archivo)
            self.__dict__.update(diccionario["camera"])

        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, self.resolution[0])
        self.stream.set(4, self.resolution[1])
        self.stream.set(cv2.CAP_PROP_FPS, self.fps)
        self.stopped = False
        self.imagen_capturada = Event()
        self.capturar = Event()
        self.punto_encontrado = Event()
        self.frames = deque()
        self.frames_lock = Lock()
        self.capturar.set()
        self.start()

    def start(self):
        Thread(target=self.update, args=()).start()
        Thread(target=self.find_laser, args=()).start()
        Thread(target=self.time_counter, args=()).start()

    def update(self):
        while True:
            if self.stopped:
                return

            self.capturar.wait()
            self.capturar.clear()
            _, frame = self.stream.read()
            with self.frames_lock:
                self.frames.append(frame)
            self.imagen_capturada.set()

    def find_laser(self):
        while True:
            self.imagen_capturada.wait()
            self.imagen_capturada.clear()

            if len(self.frames) == 1:
                self.capturar.set()

            with self.frames_lock:
                frame = self.frames.popleft()
            red_chanell = frame[:, :, 0]
            red_points = (red_chanell > self.umbral).nonzero()
            if red_points[0].any() and red_points[1].any():
                self.red_point = [float, float]
                self.red_point[0] = np.mean(red_points[0])
                self.red_point[1] = np.mean(red_points[1])
                self.punto_encontrado.set()

            else:
                self.red_point = None

            self.capturar.set()

    def time_counter(self):
        tiempos = deque()
        while True:
            start_time = time.time()
            self.punto_encontrado.wait()
            self.punto_encontrado.clear()
            tiempo = time.time() - start_time
            tiempos.append(tiempo)
            if len(tiempos) >= 1000:
                tiempos.popleft()
            print(f"fps: {1 / np.mean(np.array(list(tiempos))):.2f}")

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
