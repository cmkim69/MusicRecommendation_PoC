import tkinter
from tkinter import ttk
from dataset import UserInfo, MusicInfo, TopChartMusicInfo, MusicClassification, ContextClassification
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt

UserInfo_index=0
ClassificationValue=1
ContextValue=1
recommend_classification=[]
recommend_context=[]
recommend_artist=[]
recommend_title=[]

def find_UserIndex(userid):
    i=0
    while(UserInfo[i][0]!=userid):
        i+=1
    return i

def compute_sim(source_user, target_user):
    t_user=find_UserIndex(target_user)
    if(UserInfo[source_user][3]==UserInfo[t_user][3]):
        sum_value=25
    else:
        sum_value=0

    # c=list(set(UserInfo[source_user][5].intersection(UserInfo[t_user][5])))
    c=list(set(UserInfo[source_user][5])&set(UserInfo[t_user][5]))
    sum_value+=len(c)/len(UserInfo[source_user][5])*25

    c=list(set(UserInfo[source_user][6])&set(UserInfo[t_user][6]))
    sum_value+=len(c)/len(UserInfo[source_user][6])*25

    c=list(set(UserInfo[source_user][7])&set(UserInfo[t_user][7]))
    sum_value+=len(c)/len(UserInfo[source_user][7])*25

    print(target_user,' : ', sum_value)
    return sum_value


class SelectMuseUser:
    def __init__(self,r):

        self.listbox=tkinter.Listbox(r, height=27, selectmode='single')
        for loginid, loginname, gender, location, category, favorite_artist, favorite_title, friends in UserInfo:
            self.listbox.insert('end',loginname+' : '+loginid)
        self.listbox.grid(row=2, column=0)

        self.listScroll=tkinter.Scrollbar(r, orient=tkinter.VERTICAL, command=self.listbox.yview)
        self.listScroll.grid(row=2, column=1, sticky='nsw', rowspan=1)
        self.listbox['yscrollcommand']=self.listScroll.set

        inButton=tkinter.Button(r,text='Select User',command=self.select_user).grid(row=4,column=0)

    def select_user(self):
        global UserInfo_index

        items = self.listbox.curselection()
        print(self.listbox.curselection())
        print(UserInfo[items[0]])
        UserInfo_index=items[0]
        print(UserInfo_index)

        selected_user="Muse User Name : "+str(UserInfo[UserInfo_index][1])+"\n"+"Preference Category : "+str(UserInfo[UserInfo_index][4])+"\n"+"Favorite Artist : "+str(UserInfo[UserInfo_index][5])+"\n"+"Favorite Title : "+str(UserInfo[UserInfo_index][6])

        label = tkinter.Label(mainWindow, text=selected_user)
        label.config(font=('arial',13), width='60', foreground ='black', background ='lightskyblue')
        label.grid(row=2, column=3, sticky='nw')

        SelectMuseMusic(mainWindow2, UserInfo_index)
        SelectSoulmate(mainWindow3, UserInfo_index)



