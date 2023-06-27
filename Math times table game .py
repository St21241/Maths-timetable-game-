from tkinter import *
import random

root = Tk()
# Creating a Label Widget 
myLabel = Label(root, text=str(random.random()))
# shoving it onto the screen
myLabel.pack()



root.mainloop()