import tkinter

class User:
    def __init__(self, mainWindow):
        logo=tkinter.PhotoImage(file ="back.gif")

        label = tkinter.Label(mainWindow, text="Welcome Muse !\n\nMusic Recommendation Service\n@Web Social Data Mining")
        label.pack()
        label.config(font=('arial',15,'bold'), foreground ='black' , background ='pink')
        label.config(image=logo)
        label.config(compound='left')
        label.grid(row=0, column=0, columnspan=6)

        label = tkinter.Label(mainWindow, text="Select Muse User")
        label.grid(row=1, column=0)
        label = tkinter.Label(mainWindow, text="Listen Music")
        label.grid(row=1, column=2)