class SelectMuseMusic:
    def __init__(self,r,User_index):

        global ClassificationValue
        global ContextValue

        self.musiclist=tkinter.Listbox(r)
        self.musiclist.grid(row=2, column=0, sticky='nsew', rowspan=1)
        self.musiclist.config(border=2, relief='sunken', cursor='heart', selectbackground='pink', selectforeground='black')

        i=1
        for musicid, title, artist, bit, music_category, bag_of_word in TopChartMusicInfo:
            self.musiclist.insert(tkinter.END, "Top ["+str(i)+'] '+title+' by '+artist+' : '+music_category)
            i=i+1

        self.listScroll=tkinter.Scrollbar(r, orient=tkinter.VERTICAL, command=self.musiclist.yview)
        self.listScroll.grid(row=2, column=1, sticky='nsw', rowspan=1)
        self.musiclist['yscrollcommand']=self.listScroll.set

        self.rateFrame = tkinter.LabelFrame(r, text='Rating')
        self.rateFrame.grid(row=4, column=0, sticky='nw', columnspan=2)
        self.rateSpinner=tkinter.Spinbox(self.rateFrame, width=2, from_=1, to=5)
        self.rateSpinner.grid(row=0, column=0)

        tkinter.Button(r, text='Listen Rating Music ',command=self.select_music).grid(row=4,column=0, sticky='ne')

        optionFrame = tkinter.LabelFrame(r, text="Select Music Classification")
        optionFrame.grid(row=2, column=2, sticky='nw')

        ClassificationValue=tkinter.IntVar()
        ClassificationValue.set(1)

        # Radio buttons
        i=0
        for text, value in MusicClassification:
            tkinter.Radiobutton(optionFrame, text=text, value=value, variable=ClassificationValue).grid(row=i, column=2, sticky='w')
            i=i+1

        optionFrame = tkinter.LabelFrame(r, text="Select Your Context")
        optionFrame.grid(row=2, column=3, sticky='nw')

        ContextValue=tkinter.IntVar()
        ContextValue.set(1)

        # Radio buttons
        i=0
        for text, value in ContextClassification:
            tkinter.Radiobutton(optionFrame, text=text, value=value, variable=ContextValue).grid(row=i, column=3, sticky='w')
            i=i+1

        tkinter.Button(r, text='Please Recommend Music',command=self.select_classification).grid(row=4,column=2, columnspan=2, sticky='ew')


    def select_music(self):
        items = self.musiclist.curselection()
        print(self.musiclist.curselection())
        print(TopChartMusicInfo[items[0]])
        MusicInfo_index=items[0]
        print(MusicInfo_index)


    def select_classification(self):
        global ClassificationValue
        global ContextValue
        global recommend_classification
        global recommend_context
        global recommend_artist
        global recommend_title

        del recommend_classification[0:]
        del recommend_context[0:]
        del recommend_artist[0:]
        del recommend_title[0:]


        print(ClassificationValue.get(),ContextValue.get())

        # recommend by TopTrend+Classification, by Context, by artist, by title
        for musicid, title, artist, bit, classification, bag_word in MusicInfo:
            i=ClassificationValue.get()-1
            if(str(MusicClassification[i][0]) == classification):
                recommend_classification.append(musicid)

            j=ContextValue.get()-1
            for context in bag_word:
                if(str(ContextClassification[j][0]) == context):
                    recommend_context.append(musicid)

            for favorite_artist in UserInfo[UserInfo_index][5]:
                if(artist==favorite_artist):
                    recommend_artist.append(musicid)

            for favorite_title in UserInfo[UserInfo_index][6]:
                if(title==favorite_title):
                    recommend_title.append(musicid)

        print(recommend_classification)
        print(recommend_context)
        print(recommend_artist)
        print(recommend_title)

        # Term Frequency : how many times of musicid : Best 20
        recommend_total=recommend_classification+recommend_context+recommend_artist+recommend_title
        freqs=Counter(recommend_total).most_common(20)
        print(freqs)

        label = tkinter.Label(mainWindow2, text="Muse Recommend Just-for-You")
        label.grid(row=1, column=4)
        self.recommendlist=tkinter.Listbox(mainWindow2)
        self.recommendlist.grid(row=2, column=4, sticky='nsew', rowspan=1)
        self.recommendlist.config(border=2, relief='sunken', cursor='heart', selectbackground='pink', selectforeground='black')

        i=1
        for recommend_musicid in freqs:

            print(recommend_musicid)

            for musicid, title, artist, bit, classification, bag_word in MusicInfo:
                if(recommend_musicid[0] == musicid):
                    break

            if(recommend_musicid[1]>2):
                self.recommendlist.insert(tkinter.END, "Best ["+str(i)+'] '+title+' by '+artist+' : '+classification)
            elif(recommend_musicid[1]<1):
                self.recommendlist.insert(tkinter.END, "Like ["+str(i)+'] '+title+' by '+artist+' : '+classification)
            else:
                self.recommendlist.insert(tkinter.END, "Love ["+str(i)+'] '+title+' by '+artist+' : '+classification)

            i=i+1

        self.listScroll=tkinter.Scrollbar(mainWindow2, orient=tkinter.VERTICAL, command=self.recommendlist.yview)
        self.listScroll.grid(row=2, column=5, sticky='nsw', rowspan=1)
        self.recommendlist['yscrollcommand']=self.listScroll.set


# rating>3 add to music list
# TBD


