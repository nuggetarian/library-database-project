from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style
import psycopg2
from windows.helpwindow import Help
from windows.window import Window
import webbrowser
import logging
from windows.bookwindow import BookWindow
from windows.sqlwindow import SqlWindow

class DatabaseWindow():
  # Setting up loggers filename, append mode and format
  logging.basicConfig(filename="logfile.log",
                      filemode='a',
                      format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# Window to view, add, delete, update, filter users
  def viewUsers(self, window):
      # Destroying widgets to have a blank window 
      for widget in window.winfo_children():
          widget.destroy()

      # Constants used to connect to database
      DB_HOST = "localhost"
      DB_NAME = "librarydb"
      DB_USER = "postgres"
      DB_PASS = "postgres"

      # Setting up window resolution
      windowAppearance = Window()
      windowAppearance.centerWindow(window, 850, 700)

      # Function to open a relevant song
      def openWebsite():
        webbrowser.open_new("https://www.youtube.com/watch?v=2Q_ZzBGPdqE")
      
      # Function to open help window
      def openHelp():
        helpWindow = Help()
        helpWindow.displayHelp(window)

      db = DatabaseWindow()
      bw = BookWindow()
      sqlw = SqlWindow()
      menu = Menu(window)
      window.config(menu=menu)

      # Toolbar to switch windows
      subMenu = Menu(menu)
      menu.add_cascade(label="Window", menu=subMenu)
      subMenu.add_command(label="Book Info", background="white", foreground="black", command=lambda:bw.viewBooks(window))
      subMenu.add_command(label="SQL Injection", background="white", foreground="black", command=lambda:sqlw.sqlInjection(window))

      # Toolbar to open help
      helpMenu = Menu(menu)
      menu.add_cascade(label="Help", menu=helpMenu)
      helpMenu.add_command(label="Alexa, play The Beatles - Help!", command=openWebsite, background="white", foreground="black")
      helpMenu.add_command(label="Actual Help", command=openHelp, background="white", foreground="black")

      # Setting the style of our treeview
      style = Style('superhero')
      style.configure("Treeview", rowheight=30)

      # Creating the frame of our treeview
      treeFrame = Frame(window)
      treeFrame.pack(pady=10)

      # Creating a scrollbar
      scroll = ttk.Scrollbar(treeFrame)
      scroll.pack(side=RIGHT, fill=Y)

      # Creation of our treeview
      userTree = ttk.Treeview(treeFrame, yscrollcommand=scroll.set, selectmode="extended")
      userTree.pack()

      # Config of our scrollbar
      scroll.config(command=userTree.yview)

      # Naming our columns
      userTree['columns'] = ("ID", "First Name", "Last Name", "Mail", "City", "Role")

      # Setting up our columns
      userTree.column("#0", width=0, stretch = NO)
      userTree.column("ID", anchor=W, width=70)
      userTree.column("First Name", anchor=W, width=140)
      userTree.column("Last Name", anchor=W, width=140)
      userTree.column("Mail", anchor=W, width=140)
      userTree.column("City", anchor=W, width=140)
      userTree.column("Role", anchor=W, width=140)

      # Creating the names of our headings
      userTree.heading("#0", text="", anchor=W)
      userTree.heading("ID", text="ID", anchor=W)
      userTree.heading("First Name", text="First Name", anchor=W)
      userTree.heading("Last Name", text="Last Name", anchor=W)
      userTree.heading("Mail", text="Mail", anchor=W)
      userTree.heading("City", text="City", anchor=W)
      userTree.heading("Role", text="Role", anchor=W)

      # Changing the color of a row depending on the evenness of results
      userTree.tag_configure('oddrow', background="#2b3e50")
      userTree.tag_configure('evenrow', background="#111d29")

      # Function to read our database
      def readDatabase():
          # Using our constants to connect and creating a cursor
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
          # For loop to differentiate odd rows and even rows based on tags 'oddrow' and 'evenrow'
          for record in records:
            if count % 2 == 0:
              userTree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))
            else:
              userTree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',)) 
            count += 1
          # Closing our cursor and connection
          c.close()
          conn.close()

      def clearBoxes(): # Function to clear entry boxes
        idEntry.delete(0, END)
        firstNameEntry.delete(0, END)
        lastNameEntry.delete(0, END)
        mailEntry.delete(0, END)
        cityEntry.delete(0, END)
        roleEntry.delete(0, END)
        filterEntry.delete(0, END)

      def selectRecord(e): # Function to fill entry boxes with data when a record is selected (clicked)
          clearBoxes()

          global roleset
          # Focusing on an item
          selected = userTree.focus()
          # Getting values
          values = userTree.item(selected, 'values')

          # Filling the entry boxes
          try:
            idEntry.insert(0, values[0])
            firstNameEntry.insert(0, values[1])
            lastNameEntry.insert(0, values[2]) 
            mailEntry.insert(0, values[3])
            cityEntry.insert(0, values[4])
            roleEntry.insert(0, values[5])

            # If statement for assigning role a number
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
          except: # If we click somewhere without an item, "Click." get printed - this exception doesn't interfere with the funcionality of the program
            print("Click.")

      def removeFromDatabase(): # Function to delete a record
          try: # Deletion based on an ID that we got from an entry box 
            x = userTree.selection()[0] # Selecting an item in the treeview
            userTree.delete(x) # Deleting it from the screen
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            c = conn.cursor()
            c.execute("""DELETE FROM public.user_has_address WHERE user_id = %s""", (idEntry.get(),))
            c.execute("""DELETE FROM public.user_has_role WHERE user_id = %s""", (idEntry.get(),))
            c.execute("""DELETE FROM public.contact WHERE user_id = %s""", (idEntry.get(),))
            c.execute("""DELETE FROM public.user WHERE user_id = %s""", (idEntry.get(),))
            conn.commit()
            clearBoxes()
            conn.close()
            c.close()
          #	Exception if we press delete without selecting, also contains a transaction rollback, log entry and a message is displayed on the screen
          except IndexError:  
            warningLabel = ttk.Label(warningGrid, text="          Nothing selected          ")
            conn.rollback()
            logging.warning('IndexError: Nothing Selected.')
            warningLabel.grid(row=0, column=0)

      # Function to add a record
      def addRecord():
        # Roles get a number assigned for easier manipulation of data
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
        
        # Cities get a number assigned for easier manipulation of data
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
          conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
          c = conn.cursor()
          c.execute("""INSERT INTO public.user (user_id, first_name, last_name) VALUES (%s, %s, %s);""", 
                    (idEntry.get(), firstNameEntry.get(), lastNameEntry.get(),))
          c.execute("""INSERT INTO public.contact (user_id, mail) VALUES (%s, %s);""",
                    (idEntry.get(), mailEntry.get(),))
          c.execute("""INSERT INTO public.user_has_role (user_id, role_id) VALUES (%s, %s);""",
                    (idEntry.get(), role,))
          c.execute("""INSERT INTO public.user_has_address (user_id, address_id) VALUES (%s, %s);""",
                    (idEntry.get(), city,))
          conn.commit()
          conn.close()
          c.close()
        # Exceptions that are logged, transaction rollback is applied and a relevant message is displayed
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
        clearBoxes()
        conn.close()
        # Refresh of the treeview
        userTree.delete(*userTree.get_children())
        readDatabase()

      # Function to update a record we select
      def updateRecord():
        # Cities get a number assigned for easier manipulation of data
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

        # Roles get a number assigned for easier manipulation of data
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
          conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
          c = conn.cursor()
          c.execute("""UPDATE public.user SET last_name = %s, first_name = %s WHERE user_id = %s;""", (lastNameEntry.get(),firstNameEntry.get(),idEntry.get(),))
          c.execute("""UPDATE public.contact SET mail = %s WHERE user_id = %s;""", (mailEntry.get(),idEntry.get(),))
          c.execute("""UPDATE public.user_has_address SET address_id = %s WHERE user_id = %s;""", (city,idEntry.get(),))
          c.execute("""UPDATE public.user_has_role SET role_id = %s WHERE user_id = %s AND role_id = %s;""", (role,idEntry.get(),roleset,))
          conn.commit()
          c.close()
          conn.close()
        # Exceptions that are logged, transaction rollback is applied and a relevant message is displayed
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
        clearBoxes()
        # Refresh of the screen
        userTree.delete(*userTree.get_children())
        readDatabase()          

      def filterDatabase():
          # We delete all the elements from treeview to make some space for our new filtered list
          userTree.delete(*userTree.get_children())
          conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
          c = conn.cursor()
          # We filter basically every string in our joined select
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
          # Same function as before to differentiate odd rows and even rows based on tags
          for item in filtered:
            if count % 2 == 0:
              userTree.insert(parent='', index='end', iid=count, text='', values=(item[0], item[1], item[2], item[3], item[4], item[5]), tags=('evenrow',))
            else:
              userTree.insert(parent='', index='end', iid=count, text='', values=(item[0], item[1], item[2], item[3], item[4], item[5]), tags=('oddrow',)) 
            count += 1
          c.close()
          conn.close()

      # A refresh function, deletes all items and re-reads the database
      def refresh():
        clearBoxes()
        userTree.delete(*userTree.get_children())
        readDatabase()

      # Grid to easily display Labels and their respective Entry boxes
      dataGrid = ttk.Labelframe(window, borderwidth=0)
      dataGrid.pack(pady=10)

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

      # A grid to display warnings in the same place on the screen
      warningGrid = ttk.Labelframe(window, borderwidth=0)
      warningGrid.pack(pady=5)

      # When mouse button 1 is released, selectRecord function happens
      userTree.bind("<ButtonRelease-1>", selectRecord)

      readDatabase()