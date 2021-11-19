import json

from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel
)
from PyQt5.QtCore import Qt, pyqtSignal

from frontend.crear_layout import crear_layout


class VentanaInicio(QWidget):

    senal_conectar_cliente = pyqtSignal()
    senal_iniciar_interfaz = pyqtSignal()

    def __init__(self):
        super(VentanaInicio, self).__init__()
        with open('parametros.json', 'r') as f:
            diccionario = json.load(f)
            self.__dict__.update(diccionario['frontend']['inicio'])

        self.init_gui()
        self.show()

    def init_gui(self):
        self.setGeometry(*self.posicion, *self.tamano)
        self.setFixedSize(*self.tamano)
        self.setWindowTitle(self.titulo)

        # Boxes
        main_vbox = QVBoxLayout()
        main_hbox = QHBoxLayout()
        self.setLayout(main_hbox)

        # Texto inicial
        texto = "Asegurate de conectar este pc y la raspberr al wifi de Alex"
        texto = QLabel(texto, self)
        texto.setAlignment(Qt.AlignCenter)

        # Botones
        self.boton_conectar = QPushButton("Presiona para conectar", self)
        self.boton_conectar.clicked.connect(self.conectar_cliente)

        self.boton_continuar = QPushButton("Continuar", self)
        self.boton_continuar.hide()

        self.boton_salir = QPushButton("Salir", self)
        self.boton_salir.clicked.connect(self.close)

        # Texto de Conexion
        self.texto_conexion = QLabel(" ", self)
        self.texto_conexion.setAlignment(Qt.AlignCenter)

        crear_layout(main_vbox, texto, self.boton_conectar, self.texto_conexion, self.boton_continuar, self.boton_salir)
        crear_layout(main_hbox, main_vbox)

    def set_initial_values(self):
        self.boton_conectar.setDisabled(False)
        self.boton_continuar.hide()
        self.texto_conexion.setText(" ")

    def conectar_cliente(self):
        self.texto_conexion.setText("Intentando conectar")
        self.senal_conectar_cliente.emit()
        self.boton_conectar.setDisabled(True)

    def actualizar_intentos(self, intento: int, totales: int):
        self.texto_conexion.setText(f'Intento de conexion {intento}/{totales} fallido')

    def error_connection(self):
        self.texto_conexion.setText("No se pudo conectar con el servidor")
        self.boton_conectar.setDisabled(False)

    def succes_connection(self):
        self.texto_conexion.setText("¡Conectado!\nEsperando Datos")

    def iniciar_interfaz(self):
        self.set_initial_values()
        self.hide()
        self.senal_iniciar_interfaz.emit()

    def perdida_conexion(self):
        self.texto_conexion.setText("Conexion Perdida")
        self.boton_conectar.setDisabled(False)
        self.boton_continuar.hide()

    def continuar_listo(self):
        self.texto_conexion.setText('¡Listo!')
        self.boton_continuar.show()
        self.boton_continuar.clicked.connect(self.iniciar_interfaz)
