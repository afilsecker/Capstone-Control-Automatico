from PyQt5.QtWidgets import QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random

from frontend.pyqtdesigner.interfaz_ui import Ui_interfaz


class Interfaz(QMainWindow):
    def __init__(self):
        super(Interfaz, self).__init__()
        self.ui = Ui_interfaz()
        self.ui.setupUi(self)
        self.set_grafs()

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
            self.vals[graf[0].objectName()[15:]] = graf[1]
            graf[0].addWidget(self.grafs[graf[0].objectName()[15:]])


class Grafico(FigureCanvas):
    def __init__(self):
        self.figure = Figure()
        FigureCanvas.__init__(self, self.figure)
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)

    def plot_random(self):
        n_data = 50
        self.xdata = list(range(n_data))
        self.ydata = [random.randint(0, 10) for _ in range(n_data)]
        self.ax.cla()
        self.ax.plot(self.xdata, self.ydata, 'r')

