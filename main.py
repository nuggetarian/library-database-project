from windows.login import Login
from tkinter import *
from ttkbootstrap import Style

loginPage = Login()

# Setting up main window (icon, style, title etc.)
window = Tk()
style = Style('superhero')
window = style.master
window.title("bpc-bds-project3") 
window.iconbitmap("vut.ico")

# Opening login page
loginPage.loginPage(window)
window.mainloop()