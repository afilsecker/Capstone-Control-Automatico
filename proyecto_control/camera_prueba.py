from picamera import PiCamera
from picamera.array import PiRGBAnalysis
import numpy as np
import time

import parametros as par


class CustomCamera(PiCamera):
    def __init__(self):
        print("Inicializando Cámara")
        super(CustomCamera, self).__init__()
        self.resolution = par.RESOLUTION
        self.framerate = par.FRAMERATE
        self.output = ImageProcessing(self)
        time.sleep(2)
        print("Cámara Inicializada")

    def start(self):
        self.start_recording(self.output, format='yuv')


class ImageProcessing(PiRGBAnalysis):
    def __init__(self, camera: PiCamera):
        super(ImageProcessing, self).__init__(camera)
        self.done = False
        self.yp: np.ndarray
        self.xp: np.ndarray
        self.val_y: float = 0
        self.val_x: float = 0
        self.image_height = camera.resolution[1]
        self.image_width = camera.resolution[0]

    def analyse(self, array: np.ndarray):
        r_chanell = array[:, :, 0]
        self.yp, self.xp = (r_chanell > par.UMBRAL_R).nonzero()
        if self.yp.any() and self.xp.any():
            self.val_y, self.val_x = np.mean(self.yp), np.mean(self.xp)

        self.done = True


if __name__ == "__main__":
    with CustomCamera() as camera:
        camera.start()
        try:
            iteracion = 0
            start_time = time.time()
            while True:
                while camera.output.done:
                    iteracion += 1
                    print(f"{iteracion} Punto encontrado ({camera.output.val_x:.2f},"
                          f"{camera.output.val_y:.2f})",
                          f"Tiempo medio = {(time.time() - start_time) / iteracion * 1000:.2f}")

                    camera.output.done = False

        except KeyboardInterrupt:
            camera.stop_recording()
            camera.close()
