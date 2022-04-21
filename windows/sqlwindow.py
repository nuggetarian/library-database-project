from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style
import psycopg2
from windows.window import Window
import logging

# Class with SQL Injection playground
class SqlWindow():
  def sqlInjection(self, window):

      # Constants used to connect to database
      DB_HOST = "localhost"
      DB_NAME = "librarydb"
      DB_USER = "postgres"
      DB_PASS = "postgres"

      # Setting up window resolution
      windowAppearance = Window()
      
      # Opening a new window on top of our main window, setting the resolution and title
      popUp = Toplevel(window)
      windowAppearance.centerWindow(popUp, 700, 700)
      
      # Function to create sqlinjectiontable1
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
            # Label to clear the place where error messages are displayed
            exceptionLabel = ttk.Label(warningGrid, text="                                                                                 ").grid(row=0, column=0)
          # Exception that is logged, transaction rollback is applied and a message is displayed
          except psycopg2.errors.DuplicateTable:
            conn.rollback()
            logging.warning('psycopg2.errors.DuplicateTable: relation already exists.')

      # Reads the database to get our dummy table
      def readDatabase(entry):
        try:
          # Label to clear the place where error messages are displayed
          exceptionLabel = ttk.Label(warningGrid, text="                                                                                 ").grid(row=0, column=0)
          sqlTree.delete(*sqlTree.get_children()) # Clears the display
          conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
          c = conn.cursor()
          c.execute("SELECT * FROM public.sqlinjectiontable1 WHERE first_name = '" + entry + "';")
          conn.commit()
          records = c.fetchall()
          global count
          count = 0
          # Inserting fetched items into the treeview, based on even row and odd row
          for record in records:
            if count % 2 == 0:
              sqlTree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('evenrow',))
            else:
              sqlTree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('oddrow',)) 
            count += 1
          c.close()
          conn.close()
        # Exceptions that are logged, transaction rollback is applied and a message is displayed
        except psycopg2.ProgrammingError:
          conn.rollback()
          logging.warning("psycopg2.ProgrammingError: no results to fetch")
          exceptionLabel = ttk.Label(warningGrid, text="No results to fetch. (Table deleted)").grid(row=0, column=0)
        except IndexError:
          conn.rollback()
          logging.warning('IndexError: User Not Found.')
          exceptionLabel = ttk.Label(warningGrid, text="IndexError: User Not Found.").grid(row=0, column=0)
        except psycopg2.ProgrammingError:
          conn.rollback()
          logging.warning("psycopg2.ProgrammingError: Table sqlinjectiontable1 has been removed/doesn't exist.")
          exceptionLabel = ttk.Label(warningGrid, text="Table sqlinjectiontable1 has been removed/doesn't exist.").grid(row=0, column=0)
        except psycopg2.errors.UndefinedTable:
          conn.rollback()
          logging.warning("psycopg2.errors.UndefinedTable: Table sqlinjectiontable1 has been removed/doesn't exist.")
          exceptionLabel = ttk.Label(warningGrid, text="Table sqlinjectiontable1 has been removed/doesn't exist.").grid(row=0, column=0)

      # Entry box intended to search the database
      sqlEntry2 = ttk.Entry(popUp, width=60)
      sqlEntry2.pack(pady=10)
      # Button to search
      searchButton1 = ttk.Button(popUp, text="Search", style='danger.TButton', command=lambda:readDatabase(sqlEntry2.get()), cursor="hand2").pack(pady=10)

      # Drop Table Attack
      infoLabel2 = ttk.Label(popUp, text="This is a DROP TABLE method.").pack()
      # Entry box intended to inject the database with a drop table command
      sqlEntry = ttk.Entry(popUp, width=60)
      sqlEntry.insert(0, "';DROP TABLE public.sqlinjectiontable1;--")
      sqlEntry.pack(pady=10)
      # Button to execute the command
      searchButton = ttk.Button(popUp, text="Search", style='danger.TButton', command=lambda:readDatabase(sqlEntry.get()), cursor="hand2").pack(pady=10)

      # 1 = 1 Attack
      infoLabel2 = ttk.Label(popUp, text="This is a 1=1 method.").pack()
      # Entry box intended to inject the database by retrieving more data than expected
      sqlEntry1 = ttk.Entry(popUp, width=60)
      sqlEntry1.insert(0, "' OR 1=1;--")
      sqlEntry1.pack(pady=10)
      # Button to execute the command
      searchButton2 = ttk.Button(popUp, text="Search", style='danger.TButton', command=lambda:readDatabase(sqlEntry1.get()), cursor="hand2").pack(pady=10)
      # Button to create the dummy table again
      createTableButton = ttk.Button(popUp, text="Create sqlinjectiontable1", style='danger.TButton', command=createInjectionTable, cursor="hand2").pack(pady=5)
      
      # Setting the style of our treeview
      style = Style('superhero')
      style.configure("Treeview", rowheight=20)

      # Creating treeview frame
      treeFrame = Frame(popUp)
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
      warningGrid = ttk.LabelFrame(popUp, borderwidth=0)
      warningGrid.pack()