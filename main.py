from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import urllib.request
import json
import pymongo
import requests
import json


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/main', methods=['POST'])
def main():
    if request.method == 'POST':
        data = json.loads(json.dumps(request.form))
        print(data)
        if(len(data) == 6):
            insertRec(data)
            return render_template('main.html')
        if(len(data) == 2):
            res = checkDB(data)
            if res=='iuser':
                return '<h1><strong>Invalid Username!</strong></h1><br/><a href="/">Try again</a>'     
            if res=='pass':
                return render_template('main.html')
            return '<h1><strong>Invalid Password!</strong></h1><br/><a href="/">Try again</a>'   
        return '<h1><strong>Please Login first!</strong></h1><br/><a href="/">Login</a>'

def checkDB(cred):
    name = cred['username']
    rec = prof.find_one({'username':name})
    if rec == None:
        return 'iuser'
    if cred['pswd'] == rec['pswd']:
        return 'pass'
    return 'fail'    

def insertRec(user):
    prof.insert_one(user)

    
@app.route('/main/matches')
def matches():
    #route-1
    
    APIKey = 'g1MzozftmigqEmKPxGLyEoimYJJ3'
    baseUrl = 'http://cricapi.com/api/matches?'
    url = baseUrl + 'apikey=' + APIKey
    matchesData = requests.get(url).json()


    #storing data
    f = open('matches.json', 'w+')
    f.write(json.dumps(matchesData))
    f.close()
    

    #route-2
    #f = open('matches.json', 'r+')
    #matchesData = json.loads(f.read())
    
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

    return render_template('matches.html', curr = currMatchList, upc = upcMatchList)

@app.route('/main/latestNews', methods=['GET', 'POST'])
def latestNews():
    if request.method == 'GET':
        return render_template('searchbar.html')
    else:
        data = json.loads(json.dumps(request.form))
        playerName = data['playerName'].replace(" ", "%20")
        resp = urllib.request.urlopen("https://news.google.com/search?q=" + playerName + "&hl=en-IN&gl=IN&ceid=IN%3Aen")
        soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
        links = []
        for link in soup.find_all('a', href=True):
            if link['href'][0:2] == './':
                links.append('https://news.google.com' + link['href'][1:]) 
            else:
                links.append(link['href'])
            print("\n") 
        return render_template('searchbar.html', links = links)  

@app.route('/main/score/<matchId>')
def score(matchId):
    #route1
    
    APIKey = 'g1MzozftmigqEmKPxGLyEoimYJJ3'
    baseUrl = 'https://cricapi.com/api/cricketScore?'
    url = baseUrl + 'apikey=' + APIKey + '&unique_id=' + matchId
    matchData = requests.get(url).json()

    f = open('matchData.json', 'w+')
    f.write(json.dumps(matchData))
    f.close()
    
    #route2
    #f = open('matchData.json', 'r+')
    #matchData = json.loads(f.read())

    team1, team2 = matchData['score'].split('v')
    team = [team1.strip(), team2.strip()]
    if 'amp;' in team[0]:
        team[0] = team[0].replace('amp;','')
    if 'amp;' in team[1]:
        team[1] = team[1].replace('amp;','')    

    match = None
    for m in currMatchList:
        if m[0] == int(matchId):
            match = m
            break
    if match == None:
        match = (0, 'Match Not Found!', '', '')
    return render_template('score.html', team_sc = team, match = match)

@app.route("/main/score/<matchId>/scorecard")
def scorecard(matchId):
    #route1
    
    baseUrl = 'https://cricapi.com/api/fantasySummary?'
    APIKey = 'g1MzozftmigqEmKPxGLyEoimYJJ3' 
    url = baseUrl + 'apikey=' + APIKey + '&unique_id=' + matchId    
    scorecardInfo = requests.get(url).json()

    f = open('scorecard.json', 'w+')
    f.write(json.dumps(scorecardInfo))

    baseUrl = 'https://cricapi.com/api/cricketScore?'
    url = baseUrl + 'apikey=' + APIKey + '&unique_id=' + matchId
    matchData = requests.get(url).json()

    f = open('matchData.json', 'w+')
    f.write(json.dumps(matchData))
    f.close()
    
    #route2
    #f = open('scorecard.json', 'r+')
    #scorecardInfo = json.loads(f.read())
    #f = open('matchData.json', 'r+')
    #matchData = json.loads(f.read())

    team1, team2 = matchData['score'].split('v')
    team = [team1.strip().split()[1], team2.strip().split()[1]]
    if 'amp;' in team[0]:
        team[0] = team[0].replace('amp;','')
    if 'amp;' in team[1]:
        team[1] = team[1].replace('amp;','')    

    title = scorecardInfo["data"]["batting"][0]["title"], scorecardInfo["data"]["batting"][1]["title"] 
    scores = scorecardInfo["data"]["batting"][0]["scores"], scorecardInfo["data"]["batting"][1]["scores"]
    bowling = scorecardInfo["data"]["bowling"][0]["scores"], scorecardInfo["data"]["bowling"][1]["scores"]
    #scores[0][len(scores[0])-1]["pid"] = scores[0][len(scores[0])-1]["detail"]
    #scores[1][len(scores[1])-1]["pid"] = scores[1][len(scores[1])-1]["detail"]
    extras = scores[0][-1]["detail"], scores[1][-1]["detail"]
    scores = scores[0][:len(scores[0])-1], scores[1][:len(scores[1])-1]
    #for i in scores:
    #    print(i["pid"], i["batsman"], i["dismissal-info"], i["R"], i["B"], i["6s"], i["4s"], i["SR"])

    return render_template('scorecard.html', title = title, scorecard = scores, extras = extras, bowling = bowling)

if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb://localhost/cricstat")
    db = client["cricstat"]
    prof = db["profiles"]
    currMatchList = set()
    upcMatchList = set()
    app.run(debug=True, port=5000)
