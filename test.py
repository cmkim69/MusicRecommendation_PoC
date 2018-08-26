from tkinter import *
class App:
    def __init__(self,r):
        frame=Frame(r)
        frame.pack()
        self.listbox=Listbox(frame,height=3, selectmode=SINGLE)
        for item in ['red','green','blue','yellow','black']:
            self.listbox.insert(END,item)
        self.listbox.grid(row=0, column=0)
        inButton=Button(frame,text='input',command=self.ins).grid(row=1,column=0)

    def ins(self):
        #items = self.listbox.curselection()
        print(self.listbox.curselection())

root=Tk()
root.wm_title('title')
app=App(root)

print('finish?', app)

root.mainloop()
