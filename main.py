from flask import Flask, render_template, request
import json
import pymongo
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/main', methods=['POST'])
def main(user=None):
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

@app.route('/main/score')
def score():
    print('Hello')
    return '<h1>Hey There</h1>' 

if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb://localhost/cricstat")
    db = client["cricstat"]
    prof = db["profiles"]
    app.run(debug=True, port=5000)
