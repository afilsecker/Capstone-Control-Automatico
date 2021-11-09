import tkinter as tk
import tkinter.ttk as ttk
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()
        with open('parametros.json', 'r') as archivo:
            diccionario = json.load(archivo)
            self.par = diccionario["frontend"]

        self.center_window()
        self.title(self.par["TITULO_VENTANA"])
        self.define_styles()
        self.button_1 = ttk.Button(self, text="hola", command=self.plot)
        self.button_1.pack()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.width, self.height = self.par["TAMANO_VENTANA"]
        x_cordinate = int((screen_width/2) - (self.width/2))
        y_cordinate = int((screen_height/2) - (self.height/2))
        self.geometry("{}x{}+{}+{}".format(
            self.width, self.height, x_cordinate, y_cordinate))

    def plot(self):
        self.figure = Figure(figsize=(3, 3), dpi=100)
        y = [x ** 2 for x in range(101)]
        self.plot = self.figure.add_subplot(111)
        self.plot.plot(y)
        canvas = FigureCanvasTkAgg(self.figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def define_styles(self):
        self.style = ttk.Style()
        self.style.configure('TButton', font =
               ('calibri', 12, 'bold', 'underline'),
                foreground = 'red')
