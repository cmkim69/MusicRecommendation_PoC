
import json

with open('toptrend.json','r') as f:
    trendchart=json.load(f)

print(trendchart['tracks']['track'])

i=0
while(i<100):
    print(trendchart['tracks']['track'][i]['name'], ' by ', trendchart['tracks']['track'][i]['artist']['name'])
    i+=1

