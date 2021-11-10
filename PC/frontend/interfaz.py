import json
import os

from PyQt5.QtWidgets import QWidget


class Interfaz(QWidget):

    def __init__(self):
        super(Interfaz, self).__init__()
        with open('parametros.json', 'r') as archivo:
            diccionario = json.load(archivo)
            self.par = diccionario['frontend']

        self.init_gui()

    def init_gui(self):
        self.setGeometry(*self.par["POSITION"], *self.par["SIZE"])
        self.setFixedSize(*self.par["SIZE"])
        self.setWindowTitle(self.par["WINDOW_TITLE"])
        self.setStyleSheet(self.par["STYLE"])
