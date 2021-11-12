"""Contien a la clase Putsy"""

from camera import Camera
from servo import ServoControl

import parametros as par


class Putsy:
    """This class controls the system"""

    def __init__(self):
        self.camera = Camera()
        self.servo_alpha = ServoControl(par.SERVO_ALPHA_PIN)
        self.servo_beta = ServoControl(par.SERVO_BETA_PIN)
        self.controler()

    def controler(self):
        kp = 0.005
        try:
            while True:
                val_x, val_y, = self.camera.find_values()
                if (val_x is not None) and (val_y is not None):
                    error_x = par.RESOLUTION[0] / 2 - val_x
                    error_y = - (par.RESOLUTION[1] / 2 - val_y)
                    print(int(error_x), int(error_y))
                    alpha_angle = kp * error_y
                    beta_angle = kp * error_x
                    self.servo_alpha.turn(alpha_angle)
                    self.servo_beta.turn(beta_angle)

        except KeyboardInterrupt:
            print("\nQuiting")
            self.camera.close()
            self.servo_alpha.close()
            self.servo_beta.close()
