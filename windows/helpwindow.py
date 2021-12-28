from tkinter import *
from tkinter import ttk
from windows.window import Window

class Help():
  # Help window on in the 'User Info' window
  def displayHelp(self, window):
    windowAppearance = Window()

    # Opening a new window on top of our main window, setting the resolution and title
    popUp = Toplevel(window)
    windowAppearance.centerWindow(popUp, 250, 250)
    popUp.title("Help")
    # All the text labels are packed below each other
    infoLabel = ttk.Label(popUp, text="When adding a person: ", font='bold').pack(anchor=CENTER, pady=15)
    cityInfoLabel = ttk.Label(popUp, text="  • City must be in database:").pack(anchor="nw")
    cityInfoLabel2 = ttk.Label(popUp, text="      • Jonesboro").pack(anchor="nw")
    cityInfoLabel2 = ttk.Label(popUp, text="      • Seattle").pack(anchor="nw")
    cityInfoLabel2 = ttk.Label(popUp, text="      • Providence").pack(anchor="nw")
    cityInfoLabel2 = ttk.Label(popUp, text="      • Canton").pack(anchor="nw")
    cityInfoLabel2 = ttk.Label(popUp, text="      • Wellesley").pack(anchor="nw")
    idInfoLabel = ttk.Label(popUp, text="  • ID must be unique").pack(anchor="nw", pady=10)
  
  # Help window on in the 'SQL Injection' window
  def displayHelpSQL(self, window):
    windowAppearance = Window()
    # Opening a new window on top of our main window, setting the resolution and title
    popUp = Toplevel(window)
    windowAppearance.centerWindow(popUp, 600, 300)
    popUp.title("Help")
    # All the text labels are packed below each other
    infoLabel = ttk.Label(popUp, text="Drop table method: ", font='bold').pack(anchor=CENTER, pady=15)
    infoLabel1 = ttk.Label(popUp, text="  • First search bar is used to find users in sqlinjectiontable1").pack(anchor="nw")
    infoLabel2 = ttk.Label(popUp, text="  • Try searching 'Robert'").pack(anchor="nw")
    infoLabel3 = ttk.Label(popUp, text="  • Press 'Search' button in the second search bar to try the preloaded SQL Injection").pack(anchor="nw")
    infoLabel4 = ttk.Label(popUp, text="  • Try searching 'Robert' again").pack(anchor="nw")
    infoLabel5 = ttk.Label(popUp, text="  • If you wish to repeat the process, press 'Create sqlinjectiontable1' to create the table again").pack(anchor="nw")
    infoLabel6 = ttk.Label(popUp, text="  • You can verify the deletion by checking pgAdmin 4").pack(anchor="nw")
    # A button to move to the next help page
    nextButton = ttk.Button(popUp, text="Next", style='danger.TButton', command=lambda:Help.displayHelpSQL11(Help, popUp), cursor="hand2").pack(pady=10)

  # Next help window on in the 'SQL Injection' window
  def displayHelpSQL11(self, popUp):
    windowAppearance = Window()
    # Deleting everything from the pop up window because we moved to a next window
    for widget in popUp.winfo_children():
          widget.destroy()
    # Setting the resolution and title
    windowAppearance.centerWindow(popUp, 600, 300)
    popUp.title("Help")
    # All the text labels are packed below each other
    infoLabel = ttk.Label(popUp, text="Retrieving more data than expected (1=1): ", font='bold').pack(anchor=CENTER, pady=15)
    infoLabel1 = ttk.Label(popUp, text="  • We insert ' OR 1=1;-- into the search bar ").pack(anchor="nw")
    infoLabel2 = ttk.Label(popUp, text="  • 1=1 is always true, so the query will return all items ").pack(anchor="nw")
    # A button to move to the next help page
    nextButton = ttk.Button(popUp, text="Next", style='danger.TButton', command=lambda:Help.importanceOfPS(Help, popUp), cursor="hand2").pack(pady=10)


  def importanceOfPS(self, popUp):
    windowAppearance = Window()
    # Deleting everything from the pop up window because we moved to a next window
    for widget in popUp.winfo_children():
          widget.destroy()
    # Setting the resolution and title
    windowAppearance.centerWindow(popUp, 600, 300)
    popUp.title("Help")
    # All the text labels are packed below each other
    infoLabel = ttk.Label(popUp, text="The importance of Prepared Statements: ", font='bold').pack(anchor=CENTER, pady=15)
    infoLabel1 = ttk.Label(popUp, text="""      This particural window doesn't use 'Prepared Statements'. 
      That means any user can execute any SQL query they please by typing a special string into the search bar.
      Alwasys use 'Prepared Statements' to prevent that. 
      See 'Help' on how to use this window for learning purposes.""").pack(anchor=CENTER)