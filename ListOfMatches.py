import requests 
import json

#route-1
'''
APIKey = 'g1MzozftmigqEmKPxGLyEoimYJJ3'
baseUrl = 'http://cricapi.com/api/matches?'
url = baseUrl + 'apikey=' + APIKey
matchesData = requests.get(url).json()


#storing data
f = open('matches.json', 'w+')
f.write(json.dumps(matchesData))
f.close()
'''

#route-2
f = open('matches.json', 'r+')
matchesData = json.loads(f.read())

currMatchList = set()
upcMatchList = set()
matches = 0

matchList = matchesData['matches']
for match in matchList:
    if match['team-1'] == 'TBA':
        pass
    elif match["matchStarted"]:
        info = (match['unique_id'], match['team-1'] + ' vs ' + match['team-2'], match['type'], match['toss_winner_team'])
        currMatchList.add(info)
    else:
        info = (match['unique_id'], match['team-1'] + ' vs ' + match['team-2'], match['type'], match['dateTimeGMT'].split('T')[1].split('.')[0] )
        upcMatchList.add(info)

for match in currMatchList:
    print(match)   

print("\n-----------------------------------------\n")

for match in upcMatchList:
    print(match)
    