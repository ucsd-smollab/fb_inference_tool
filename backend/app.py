from flask import Flask
from flask import json
from flask import request
from flask import render_template
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

@app.route("/stage_three_step_two", methods=["GET"])
@cross_origin()
def StageThreeStepTwoOne():
    attribute_query = "SELECT attribute FROM privacy_db.attribute_count WHERE inf_count>=5 AND mutual_count>1 ORDER BY mutual_count DESC LIMIT 1;"
    mycursor.execute(attribute_query)
    attribute = mycursor.fetchall()
    if attribute:
        attribute = attribute[0][0]
    else:
        attribute = "Not Enough Data"

    category_query = "SELECT category FROM privacy_db.attribute_count WHERE inf_count>=5 ORDER BY mutual_count DESC LIMIT 1;"
    mycursor.execute(category_query)
    category = mycursor.fetchall()[0][0]

    participant_url_query = "SELECT participant_url FROM privacy_db.participant_profile;"
    mycursor.execute(participant_url_query)
    participant_url = mycursor.fetchall()[0][0]

    category_line = f"category: {category} attribute: {attribute}"
    if category=="high_school":
        five_shared_query = f"SELECT friend_url FROM privacy_db.high_school WHERE hs_name=%s AND friend_url!='{participant_url}' LIMIT 5;"
        category_line = f"Some of your friends who went to {attribute}"
    elif category=="college":
        five_shared_query = f"SELECT friend_url FROM privacy_db.college WHERE college_name=%s AND friend_url!='{participant_url}' LIMIT 5;"
        category_line = f"Some of your friends who went to {attribute}"
    elif category=="work":
        five_shared_query = f"SELECT friend_url FROM privacy_db.work WHERE workplace=%s AND friend_url!='{participant_url}' LIMIT 5;"
        category_line = f"Some of your friends who worked at {attribute}"
    elif category=="places_lived":
        five_shared_query = f"SELECT friend_url FROM privacy_db.places_lived WHERE location=%s AND friend_url!='{participant_url}' LIMIT 5;"
        category_line = f"Some of your friends who lived in {attribute}"
    else:
        five_shared_query = f"SELECT friend_url FROM privacy_db.friend_profiles WHERE {category}=%s AND friend_url!='{participant_url}' ORDER BY mutual_count DESC LIMIT 5;"
        if category=="religion":
            category_line = f"Some of your friends whose religion is {attribute}"
        elif category=="politics":
            category_line = f"Some of your friends who politically identify as {attribute}"

    val = (attribute,)
    mycursor.execute(five_shared_query, val)
    five_shared = mycursor.fetchall()

    shared_to_display = []
    for url in five_shared:
        query = "SELECT name FROM privacy_db.friend_profiles WHERE friend_url=%s;"
        value = (url[0],)
        mycursor.execute(query, value)
        temp_name = mycursor.fetchall()
        shared_to_display.append(temp_name[0])

    five_inf_query = "SELECT friend_url, category FROM privacy_db.mutual_count WHERE category=%s AND attribute=%s ORDER BY mutual_count DESC;"
    val = (category, attribute)
    mycursor.execute(five_inf_query, val)
    five_inf = mycursor.fetchall()

    inf_to_display_url = []
    for url, cat in five_inf:
        if cat=="religion" or cat=="politics":
            query = f"SELECT {cat} FROM privacy_db.friend_profiles WHERE friend_url=%s;"
            value = (url,)
            mycursor.execute(query, value)
            temp_val = mycursor.fetchall()
            if temp_val=="NA":
                inf_to_display_url.append(url)
        else:
            query = f"SELECT friend_url FROM privacy_db.{cat} WHERE friend_url=%s;"
            value = (url,)
            mycursor.execute(query, value)
            temp_val = mycursor.fetchall()
            if not temp_val:
                inf_to_display_url.append(url)
        if len(inf_to_display_url) >= 5:
            break
    
    inf_to_display = []
    for url in inf_to_display_url:
        query = "SELECT name FROM privacy_db.friend_profiles WHERE friend_url=%s;"
        value = (url,)
        mycursor.execute(query, value)
        temp_name = mycursor.fetchall()
        inf_to_display.append(temp_name)

    newList = [category_line, shared_to_display, inf_to_display]

    response = app.response_class(
        response=json.dumps(newList),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/stage_three_step_three", methods=["GET"])
@cross_origin()
def StageThreeStepThree():
    attribute_query = "SELECT attribute FROM privacy_db.attribute_count WHERE inf_count>=5 AND mutual_count>1 ORDER BY mutual_count DESC LIMIT 4;"
    mycursor.execute(attribute_query)
    attribute_list = mycursor.fetchall()

    category_query = "SELECT category FROM privacy_db.attribute_count WHERE inf_count>=5 ORDER BY mutual_count DESC LIMIT 4;"
    mycursor.execute(category_query)
    category_li = mycursor.fetchall()

    participant_url_query = "SELECT participant_url FROM privacy_db.participant_profile;"
    mycursor.execute(participant_url_query)
    participant_url = mycursor.fetchall()[0][0]

    category_list = []
    shared_list = []
    inferred_list = []
    for i in range(1, len(attribute_list)):
        attribute = attribute_list[i][0]
        category = category_li[i][0]

        category_line = f"category: {category} attribute: {attribute}"
        if category=="high_school":
            five_shared_query = f"SELECT friend_url FROM privacy_db.high_school WHERE hs_name=%s AND friend_url!='{participant_url}' LIMIT 5;"
            category_line = f"Some of your friends who went to {attribute}"
        elif category=="college":
            five_shared_query = f"SELECT friend_url FROM privacy_db.college WHERE college_name=%s AND friend_url!='{participant_url}' LIMIT 5;"
            category_line = f"Some of your friends who went to {attribute}"
        elif category=="work":
            five_shared_query = f"SELECT friend_url FROM privacy_db.work WHERE workplace=%s AND friend_url!='{participant_url}' LIMIT 5;"
            category_line = f"Some of your friends who worked at {attribute}"
        elif category=="places_lived":
            five_shared_query = f"SELECT friend_url FROM privacy_db.places_lived WHERE location=%s AND friend_url!='{participant_url}' LIMIT 5;"
            category_line = f"Some of your friends who lived in {attribute}"
        else:
            five_shared_query = f"SELECT friend_url FROM privacy_db.friend_profiles WHERE {category}=%s AND friend_url!='{participant_url}' ORDER BY mutual_count DESC LIMIT 5;"
            if category=="religion":
                category_line = f"Some of your friends whose religion is {attribute}"
            elif category=="politics":
                category_line = f"Some of your friends who politically identify as {attribute}"

        val = (attribute,)
        mycursor.execute(five_shared_query, val)
        five_shared = mycursor.fetchall()
        if not five_shared:
            print("no shared friends")
            continue

        shared_to_display = []
        for url in five_shared:
            query = "SELECT name FROM privacy_db.friend_profiles WHERE friend_url=%s;"
            value = (url[0],)
            mycursor.execute(query, value)
            temp_name = mycursor.fetchall()
            shared_to_display.append(temp_name[0])

        five_inf_query = "SELECT friend_url, category FROM privacy_db.mutual_count WHERE category=%s AND attribute=%s ORDER BY mutual_count DESC;"
        val = (category, attribute)
        mycursor.execute(five_inf_query, val)
        five_inf = mycursor.fetchall()

        inf_to_display_url = []
        for url, cat in five_inf:
            if cat=="religion" or cat=="politics":
                query = f"SELECT {cat} FROM privacy_db.friend_profiles WHERE friend_url=%s;"
                value = (url,)
                mycursor.execute(query, value)
                temp_val = mycursor.fetchall()
                if temp_val=="NA":
                    inf_to_display_url.append(url)
            else:
                query = f"SELECT friend_url FROM privacy_db.{cat} WHERE friend_url=%s;"
                value = (url,)
                mycursor.execute(query, value)
                temp_val = mycursor.fetchall()
                if not temp_val:
                    inf_to_display_url.append(url)
            if len(inf_to_display_url) >= 5:
                break
        
        inf_to_display = []
        for url in inf_to_display_url:
            query = "SELECT name FROM privacy_db.friend_profiles WHERE friend_url=%s;"
            value = (url,)
            mycursor.execute(query, value)
            temp_name = mycursor.fetchall()
            inf_to_display.append(temp_name)

        category_list.append(category_line)
        shared_list.append(shared_to_display)
        inferred_list.append(inf_to_display)

    newList = [category_list, shared_list, inferred_list]

    response = app.response_class(
        response=json.dumps(newList),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/stage_four_friend", methods=["POST"])
@cross_origin()
def getFriendData():
    friend_url = request.get_json()['friend_url']
    print(f"friend_url: {friend_url}")

    query = "SELECT * FROM privacy_db.friend_profiles WHERE friend_url=%s;"
    mycursor.execute(query, (friend_url,))
    friend_info = mycursor.fetchall()[0]

    query = "SELECT workplace FROM privacy_db.work WHERE friend_url=%s;"
    mycursor.execute(query, (friend_url,))
    workplaces = mycursor.fetchall()
    if not workplaces:
        workplaces = ["No Data"]
    else:
        workplaces = [''.join(i) for i in workplaces]

    query = "SELECT college_name FROM privacy_db.college WHERE friend_url=%s;"
    mycursor.execute(query, (friend_url,))
    college = mycursor.fetchall()
    if not college:
        college = ["No Data"]
    else:
        college = [''.join(i) for i in college]

    query = "SELECT hs_name FROM privacy_db.high_school WHERE friend_url=%s;"
    mycursor.execute(query, (friend_url,))
    high_school = mycursor.fetchall()
    if not high_school:
        high_school = ["No Data"]
    else:
        high_school = [''.join(i) for i in high_school]

    query = "SELECT location FROM privacy_db.places_lived WHERE friend_url=%s;"
    mycursor.execute(query, (friend_url,))
    places_lived = mycursor.fetchall()
    if not places_lived:
        places_lived = ["No Data"]
    else:
        places_lived = [''.join(i) for i in places_lived]

    if friend_info[6]=="NA":
        religion = ["No Data"]
    else:
        religion = [friend_info[6]]

    if friend_info[7]=="NA":
        politics = ["No Data"]
    else:
        politics = [friend_info[7]]

    FriendData = {
        'name': friend_info[1],
        'profilePictureURL': friend_info[2],
        'mutualFriendCount': friend_info[3],
        'workplace': workplaces,
        'college': college,
        'highschool': high_school,
        'places': places_lived,
        'religion': religion,
        'politics': politics,
    }

    return FriendData

@app.route("/stage_four_query", methods=["POST"])
@cross_origin()
def getFriendQuery():
    search_query = request.get_json()['query']

    query = "SELECT friend_url, name, mutual_count, prof_pic_url FROM privacy_db.friend_profiles WHERE name SOUNDS LIKE %s;"
    mycursor.execute(query, (search_query,))
    similar_friends_name = mycursor.fetchall()
    print(f"names: {similar_friends_name}")
    
    query_dict = {}
    for friend in similar_friends_name:
        query_dict[friend[0]] = [friend[1], friend[2], friend[3]]
    print(query_dict)
    
    return query_dict

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
        print(end_scrape)
        return response
    else:
        end_scrape = True
        print("Changed")
        end_scrape = True
        response = app.response_class(
            response=json.dumps(end_scrape),
            status=200,
            mimetype='application/json'
        )
        print(end_scrape)
        return response

if __name__ == '__main__':
    global end_scrape 
    end_scrape = False
    app.run()