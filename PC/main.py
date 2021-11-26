"""This is the main program"""

import sys

from PyQt5.QtWidgets import QApplication

from frontend.inicio import Inicio
from frontend.interfaz import Interfaz
from frontend.serial import Serial

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
    interfaz = Interfaz()
    serial_perturbador = Serial()

    # Para la ventana de inicio
    inicio.senal_conectar_cliente.connect(client.connect_to_server)
    client.senal_intentos.connect(inicio.actualizar_intentos)
    client.senal_conexion_exitosa.connect(logica.succes_connection)
    client.senal_conexion_exitosa.connect(inicio.succes_connection)
    client.senal_conexion_fallida.connect(inicio.error_connection)
    client.senal_perdida_conexion.connect(inicio.perdida_conexion)
    inicio.senal_continuar.connect(logica.iniciar_interfaz)


    # Conexion logic-cliente
    client.senal_recibido_list.connect(logica.handler)
    client.senal_recibido_str.connect(logica.handler)
    logica.senal_send_list.connect(client.send)
    logica.senal_send_str.connect(client.send)

    client.senal_perdida_conexion.connect(logica.perdida_conexion)

    # Conexion logica-interfaz
    logica.senal_listo_para_continuar.connect(inicio.continuar_listo)
    logica.senal_inicializar_interfaz.connect(interfaz.inicializar)

    interfaz.senal_abrir_serial.connect(serial_perturbador.show)
    interfaz.senal_prueba_procesamiento.connect(logica.pedir_prueba_procesamiento)
    logica.senal_actualizar_control.connect(interfaz.actualizar_control)
    interfaz.senal_comenzar_actualizacion.connect(logica.comenzar_actualizacion)
    logica.senal_actualizar_archivos.connect(interfaz.actualizar_archivos)
    logica.senal_actualizar_text_controlador.connect(interfaz.actualizar_text_controlador)
    interfaz.senal_actualizar_controlador.connect(logica.actualizar_controlador)
    logica.senal_actualizar_limites_graficos.connect(interfaz.actualizar_limites_graficos)
    logica.senal_pedir_grafs_keys.connect(interfaz.enviar_grafs_keys)
    interfaz.senal_graficos_keys.connect(logica.obtener_graficos_keys)

    # Conexion logica-serial
    logica.senal_mensaje_perturbador_recibido.connect(serial_perturbador.recieve)
    serial_perturbador.senal_send.connect(logica.enviar_perturbador)
    serial_perturbador.senal_reset.connect(logica.reset_perturbador)

    sys.exit(app.exec_())

