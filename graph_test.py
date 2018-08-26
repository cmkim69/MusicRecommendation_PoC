from dataset import UserInfo, MusicInfo, TopChartMusicInfo, MusicClassification, ContextClassification

import tkinter
import networkx as nx
import math
import matplotlib.pyplot as plt

#mainWindow=tkinter.Frame()

def find_UserIndex(userid):
    i=0
    while(UserInfo[i][0]!=userid):
        i+=1
    return i

G=nx.Graph()

for friends in UserInfo[4][7]:
    G.add_edge(UserInfo[4][0], friends)
    level2_index=find_UserIndex(friends)
    for friends_level2 in UserInfo[level2_index][7]:
        G.add_edge(UserInfo[level2_index][0], friends_level2)

plt.subplot(121)
nx.draw(G, with_labels=True)
plt.show()

centrality=nx.degree_centrality(G)
for v,c in centrality.items():
    print(v,c)
