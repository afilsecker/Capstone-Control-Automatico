from PyQt5.QtCore import QObject, pyqtSignal
import sys
from matplotlib import pyplot as plt
import cv2
from os import listdir
from os.path import isfile, join
import numpy as np

class Logica(QObject):

    senal_send_str = pyqtSignal(str)
    senal_send_list = pyqtSignal(list)

    senal_listo_para_continuar = pyqtSignal()
    senal_inicializar_interfaz = pyqtSignal(dict)
    senal_actualizar_control = pyqtSignal(dict)
    senal_actualizar_archivos = pyqtSignal(list)
    senal_actualizar_text_controlador = pyqtSignal(dict)
    senal_actualizar_limites_graficos = pyqtSignal(dict)
    senal_pedir_grafs_keys = pyqtSignal()

    senal_mensaje_perturbador_recibido = pyqtSignal(str)
    senal_enviar_mensaje_perturbador = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.connected = False
        self.en_interfaz = False
        self.parametros = dict()
        self.limites_graficos = dict()
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
        self.parametros = datos['parametros']
        self.senal_listo_para_continuar.emit()
        value = self.parametros.copy()
        value["name"] = 'inicial'
        self.senal_actualizar_text_controlador.emit(value)
        self.senal_pedir_grafs_keys.emit()
        self.actualizar_limites_graficos()
        self.escribir_parametros('inicial', self.parametros)
        self.obtener_paths_parametros()

    def escribir_parametros(self, nombre: str, parametros: dict):
        with open(f'backend/parametros/{nombre}.txt', 'w') as f:
            for parametro in parametros.keys():
                f.write(f'{parametro}={parametros[parametro]}\n')

    def obtener_paths_parametros(self):
        path = 'backend/parametros/'
        files = [f for f in listdir(path) if isfile(join(path, f))]
        self.senal_actualizar_archivos.emit(files)

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

    def actualizar_controlador(self, parametros: dict):
        for key in parametros:
            self.parametros[key] = float(parametros[key])
        print("hola")
        self.actualizar_limites_graficos()

        value = ['nuevos_parametros', {'parametros': self.parametros}]
        envio = ['send_to_controlador', {'value': value}]
        self.senal_send_list.emit(envio)

    def obtener_graficos_keys(self, keys: list):
        self.graficos_keys = keys

    def actualizar_limites_graficos(self):
        for key in self.graficos_keys:
            if key == 'e_abs':
                limite = np.sqrt(self.resolution[0] ** 2 + self.resolution[1] ** 2)
                self.limites_graficos[key] = [0, limite]
            else:
                if key == 'e_a':
                    limite = self.resolution[1]
                    
                elif key == 'e_b':
                    limite = self.resolution[1]
                elif key == 'u_a':
                    max_p = self.resolution[1] * self.parametros['kpa']
                    max_d = self.resolution[1] / 10 * self.parametros['kda']
                    max_i = self.parametros['max_i_a']
                    limite = max_p + max_d + max_i
                elif key == 'u_b':
                    max_p = self.resolution[0] * self.parametros['kpb']
                    max_d = self.resolution[0] / 10 * self.parametros['kdb']
                    max_i = self.parametros['max_i_b']
                    limite = max_p + max_d + max_i
                elif key == 'p_a':
                    limite = self.resolution[1] * self.parametros['kpa']
                elif key == 'p_b':
                    limite = self.resolution[0] * self.parametros['kpb']
                elif key == 'd_a':
                    limite = self.resolution[1] / 10 * self.parametros['kda']
                elif key == 'd_b':
                    limite = self.resolution[0] / 10 * self.parametros['kdb']
                elif key == 'i_a':
                    limite = self.parametros['max_i_a']
                elif key == 'i_b':
                    limite = self.parametros['max_i_b']

                self.limites_graficos[key] = [-limite, limite]

        self.senal_actualizar_limites_graficos.emit(self.limites_graficos)
