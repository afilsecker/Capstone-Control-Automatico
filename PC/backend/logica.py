from PyQt5.QtCore import QObject, pyqtSignal
import sys
from matplotlib import pyplot as plt
import cv2

class Logica(QObject):

    senal_send_str = pyqtSignal(str)
    senal_send_list = pyqtSignal(list)

    senal_listo_para_continuar = pyqtSignal()
    senal_inicializar_interfaz = pyqtSignal(dict)
    senal_actualizar_control = pyqtSignal(dict)

    senal_mensaje_perturbador_recibido = pyqtSignal(str)
    senal_enviar_mensaje_perturbador = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.connected = False
        self.en_interfaz = False
        self.generar_diccionario_acciones()

    def succes_connection(self):
        self.connected = True
        value = ['initial_data_request', None]
        envio = ['send_to_controlador', {'value': value}]
        self.senal_send_list.emit(envio)

    def perdida_conexion(self):
        self.connected = False
        print("Se perdio la conexion")
        if self.en_interfaz:
            sys.exit()

    def handler(self, recibido):
        if isinstance(recibido, str):
            print(f"recibido: {recibido}")

        elif isinstance(recibido, list):
            if recibido[0] in self.acciones.keys():
                if recibido[1] is not None:
                    self.acciones[recibido[0]](**recibido[1])

                else:
                    self.acciones[recibido[0]]()

            else:
                print(recibido[0], "not part of diccionario acciones")

    def generar_diccionario_acciones(self):
        self.acciones = {
            'initial_data': self.acquire_initial_data,
            'perturbador': self.recibir_perturbador,
            'prueba_procesamiento_response': self.recibir_prueba_procesamiento,
            'control': self.recibir_control
        }

    def acquire_initial_data(self, **datos):
        self.resolution = datos['resolution']
        parametros = datos['parametros']
        self.senal_listo_para_continuar.emit()
        self.escribir_parametros('inicial', parametros)

    def escribir_parametros(self, nombre: str, parametros: dict):
        with open(f'backend/parametros/{nombre}.txt', 'w') as f:
            for parametro in parametros.keys():
                f.write(f'{parametro}={parametros[parametro]}\n')

    def iniciar_interfaz(self):
        datos = {'resolucion': self.resolution}
        self.senal_inicializar_interfaz.emit(datos)
        self.en_interfaz = True

    def comenzar_actualizacion(self):
        value = ['interfaz_lista', None]
        envio = ['send_to_controlador', {'value': value}]
        self.senal_send_list.emit(envio)

    def recibir_perturbador(self, recibido: str):
        self.senal_mensaje_perturbador_recibido.emit(recibido)

    def enviar_perturbador(self, msg):
        value = ['send', {'msg': msg}]
        envio = ['send_to_perturbador', {'value': value}]
        self.senal_send_list.emit(envio)

    def reset_perturbador(self):
        value = ['reset', None]
        send = ['send_to_perturbador', {'value': value}]
        self.senal_send_list.emit(send)

    def pedir_prueba_procesamiento(self):
        value = ['prueba_procesamiento', None]
        envio = ['send_to_controlador', {'value': value}]
        self.senal_send_list.emit(envio)

    def recibir_prueba_procesamiento(self, image, puntos, punto_rojo):
        if image is not None:
            plt.figure()
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if puntos is not None:
                plt.scatter(puntos[1], puntos[0], c='blue')
            if punto_rojo[0] is not None:
                plt.scatter(punto_rojo[1], punto_rojo[0], c='red')
            plt.show()

    def recibir_control(self, datos):
        self.senal_actualizar_control.emit(datos)
