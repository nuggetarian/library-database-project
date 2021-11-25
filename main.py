from windows.login import Login
from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style

style = Style('superhero')
window = style.master
window.title("bpc-bds-project3") 
"""Pridat ikonu VUT"""
window.geometry("500x500")

loginPage = Login()
loginPage.loginPage(window)

window.mainloop() 
