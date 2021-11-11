from flask import Flask
from flask import request
from flask import render_template

import mysql.connector
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="privacy_admin",
  password="kristenisthebest",
)
mycursor = mydb.cursor()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Hello world"

@app.route("/stage_three_step_one/most_shared", methods=["GET"])
def StageThreeStepOne():
    query = "SELECT participant_url FROM privacy_db.participant_profile ORDER BY perc_comp_total LIMIT 5;"
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    print(myresult)
    return myresult[0]

if __name__ == '__main__':
    app.run()

'''
localhost:5000/StageThreeStepOne/mostShared
GET request
'''