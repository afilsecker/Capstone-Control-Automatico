from PyQt5.QtWidgets import QLayout, QWidget


def crear_layout(box: QLayout, *args, centrado=True):
    box.addStretch(1)
    for argument in args:
        if isinstance(argument, QLayout):
            box.addLayout(argument)

        elif isinstance(argument, QWidget):
            box.addWidget(argument)

        else:
            raise Exception()

        if centrado:
            box.addStretch(1)