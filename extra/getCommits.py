'''
after generate code to get list of repos, 
this code will grab a user commit history with in this year
It will use restAP to fetch commit history for a given user across their repositories.

'''

import os
import requests
import json
import gql
from datetime import date

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")   
USERNAME = os.getenv("USERNAME")


url = "https://api.github.com/users/AKIEN-MGA/events"
r = requests.get(url, headers={"Authorization": f"Bearer {GITHUB_TOKEN}"  }     )


pageNum = 1
listR = r.json()
holder = []
temp = []

while True: 
   
   tempR = requests.get(url, headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}, params={"page":pageNum }   )
   if len(tempR.json()) == 0:
     break
   temp.extend(tempR.json())
   pageNum += 1

print(pageNum)

for i in temp:
    if(i["type"] == "PushEvent"):
        holder.append(i)

with open('#', 'w') as f:
   json.dump(holder , f, indent=2)



this_year = date(2026, 1, 1)
'''
for i in temp:
    if(i["created_at"] > this_year):
        holder.append(i)

'''




"""

all the commit is a defined repo 

url = "https://api.github.com/repos/RylanSanders/paint-clone/commits"
r = requests.get(url, headers={"Authorization": f"Bearer {GITHUB_TOKEN}"  }     )


# write list of all commits there messeges and date stamp
listR = r.json()
holder = [""]
print(listR[0]["commit"]["message"])
print(listR[0]["commit"]["committer"]["date"])
for i in listR:
    holder.append(i["commit"]["message"])
    holder.append(i["commit"]["committer"]["date"])
    
print("after: ", holder)
with open('#', 'w') as f:
   json.dump(holder , f, indent=2)


# make whole response into file
with open('#', 'w') as f:
   json.dump(r.json() , f, indent=2)
"""









#print(r.json())




