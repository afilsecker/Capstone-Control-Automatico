"""This is the main program"""

import sys

from PyQt5.QtWidgets import QApplication

from frontend.inicio_2 import Inicio

from backend.client import Client
from backend.logica import Logica

# Para poder debbuguear
def hook(type_error, traceback):
    print(type_error)
    print(traceback)


if __name__ == '__main__':
    sys.__excepthook__ = hook
    app = QApplication(sys.argv)

    logica = Logica()
    inicio = Inicio()
    client = Client()

    # Para la ventana de inicio
    inicio.senal_conectar_cliente.connect(client.connect_to_server)
    client.senal_intentos.connect(inicio.actualizar_intentos)
    client.senal_conexion_exitosa.connect(logica.succes_connection)
    client.senal_conexion_exitosa.connect(inicio.succes_connection)
    client.senal_conexion_fallida.connect(inicio.error_connection)
    client.senal_perdida_conexion.connect(inicio.perdida_conexion)
    

    # Conexion logic-cliente
    client.senal_recibido_list.connect(logica.handler)
    client.senal_recibido_str.connect(logica.handler)
    logica.senal_send_list.connect(client.send)
    logica.senal_send_str.connect(client.send)

    client.senal_perdida_conexion.connect(logica.perdida_conexion)


    # Conexion logica-interfaz
    logica.senal_listo_para_continuar.connect(inicio.continuar_listo)

    sys.exit(app.exec_())

