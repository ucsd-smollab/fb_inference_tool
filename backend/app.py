from flask import Flask
from flask import json
from flask import request
from flask import render_template
from flask_cors import CORS, cross_origin
import mysql.connector

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

def mysql_connect():
    mydb = mysql.connector.connect(
      host="127.0.0.1",
      user="privacy_admin",
      password="kristenisthebest",
    )
    return mydb

@app.route("/", methods=["GET"])
def index():
    return "Hello world"

@app.route("/stage_one_query", methods=["GET"])
@cross_origin()
def StageOne():
    mydb = mysql_connect()
    mydb.commit()
    mycursor = mydb.cursor()
    query = "SELECT participant_url from privacy_db.participant_profile;"
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    participant_url = myresult[0][0]
    url = 'https://www.facebook.com/{}/about'.format(participant_url)

    response = app.response_class(
        response=json.dumps(url),
        status=200,
        mimetype='application/json'
    )
    mycursor.close()
    return response

@app.route("/stage_three_step_one", methods=["GET"])
@cross_origin()
def StageThreeStepOne():
    mydb = mysql_connect()
    mydb.commit()
    mycursor = mydb.cursor()
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
    mycursor.close()
    return response

@app.route("/stage_three_step_two", methods=["GET"])
@cross_origin()
def StageThreeStepTwoOne():
    mydb = mysql_connect()
    mydb.commit()
    mycursor = mydb.cursor()
    attribute_cat_query = "SELECT attribute, category FROM privacy_db.attribute_count WHERE inf_count>=5 AND mutual_count>1 ORDER BY mutual_count DESC LIMIT 1;"
    mycursor.execute(attribute_cat_query)
    attribute_cat = mycursor.fetchall()
    if attribute_cat:
        (attribute, category) = attribute_cat[0]
    else:
        raise Exception('Not enough inferences!')

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

    five_inf_query = "SELECT friend_url FROM privacy_db.mutual_count WHERE category=%s AND attribute=%s ORDER BY mutual_count DESC LIMIT 5;"
    val = (category, attribute)
    mycursor.execute(five_inf_query, val)
    five_inf = mycursor.fetchall()

    inf_to_display = []
    for (url,) in five_inf:
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
    mycursor.close()
    return response

@app.route("/stage_three_step_three", methods=["GET"])
@cross_origin()
def StageThreeStepThree():
    mydb = mysql_connect()
    mydb.commit()
    mycursor = mydb.cursor()

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

        five_inf_query = "SELECT friend_url, category FROM privacy_db.mutual_count WHERE category=%s AND attribute=%s ORDER BY mutual_count DESC LIMIT 5;"
        val = (category, attribute)
        mycursor.execute(five_inf_query, val)
        five_inf = mycursor.fetchall()

        inf_to_display = []
        for (url, _) in five_inf:
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
    mycursor.close()
    return response

@app.route("/stage_four_friend", methods=["GET"])
@cross_origin()
def getFriendData():
    mydb = mysql_connect()
    mydb.commit()
    mycursor = mydb.cursor()

    friend_url = request.args.get('friend_url')
    print(f"friend_url: {friend_url}")

    query = "SELECT * FROM privacy_db.friend_profiles WHERE friend_url=%s;"
    mycursor.execute(query, (friend_url,))
    friend_info = mycursor.fetchall()[0]

    query = "SELECT work_inf, college_inf, high_school_inf, places_lived_inf, religion_inf, politic_inf FROM privacy_db.friend_inf WHERE friend_url=%s;"
    mycursor.execute(query, (friend_url,))
    all_inf = mycursor.fetchall()
    if all_inf:
        (work_inf, college_inf, hs_inf, places_inf, religion_inf, politic_inf) = all_inf[0]
    else:
        work_inf, college_inf, hs_inf, places_inf, religion_inf, politic_inf = None;

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
    InferenceData = {
        'work': work_inf,
        'college': college_inf,
        'highschool': hs_inf,
        'places': places_inf,
        'religion': religion_inf,
        'politics': politic_inf,
    }
    data = {
        'shared': FriendData,
        'inferred': InferenceData,
    }
    mycursor.close()
    return data

@app.route("/stage_four_query", methods=["GET"])
@cross_origin()
def getFriendQuery():
    mydb = mysql_connect()
    mydb.commit()
    mycursor = mydb.cursor()

    query = request.args.get('query')
    if query == '':
        query = "SELECT friend_url, name, mutual_count, prof_pic_url FROM privacy_db.friend_profiles ORDER BY RAND() LIMIT 4;"
        mycursor.execute(query)
        friends = mycursor.fetchall()
        print(f"names: {friends}")

        query_dict = {}
        for friend in friends:
            query_dict[friend[0]] = [friend[1], friend[2], friend[3]]
        mycursor.close()
        return query_dict
    else:
        search_query = '%' + query + '%'
        query = "SELECT friend_url, name, mutual_count, prof_pic_url FROM privacy_db.friend_profiles WHERE name LIKE %s;"
        mycursor.execute(query, (search_query,))
        similar_friends_name = mycursor.fetchall()
        print(f"names: {similar_friends_name}")

        query_dict = {}
        for friend in similar_friends_name:
            query_dict[friend[0]] = [friend[1], friend[2], friend[3]]
        mycursor.close()
        return query_dict

@app.route("/stop_scraper", methods=["GET", "POST"])
@cross_origin()
def StopScrape():
    mydb = mysql_connect()
    mydb.commit()
    mycursor = mydb.cursor()

    if request.method == "GET":
        query = "SELECT COUNT(*) from privacy_db.stop_scraping WHERE stop=1;"
        mycursor.execute(query)
        end_scrape = mycursor.fetchall()[0][0]
        if end_scrape>0:
            status = 200
        else:
            status = 404
        response = app.response_class (
            response=json.dumps(end_scrape),
            status = status,
            mimetype='application/json'
        )
        mycursor.close()
        return response
    else:
        query = "INSERT INTO privacy_db.stop_scraping (stop) VALUES (1);"
        mycursor.execute(query)
        end_scrape = 1
        response = app.response_class(
            response=json.dumps(end_scrape),
            status=200,
            mimetype='application/json'
        )
        mydb.commit()
        mycursor.close()
        return response

if __name__ == '__main__':
    app.run()
