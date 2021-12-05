from tkinter import *
from tkinter import ttk
from tkinter import font
from typing import Counter
import psycopg2
from windows.window import Window
import webbrowser


class DatabaseWindow():
  def viewDatabase(self, window):
      
      DB_HOST = "localhost"
      DB_NAME = "library-db"
      DB_USER = "postgres"
      DB_PASS = "postgres"
      windowAppearance = Window()
      windowAppearance.centerWindow(window, 850, 500)

      def openWebsite():
        webbrowser.open_new("https://www.youtube.com/watch?v=2Q_ZzBGPdqE")
        
      menu = Menu(window)
      window.config(menu=menu)

      subMenu = Menu(menu)
      menu.add_cascade(label="File", menu=subMenu)

      helpMenu = Menu(menu)
      menu.add_cascade(label="Help", menu=helpMenu)
      helpMenu.add_command(label="Alexa, play The Beatles - Help!", command=openWebsite, background="white", foreground="black")
   
      # Set Treeview style
      style = ttk.Style()
      style.theme_use("clam")
      style.configure("Treeview", rowheight=30)

      # Vytvorenie treeview frame-u
      tree_frame = Frame(window)
      tree_frame.pack(pady=10)

      # Vytvorenie scrollbaru
      tree_scroll = Scrollbar(tree_frame)
      tree_scroll.pack(side=RIGHT, fill=Y)

      # Vytvorenie treeview
      my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
      my_tree.pack()

      # Konfiguracia scrollbaru
      tree_scroll.config(command=my_tree.yview)

      # Definovanie stlpcov
      my_tree['columns'] = ("ID", "First Name", "Last Name", "Mail", "City", "Role")

      # Formatovanie stlpcov
      my_tree.column("#0", width=0, stretch = NO)
      my_tree.column("ID", anchor=W, width=70)
      my_tree.column("First Name", anchor=W, width=140)
      my_tree.column("Last Name", anchor=W, width=140)
      my_tree.column("Mail", anchor=W, width=140)
      my_tree.column("City", anchor=W, width=140)
      my_tree.column("Role", anchor=W, width=140)

      # Vytvorenie nadpisov
      my_tree.heading("#0", text="", anchor=W)
      my_tree.heading("ID", text="ID", anchor=W)
      my_tree.heading("First Name", text="First Name", anchor=W)
      my_tree.heading("Last Name", text="Last Name", anchor=W)
      my_tree.heading("Mail", text="Mail", anchor=W)
      my_tree.heading("City", text="City", anchor=W)
      my_tree.heading("Role", text="Role", anchor=W)

      # Vytvorenie pruhovanych riadkov na zaklade toho ci su liche alebo sude
      my_tree.tag_configure('oddrow', background="#2b3e50")
      my_tree.tag_configure('evenrow', background="#111d29")

      def readDatabase():
          conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
          c = conn.cursor()

          c.execute("""SELECT DISTINCT
                        u.user_id,
                        u.first_name,
                        u.last_name,
                        c.mail,
                        ad.city,
                        ro.role_type
          FROM public.user u
          JOIN public.contact c ON u.user_id = c.user_id
          JOIN public.user_has_address a ON u.user_id = a.user_id
          JOIN public.address ad ON a.address_id = ad.address_id
          JOIN public.user_has_role r ON r.user_id = u.user_id
          JOIN public.role ro ON r.role_id = ro.role_id""")
          conn.commit()
          records = c.fetchall()
          global count
          count = 0
          for record in records:
            if count % 2 == 0:
              my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))
            else:
              my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',)) 
            count += 1
          c.close()
          conn.close()

      """def selectRecord(e):
        selected = my_tree.focus()"""

      """my_tree.bind("<ButtonRelease-1>", selectRecord)"""
      readDatabase()
          
