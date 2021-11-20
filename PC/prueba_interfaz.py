from PyQt5.QtWidgets import QApplication
import sys

from frontend.interfaz import Interfaz

if __name__ == '__main__':
    app = QApplication(sys.argv)
    interfaz = Interfaz()
    interfaz.show()
    sys.exit(app.exec_())
