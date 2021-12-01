from windows.login import Login
from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style
import os
from windows.postgre import Postgres
import bcrypt


absolutepath = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolutepath)

style = Style('superhero')
window = style.master
window.title("bpc-bds-project3") 
window.iconbitmap(fileDirectory + "\\windows\\media\\vut.ico")
window.geometry("500x500")
loginPage = Login()

loginPage.loginPage(window)

window.mainloop() 

# TO DO
# Pridat do tabulky user heslo, sifrovat ako na AKR cez bcrypt
# .gitignore
