import requests 

APIKey = 'g1MzozftmigqEmKPxGLyEoimYJJ3'
baseUrl = 'http://cricapi.com/api/matches?'

url = baseUrl + 'apikey=' + APIKey
matchesData = requests.get(url).json()
matchList = set()
matches = 0
while True:
    try:
        matchList.add(matchesData["matches"][matches]["team-2"] + ' vs ' + matchesData["matches"][matches]["team-1"])
        matches += 1
    except:
        print('No. of matches: ' + str(len(matchList)))
        #print('End of List')
        break    

for match in matchList:
    print(match)      