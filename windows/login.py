from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style 
from PIL import ImageTk, Image
import os

absolutepath = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolutepath)

class Login():
  def loginPage(self, window):
    def fektImage():
      fekt_img = Image.open(fileDirectory + "\\media\\fekt.png")
      fekt_img = fekt_img.resize((342,111), Image.ANTIALIAS)
      fekt_img = ImageTk.PhotoImage(fekt_img)
      fekt_label = ttk.Label(image=fekt_img)
      fekt_label.image = fekt_img
      fekt_label.config(anchor=CENTER)
      fekt_label.pack()

    fektImage()
    loginGrid = ttk.Labelframe(window, borderwidth=0)
    loginGrid.pack(pady=10)
    emailLabel = ttk.Label(loginGrid, text="E-mail: ").grid(row=0, column=0)
    emailEntry = ttk.Entry(loginGrid, width=30).grid(row=0, column=1, pady=10)
    passwordLabel = ttk.Label(loginGrid, text="Password: ").grid(row=1, column=0)
    passwordEntry = ttk.Entry(loginGrid, width=30, show="*").grid(row=1, column=1)
    loginButton = ttk.Button(window, text="Login", style='danger.TButton').pack()