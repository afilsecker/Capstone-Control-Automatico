from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

from frontend.pyqtdesigner.inicio_ui import Ui_inicio


class Inicio(QWidget):

    senal_conectar_cliente = pyqtSignal()
    senal_iniciar_interfaz = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.inicio = Ui_inicio()
        self.inicio.setupUi(self)
        self.set_initial_values()
        self.show()

    def set_initial_values(self):
        self.inicio.boton_conectar.setDisabled(False)
        self.inicio.boton_conectar.clicked.connect(self.conectar_cliente)
        self.inicio.boton_continuar.hide()
        self.inicio.texto_conexion.setText("Presiona para conectar")

    def conectar_cliente(self):
        self.inicio.texto_conexion.setText("Intentando conectar")
        self.senal_conectar_cliente.emit()
        self.inicio.boton_conectar.setDisabled(True)

    def actualizar_intentos(self, intento: int, totales: int):
        self.inicio.texto_conexion.setText(f'Intento de conexion {intento}/{totales} fallido')

    def error_connection(self):
        self.inicio.texto_conexion.setText("No se pudo conectar con el servidor")
        self.inicio.boton_conectar.setDisabled(False)

    def succes_connection(self):
        self.inicio.texto_conexion.setText("¡Conectado!\nEsperando Datos")

    def iniciar_interfaz(self):
        self.set_initial_values()
        self.hide()
        self.senal_iniciar_interfaz.emit()

    def perdida_conexion(self):
        self.inicio.texto_conexion.setText("Conexion Perdida")
        self.inicio.boton_conectar.setDisabled(False)
        self.inicio.boton_continuar.hide()

    def continuar_listo(self):
        self.inicio.texto_conexion.setText('¡Listo!')
        self.inicio.boton_continuar.show()
        self.inicio.boton_continuar.clicked.connect(self.iniciar_interfaz)
