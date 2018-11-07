import requests
import json

matchId = '1157760'
#route1
'''APIKey = 'g1MzozftmigqEmKPxGLyEoimYJJ3'
baseUrl = 'https://cricapi.com/api/cricketScore?'
url = baseUrl + 'apikey=' + APIKey + '&unique_id=' + matchId
matchData = requests.get(url).json()

f = open('matchData.json', 'w+')
f.write(json.dumps(matchData))
f.close()
'''

f = open('matchData.json', 'r+')
matchData = json.loads(f.read())

team1, team2 = matchData['score'].split('v')
print('Score: \n' + team1.strip() + '\n' + team2.strip())