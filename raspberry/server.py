import socket
import json
import pickle
from threading import Thread


class Server:

    def __init__(self):
        with open('parametros.json', 'r') as archivo:
            diccionario = json.load(archivo)
            self.__dict__.update(diccionario["server"])

        self.host = socket.gethostname()
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_and_listen()
        self.accept_connections()

    # Cosas de Server
    def bind_and_listen(self):
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        self.iniciar_log()

    def accept_connections(self):
        thread = Thread(target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self):
        self.server_full = False
        while True:
            client_socket, _ = self.socket_server.accept()
            self.mensaje_log("Cliente Intenta Ingresar", "")
            listenint_client_thread = Thread(
                target=self.listen_client_thread,
                kwargs={"client_socket": client_socket},
                daemon=True
            )
            self.server_full = True
            if not self.server_full:
                self.client_socket = client_socket
                listenint_client_thread.start()
                self.mensaje_log("Conectado de Pana", "")

    def listen_client_thread(self, client_socket):
        try:
            while True:
                response_bytes_length = client_socket.recv(self.tamanos['indicador_largo'])
                response_length = int.from_bytes(
                    response_bytes_length, byteorder='big')

                numero_bloques = response_length // self.tamanos['bloques'] + 1
                contador = 0
                response = bytearray()
                while len(response) < response_length:
                    indice_bloque_bytes = client_socket.recv(self.tamanos['numero'])
                    indice_bloque = int.from_bytes(
                        indice_bloque_bytes, byteorder='little')

                    if indice_bloque - 1 != contador:
                        raise Exception

                    if contador + 1 == numero_bloques:
                        response.extend(client_socket.recv(response_length - len(response)))
                        client_socket.recv(
                            numero_bloques * self.tamanos["bloques"] - response_length)

                    else:
                        response.extend(client_socket.recv(self.tamanos['bloques']))

                    contador += 1

                if len(response) > 0:
                    recibido = pickle.loads(response)
                    self.handler(recibido)

        except ConnectionResetError:
            self.mensaje_log("Desconección", "")
            self.client_socket.close()
            self.server_full = False

    def handler(self, recibido):
        if recibido[1] is not None:
            self.acciones[recibido[0]](**recibido[1])

        else:
            self.acciones[recibido[0]]()

    # Cosas de LOG
    def iniciar_log(self):
        txt = "|  {:<40}|  {:<40}|"
        print()
        print(txt.format("Evento", "Detalles"))
        print(("|" + "-" * 42) * 2 + "|")

    def mensaje_log(self, evento, detalles):
        txt = "|  {:<40}|  {:<40}|"
        print(txt.format(evento, detalles))

    # Acciones por Cliente
    def generar_diccionario_acciones(self):
        self.acciones = {
            'pene': self.pene
        }

    def pene(self):
        print('caca')
