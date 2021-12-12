# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend/pyqtdesigner/inicio.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_inicio(object):
    def setupUi(self, inicio):
        inicio.setObjectName("inicio")
        inicio.resize(400, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(inicio.sizePolicy().hasHeightForWidth())
        inicio.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        inicio.setFont(font)
        inicio.setWindowTitle("Inicio")
        self.verticalLayout = QtWidgets.QVBoxLayout(inicio)
        self.verticalLayout.setObjectName("verticalLayout")
        self.texto_inicio = QtWidgets.QLabel(inicio)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.texto_inicio.sizePolicy().hasHeightForWidth())
        self.texto_inicio.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.texto_inicio.setFont(font)
        self.texto_inicio.setAlignment(QtCore.Qt.AlignCenter)
        self.texto_inicio.setObjectName("texto_inicio")
        self.verticalLayout.addWidget(self.texto_inicio, 0, QtCore.Qt.AlignHCenter)
        self.texto_info = QtWidgets.QLabel(inicio)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.texto_info.sizePolicy().hasHeightForWidth())
        self.texto_info.setSizePolicy(sizePolicy)
        self.texto_info.setAlignment(QtCore.Qt.AlignCenter)
        self.texto_info.setObjectName("texto_info")
        self.verticalLayout.addWidget(self.texto_info, 0, QtCore.Qt.AlignHCenter)
        self.boton_conectar = QtWidgets.QPushButton(inicio)
        self.boton_conectar.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boton_conectar.sizePolicy().hasHeightForWidth())
        self.boton_conectar.setSizePolicy(sizePolicy)
        self.boton_conectar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.boton_conectar.setAutoFillBackground(False)
        self.boton_conectar.setObjectName("boton_conectar")
        self.verticalLayout.addWidget(self.boton_conectar)
        self.texto_conexion = QtWidgets.QLabel(inicio)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.texto_conexion.sizePolicy().hasHeightForWidth())
        self.texto_conexion.setSizePolicy(sizePolicy)
        self.texto_conexion.setText("")
        self.texto_conexion.setAlignment(QtCore.Qt.AlignCenter)
        self.texto_conexion.setObjectName("texto_conexion")
        self.verticalLayout.addWidget(self.texto_conexion)
        self.boton_continuar = QtWidgets.QPushButton(inicio)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boton_continuar.sizePolicy().hasHeightForWidth())
        self.boton_continuar.setSizePolicy(sizePolicy)
        self.boton_continuar.setObjectName("boton_continuar")
        self.verticalLayout.addWidget(self.boton_continuar)
        self.boton_salir = QtWidgets.QPushButton(inicio)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boton_salir.sizePolicy().hasHeightForWidth())
        self.boton_salir.setSizePolicy(sizePolicy)
        self.boton_salir.setObjectName("boton_salir")
        self.verticalLayout.addWidget(self.boton_salir)

        self.retranslateUi(inicio)
        QtCore.QMetaObject.connectSlotsByName(inicio)

    def retranslateUi(self, inicio):
        _translate = QtCore.QCoreApplication.translate
        self.texto_inicio.setText(_translate("inicio", "PROYECTO CAPSTONE CONTROL"))
        self.texto_info.setText(_translate("inicio", "Asegurate de conectar este PC y la Raspberry al wifi de Alex"))
        self.boton_conectar.setText(_translate("inicio", "Conectar"))
        self.boton_continuar.setText(_translate("inicio", "Continuar"))
        self.boton_salir.setText(_translate("inicio", "Salir"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    inicio = QtWidgets.QWidget()
    ui = Ui_inicio()
    ui.setupUi(inicio)
    inicio.show()
    sys.exit(app.exec_())