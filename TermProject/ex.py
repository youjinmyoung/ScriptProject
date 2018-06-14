from tkinter import *

def map():
    window = Tk()
    photo = PhotoImage(file = "map.GIF")
    imageLabel = Label(window, image= photo)
    imageLabel.pack()

    window.mainloop()

map()