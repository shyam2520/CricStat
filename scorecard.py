import requests
import json

matchId = '1157760'
'''
baseUrl = 'https://cricapi.com/api/fantasySummary?'
APIKey = 'g1MzozftmigqEmKPxGLyEoimYJJ3' 
url = baseUrl + 'apikey=' + APIKey + '&unique_id=' + matchId    
scorecardInfo = requests.get(url).json()

f = open('scorecard.json', 'w+')
f.write(json.dumps(scorecardInfo))
'''

f = open('scorecard.json', 'r+')
scorecardInfo = json.loads(f.read())

