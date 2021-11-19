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
    attribute_query = "SELECT attribute FROM privacy_db.attribute_count WHERE inf_count>=5 ORDER BY mutual_count DESC LIMIT 1;"
    mycursor.execute(attribute_query)
    attribute = mycursor.fetchall()[0][0]
    category_query = "SELECT category FROM privacy_db.attribute_count WHERE inf_count>=5 ORDER BY mutual_count DESC LIMIT 1;"
    mycursor.execute(category_query)
    category = mycursor.fetchall()[0][0]

    # do if statements to determine how it should be formatter
    # example These friends lived in ____ vs These friends went to ____ for college
    # remove user from list and fix %s in else

    category_line = f"category: {category} attribute: {attribute}"
    if category=="high_school":
        five_shared_query = "SELECT friend_url FROM privacy_db.high_school WHERE hs_name=%s LIMIT 5;"
    elif category=="college":
        five_shared_query = "SELECT friend_url FROM privacy_db.college WHERE college_name=%s LIMIT 5;"
    elif category=="work":
        five_shared_query = "SELECT friend_url FROM privacy_db.work WHERE workplace=%s LIMIT 5;"
    elif category=="places_lived":
        five_shared_query = "SELECT friend_url FROM privacy_db.places_lived WHERE location=%s LIMIT 5;"
    else:
        five_shared_query = f"SELECT friend_url FROM privacy_db.friend_profiles WHERE {category}=%s ORDER BY mutual_count DESC LIMIT 5;"

    val = (attribute,)
    mycursor.execute(five_shared_query, val)
    five_shared = mycursor.fetchall()

    five_inf_query = "SELECT friend_url FROM privacy_db.mutual_count WHERE category=%s AND attribute=%s ORDER BY mutual_count DESC LIMIT 5;"
    val = (category, attribute)
    mycursor.execute(five_inf_query, val)
    five_inf = mycursor.fetchall()

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
    global end_scrape

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
        end_scrape = True
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