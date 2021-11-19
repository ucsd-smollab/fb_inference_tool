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


end_scrape = False
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

@app.route("/stage_three_step_two_one_one", methods=["GET"])
@cross_origin()
def StageThreeStepTwoOne():
    top_attribute_query = "SELECT attribute, category FROM privacy_db.attribute_count WHERE inf_count>=5 ORDER BY mutual_count DESC LIMIT 1;"
    mycursor.execute(top_attribute_query)
    top_attribute = mycursor.fetchall()

    # do if statements to determine how it should be formatter
    # example These friends lived in ____ vs These friends went to ____ for college
    category_line = top_attribute

    five_shared = []
    five_shared_query = "SELECT attribute, category FROM attribute_count WHERE inf_count>=5 ORDER BY mutual_count DESC LIMIT 1;"

    five_inf = []
    five_inf_query = "SELECT attribute, category FROM attribute_count WHERE inf_count>=5 ORDER BY mutual_count DESC LIMIT 1;"

    newList = [category_line, five_shared, five_inf]

    response = app.response_class(
        response=json.dumps(newList),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/stage_three_step_three", methods=["GET"])
@cross_origin()
def StageThreeStepThree():
    '''
    choose a specific name for each category
    - places lived
    - workplaces
    - highschool/college
    - religion

    for each of these category names, select 5 people who have shared directly and top 5 friends who can be confidently predicted
    '''
    top_mutual = "SELECT attribute FROM attribute_count WHERE inf_count>=5 ORDER BY mutual_count DESC LIMIT 4;"
    mycursor.execute(top_mutual)
    top_mutual_list = mycursor.fetchall()[1:]
    print(top_mutual_list)

    newList = []
    response = app.response_class(
        response=json.dumps(newList),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/stop_scraper", methods=["GET", "POST"])
@cross_origin()
def StopScrape():
    end_scrape = True

    if request.method == "GET":
        response = app.response_class (
            response=json.dumps("wow"),
            status = 400,
            mimetype='application/json'
        )
        if end_scrape:
            print("ended scraper")
            response.status = 200

        return response
    else:
        print("Changed")
        response = app.response_class(
            response=json.dumps(end_scrape),
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