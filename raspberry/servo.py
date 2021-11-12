import pigpio
import time

import parametros as par


class ServoControl:
    def __init__(self, pin):  # position 0 for alpha, 1 for beta
        self.pin = pin
        if (self.pin == par.SERVO_ALPHA_PIN):
            self.angle_m90 = par.ALPHA_M90_DEGREES
            self.angle_0 = par.ALPHA_0_DEGREES
            self.angle_90 = par.ALPHA_90_DEGREES
            self.max_angle = par.ALPHA_MAX_ANGLE
            self.min_angle = par.ALPHA_MIN_ANGLE
            self.name = "ALPHA"

        elif (self.pin == par.SERVO_BETA_PIN):
            self.angle_m90 = par.BETA_M90_DEGREES
            self.angle_0 = par.BETA_0_DEGREES
            self.angle_90 = par.BETA_90_DEGREES
            self.max_angle = par.BETA_MAX_ANGLE
            self.min_angle = par.BETA_MIN_ANGLE
            self.name = "BETA"

        self.frecuency = par.SERVO_FRECUENCY
        self.pwm = pigpio.pi()
        self.pwm.set_mode(self.pin, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency(self.pin, self.frecuency)
        self.current_angle = 0
        self.neutral()

    def start(self):
        self.calibrate()

    def neutral(self):
        self.set_angle(0)

    def close(self):
        self.pwm.set_PWM_dutycycle(self.pin, 0)
        self.pwm.set_PWM_frequency(self.pin, 0)

    def set_pwm(self, pulse_width):
        if pulse_width > 1800 or pulse_width < 1300:
            pass

        else:
            self.pwm.set_servo_pulsewidth(self.pin, pulse_width)
            self.pulsewidth = pulse_width

    def set_angle(self, angle):
        if angle > self.max_angle or angle < self.min_angle:
            print(f"Error en {self.name}")
            if angle > self.max_angle:
                print(f"Atempted {angle} when max angle is {self.max_angle}")
            elif angle < self.min_angle:
                print(f"Attempted {angle} when min angle is {self.min_angle}")
            print(f"Returning {self.name} to natural position")
            self.set_angle(0)
        else:
            if (angle >= 0):
                pulse_width = (self.angle_90 - self.angle_0) * (angle - 0)\
                    / (90 - 0) + self.angle_0
            elif (angle < 0):
                pulse_width = (self.angle_0 - self.angle_m90) * (angle + 90) \
                    / (0 + 90) + self.angle_m90

            self.pwm.set_servo_pulsewidth(self.pin, pulse_width)
            self.pulsewidth = pulse_width
            self.current_angle = angle

    def turn(self, angle):
        self.set_angle(self.current_angle + angle)

    def calibrate(self):
        while True:
            angle = float(input("type angle: "))
            self.set_angle(angle)

    def iter(self):
        for _ in range(2):
            print("0 degrees")
            self.pwm.set_servo_pulsewidth(self.pin, 1200)
            time.sleep(1)
            print("180 degrees")
            self.pwm.set_servo_pulsewidth(self.pin, 1450)
            time.sleep(1)


def prueba_alpha():
    servo_alpha = ServoControl(par.SERVO_ALPHA_PIN)
    servo_alpha.close()


def prueba_beta():
    servo_beta = ServoControl(par.SERVO_BETA_PIN)
    servo_beta.close()


def prueba_doble():
    servo_alpha = ServoControl(par.SERVO_ALPHA_PIN)
    servo_beta = ServoControl(par.SERVO_BETA_PIN)
    """
    movimientos_1 = (
        (par.ALPHA_MAX_ANGLE, par.BETA_MAX_ANGLE),
        (par.ALPHA_MAX_ANGLE, par.BETA_MIN_ANGLE),
        (par.ALPHA_MIN_ANGLE, par.BETA_MIN_ANGLE),
        (par.ALPHA_MIN_ANGLE, par.BETA_MAX_ANGLE)
    )
    """

    movimientos_2 = (
        (10, 10),
        (10, -10),
        (-10, 10),
        (-10, -10)
    )

    for _ in range(10):
        for movimiento in movimientos_2:
            servo_alpha.set_angle(movimiento[0])
            servo_beta.set_angle(movimiento[1])
            time.sleep(0.5)


def prueba_oscilacion_beta():
    servo_beta = ServoControl(par.SERVO_BETA_PIN)
    servo_beta.neutral()
    time.sleep(3)
    beta_range = (-6.4, 6.3)
    servo_beta.set_angle(beta_range[0])
    time.sleep(1)
    servo_beta.set_angle(beta_range[1])
    time.sleep(1)
    for i in range(10):
        servo_beta.set_angle(beta_range[i % 2])
        time.sleep(1 / 6 / 2)

    servo_beta.close()


def prueba_oscilacion_alpha():
    servo_alpha = ServoControl(par.SERVO_ALPHA_PIN)
    servo_alpha.neutral()
    alpha_range = (-3, 3)
    time.sleep(1)
    for i in range(100):
        servo_alpha.set_angle(alpha_range[i % 2])
        time.sleep(1 / 6 / 2)

    servo_alpha.neutral()
    time.sleep(1)
    servo_alpha.close()


def prueba_calibracion():
    servo_alpha = ServoControl(par.SERVO_ALPHA_PIN)
    servo_beta = ServoControl(par.SERVO_BETA_PIN)
    try:
        while True:
            angulo_alpha, angulo_beta = input("angulos: ").split(" ")
            servo_alpha.set_angle(float(angulo_alpha))
            servo_beta.set_angle(float(angulo_beta))

    except KeyboardInterrupt:
        servo_alpha.close()
        servo_beta.close()


def prueba_resolucion():
    servo_alpha = ServoControl(par.SERVO_ALPHA_PIN)
    servo_beta = ServoControl(par.SERVO_BETA_PIN)
    try:
        while True:
            servo_beta.turn(-0.01)
            print(f"{servo_beta.current_angle:.2f}, {servo_beta.pulsewidth:.2f}")
            time.sleep(0.05)

    except KeyboardInterrupt:
        servo_alpha.close()
        servo_beta.close()


def prueba_resolucion_2():
    servo_alpha = ServoControl(par.SERVO_ALPHA_PIN)
    servo_beta = ServoControl(par.SERVO_BETA_PIN)
    pulse_width = 1300
    try:
        while True:
            servo_alpha.set_pwm(pulse_width)
            input()
            pulse_width += 5
            print(pulse_width)
        

    except KeyboardInterrupt:
        servo_alpha.close()
        servo_beta.close()


if __name__ == "__main__":
    prueba_resolucion_2()
