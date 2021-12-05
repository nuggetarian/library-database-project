from windows.login import Login
from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style
import os

loginPage = Login()

absolutepath = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolutepath)

style = Style('superhero')
window = style.master
window.title("bpc-bds-project3") 
window.iconbitmap(fileDirectory + "\\windows\\media\\vut.ico")
window.geometry("500x500")


loginPage.loginPage(window)

window.mainloop() 

# TO DO
# Ak zadame nespravny mail osetrit