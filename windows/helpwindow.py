from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from windows.window import Window

class Help():
  def displayHelp(self, window):
    windowAppearance = Window()

    popUp = Toplevel(window)
    windowAppearance.centerWindow(popUp, 250, 250)
    popUp.title("Help")
    infoLabel = ttk.Label(popUp, text="When adding a person: ", font='bold').pack(anchor=CENTER, pady=10)
    cityInfoLabel = ttk.Label(popUp, text="  • City must be in database").pack(anchor="nw")
    idInfoLabel = ttk.Label(popUp, text="  • ID must be unique").pack(anchor="nw")


