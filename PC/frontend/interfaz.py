from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import random
import numpy as np

from frontend.pyqtdesigner.interfaz_ui import Ui_interfaz


class Interfaz(QMainWindow):

    senal_abrir_serial = pyqtSignal()
    senal_prueba_procesamiento = pyqtSignal()
    senal_comenzar_actualizacion = pyqtSignal()

    def __init__(self):
        super(Interfaz, self).__init__()
        self.ui = Ui_interfaz()
        self.ui.setupUi(self)
        self.fps_list = list()
        self.set_grafs()
        self.set_perturbador()
        self.set_botones()

    def set_grafs(self):
        grafs_list = [
            [self.ui.verticalLayout_e_abs, self.ui.val_e_abs],
            [self.ui.verticalLayout_e_a, self.ui.val_e_a],
            [self.ui.verticalLayout_e_b, self.ui.val_e_b],
            [self.ui.verticalLayout_u_a, self.ui.val_u_a],
            [self.ui.verticalLayout_u_b, self.ui.val_u_b],
            [self.ui.verticalLayout_p_a, self.ui.val_p_a],
            [self.ui.verticalLayout_p_b, self.ui.val_p_b],
            [self.ui.verticalLayout_d_a, self.ui.val_d_a],
            [self.ui.verticalLayout_d_b, self.ui.val_d_b],
            [self.ui.verticalLayout_i_a, self.ui.val_i_a],
            [self.ui.verticalLayout_i_b, self.ui.val_i_b]
        ]
        self.grafs = dict()
        self.vals = dict()
        for graf in grafs_list:
            self.grafs[graf[0].objectName()[15:]] = Grafico()
            graf[0].addWidget(self.grafs[graf[0].objectName()[15:]])

    def set_perturbador(self):
        self.ui.bttn_serial.clicked.connect(self.senal_abrir_serial.emit)

    def set_botones(self):
        self.ui.boton_prueba_procesamiento.clicked.connect(self.senal_prueba_procesamiento.emit)
        self.ui.boton_actualizar.clicked.connect(self.boton_actualizar_apretado)

    def boton_actualizar_apretado(self):
        if self.ui.boton_actualizar.text() == 'Comenzar Actualizacion':
            self.ui.boton_actualizar.setText('Reiniciar Graficos')
        self.senal_comenzar_actualizacion.emit()

    def inicializar(self, datos: dict):
        texto_resolucion = f'Resolucion Camara: {datos["resolucion"][0]}X{datos["resolucion"][1]}'
        self.ui.label_res.setText(texto_resolucion)
        self.show()

    def contar_fps(self, fps):
        self.fps_list.append(fps)
        if len(self.fps_list) > 10:
            self.fps_list.pop(0)
        return np.mean(np.array(self.fps_list))

    def actualizar_archivos(self, files):
        self.ui.combo_box_loads.clear()
        for file in files:
            self.ui.combo_box_loads.addItem(file[:-4])

    def actualizar_text_controlador(self, values):
        pass

    def actualizar_control(self, datos: dict):
        for key in datos.keys():
            if f'val_{key}' in self.ui.__dict__:
                if datos[key] is not None:
                    self.ui.__dict__[f'val_{key}'].setText(f'{datos[key]:.2f}')
                else:
                    self.ui.__dict__[f'val_{key}'].setText(' ')

        self.ui.label_fps.setText(f'FPS: {self.contar_fps(datos["fps"]):.2f}')


class Grafico(FigureCanvas):
    def __init__(self):
        self.figure = Figure()
        FigureCanvas.__init__(self, self.figure)
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.xdata = list()
        self.ydata = list()

    def plot_random(self):
        n_data = 50
        self.xdata = list(range(n_data))
        self.ydata = [random.randint(0, 10) for _ in range(n_data)]
        self.ax.cla()
        self.ax.plot(self.xdata, self.ydata, 'r')