class SelectSoulmate:
    def __init__(self,r,User_index):

        global UserInfo_index
        similarity={}

        self.listbox=tkinter.Listbox(r, height=15, selectmode='single')
        i=0
        for soulmate in UserInfo[User_index][7]:
            self.listbox.insert('end','['+str(i+1)+'] '+soulmate)
            sim_val=compute_sim(User_index,soulmate)
            similarity[soulmate]=sim_val
            i+=1

        # similarity.sort()
        # print(sorted(similarity.items(), key=lambda x:x[1], reverse=True))

        sort_sim=sorted(similarity.items(), key=lambda x:x[1], reverse=True)
        print(sort_sim)
        print(sort_sim[0][0])
        print(sort_sim[len(similarity)-1][0])
        self.listbox.insert('end', '+BestFriend('+str(int(sort_sim[0][1]))+'): '+sort_sim[1][0])
        self.listbox.insert('end', '-Dissimilarity('+str(int(sort_sim[len(similarity)-1][1]))+'): '+sort_sim[len(similarity)-1][0])

        self.listbox.grid(row=2, column=0, ipadx=1, ipady=1, padx=1, pady=1)

        self.listScroll=tkinter.Scrollbar(r, orient=tkinter.VERTICAL, command=self.listbox.yview)
        self.listScroll.grid(row=2, column=1, sticky='nse', rowspan=1)
        self.listbox['yscrollcommand']=self.listScroll.set

        print(UserInfo_index)

        tkinter.Button(r,text='Select Soulmate & Suprise Me',command=self.select_soulmate).grid(row=4,column=0, columnspan=2)
        tkinter.Button(r,text='Visualize My Soulmate',command=self.visualize_soulmate).grid(row=4,column=2)
        tkinter.Button(r,text='Visualize Second Level',command=self.visualize_level2).grid(row=4,column=3)
        tkinter.Button(r,text='Visualize Whole Network',command=self.visualize_whole).grid(row=4,column=4)



    def select_soulmate(self):

        global UserInfo_index

        items = self.listbox.curselection()
        friend_index=items[0]
        friends=UserInfo[UserInfo_index][7]
        print(friends)
        print(UserInfo_index)
        print(UserInfo[UserInfo_index][7][friend_index])

        i=0
        for x in UserInfo:
            if (UserInfo[UserInfo_index][7][friend_index] == UserInfo[i][0]):
                break
            i+=1

        selected_soulmate="My Soulmate : "+str(UserInfo[i][0])+"\n"+"Preference Category : "+str(UserInfo[UserInfo_index][4])+"\n"+"Favorite Artist : "+str(UserInfo[i][5])+"\n"+"Favorite Title : "+str(UserInfo[i][6])

        label = tkinter.Label(mainWindow3, text=selected_soulmate)
        label.config(font=('arial',13), width='60', foreground ='black', background ='yellowgreen')
        label.grid(row=2, column=2, columnspan=3, sticky='nw')

        print('friend index :',friend_index)
        friend=UserInfo[UserInfo_index][7][friend_index]
        print("friend:", friend)

        for x in UserInfo:
            print(UserInfo[UserInfo_index][7][friend_index], x[0])
            if(x[0]==UserInfo[UserInfo_index][7][friend_index]):
                titles=x[6]
                break

        print(titles)
        print(UserInfo[UserInfo_index][6])
        print(set(titles)-set(UserInfo[UserInfo_index][6]))

        if((set(titles)-set(UserInfo[UserInfo_index][6]))==set()):
            selected_surprise="No Surprise : My friend is listening same music....\nvery close music soulmate"
        else:
            selected_surprise="Surprise Me : "+str(set(titles)-set(UserInfo[UserInfo_index][6]))+"\nMy friend is listening different song....try it"

        label = tkinter.Label(mainWindow3, text=selected_surprise)
        label.config(font=('arial',13), width='60', foreground ='black', background ='yellow')
        label.grid(row=3, column=2, columnspan=3, sticky='nw')


    def get_title_friend(self, userid):
        for x in UserInfo:
            print(userid, x[0])
            if(x[0]==userid):
                break
        return x[0][6]


    def visualize_soulmate(self):

        global UserInfo_index

        G=nx.Graph()

        for friends in UserInfo[UserInfo_index][7]:
            G.add_edge(UserInfo[UserInfo_index][0], friends)

        plt.subplot(1,1,1)
        nx.draw(G, with_labels=True, node_color='aquamarine', node_size=200, font_weight="bold", label="Visualize Musical Soulmate")
        plt.show()

    def visualize_level2(self):

        global UserInfo_index

        G=nx.Graph()

        for friends in UserInfo[UserInfo_index][7]:
            G.add_edge(UserInfo[UserInfo_index][0], friends)
            level2_index=find_UserIndex(friends)
            for friends_level2 in UserInfo[level2_index][7]:
                G.add_edge(UserInfo[level2_index][0], friends_level2)

        plt.subplot(1,1,1)
        nx.draw(G, with_labels=True, node_color='orchid', node_size=200, font_weight="bold", label="Visualize Musical Soulmate")
        plt.show()

    def visualize_whole(self):

        global UserInfo_index

        # Directed Graph
        G=nx.DiGraph()

        index=0
        while(index!=len(UserInfo)):
            for friends in UserInfo[index][7]:
                G.add_edge(UserInfo[index][0], friends)
            index+=1

        """
        centrality=nx.degree_centrality(G)
        for v,c in centrality.items():
            print(v,c)
    
        """

        plt.subplot(1,1,1)
        nx.draw(G, with_labels=True, node_color='greenyellow', node_size=200, font_weight="bold", label="Visualize Musical Soulmate")
        plt.show()

