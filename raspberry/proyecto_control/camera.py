import time
import numpy as np
from matplotlib import pyplot as plt
from picamera import PiCamera

import parametros as par


class Camera:
    def __init__(self):
        self.width = par.RESOLUTION[0]
        self.height = par.RESOLUTION[1]
        print("inicializando camara")
        self.pi_camera = PiCamera()
        time.sleep(1)
        print("camara inicializada")
        # self.pi_camera.preview_fullscreen=False
        # self.pi_camera.preview_window=(620, 320, 640, 480)
        self.pi_camera.resolution = (self.width, self.height)
        self.pi_camera.framerate = par.FRAMERATE
        self.output = np.empty((self.height, self.width, 3), dtype=np.uint8)
        self.r_chanell = self.output[:, :, 0]
        self.punto_rojo_x = int()
        self.punto_rojo_y = int()

    def capture(self):
        self.pi_camera.capture(self.output, 'rgb', use_video_port=True)

    def find_punto_rojo(self):
        self.yp, self.xp = (self.r_chanell > par.UMBRAL_R).nonzero()
        if self.xp.any() and self.yp.any():
            self.punto_rojo_x = np.mean(self.xp)
            self.punto_rojo_y = np.mean(self.yp)

        else:
            self.punto_rojo_x = None
            self.punto_rojo_y = None

    def diez_puntos_rojos(self):
        suma_tiempo_captura = 0
        suma_tiempo_procesado = 0
        for _ in range(10):
            start_capture_time = time.time()
            self.capture()
            start_proces_time = time.time()
            self.find_punto_rojo()
            suma_tiempo_captura += start_proces_time - start_capture_time
            suma_tiempo_procesado += time.time() - start_proces_time

        return suma_tiempo_captura / 10, suma_tiempo_procesado / 10

    def show_image(self):
        plt.imshow(self.r_chanell, cmap='gray')
        plt.scatter(self.xp, self.yp, c='red')
        plt.scatter(self.punto_rojo_x, self.punto_rojo_y, c='blue')
        plt.show()

    def close(self):
        self.pi_camera.close()

    def find_values(self):
        self.capture()
        self.find_punto_rojo()
        return self.punto_rojo_x, self.punto_rojo_y


def hola():
    camera = Camera()
    print("instanciando camara")
    time.sleep(2)
    print("iniciando")
    start_time = time.time()
    med_tiempo_captura, med_tiempo_procesado = camera.diez_puntos_rojos()
    print(f"Se procesaron 10 imágenes en {(time.time() - start_time) * 1000:.2f} ms")
    print(f"Tiempo medio de captura = {med_tiempo_captura * 1000:.2f} ms")
    print(f"Tiempo medio de procesado = {med_tiempo_procesado * 1000:.2f} ms")
    camera.show_image()
    camera.pi_camera.close()


if __name__ == "__main__":
    hola()
