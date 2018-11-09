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

print(scorecardInfo["data"]["batting"][1]["title"])
scores = scorecardInfo["data"]["batting"][1]["scores"]
scores[len(scores)-1]["pid"] = scores[len(scores)-1]["detail"]
for i in scores:
    print(i["pid"], i["batsman"], i["dismissal-info"], i["R"], i["B"], i["6s"], i["4s"], i["SR"])

#print(scorecardInfo["data"]["batting"][1])
