class Window():
  
  # Function to center the window by calculating the height and width of users monitor
  def centerWindow(self, window, app_width, app_height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width / 2) - (app_width / 2) 
    y = (screen_height / 2) - (app_height / 2)

    window.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
    window.resizable(False, False)