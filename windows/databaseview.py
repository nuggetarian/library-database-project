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

      def clearBoxes(): # Funkcia na vycistenie entry boxov, tuto funkciu volame ked cosi pridame alebo zmazeme
        idEntry.delete(0, END)
        firstNameEntry.delete(0, END)
        lastNameEntry.delete(0, END)
        mailEntry.delete(0, END)
        cityEntry.delete(0, END)
        roleEntry.delete(0, END)

      def selectRecord(e): # Funkcia na vyplnenie entry boxov ked zvolime zaznam (klikneme na neho)
          clearBoxes()

          # Zvolenie kliknuteho zaznamu
          selected = my_tree.focus()
          # Ziskanie obsahu zaznamu
          values = my_tree.item(selected, 'values')

          # Vpisanie dat do entry boxov
          try:
            idEntry.insert(0, values[0])
            firstNameEntry.insert(0, values[1])
            lastNameEntry.insert(0, values[2]) 
            mailEntry.insert(0, values[3])
            cityEntry.insert(0, values[4])
            roleEntry.insert(0, values[5])
          except: # Ked klikame mimo, nevyhadzuje nam to error, ale napise do konzole "Click."
            print("Click.")

      dataGrid = LabelFrame(window, borderwidth=0)
      dataGrid.pack(pady=10)

      #data_frame.pack(fill="x", expand="yes", padx=20)

      idLabel = Label(dataGrid, text="ID")
      idLabel.grid(row=0, column=0, padx=10, pady=10)
      idEntry = Entry(dataGrid, borderwidth=2)
      idEntry.grid(row=0, column=1, padx=10, pady=10)

      firstNameLabel = Label(dataGrid, text="First Name")
      firstNameLabel.grid(row=0, column=2, padx=10, pady=10)
      firstNameEntry = Entry(dataGrid, borderwidth=2)
      firstNameEntry.grid(row=0, column=3, padx=10, pady=10)

      lastNameLabel = Label(dataGrid, text="Last Name")
      lastNameLabel.grid(row=0, column=4, padx=10, pady=10)
      lastNameEntry = Entry(dataGrid, borderwidth=2)
      lastNameEntry.grid(row=0, column=5, padx=10, pady=10)

      mailLabel = Label(dataGrid, text="Mail")
      mailLabel.grid(row=1, column=0, padx=10, pady=10)
      mailEntry = Entry(dataGrid, borderwidth=2)
      mailEntry.grid(row=1, column=1, padx=10, pady=10)

      cityLabel = Label(dataGrid, text="City")
      cityLabel.grid(row=1, column=2, padx=10, pady=10)
      cityEntry = Entry(dataGrid, borderwidth=2)
      cityEntry.grid(row=1, column=3, padx=10, pady=10)

      roleLabel = Label(dataGrid, text="Role")
      roleLabel.grid(row=1, column=4, padx=10, pady=10)
      roleEntry = Entry(dataGrid, borderwidth=2)
      roleEntry.grid(row=1, column=5, padx=10, pady=10)

      # Pri uvolneni tlacidla 1 na mysi sa vykona funkcia select_record a zvoli sa dany zaznam
      my_tree.bind("<ButtonRelease-1>", selectRecord)

      readDatabase()
          
