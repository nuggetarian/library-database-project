from windows.login import Login
from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style
import os

loginPage = Login()

absolutepath = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolutepath)

window = Tk()
style = Style('superhero')
window = style.master
window.title("bpc-bds-project3") 
window.iconbitmap(fileDirectory + "\\windows\\media\\vut.ico")

loginPage.loginPage(window)

window.mainloop() 

# TO DO
# Ak zadame nespravny mail osetrit