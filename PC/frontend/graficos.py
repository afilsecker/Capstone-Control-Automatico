import json

from PyQt5.QtWidgets import (
    QHBoxLayout, QFrame, QLabel
)

from PyQt5.QtCore import Qt

from frontend.crear_layout import crear_layout


class Graficos(QFrame):
    def __init__(self):
        super().__init__()

        with open('parametros.json', 'r') as archivo:
            diccionario = json.load(archivo)
            self.obtener_parametros(diccionario)

        self.main_hbox = QHBoxLayout()
        self.setLayout(self.main_hbox)

    def obtener_parametros(self, diccionario):
        self.__dict__.update(diccionario['frontend']['graficos'])

    def init_gui(self):
        textos = [f'hola {i + 1}' for i in range(self.hola)]
        for contador in range(len(textos)):
            texto = QLabel(textos[contador], self)
            texto.setAlignment(Qt.AlignCenter)
            textos[contador] = texto

        crear_layout(self.main_hbox, *textos)

