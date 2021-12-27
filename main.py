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
window.iconbitmap("vut.ico")

loginPage.loginPage(window)
window.mainloop()

# TO DO
# zmenit file na window a dat tam windows na sql attack, tabulku s knizkami
# Prisposobit bookview tomuto
# transaction rollback ak pridame cosi do transactions tabulky https://www.oracletutorial.com/python-oracle/transactions/