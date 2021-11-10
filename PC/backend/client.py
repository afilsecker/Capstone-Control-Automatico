import socket
import json
import pickle

from threading import Thread
from PyQt5.QtCore import QObject

class Client(QObject):

    def __init__(self):
        with open('parametros.json', 'r') as archivo:
            diccionario = json.load(archivo)
            self.__dict__.update(diccionario['backend']['cliente'])

        super().__init__()
        self.host = socket.gethostname()
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        thread = Thread(target=self.bind_and_listen, daemon=True)
        thread.start()

    def bind_and_listen(self):
        conectado = False
        while not conectado:
            print("holas")
            try:
                self.connect_to_server()
                self.listen()
                conectado = True

            except ConnectionError:
                print("caca")

    def connect_to_server(self):
        self.socket_client.connect((self.host, self.port))
        print("holas")

    def send(self, msg):
        msg_bytes = pickle.dumps(msg)
        largo = len(msg_bytes)
        msg_lenght = largo.to_bytes(self.tamanos["indicador_largo"], byteorder='big')
        self.socket_client.sendall(msg_lenght)
        numero_bloques = largo // self.tamanos['bloques'] + 1
        contador = 0
        while contador < numero_bloques:
            indice_bloque = (contador + 1).to_bytes(self.tamanos['numero'], byteorder='little')
            self.socket_client.sendall(indice_bloque)
            if contador + 1 == numero_bloques:
                inicio = contador * self.tamanos['bloques']
                bloque = msg_bytes[inicio:]
                bloque += (self.tamanos['bloques'] - len(bloque)) * b'\x00'
                self.socket_client.sendall(bloque)

            else:
                inicio = contador * self.tamanos['bloques']
                fin = (contador + 1) * self.tamanos['bloques']
                bloque = msg_bytes[inicio:fin]
                self.socket_client.sendall(bloque)

            contador += 1

    def listen(self):
        self.thread_listen = Thread(target=self.listen_thread, daemon=True)
        self.thread_listen.start()

    def listen_thread(self):
        try:
            while True:
                response_bytes_length = self.socket_client.recv(self.tamanos['indicador_largo'])
                response_length = int.from_bytes(
                    response_bytes_length, byteorder='big')
                numero_bloques = response_length // self.tamanos['bloques'] + 1
                contador = 0
                response = bytearray()
                while len(response) < response_length:
                    indice_bloque_bytes = self.socket_client.recv(self.tamanos['numero'])
                    indice_bloque = int.from_bytes(
                        indice_bloque_bytes, byteorder='little')

                    if indice_bloque - 1 != contador:
                        pass

                    if contador + 1 == numero_bloques:
                        recepcion = self.socket_client.recv(response_length - len(response))
                        bloque = recepcion
                        response.extend(recepcion)
                        recepcion = self.socket_client.recv(
                            numero_bloques * self.tamanos["bloques"] - response_length)
                        bloque += recepcion

                    else:
                        recepcion = self.socket_client.recv(self.tamanos["bloques"])
                        response.extend(recepcion)

                    contador += 1

                if len(response) > 0:
                    try:
                        recibido = pickle.loads(response)
                        self.handler(recibido)

                    except pickle.UnpicklingError:
                        self.reset()

        except ConnectionResetError:
            self.reset()

    def reset(self):
        self.senal_perdida_de_conexion.emit()
        self.socket_client.close()

    def handler(self, recibido):
        if isinstance(recibido, str):
            print(f"recibido: {recibido}")

        elif isinstance(recibido, list):
            if recibido[1] is not None:
                self.acciones[recibido[0]](**recibido[1])

            else:
                self.acciones[recibido[0]]()