from PyQt5.QtWidgets import QWidget
from frontend.graficos_ui import Ui_graficos


class Graficos(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.graficos = Ui_graficos()
        self.graficos.setupUi(parent)
