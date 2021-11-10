"""This is the main program"""

import sys

from PyQt5.QtWidgets import QApplication

from frontend.interfaz import Interfaz

from backend.client import Client

# Para poder debbuguear
def hook(type_error, traceback):
    print(type_error)
    print(traceback)


if __name__ == '__main__':
    Client()
