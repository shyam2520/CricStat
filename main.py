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
            return render_template('main.html')
        return     
        

def checkDB():
    prof = db["profiles"]

def insertRec(user):
    prof.insert_one(user)

if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb://localhost/cricstat")
    db = client["cricstat"]
    prof = db["profiles"]
    app.run(debug=True, port=5000)
