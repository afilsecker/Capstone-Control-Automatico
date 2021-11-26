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
    senal_actualizar_controlador = pyqtSignal(dict)
    senal_graficos_keys = pyqtSignal(list)

    def __init__(self):
        super(Interfaz, self).__init__()
        self.ui = Ui_interfaz()
        self.ui.setupUi(self)
        self.fps_list = list()
        self.keys_parametros = list()
        self.parametros = dict()
        for key in self.ui.__dict__:
            if key[:5] == 'edit_':
                if key[5:] != 'save':
                    self.keys_parametros.append(key[5:])
        self.set_text_edit()
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
        self.grafs_keys = list()
        for graf in grafs_list:
            self.grafs[graf[0].objectName()[15:]] = Grafico()
            self.grafs_keys.append(graf[0].objectName()[15:])
            graf[0].addWidget(self.grafs[graf[0].objectName()[15:]])

    def enviar_grafs_keys(self):
        self.senal_graficos_keys.emit(self.grafs_keys)

    def set_perturbador(self):
        self.ui.bttn_serial.clicked.connect(self.senal_abrir_serial.emit)

    def set_text_edit(self):
        for edit in [self.ui.__dict__[f'edit_{key}'] for key in self.keys_parametros]:
            edit.returnPressed.connect(self.boton_actualizar_controlador)

    def set_botones(self):
        self.ui.boton_prueba_procesamiento.clicked.connect(self.senal_prueba_procesamiento.emit)
        self.ui.boton_actualizar.clicked.connect(self.boton_actualizar_apretado)
        self.ui.bttn_actualizar_controlador.clicked.connect(self.boton_actualizar_controlador)

    def boton_actualizar_apretado(self):
        if self.ui.boton_actualizar.text() == 'Comenzar Actualizacion':
            self.ui.boton_actualizar.setText('Reiniciar Graficos')
        self.senal_comenzar_actualizacion.emit()

    def boton_actualizar_controlador(self):
        distinto = False
        for key in self.keys_parametros:
            edit = self.ui.__dict__[f'edit_{key}']
            if edit.text() != self.parametros[key]:
                distinto = True

        if distinto:
            for key in self.keys_parametros:
                self.parametros[key] = self.ui.__dict__[f'edit_{key}'].text()

            self.senal_actualizar_controlador.emit(self.parametros)

    def inicializar(self, datos: dict):
        texto_resolucion = f'Resolucion Camara: {datos["resolucion"][0]}X{datos["resolucion"][1]}'
        self.ui.label_res.setText(texto_resolucion)
        self.show()

    def contar_fps(self, fps):
        self.fps_list.append(fps)
        if len(self.fps_list) > 100:
            self.fps_list.pop(0)
        return np.mean(np.array(self.fps_list))

    def actualizar_archivos(self, files):
        self.ui.combo_box_loads.clear()
        for file in files:
            self.ui.combo_box_loads.addItem(file[:-4])

    def actualizar_text_controlador(self, values: dict):
        for key in values.keys():
            if f'edit_{key}' in self.ui.__dict__:
                self.parametros[key] = str(values[key])
                self.ui.__dict__[f'edit_{key}'].setText(str(values[key]))

    def actualizar_limites_graficos(self, limites: dict):
        for key in limites:
            self.grafs[key].set_ylimits(limites[key])

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

    def set_ylimits(self, limits):
        self.ylimits = limits
        self.ax.set_ylim(self.ylimits)

    def plot_random(self):
        n_data = 50
        self.xdata = list(range(n_data))
        self.ydata = [random.randint(0, 10) for _ in range(n_data)]
        self.ax.cla()
        self.ax.plot(self.xdata, self.ydata, 'r')
