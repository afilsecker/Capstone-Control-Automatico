from frontend.ventana_inicio import Ui_Form
from PyQt5.QtWidgets import QApplication, QWidget
import cv2
import pickle
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_Form()
    Form = QWidget()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
