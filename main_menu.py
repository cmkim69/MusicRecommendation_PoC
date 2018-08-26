import music_recommend
import os

listing = os.walk('.')
for root, directories, files in listing:
    for file in files:
        print(file)

#music_recommend.recommend()