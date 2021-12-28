from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style
import psycopg2
from windows.helpwindow import Help
from windows.window import Window
import webbrowser
import logging

class DatabaseWindow():
  logging.basicConfig(filename="logfile.log",
                      filemode='a',
                      format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

  def viewUsers(self, window):
      for widget in window.winfo_children():
          widget.destroy()

      DB_HOST = "localhost"
      DB_NAME = "librarydb"
      DB_USER = "postgres"
      DB_PASS = "postgres"

      windowAppearance = Window()
      windowAppearance.centerWindow(window, 850, 700)

      def openWebsite():
        webbrowser.open_new("https://www.youtube.com/watch?v=2Q_ZzBGPdqE")
      
      def openHelp():
        helpWindow = Help()
        helpWindow.displayHelp(window)

      db = DatabaseWindow()
      menu = Menu(window)
      window.config(menu=menu)

      subMenu = Menu(menu)
      menu.add_cascade(label="Window", menu=subMenu)
      subMenu.add_command(label="Book Info", background="white", foreground="black", command=lambda:db.viewBooks(window))
      subMenu.add_command(label="SQL Injection", background="white", foreground="black", command=lambda:db.sqlInjection(window))

      helpMenu = Menu(menu)
      menu.add_cascade(label="Help", menu=helpMenu)
      helpMenu.add_command(label="Alexa, play The Beatles - Help!", command=openWebsite, background="white", foreground="black")
      helpMenu.add_command(label="Actual Help", command=openHelp, background="white", foreground="black")

      # Set Treeview style
      style = Style('superhero')
      style.configure("Treeview", rowheight=30)

      # Vytvorenie treeview frame-u
      treeFrame = Frame(window)
      treeFrame.pack(pady=10)

      # Vytvorenie scrollbaru
      scroll = ttk.Scrollbar(treeFrame)
      scroll.pack(side=RIGHT, fill=Y)

      # Vytvorenie treeview
      userTree = ttk.Treeview(treeFrame, yscrollcommand=scroll.set, selectmode="extended")
      userTree.pack()

      # Konfiguracia scrollbaru
      scroll.config(command=userTree.yview)

      # Definovanie stlpcov
      userTree['columns'] = ("ID", "First Name", "Last Name", "Mail", "City", "Role")

      # Formatovanie stlpcov
      userTree.column("#0", width=0, stretch = NO)
      userTree.column("ID", anchor=W, width=70)
      userTree.column("First Name", anchor=W, width=140)
      userTree.column("Last Name", anchor=W, width=140)
      userTree.column("Mail", anchor=W, width=140)
      userTree.column("City", anchor=W, width=140)
      userTree.column("Role", anchor=W, width=140)

      # Vytvorenie nadpisov
      userTree.heading("#0", text="", anchor=W)
      userTree.heading("ID", text="ID", anchor=W)
      userTree.heading("First Name", text="First Name", anchor=W)
      userTree.heading("Last Name", text="Last Name", anchor=W)
      userTree.heading("Mail", text="Mail", anchor=W)
      userTree.heading("City", text="City", anchor=W)
      userTree.heading("Role", text="Role", anchor=W)

      # Vytvorenie pruhovanych riadkov na zaklade toho ci su liche alebo sude
      userTree.tag_configure('oddrow', background="#2b3e50")
      userTree.tag_configure('evenrow', background="#111d29")

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
          LEFT JOIN public.contact c ON u.user_id = c.user_id
          LEFT JOIN public.user_has_address a ON u.user_id = a.user_id
          LEFT JOIN public.address ad ON a.address_id = ad.address_id
          LEFT JOIN public.user_has_role r ON r.user_id = u.user_id
          LEFT JOIN public.role ro ON r.role_id = ro.role_id
          ORDER BY u.user_id ASC""")
          conn.commit()
          records = c.fetchall()
          global count
          count = 0
          for record in records:
            if count % 2 == 0:
              userTree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))
            else:
              userTree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',)) 
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
        filterEntry.delete(0, END)

      def selectRecord(e): # Funkcia na vyplnenie entry boxov ked zvolime zaznam (klikneme na neho)
          clearBoxes()

          global roleset
          # Zvolenie kliknuteho zaznamu
          selected = userTree.focus()
          # Ziskanie obsahu zaznamu
          values = userTree.item(selected, 'values')

          # Vpisanie dat do entry boxov
          try:
            idEntry.insert(0, values[0])
            firstNameEntry.insert(0, values[1])
            lastNameEntry.insert(0, values[2]) 
            mailEntry.insert(0, values[3])
            cityEntry.insert(0, values[4])
            roleEntry.insert(0, values[5])

            if roleEntry.get() == "admin":
              roleset = 1
            elif roleEntry.get() == "manager":
              roleset = 2
            elif roleEntry.get() == "employee":
              roleset = 3
            elif roleEntry.get() == "donator":
              roleset = 4
            elif roleEntry.get() == "customer":
              roleset = 5
          except: # Ked klikame mimo, nevyhadzuje nam to error, ale napise do konzole "Click."
            print("Click.")

      def removeFromDatabase(): # Funkcia na zmazanie zaznamu
          try: # Vymazanie na zaklade id ktore ziskame z pola, ked zvolime nejaky riadok
            x = userTree.selection()[0]
            userTree.delete(x)
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            c = conn.cursor()
            c.execute("""DELETE FROM public.user_has_address WHERE user_id = %s""", (idEntry.get(),))
            c.execute("""DELETE FROM public.user_has_role WHERE user_id = %s""", (idEntry.get(),))
            c.execute("""DELETE FROM public.contact WHERE user_id = %s""", (idEntry.get(),))
            c.execute("""DELETE FROM public.user WHERE user_id = %s""", (idEntry.get(),))
            conn.commit()
            clearBoxes()
            #conn.close()		
          except IndexError:  
            warningLabel = ttk.Label(warningGrid, text="          Nothing selected          ")
            conn.rollback()
            logging.warning('IndexError: Nothing Selected.')
            warningLabel.grid(row=0, column=0)

      def addRecord():
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        c = conn.cursor()
        role = 0
        if roleEntry.get() == "admin":
          role = 1
        elif roleEntry.get() == "manager":
          role = 2
        elif roleEntry.get() == "employee":
          role = 3
        elif roleEntry.get() == "donator":
          role = 4
        elif roleEntry.get() == "customer":
          role = 5
        
        city = 0
        if cityEntry.get() == "Jonesboro":
          city = 1
        elif cityEntry.get() == "Seattle":
          city = 2
        elif cityEntry.get() == "Providence":
          city = 3
        elif cityEntry.get() == "Canton":
          city = 4
        elif cityEntry.get() == "Wellesley":
          city = 5
        try:
          c.execute("""INSERT INTO public.user (user_id, first_name, last_name) VALUES (%s, %s, %s);""", 
                    (idEntry.get(), firstNameEntry.get(), lastNameEntry.get(),))
          c.execute("""INSERT INTO public.contact (user_id, mail) VALUES (%s, %s);""",
                    (idEntry.get(), mailEntry.get(),))
          c.execute("""INSERT INTO public.user_has_role (user_id, role_id) VALUES (%s, %s);""",
                    (idEntry.get(), role,))
          c.execute("""INSERT INTO public.user_has_address (user_id, address_id) VALUES (%s, %s);""",
                    (idEntry.get(), city,))
        except psycopg2.errors.UniqueViolation:
          conn.rollback()
          logging.warning('psycopg2.errors.UniqueViolation: Error Adding Record (Duplicate)')
          duplicateError = ttk.Label(warningGrid, text="      Duplicate ID      ").grid(row=0, column=0)
        except psycopg2.errors.InvalidTextRepresentation:
          conn.rollback()
          logging.warning('psycopg2.errors.InvalidTextRepresentation: Invalid Datatype')
          invalidDatatypeError = ttk.Label(warningGrid, text="      Invalid Datatype      ").grid(row=0, column=0)
        except psycopg2.errors.ForeignKeyViolation:
          conn.rollback()
          logging.warning('psycopg2.errors.ForeignKeyViolation')
          foreignKeyError = ttk.Label(warningGrid, text="      Foreign Key Violation      ").grid(row=0, column=0)

        conn.commit()
        clearBoxes()
        conn.close()

        userTree.delete(*userTree.get_children())
        readDatabase()

      def updateRecord():
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        c = conn.cursor()
        #c.execute("""INSERT INTO public.user (user_id, first_name, last_name) VALUES (%s, %s, %s);""", 
        #          (idEntry.get(), firstNameEntry.get(), lastNameEntry.get(),))
        city = 0
        if cityEntry.get() == "Jonesboro":
          city = 1
        elif cityEntry.get() == "Seattle":
          city = 2
        elif cityEntry.get() == "Providence":
          city = 3
        elif cityEntry.get() == "Canton":
          city = 4
        elif cityEntry.get() == "Wellesley":
          city = 5

        role = 0
        if roleEntry.get() == "admin":
          role = 1
        elif roleEntry.get() == "manager":
          role = 2
        elif roleEntry.get() == "employee":
          role = 3
        elif roleEntry.get() == "donator":
          role = 4
        elif roleEntry.get() == "customer":
          role = 5
        
        try:
          c.execute("""UPDATE public.user SET last_name = %s, first_name = %s WHERE user_id = %s;""", (lastNameEntry.get(),firstNameEntry.get(),idEntry.get(),))
          c.execute("""UPDATE public.contact SET mail = %s WHERE user_id = %s;""", (mailEntry.get(),idEntry.get(),))
          c.execute("""UPDATE public.user_has_address SET address_id = %s WHERE user_id = %s;""", (city,idEntry.get(),))
          c.execute("""UPDATE public.user_has_role SET role_id = %s WHERE user_id = %s AND role_id = %s;""", (role,idEntry.get(),roleset,))
        except psycopg2.errors.UniqueViolation:
          conn.rollback()
          logging.warning('psycopg2.errors.UniqueViolation')
          duplicateError = ttk.Label(warningGrid, text="      Unique Violation      ").grid(row=0, column=0)
        except psycopg2.errors.InvalidTextRepresentation:
          conn.rollback()
          logging.warning('psycopg2.errors.InvalidTextRepresentation: Invalid Datatype')
          invalidDatatypeError = ttk.Label(warningGrid, text="      Invalid Datatype      ").grid(row=0, column=0)
        except psycopg2.errors.ForeignKeyViolation:
          conn.rollback()
          logging.warning('psycopg2.errors.ForeignKeyViolation')
          foreignKeyError = ttk.Label(warningGrid, text="      Foreign Key Violation      ").grid(row=0, column=0)
        except NameError:
          conn.rollback()
          logging.warning('NameError: Roleset not defined ')
          foreignKeyError = ttk.Label(warningGrid, text="      NameError: Roleset not defined      ").grid(row=0, column=0)

        conn.commit()
        clearBoxes()
        conn.close()

        userTree.delete(*userTree.get_children())
        readDatabase()          

      def filterDatabase():
          userTree.delete(*userTree.get_children())
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
          LEFT JOIN public.contact c ON u.user_id = c.user_id
          LEFT JOIN public.user_has_address a ON u.user_id = a.user_id
          LEFT JOIN public.address ad ON a.address_id = ad.address_id
          LEFT JOIN public.user_has_role r ON r.user_id = u.user_id
          LEFT JOIN public.role ro ON r.role_id = ro.role_id
		      WHERE u.last_name = %s OR u.first_name = %s 
          OR c.mail = %s OR ro.role_type = %s 
          OR ad.city = %s;""", (filterEntry.get(),filterEntry.get(),filterEntry.get(),filterEntry.get(),filterEntry.get(),))
          conn.commit()
          filtered = c.fetchall()
          global count
          count = 0
          for item in filtered:
            if count % 2 == 0:
              userTree.insert(parent='', index='end', iid=count, text='', values=(item[0], item[1], item[2], item[3], item[4], item[5]), tags=('evenrow',))
            else:
              userTree.insert(parent='', index='end', iid=count, text='', values=(item[0], item[1], item[2], item[3], item[4], item[5]), tags=('oddrow',)) 
            count += 1
          c.close()
          conn.close()

      def refresh():
        clearBoxes()
        userTree.delete(*userTree.get_children())
        readDatabase()

      dataGrid = ttk.Labelframe(window, borderwidth=0)
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

      buttonGrid = ttk.Labelframe(window, borderwidth=0)
      buttonGrid.pack()
      addRecordButton = ttk.Button(buttonGrid, text="Add", command=addRecord, cursor="hand2", style='danger.TButton')
      addRecordButton.grid(row=0, column=0, padx=5)
      addRecordButton = ttk.Button(buttonGrid, text="Update", command=updateRecord, cursor="hand2", style='danger.TButton')
      addRecordButton.grid(row=0, column=1, padx=5)
      removeOneButton = ttk.Button(buttonGrid, text="Remove", command=removeFromDatabase, cursor="hand2", style='danger.TButton')
      removeOneButton.grid(row=0, column=2, padx=5)
      clearBoxesButton = ttk.Button(buttonGrid, text="Clear", command=clearBoxes, cursor="hand2", style='danger.TButton')
      clearBoxesButton.grid(row=0, column=3, padx=5)
      refreshButton = ttk.Button(buttonGrid, text="Refresh", command=refresh, cursor="hand2", style='danger.TButton')
      refreshButton.grid(row=0, column=4, padx=5)

      filterGrid = ttk.Labelframe(window, borderwidth=0)
      filterGrid.pack()
      filterEntry = Entry(filterGrid, borderwidth=2)
      filterEntry.grid(row=0, column=0, padx=10, pady=10)
      clearBoxesButton = ttk.Button(filterGrid, text="Filter", command=filterDatabase, cursor="hand2", style='danger.TButton')
      clearBoxesButton.grid(row=0, column=1, padx=5)


      warningGrid = ttk.Labelframe(window, borderwidth=0)
      warningGrid.pack(pady=5)

      # Pri uvolneni tlacidla 1 na mysi sa vykona funkcia select_record a zvoli sa dany zaznam
      userTree.bind("<ButtonRelease-1>", selectRecord)

      readDatabase()

  def viewBooks(self, window):
      for widget in window.winfo_children():
          widget.destroy()

      DB_HOST = "localhost"
      DB_NAME = "librarydb"
      DB_USER = "postgres"
      DB_PASS = "postgres"
      
      windowAppearance = Window()
      windowAppearance.centerWindow(window, 900, 600)

      def openWebsite():
        webbrowser.open_new("https://www.youtube.com/watch?v=2Q_ZzBGPdqE")

      db = DatabaseWindow()
      menu = Menu(window)
      window.config(menu=menu)

      subMenu = Menu(menu)
      menu.add_cascade(label="Window", menu=subMenu)
      subMenu.add_command(label="User Info", background="white", foreground="black", command=lambda:db.viewUsers(window))
      subMenu.add_command(label="SQL Injection", background="white", foreground="black", command=lambda:db.sqlInjection(window))

      helpMenu = Menu(menu)
      menu.add_cascade(label="Help", menu=helpMenu)
      helpMenu.add_command(label="Alexa, play The Beatles - Help!", command=openWebsite, background="white", foreground="black")
  

      # Set Treeview style
      style = Style('superhero')
      style.configure("Treeview", rowheight=30)

      # Vytvorenie treeview frame-u
      treeFrame = Frame(window)
      treeFrame.pack(pady=10)

      # Vytvorenie scrollbaru
      treeFrame = ttk.Scrollbar(treeFrame)
      treeFrame.pack(side=RIGHT, fill=Y)

      # Vytvorenie treeview
      bookTree = ttk.Treeview(treeFrame, yscrollcommand=treeFrame.set, selectmode="extended")
      bookTree.pack()

      # Konfiguracia scrollbaru
      treeFrame.config(command=bookTree.yview)

      # Definovanie stlpcov
      bookTree['columns'] = ("ID", "Name", "First Name", "Last Name", "Genre", "Year", "ISBN")

      # Formatovanie stlpcov
      bookTree.column("#0", width=0, stretch = NO)
      bookTree.column("ID", anchor=W, width=70)
      bookTree.column("Name", anchor=W, width=160)
      bookTree.column("First Name", anchor=W, width=120)
      bookTree.column("Last Name", anchor=W, width=140)
      bookTree.column("Genre", anchor=W, width=140)
      bookTree.column("Year", anchor=W, width=70)
      bookTree.column("ISBN", anchor=W, width=140)

      # Vytvorenie nadpisov
      bookTree.heading("#0", text="", anchor=W)
      bookTree.heading("ID", text="ID", anchor=W)
      bookTree.heading("Name", text="Name", anchor=W)
      bookTree.heading("First Name", text="First Name", anchor=W)
      bookTree.heading("Last Name", text="Last Name", anchor=W)
      bookTree.heading("Genre", text="Genre", anchor=W)
      bookTree.heading("Year", text="Year", anchor=W)
      bookTree.heading("ISBN", text="ISBN", anchor=W)

      # Vytvorenie pruhovanych riadkov na zaklade toho ci su liche alebo sude
      bookTree.tag_configure('oddrow', background="#2b3e50")
      bookTree.tag_configure('evenrow', background="#111d29")

      def readDatabase():
          conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
          c = conn.cursor()

          c.execute("""SELECT b.book_id,
                              b.name,
                              a.first_name,
                              a.last_name,
                              b.genre,
                              b.year,
                              b.isbn
                          FROM public.book_info b
                          JOIN public.author_has_book ahb ON b.book_id = ahb.book_id
                          JOIN public.author a ON ahb.author_id = a.author_id
                          ORDER BY b.book_id ASC""")
          conn.commit()
          records = c.fetchall()
          global count
          count = 0
          for record in records:
            if count % 2 == 0:
              bookTree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('evenrow',))
            else:
              bookTree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('oddrow',)) 
            count += 1
          c.close()
          conn.close()

      def clearBoxes(): # Funkcia na vycistenie entry boxov, tuto funkciu volame ked cosi pridame alebo zmazeme
        idEntry.delete(0, END)
        nameEntry.delete(0, END)
        firstNameEntry.delete(0, END)
        lastNameEntry.delete(0, END)
        genreEntry.delete(0, END)
        yearEntry.delete(0, END)
        isbnEntry.delete(0, END)

      def selectRecord(e): # Funkcia na vyplnenie entry boxov ked zvolime zaznam (klikneme na neho)
          clearBoxes()

          # Zvolenie kliknuteho zaznamu
          selected = bookTree.focus()
          # Ziskanie obsahu zaznamu
          values = bookTree.item(selected, 'values')

          # Vpisanie dat do entry boxov
          try:
            idEntry.insert(0, values[0])
            nameEntry.insert(0, values[1])
            firstNameEntry.insert(0, values[2])
            lastNameEntry.insert(0, values[3]) 
            genreEntry.insert(0, values[4])
            yearEntry.insert(0, values[5])
            isbnEntry.insert(0, values[6])
          except: # Ked klikame mimo, nevyhadzuje nam to error, ale napise do konzole "Click."
            print("Click.")

      def removeFromDatabase(): # Funkcia na zmazanie zaznamu
          try: # Vymazanie na zaklade id ktore ziskame z pola, ked zvolime nejaky riadok
            x = bookTree.selection()[0]
            bookTree.delete(x)
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            c = conn.cursor()
            c.execute("""DELETE FROM public.author_has_book WHERE author_id = %s;""", (idEntry.get(),))
            c.execute("""DELETE FROM public.author WHERE author_id = %s;""", (idEntry.get(),))
            c.execute("""DELETE FROM public.book_info WHERE book_id = %s;""", (idEntry.get(),))
            conn.commit()
            clearBoxes()
            #conn.close()		
          except IndexError:  
            warningLabel = ttk.Label(warningGrid, text="          Nothing selected          ")
            conn.rollback()
            logging.warning('IndexError: Nothing Selected.')
            warningLabel.grid(row=0, column=0)

      def addRecord():
        bookTree.delete(*bookTree.get_children())
        readDatabase()

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        c = conn.cursor()

        try:
          c.execute("""INSERT INTO public.author (author_id, first_name, last_name) VALUES (%s, %s, %s);""", (idEntry.get(), firstNameEntry.get(), lastNameEntry.get(),))
          c.execute("""INSERT INTO public.book_info (book_id, name, genre, year, isbn) 
                      VALUES (%s, %s, %s, %s, %s)""", (idEntry.get(), nameEntry.get(), genreEntry.get(), yearEntry.get(), isbnEntry.get(),))
          c.execute("""INSERT INTO public.author_has_book (author_id, book_id) VALUES (%s, %s);""", (idEntry.get(), idEntry.get(),))
        except psycopg2.errors.UniqueViolation:
          conn.rollback()
          logging.warning('psycopg2.errors.UniqueViolation: Error Adding Record (Duplicate)')
          duplicateError = ttk.Label(warningGrid, text="      Duplicate ID      ").grid(row=0, column=0)
        except psycopg2.errors.InvalidTextRepresentation:
          conn.rollback()
          logging.warning('psycopg2.errors.InvalidTextRepresentation: Invalid Datatype')
          invalidDatatypeError = ttk.Label(warningGrid, text="      Invalid Datatype      ").grid(row=0, column=0)
        except psycopg2.errors.ForeignKeyViolation:
          conn.rollback()
          logging.warning('psycopg2.errors.ForeignKeyViolation')
          foreignKeyError = ttk.Label(warningGrid, text="      Foreign Key Violation      ").grid(row=0, column=0)

        conn.commit()
        clearBoxes()
        conn.close()

        bookTree.delete(*bookTree.get_children())
        readDatabase()


      dataGrid = ttk.Labelframe(window, borderwidth=0)
      dataGrid.pack(pady=10)

      #data_frame.pack(fill="x", expand="yes", padx=20)

      idLabel = Label(dataGrid, text="ID")
      idLabel.grid(row=0, column=0, padx=10, pady=10)
      idEntry = Entry(dataGrid, borderwidth=2)
      idEntry.grid(row=0, column=1, padx=10, pady=10)

      nameLabel = Label(dataGrid, text="Name")
      nameLabel.grid(row=0, column=2, padx=10, pady=10)
      nameEntry = Entry(dataGrid, borderwidth=2)
      nameEntry.grid(row=0, column=3, padx=10, pady=10)

      firstNameLabel = Label(dataGrid, text="First Name")
      firstNameLabel.grid(row=0, column=4, padx=10, pady=10)
      firstNameEntry = Entry(dataGrid, borderwidth=2)
      firstNameEntry.grid(row=0, column=5, padx=10, pady=10)

      lastNameLabel = Label(dataGrid, text="Last Name")
      lastNameLabel.grid(row=1, column=0, padx=10, pady=10)
      lastNameEntry = Entry(dataGrid, borderwidth=2)
      lastNameEntry.grid(row=1, column=1, padx=10, pady=10)

      genreLabel = Label(dataGrid, text="Genre")
      genreLabel.grid(row=1, column=2, padx=10, pady=10)
      genreEntry = Entry(dataGrid, borderwidth=2)
      genreEntry.grid(row=1, column=3, padx=10, pady=10)

      yearLabel = Label(dataGrid, text="Year")
      yearLabel.grid(row=1, column=4, padx=10, pady=10)
      yearEntry = Entry(dataGrid, borderwidth=2)
      yearEntry.grid(row=1, column=5, padx=10, pady=10)

      isbnLabel = Label(dataGrid, text="ISBN")
      isbnLabel.grid(row=2, column=2, padx=10, pady=10)
      isbnEntry = Entry(dataGrid, borderwidth=2)
      isbnEntry.grid(row=2, column=3, padx=10, pady=10)

      buttonGrid = ttk.Labelframe(window, borderwidth=0)
      buttonGrid.pack()
      addRecordButton = ttk.Button(buttonGrid, text="Add", command=addRecord, cursor="hand2", style='danger.TButton')
      addRecordButton.grid(row=0, column=0, padx=5)
      removeOneButton = ttk.Button(buttonGrid, text="Remove", command=removeFromDatabase, cursor="hand2", style='danger.TButton')
      removeOneButton.grid(row=0, column=1, padx=5)
      clearBoxesButton = ttk.Button(buttonGrid, text="Clear", command=clearBoxes, cursor="hand2", style='danger.TButton')
      clearBoxesButton.grid(row=0, column=2, padx=5)

      warningGrid = ttk.Labelframe(window, borderwidth=0)
      warningGrid.pack(pady=5)

      # Pri uvolneni tlacidla 1 na mysi sa vykona funkcia select_record a zvoli sa dany zaznam
      bookTree.bind("<ButtonRelease-1>", selectRecord)

      readDatabase()          

  def sqlInjection(self, window):
      for widget in window.winfo_children():
          widget.destroy()

      DB_HOST = "localhost"
      DB_NAME = "librarydb"
      DB_USER = "postgres"
      DB_PASS = "postgres"

      windowAppearance = Window()
      windowAppearance.centerWindow(window, 700, 700)

      def openWebsite():
        webbrowser.open_new("https://www.youtube.com/watch?v=2Q_ZzBGPdqE")

      def openHelp():
        helpWindow = Help()
        helpWindow.displayHelpSQL(window)

      db = DatabaseWindow()
      menu = Menu(window)
      window.config(menu=menu)

      subMenu = Menu(menu)
      menu.add_cascade(label="Window", menu=subMenu)
      subMenu.add_command(label="User Info", background="white", foreground="black", command=lambda:db.viewUsers(window))
      subMenu.add_command(label="Book Info", background="white", foreground="black", command=lambda:db.viewBooks(window))

      helpMenu = Menu(menu)
      menu.add_cascade(label="Help", menu=helpMenu)
      helpMenu.add_command(label="Alexa, play The Beatles - Help!", command=openWebsite, background="white", foreground="black")
      helpMenu.add_command(label="Actual Help", command=openHelp, background="white", foreground="black")

      """def injectTable():
        try:
          conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
          c = conn.cursor()
          c.execute("SELECT nickname FROM public.sqlinjectiontable1 WHERE first_name = '" + sqlEntry.get() + "';")
          conn.commit()
          find = c.fetchall()
          result = find[0][0]
          c.close()
          conn.close()
          infoLabel4 = ttk.Label(warningGrid, text="                     " + result+  "                      ")
          infoLabel4.grid(row=0, column=0)
        except IndexError:
          conn.rollback()
          logging.warning('IndexError: User Not Found.')
        except psycopg2.ProgrammingError:
          conn.rollback()
          infoLabel3 = ttk.Label(warningGrid, text="Table sqlinjectiontable1 has been removed/doesn't exist.")
          infoLabel3.grid(row=0, column=0)
        except psycopg2.errors.UndefinedTable:
          conn.rollback()
          infoLabel3 = ttk.Label(warningGrid, text="Table sqlinjectiontable1 has been removed/doesn't exist.")
          infoLabel3.grid(row=0, column=0)"""
      
      def createInjectionTable():
          try:
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            c = conn.cursor()
            c.execute("""CREATE TABLE public.sqlinjectiontable1(user_id INT PRIMARY KEY      NOT NULL,
                                                                first_name          CHAR(50) NOT NULL,
                                                                nickname            char(50) NOT NULL
                                                                );""")
            c.execute("INSERT INTO public.sqlInjectiontable1 (user_id, first_name, nickname) VALUES (1, 'Robert', 'Bob');")
            c.execute("INSERT INTO public.sqlInjectiontable1 (user_id, first_name, nickname) VALUES (2, 'Peter', 'Pete');")
            c.execute("INSERT INTO public.sqlInjectiontable1 (user_id, first_name, nickname) VALUES (3, 'Michael', 'Mike');")
            c.execute("INSERT INTO public.sqlInjectiontable1 (user_id, first_name, nickname) VALUES (4, 'Daniel', 'Dan');")
            conn.commit()
            c.close()
            conn.close()
            exceptionLabel = ttk.Label(warningGrid, text="                                                              ").grid(row=0, column=0)
          except psycopg2.errors.DuplicateTable:
            conn.rollback()
            logging.warning('psycopg2.errors.DuplicateTable: relation already exists.')

      def readDatabase(entry):
        try:
          sqlTree.delete(*sqlTree.get_children())
          conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
          c = conn.cursor()

          c.execute("SELECT * FROM public.sqlinjectiontable1 WHERE first_name = '" + entry + "';")
          conn.commit()
          records = c.fetchall()
          global count
          count = 0
          for record in records:
            if count % 2 == 0:
              sqlTree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('evenrow',))
            else:
              sqlTree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('oddrow',)) 
            count += 1
          c.close()
          conn.close()
        except psycopg2.ProgrammingError:
          logging.warning("psycopg2.ProgrammingError: no results to fetch")
          exceptionLabel = ttk.Label(warningGrid, text="No results to fetch. (Table deleted)").grid(row=0, column=0)
        except IndexError:
          conn.rollback()
          logging.warning('IndexError: User Not Found.')
        except psycopg2.ProgrammingError:
          conn.rollback()
          logging.warning("psycopg2.ProgrammingError: Table sqlinjectiontable1 has been removed/doesn't exist.")
          exceptionLabel = ttk.Label(warningGrid, text="Table sqlinjectiontable1 has been removed/doesn't exist.").grid(row=0, column=0)
        except psycopg2.errors.UndefinedTable:
          conn.rollback()
          logging.warning("psycopg2.errors.UndefinedTable: Table sqlinjectiontable1 has been removed/doesn't exist.")
          exceptionLabel = ttk.Label(warningGrid, text="Table sqlinjectiontable1 has been removed/doesn't exist.").grid(row=0, column=0)

      # Entry box intended to search the database
      sqlEntry2 = ttk.Entry(window, width=60)
      sqlEntry2.pack(pady=10)
      # Button to search
      searchButton1 = ttk.Button(window, text="Search", style='danger.TButton', command=lambda:readDatabase(sqlEntry2.get()), cursor="hand2").pack(pady=10)

      # Drop Table Attack
      infoLabel2 = ttk.Label(window, text="This is a DROP TABLE method.").pack()
      # Entry box intended to inject the database with a drop table command
      sqlEntry = ttk.Entry(window, width=60)
      sqlEntry.insert(0, "';DROP TABLE public.sqlinjectiontable1;--")
      sqlEntry.pack(pady=10)
      # Button to execute the command
      searchButton = ttk.Button(window, text="Search", style='danger.TButton', command=lambda:readDatabase(sqlEntry.get()), cursor="hand2").pack(pady=10)

      # 1 = 1 Attack
      infoLabel2 = ttk.Label(window, text="This is a 1=1 method.").pack()
      # Entry box intended to inject the database by retrieving more data than expected
      sqlEntry1 = ttk.Entry(window, width=60)
      sqlEntry1.insert(0, "' OR 1=1;--")
      sqlEntry1.pack(pady=10)
      # Button to execute the command
      searchButton2 = ttk.Button(window, text="Search", style='danger.TButton', command=lambda:readDatabase(sqlEntry1.get()), cursor="hand2").pack(pady=10)
      # Button to create the dummy table again
      createTableButton = ttk.Button(window, text="Create sqlinjectiontable1", style='danger.TButton', command=createInjectionTable, cursor="hand2").pack(pady=5)
      
      # Setting the style of our treeview
      style = Style('superhero')
      style.configure("Treeview", rowheight=20)

      # Creating treeview frame
      treeFrame = Frame(window)
      treeFrame.pack(pady=10)

      # Creating the scrollbar
      scroll = ttk.Scrollbar(treeFrame)
      scroll.pack(side=RIGHT, fill=Y)

      # Creating the treeview
      sqlTree = ttk.Treeview(treeFrame, yscrollcommand=scroll.set, selectmode="extended")
      sqlTree.pack()

      # Configuration of our scrollbar
      scroll.config(command=sqlTree.yview)

      # Defining our columns
      sqlTree['columns'] = ("ID", "First Name", "Nickname")

      # Formatting our columns 
      sqlTree.column("#0", width=0, stretch = NO)
      sqlTree.column("ID", anchor=W, width=70)
      sqlTree.column("First Name", anchor=W, width=140)
      sqlTree.column("Nickname", anchor=W, width=140)

      # Creating headings with the names of our columns
      sqlTree.heading("#0", text="", anchor=W)
      sqlTree.heading("ID", text="ID", anchor=W)
      sqlTree.heading("First Name", text="First Name", anchor=W)
      sqlTree.heading("Nickname", text="Nickname", anchor=W)

      # Diferentiating between an odd row and even row with different colors
      sqlTree.tag_configure('oddrow', background="#2b3e50")
      sqlTree.tag_configure('evenrow', background="#111d29")

      # Grid for warning messages
      warningGrid = ttk.LabelFrame(window, borderwidth=0)
      warningGrid.pack()