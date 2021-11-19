import json

from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout
)

from frontend.crear_layout import crear_layout
from frontend.graficos import Graficos
from frontend.opciones import Opciones
import cv2
import numpy as np
import pickle

class Interfaz(QWidget):
    def __init__(self):
        super(Interfaz, self).__init__()
        with open('parametros.json', 'r') as archivo:
            diccionario = json.load(archivo)
            self.obtener_parametros(diccionario)

        self.graficos = Graficos()
        self.opciones = Opciones()

        self.main_hbox = QHBoxLayout()
        self.setLayout(self.main_hbox)

    def obtener_parametros(self, diccionario):
        self.__dict__.update(diccionario["frontend"]["interfaz"])

    def init_gui(self, byte_image):
        self.setGeometry(*self.posicion, *self.tamano)
        self.setFixedSize(*self.tamano)
        self.setWindowTitle(self.titulo)
        self.graficos.init_gui(byte_image)
        self.opciones.init_gui()
        crear_layout(self.main_hbox, self.graficos, self.opciones)
