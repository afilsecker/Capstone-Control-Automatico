import json

from PyQt5.QtWidgets import (
    QPushButton, QVBoxLayout, QFrame, QLabel, QLineEdit, QGridLayout, QHBoxLayout
)

from PyQt5.QtCore import Qt

from frontend.crear_layout import crear_layout


class Opciones(QFrame):
    def __init__(self):
        super().__init__()

        with open('parametros.json', 'r') as archivo:
            diccionario = json.load(archivo)
            self.obtener_parametros(diccionario)

        self.main_vbox = QVBoxLayout()
        self.setLayout(self.main_vbox)

    def obtener_parametros(self, diccionario):
        self.__dict__.update(diccionario['frontend']['opciones'])
        self.estilo = ""
        for value in diccionario['frontend']["styles"]["style"].values():
            self.estilo += value

        self.label_style = ""
        for value in diccionario['frontend']["styles"]["label_style"].values():
            self.label_style += value

        self.button_style = ""
        for value in diccionario['frontend']["styles"]["button_style"].values():
            self.button_style += value

    def init_gui(self):
        self.set_style()
        self.setFixedWidth(self.ancho)

        parametros_frame = QFrame()
        parametros_frame.setProperty("parametros", True)
        parametros_gbox = QGridLayout()
        variables = ["Alpha", "Beta"]
        parametros = ["kp", "kd", "ki"]
        parametros_edits = dict()
        
        columna = 0
        for variable in variables:
            fila = 0
            titulo_variable = QLabel(variable, self)
            parametros_gbox.addWidget(titulo_variable, fila, columna, 1, 2, Qt.AlignCenter)
            
            for parametro in parametros:
                fila += 1
                parametro_text = QLabel(parametro, self)
                parametros_gbox.addWidget(parametro_text, fila, columna, 1, 1, Qt.AlignCenter)
                parametro_edit = QLineEdit(self)
                parametros_gbox.addWidget(parametro_edit, fila, columna + 1, 1, 1, Qt.AlignCenter)
                parametros_edits[f'{variable}_{parametro}'] = parametro_edit

            columna += 2

        self.update_controller_button = QPushButton('Actualizar Parametros', self)
        parametros_gbox.addWidget(self.update_controller_button, fila + 1, 0, 1, 4, Qt.AlignCenter)

        parametros_frame.setLayout(parametros_gbox)
        crear_layout(self.main_vbox, parametros_frame)
                

    def set_style(self):
        self.setStyleSheet(f"""
            Opciones
            {{
                {self.estilo}
            }}

            QLabel
            {{
                {self.label_style}
            }}

            QFrame[parametros=true]
            {{
                {self.button_style}
            }}

            """)
