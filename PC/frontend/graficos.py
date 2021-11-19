import json
import pickle

from PyQt5.QtWidgets import (
    QHBoxLayout, QFrame, QLabel
)

from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import cv2
from frontend.crear_layout import crear_layout


class Graficos(QFrame):
    def __init__(self):
        super().__init__()

        with open('parametros.json', 'r') as archivo:
            diccionario = json.load(archivo)
            self.obtener_parametros(diccionario)

        self.main_vbox = QHBoxLayout()
        self.setLayout(self.main_vbox)

    def obtener_parametros(self, diccionario):
        self.__dict__.update(diccionario['frontend']['graficos'])

    def init_gui(self, byte_image):
        image = pickle.loads(byte_image)
        
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.axes.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        crear_layout(self.main_vbox, self.canvas)

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(211)
        print(self.axes)
        super(MplCanvas, self).__init__(fig)