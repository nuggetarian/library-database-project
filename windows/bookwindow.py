from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style
import psycopg2
from windows.window import Window
import logging

# Class to view, add and remove books
class BookWindow():

    def viewBooks(self, window):
    
      windowAppearance = Window()

      # Opening a new window on top of our main window, setting the resolution and title
      popUp = Toplevel(window)
      windowAppearance.centerWindow(popUp, 900, 600)

      # Constants used to connect to database
      DB_HOST = "localhost"
      DB_NAME = "librarydb"
      DB_USER = "postgres"
      DB_PASS = "postgres"
  
      # Setting the style of our treeview
      style = Style('superhero')
      style.configure("Treeview", rowheight=30)

      # Creating treeview frame
      treeFrame = Frame(popUp)
      treeFrame.pack(pady=10)

      # Creating the scrollbar
      treeFrame = ttk.Scrollbar(treeFrame)
      treeFrame.pack(side=RIGHT, fill=Y)

      # Creating the treeview
      bookTree = ttk.Treeview(treeFrame, yscrollcommand=treeFrame.set, selectmode="extended")
      bookTree.pack()

      # Configuration of our scrollbar
      treeFrame.config(command=bookTree.yview)

      # Defining our columns
      bookTree['columns'] = ("ID", "Name", "First Name", "Last Name", "Genre", "Year", "ISBN")

      # Formatting our columns 
      bookTree.column("#0", width=0, stretch = NO)
      bookTree.column("ID", anchor=W, width=70)
      bookTree.column("Name", anchor=W, width=160)
      bookTree.column("First Name", anchor=W, width=120)
      bookTree.column("Last Name", anchor=W, width=140)
      bookTree.column("Genre", anchor=W, width=140)
      bookTree.column("Year", anchor=W, width=70)
      bookTree.column("ISBN", anchor=W, width=140)

      # Creating headings with the names of our columns
      bookTree.heading("#0", text="", anchor=W)
      bookTree.heading("ID", text="ID", anchor=W)
      bookTree.heading("Name", text="Name", anchor=W)
      bookTree.heading("First Name", text="First Name", anchor=W)
      bookTree.heading("Last Name", text="Last Name", anchor=W)
      bookTree.heading("Genre", text="Genre", anchor=W)
      bookTree.heading("Year", text="Year", anchor=W)
      bookTree.heading("ISBN", text="ISBN", anchor=W)

      # Diferentiating between an odd row and even row with different colors
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
          # Inserting fetched items into the treeview, based on even row and odd row
          for record in records:
            if count % 2 == 0:
              bookTree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('evenrow',))
            else:
              bookTree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('oddrow',)) 
            count += 1
          c.close()
          conn.close()

      def clearBoxes(): # Function to clear entry boxes
        idEntry.delete(0, END)
        nameEntry.delete(0, END)
        firstNameEntry.delete(0, END)
        lastNameEntry.delete(0, END)
        genreEntry.delete(0, END)
        yearEntry.delete(0, END)
        isbnEntry.delete(0, END)

      def selectRecord(e): # Function to fill entry boxes with selected item
          clearBoxes()
          # Focus on the selected item and its values
          selected = bookTree.focus()
          values = bookTree.item(selected, 'values')

          # Selected item gets its values written into the entry boxes
          try:
            idEntry.insert(0, values[0])
            nameEntry.insert(0, values[1])
            firstNameEntry.insert(0, values[2])
            lastNameEntry.insert(0, values[3]) 
            genreEntry.insert(0, values[4])
            yearEntry.insert(0, values[5])
            isbnEntry.insert(0, values[6])
          except: # If we click someplace without an item, we get this printed to console - doesn't affect the funcionality of the program
            print("Click.")

      def removeFromDatabase(): # Function to remove records
          try: # Removes the selected item
            x = bookTree.selection()[0]
            bookTree.delete(x)
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            c = conn.cursor()
            c.execute("""DELETE FROM public.author_has_book WHERE author_id = %s;""", (idEntry.get(),))
            c.execute("""DELETE FROM public.author WHERE author_id = %s;""", (idEntry.get(),))
            c.execute("""DELETE FROM public.book_info WHERE book_id = %s;""", (idEntry.get(),))
            conn.commit()
            clearBoxes()
            conn.close()
            c.close()
          # Exception that is logged, transaction rollback is applied and a message is displayed 	
          except IndexError:  
            warningLabel = ttk.Label(warningGrid, text="          Nothing selected          ")
            conn.rollback()
            logging.warning('IndexError: Nothing Selected.')
            warningLabel.grid(row=0, column=0)

      # Function to add a new book
      def addRecord():
        # Deletes all entries to make sure the screen updates when a book is added
        bookTree.delete(*bookTree.get_children())
        readDatabase()
        try:
          # Connection, cursor and queries
          conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
          c = conn.cursor()
          c.execute("""INSERT INTO public.author (author_id, first_name, last_name) VALUES (%s, %s, %s);""", (idEntry.get(), firstNameEntry.get(), lastNameEntry.get(),))
          c.execute("""INSERT INTO public.book_info (book_id, name, genre, year, isbn) 
                      VALUES (%s, %s, %s, %s, %s)""", (idEntry.get(), nameEntry.get(), genreEntry.get(), yearEntry.get(), isbnEntry.get(),))
          c.execute("""INSERT INTO public.author_has_book (author_id, book_id) VALUES (%s, %s);""", (idEntry.get(), idEntry.get(),))
          conn.commit()
          conn.close()
          c.close()
        # Exceptions that are logged, transaction rollback is applied and a message is displayed
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
        # Deletes elements from screen and reads them again
        bookTree.delete(*bookTree.get_children())
        readDatabase()

      # Grid to put every entry box to
      dataGrid = ttk.Labelframe(popUp, borderwidth=0)
      dataGrid.pack(pady=10)

      # Labels and entry boxes to Edit and Add entries, put into the grid
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

      # Buttons used to control the database
      buttonGrid = ttk.Labelframe(popUp, borderwidth=0)
      buttonGrid.pack()
      addRecordButton = ttk.Button(buttonGrid, text="Add", command=addRecord, cursor="hand2", style='danger.TButton')
      addRecordButton.grid(row=0, column=0, padx=5)
      removeOneButton = ttk.Button(buttonGrid, text="Remove", command=removeFromDatabase, cursor="hand2", style='danger.TButton')
      removeOneButton.grid(row=0, column=1, padx=5)
      clearBoxesButton = ttk.Button(buttonGrid, text="Clear", command=clearBoxes, cursor="hand2", style='danger.TButton')
      clearBoxesButton.grid(row=0, column=2, padx=5)

      warningGrid = ttk.Labelframe(popUp, borderwidth=0)
      warningGrid.pack(pady=5)

      # When mouse button 1 is released, selectRecord function happens
      bookTree.bind("<ButtonRelease-1>", selectRecord)

      readDatabase()