#        print(nx.degree_centrality(G))

class UserProfile(object):

    def __init__(self, userid, username, gender):
        self.userid= userid
        self.username=username
        self.gender=gender
        musicid=1
        rate=range(1,5)
        # Dictionary : musicNo, rate
        self.musicRatingList={'0':0}

    def music_rating(self, musicid, rate):
#        if musicid in self.musicRatingList:
#            del self.musicRatingList[musicid]
        self.musicRatingList[musicid]=rate

def selectUser():
    print(userlist.curselection)
    print('select user')

def suprise_me(self, user=None):
    print("random music")

UserInfo_index=0
root = tkinter.Tk()
logo=tkinter.PhotoImage(file ="back.gif")


notebook=ttk.Notebook(root)
notebook.pack()
mainWindow=ttk.Frame(notebook)
mainWindow2=ttk.Frame(notebook)
mainWindow3=ttk.Frame(notebook)
notebook.add(mainWindow, text='User Profile')
notebook.add(mainWindow2, text='Recommend Music')
notebook.add(mainWindow3, text='Musical Soulmate')

root.title("Muse")
root.geometry("960x740")
root.configure(background='pink')

#    label = tkinter.Label(mainWindow, text="Welcome Muse", image=logo)
#    label.grid(row=0, column=0, columnspan=6)
label = tkinter.Label(mainWindow, text="Welcome Muse !\n\n          Music Recommendation Service   Just-for-you         \n@Muse 2018")
label.pack()
label.config(font=('arial',15,'bold'), foreground ='black' , background ='pink')
label.config(image=logo)
label.config(compound='left')
label.grid(row=0, column=0, columnspan=6)

label = tkinter.Label(mainWindow, text="Select Muse User")
label.grid(row=1, column=0)

mainWindow.columnconfigure(0, weight=1)
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

SelectMuseUser(mainWindow)

#window2

logo2=tkinter.PhotoImage(file ="back2.gif")
label = tkinter.Label(mainWindow2, text="Recommendation Just-for-You\n\n  by Context : Location, Emotion, Activity, TopTrends  \n@Muse 2018")
label.pack()
label.config(font=('arial',15,'bold'), foreground ='black' , background ='pink')
label.config(image=logo2)
label.config(compound='left')
label.grid(row=0, column=0, columnspan=6)

label = tkinter.Label(mainWindow2, text="Top Chart Music")
label.grid(row=1, column=0)

mainWindow2.columnconfigure(0, weight=4)
mainWindow2.columnconfigure(1, weight=1)
mainWindow2.columnconfigure(2, weight=3)
mainWindow2.columnconfigure(3, weight=3)
mainWindow2.columnconfigure(4, weight=5)
mainWindow2.columnconfigure(5, weight=1)

