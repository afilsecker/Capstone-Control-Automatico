from matplotlib import pyplot as plt
import numpy as np

U_MAX = 255
U_MIN = 1
TOP = 65536
STEPS = 6400
F_CPU = 16000000

def calcular_count(u: int):
    if u == 0:
        return 0
    else:
        return int((F_CPU * TOP * (U_MAX - U_MIN)) / ((u - U_MIN) * 4 * STEPS * TOP - (u - U_MAX) * F_CPU))

us = [u for u in range(0, 256)]
counts = [calcular_count(u) for u in us]

for u in range(0, 256, 16):
    u_list = [u + i for i in range(16)]
    print("    {:>5}, {:>5}, {:>5}, {:>5}, {:>5}, {:>5}, {:>5}, {:>5}, {:>5}, {:>5}, {:>5}, {:>5}, {:>5}, {:>5}, {:>5}, {:>5},".format(*[counts[j] for j in u_list]))
