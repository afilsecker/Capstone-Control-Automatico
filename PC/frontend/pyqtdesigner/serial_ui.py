# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend/pyqtdesigner/serial.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_serial(object):
    def setupUi(self, serial):
        serial.setObjectName("serial")
        serial.resize(1022, 546)
        self.verticalLayout = QtWidgets.QVBoxLayout(serial)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.input = QtWidgets.QLineEdit(serial)
        self.input.setObjectName("input")
        self.horizontalLayout.addWidget(self.input)
        self.boton_send = QtWidgets.QPushButton(serial)
        self.boton_send.setObjectName("boton_send")
        self.horizontalLayout.addWidget(self.boton_send)
        self.boton_reset = QtWidgets.QPushButton(serial)
        self.boton_reset.setObjectName("boton_reset")
        self.horizontalLayout.addWidget(self.boton_reset)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.texto = QtWidgets.QTextBrowser(serial)
        self.texto.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.texto.setObjectName("texto")
        self.verticalLayout.addWidget(self.texto)

        self.retranslateUi(serial)
        QtCore.QMetaObject.connectSlotsByName(serial)

    def retranslateUi(self, serial):
        _translate = QtCore.QCoreApplication.translate
        serial.setWindowTitle(_translate("serial", "Puerto Serial Perturbador"))
        self.boton_send.setText(_translate("serial", "Send"))
        self.boton_reset.setText(_translate("serial", "Reset"))
        self.texto.setHtml(_translate("serial", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    serial = QtWidgets.QWidget()
    ui = Ui_serial()
    ui.setupUi(serial)
    serial.show()
    sys.exit(app.exec_())
