import json
from PyQt5.QtCore import QObject, pyqtSignal
import pickle


class Logica(QObject):

    senal_send_str = pyqtSignal(str)
    senal_send_list = pyqtSignal(list)

    senal_listo_para_continuar = pyqtSignal()
    senal_inicializar_interfaz = pyqtSignal(bytes)

    def __init__(self):
        super().__init__()

        self.connected = False
        self.generar_diccionario_acciones()

    def succes_connection(self):
        envio = ['initial_data_request', None]
        self.senal_send_list.emit(envio)

    def perdida_conexion(self):
        print("Se perdio la conexion")

    def handler(self, recibido):
        if isinstance(recibido, str):
            print(f"recibido: {recibido}")

        elif isinstance(recibido, list):
            if recibido[1] is not None:
                self.acciones[recibido[0]](**recibido[1])

            else:
                self.acciones[recibido[0]]()

    def generar_diccionario_acciones(self):
        self.acciones = {
            'initial_data': self.acquire_initial_data
        }

    def acquire_initial_data(self, image):
        self.initial_image = image
        self.senal_listo_para_continuar.emit()
        byte_image = pickle.dumps(image)
        self.senal_inicializar_interfaz.emit(byte_image)
