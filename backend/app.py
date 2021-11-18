from flask import Flask
from flask import json
from flask import request
from flask import render_template
# from flask_cors import CORS
from flask_cors import CORS, cross_origin

import mysql.connector
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="privacy_admin",
  password="kristenisthebest",
)
mycursor = mydb.cursor()

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.route("/", methods=["GET"])
def index():
    return "Hello world"

@app.route("/stage_three_step_one", methods=["GET"])
@cross_origin()
def StageThreeStepOne():
    # if using total complete
    # query_most = "SELECT name FROM privacy_db.friend_profiles ORDER BY perc_comp_total DESC, perc_comp_inf DESC LIMIT 5;"
    # query_least = "SELECT name FROM privacy_db.friend_profiles ORDER BY perc_comp_total, perc_comp_inf LIMIT 5;"
    query_most = "SELECT name FROM privacy_db.friend_profiles ORDER BY perc_comp_inf DESC LIMIT 5;"
    query_least = "SELECT name FROM privacy_db.friend_profiles ORDER BY perc_comp_inf LIMIT 5;"
    mycursor.execute(query_most)
    myresult_most = mycursor.fetchall()
    myresult_most = [name[0] for name in myresult_most]

    mycursor.execute(query_least)
    myresult_least = mycursor.fetchall()
    myresult_least = [name[0] for name in myresult_least]

    newList = [myresult_least, myresult_most]

    response = app.response_class(
        response=json.dumps(newList),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run()

'''
localhost:5000/StageThreeStepOne/mostShared
GET request
'''