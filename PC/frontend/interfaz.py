from PyQt5.QtWidgets import QMainWindow

from frontend.interfaz_ui import Ui_interfaz
from frontend.graficos import Graficos


class Interfaz(QMainWindow):
    def __init__(self):
        super(Interfaz, self).__init__()
        self.interfaz = Ui_interfaz()
        self.interfaz.setupUi(self)
        self.graficos = Graficos(self)