mainWindow2.rowconfigure(0, weight=1)
mainWindow2.rowconfigure(1, weight=3)
mainWindow2.rowconfigure(2, weight=3)
mainWindow2.rowconfigure(3, weight=1)
mainWindow2.rowconfigure(4, weight=1)

for topmusic in TopChartMusicInfo:
    MusicInfo.append(topmusic)


"""
musiclist=tkinter.Listbox(mainWindow2)
musiclist.grid(row=2, column=0, sticky='nsew', rowspan=1)
musiclist.config(border=2, relief='sunken', cursor='heart', selectbackground='pink', selectforeground='black')

for musicid, title, artist, bit, music_category in MusicInfo:
    musiclist.insert(tkinter.END, str(UserInfo_index)+'['+musicid+'] : '+title+' by '+artist)

listScroll=tkinter.Scrollbar(mainWindow2, orient=tkinter.VERTICAL, command=musiclist.yview)
listScroll.grid(row=2, column=1, sticky='nsw', rowspan=1)
musiclist['yscrollcommand']= listScroll.set

optionFrame = tkinter.LabelFrame(mainWindow2, text="Music Details")
optionFrame.grid(row=2, column=2, sticky='nw')

rbValue = tkinter.IntVar()
rbValue.set(2)

# Radio buttons
radio1 = tkinter.Radiobutton(optionFrame, text="Artist", value=1, variable=rbValue)
radio2 = tkinter.Radiobutton(optionFrame, text="Album", value=2, variable=rbValue)
radio3 = tkinter.Radiobutton(optionFrame, text="Description", value=3, variable=rbValue)
radio1.grid(row=1, column=0, sticky='w')
radio2.grid(row=2, column=0, sticky='w')
radio3.grid(row=3, column=0, sticky='w')

resultLabel=tkinter.Label(mainWindow2)
resultLabel.grid(row=2, column=3, sticky='sw')
result=tkinter.Entry(mainWindow2)
result.grid(row=2, column=3, sticky='sw')

rateFrame = tkinter.LabelFrame(mainWindow2, text='Rating')
rateFrame.grid(row=4, column=0, sticky='new')
rateSpinner=tkinter.Spinbox(rateFrame, width=2, from_=1, to=5)
rateSpinner.grid(row=0, column=0)

style = ttk.Style()
style.map("C.TButton",
          foreground=[('pressed', 'red'), ('active', 'blue')],
          background=[('pressed', '!disabled', 'black'), ('active', 'white')]
          )

#colored_btn = ttk.Button(text="Test", style="C.TButton").pack()

supriseFrame = tkinter.Frame(mainWindow2)
supriseFrame.grid(row=5, column=0, sticky='new')
ttk.Button(supriseFrame, text='Suprise Me', command=suprise_me(self=supriseFrame), style="C.TButton").grid(row=0, column=0)

user1 = UserProfile(1,"chaemee","Female")
print("userid={}, username={}".format(user1.userid, user1.username))
user1.music_rating('10',5)
user1.music_rating('11',3)
user1.music_rating('10',4)
print(user1.musicRatingList)
"""

#Window3

logo3=tkinter.PhotoImage(file ="back3.gif")
label = tkinter.Label(mainWindow3, text="Your Musical Soulmate\n\n Listening This Song, Try New Song \n@Muse 2018")
label.pack()
label.config(font=('arial',15,'bold'), foreground ='black' , background ='pink')
label.config(image=logo3)
label.config(compound='left')
label.grid(row=0, column=0, columnspan=6)

label = tkinter.Label(mainWindow3, text="Your Musical Soulmate")
label.grid(row=1, column=0)

mainWindow3.columnconfigure(0, weight=4)
mainWindow3.columnconfigure(1, weight=1)
mainWindow3.columnconfigure(2, weight=4)
mainWindow3.columnconfigure(3, weight=1)
mainWindow3.columnconfigure(4, weight=4)
mainWindow3.columnconfigure(5, weight=1)

mainWindow3.rowconfigure(0, weight=1)
mainWindow3.rowconfigure(1, weight=3)
mainWindow3.rowconfigure(2, weight=3)
mainWindow3.rowconfigure(3, weight=1)
mainWindow3.rowconfigure(4, weight=1)



mainWindow.mainloop()
