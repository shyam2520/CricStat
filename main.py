from flask import Flask, render_template, request
import json
import pymongo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/main', methods=['POST'])
@app.route('/main/<user>', methods=['POST'])
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

if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb://localhost/cricstat")
    db = client["cricstat"]
    prof = db["profiles"]
    app.run(debug=True, port=5000)
