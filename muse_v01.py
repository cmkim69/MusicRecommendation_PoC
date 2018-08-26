
import tkinter
from tkinter import ttk
from dataset import UserInfo
import userprofile

class User:
    def __init__(self, mainWindow):

        logo=tkinter.PhotoImage(file ="back.gif")

        label = tkinter.Label(mainWindow, text="Welcome Muse !\n\nMusic Recommendation Service\n@Web Social Data Mining")
#        label.pack()
        label.config(image=logo)
        label.config(font=('arial',15,'bold'), foreground ='black' , background ='pink')
        label.config(compound='left')
        label.grid(row=0, column=0, columnspan=6)

        label = tkinter.Label(mainWindow, text="Select Muse User")
        label.grid(row=1, column=0)
        label = tkinter.Label(mainWindow, text="User Preference")
        label.grid(row=1, column=2)

        mainWindow.columnconfigure(0, weight=4)
        mainWindow.columnconfigure(1, weight=1)
        mainWindow.columnconfigure(2, weight=4)
        mainWindow.columnconfigure(3, weight=1)
        mainWindow.columnconfigure(4, weight=4)
        mainWindow.columnconfigure(5, weight=1)

        mainWindow.rowconfigure(0, weight=1)
        mainWindow.rowconfigure(1, weight=3)
        mainWindow.rowconfigure(2, weight=3)
        mainWindow.rowconfigure(3, weight=1)
        mainWindow.rowconfigure(4, weight=1)

        userlist=tkinter.Listbox(mainWindow, )
        userlist.grid(row=2, column=0, sticky='nsew', rowspan=1)
        userlist.config(border=2, relief='sunken', cursor='heart', selectbackground='pink', selectforeground='black')
#    for zone in open(file='imelda3.txt'):
#            filelist.insert(tkinter.END,zone)
        for loginid, loginname, gender in UserInfo:
            userlist.insert(tkinter.END,'['+loginid+'] : '+loginname)


        listScroll=tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL, command=userlist.yview)
        listScroll.grid(row=2, column=1, sticky='nsw', rowspan=1)
        userlist['yscrollcommand']= listScroll.set

        userButton=tkinter.Button(mainWindow, text='Select User', command=self.selectUser(userlist))
        userButton.grid(row=3, column=0, sticky='new')
#   print(userlist.curselection())

    def selectUser(self, ulist):
        print(ulist.curselection())
        print('test')

root = tkinter.Tk()

notebook=ttk.Notebook(root)
notebook.pack()
mainWindow1=ttk.Frame(notebook)
mainWindow2=ttk.Frame(notebook)
mainWindow3=ttk.Frame(notebook)
notebook.add(mainWindow1, text='User Profile')
notebook.add(mainWindow2, text='Recommend Music')
notebook.add(mainWindow3, text='Music Soulmate')

root.title("Muse")
root.geometry("960x640")
root.configure(background='pink')

User(mainWindow1)

notebook.mainloop()

