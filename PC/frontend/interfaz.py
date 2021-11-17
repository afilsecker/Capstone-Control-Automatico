import json

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout
)

from frontend.crear_layout import crear_layout
from frontend.graficos import Graficos
from frontend.opciones import Opciones

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

        self.init_gui()
        self.show()

    def obtener_parametros(self, diccionario):
        self.__dict__.update(diccionario["frontend"]["interfaz"])

    def init_gui(self):
        self.setGeometry(*self.posicion, *self.tamano)
        self.setFixedSize(*self.tamano)
        self.setWindowTitle(self.titulo)
        self.setStyleSheet(self.estilo)
        self.graficos.init_gui()
        self.opciones.init_gui()
        crear_layout(self.main_hbox, self.graficos, self.opciones)
