def insert_scraped_into_database(friend, mydb, mycursor, is_participant=False):
    if is_participant:
        sql = "REPLACE INTO participant_profile (participant_url, name, prof_pic_url, perc_comp_total, perc_comp_inf, religion, politics, num_friends_scraped) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (friend.url, friend.name, friend.profile_picture_url, friend.percent_total_complete, friend.percent_complete, \
        friend.attributes["contact and basic"]["basic_info"]["religiousviews"], friend.attributes["contact and basic"]["basic_info"]["politicalviews"], '0')
        mycursor.execute(sql, val)
    else:
        sql = "REPLACE INTO friend_profiles (friend_url, name, prof_pic_url, mutual_count, perc_comp_total, perc_comp_inf, religion, politics) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (friend.url, friend.name, friend.profile_picture_url, friend.numMutualFriends, friend.percent_total_complete, friend.percent_complete, \
        friend.attributes["contact and basic"]["basic_info"]["religiousviews"], friend.attributes["contact and basic"]["basic_info"]["politicalviews"])
        mycursor.execute(sql, val)

        for mutual_friend in friend.mutual_friends:
            sql = "INSERT IGNORE INTO mutual_friends (friend_url, mutual_url) VALUES (%s, %s)"
            val = (friend.url, mutual_friend)
            mycursor.execute(sql, val)

            sql = "INSERT IGNORE INTO mutual_friends (friend_url, mutual_url) VALUES (%s, %s)"
            val = (mutual_friend, friend.url)
            mycursor.execute(sql, val)

    if friend.attributes["work"] != "NA":
        for work in friend.attributes["work"]:
            sql = "INSERT IGNORE INTO work (friend_url, workplace) VALUES (%s, %s)"
            val = (friend.url, work["title"])
            mycursor.execute(sql, val)

    if friend.attributes["college"] != "NA":
        for college in friend.attributes["college"]:
            sql = "INSERT IGNORE INTO college (friend_url, college_name) VALUES (%s, %s)"
            val = (friend.url, college["title"])
            mycursor.execute(sql, val)

    if friend.attributes["highschool"] != "NA":
        for hs in friend.attributes["highschool"]:
            sql = "INSERT IGNORE INTO high_school (friend_url, hs_name) VALUES (%s, %s)"
            val = (friend.url, hs["title"])
            mycursor.execute(sql, val)

    if friend.attributes["places lived"]["list_of_cities"] != "NA":
        for city in friend.attributes["places lived"]["list_of_cities"]:
            sql = "INSERT IGNORE INTO places_lived (friend_url, location) VALUES (%s, %s)"
            val = (friend.url, city)
            mycursor.execute(sql, val)
    mydb.commit()

def insert_inf_into_database(friend, mydb, mycursor):
    one = 1
    work_max = 0
    work_max_inf = None
    for work in friend.inference_count["work"]:
        if work=="no_data" or friend.attributes["work"]!="NA":
            continue
        mutual_count = len(friend.inference_count["work"][work])
        if mutual_count > work_max:
            work_max = mutual_count
            work_max_inf = work

        if mutual_count:
            sql = "INSERT INTO work_inf (friend_url, workplace, mutual_count) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE mutual_count=mutual_count+%s"
            val = (friend.url, work, mutual_count, mutual_count)
            mycursor.execute(sql, val)
    if work_max_inf and work_max_inf != "no_data" and work_max>1:
        sql = "INSERT INTO attribute_count (attribute, category, inf_count) VALUES (%s, 'work', %s) ON DUPLICATE KEY UPDATE inf_count=inf_count+%s"
        val = (work_max_inf, one, one)
        mycursor.execute(sql, val)

    college_max = 0
    college_max_inf = None
    for college in friend.inference_count["college"]:
        if college=="no_data" or friend.attributes["college"]!="NA":
            continue
        mutual_count = len(friend.inference_count["college"][college])
        if mutual_count > college_max:
            college_max = mutual_count
            college_max_inf = college
        if mutual_count:
            sql = "INSERT INTO college_inf (friend_url, college_name, mutual_count) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE mutual_count=mutual_count+%s"
            val = (friend.url, college, mutual_count, mutual_count)
            mycursor.execute(sql, val)
    if college_max_inf and college_max_inf != "no_data" and college_max>1:
        sql = "INSERT INTO attribute_count (attribute, category, inf_count) VALUES (%s, 'college', %s) ON DUPLICATE KEY UPDATE inf_count=inf_count+%s"
        val = (college_max_inf, one, one)
        mycursor.execute(sql, val)

    hs_max = 0
    hs_max_inf = None
    for hs in friend.inference_count["highschool"]:
        if hs=="no_data" or friend.attributes["highschool"]!="NA":
            continue
        mutual_count = len(friend.inference_count["highschool"][hs])
        if mutual_count > hs_max:
            hs_max = mutual_count
            hs_max_inf = hs
        if mutual_count:
            sql = "INSERT INTO high_school_inf (friend_url, hs_name, mutual_count) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE mutual_count=mutual_count+%s"
            val = (friend.url, hs, mutual_count, mutual_count)
            mycursor.execute(sql, val)
    if hs_max_inf and hs_max_inf != "no_data" and hs_max>1:
        sql = "INSERT INTO attribute_count (attribute, category, inf_count) VALUES (%s, 'high_school', %s) ON DUPLICATE KEY UPDATE inf_count=inf_count+%s"
        val = (hs_max_inf, one, one)
        mycursor.execute(sql, val)

    city_max = 0
    city_max_inf = None
    for city in friend.inference_count["cities"]:
        if city=="no_data" or friend.attributes["places lived"]["list_of_cities"]!="NA":
            continue
        mutual_count = len(friend.inference_count["cities"][city])
        if mutual_count > city_max:
            city_max = mutual_count
            city_max_inf = city
        if mutual_count:
            sql = "INSERT INTO places_lived_inf (friend_url, location, mutual_count) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE mutual_count=mutual_count+%s"
            val = (friend.url, city, mutual_count, mutual_count)
            mycursor.execute(sql, val)
    if city_max_inf and city_max_inf != "no_data" and city_max>1:
        sql = "INSERT INTO attribute_count (attribute, category, inf_count) VALUES (%s, 'places_lived', %s) ON DUPLICATE KEY UPDATE inf_count=inf_count+%s"
        val = (city_max_inf, one, one)
        mycursor.execute(sql, val)

    religion_max = 0
    religion_max_inf = None
    for religion in friend.inference_count["religiousviews"]:
        if religion=="no_data" or friend.attributes['contact and basic']['basic_info']["religiousviews"]!="NA":
            continue
        mutual_count = len(friend.inference_count["religiousviews"][religion])
        if mutual_count > religion_max:
            religion_max = mutual_count
            religion_max_inf = religion
        if mutual_count:
            sql = "INSERT INTO religion_inf (friend_url, religious_belief, mutual_count) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE mutual_count=mutual_count+%s"
            val = (friend.url, religion, mutual_count, mutual_count)
            mycursor.execute(sql, val)
    if religion_max_inf and religion_max_inf != "no_data" and religion_max>1:
        sql = "INSERT INTO attribute_count (attribute, category, inf_count) VALUES (%s, 'religion', %s) ON DUPLICATE KEY UPDATE inf_count=inf_count+%s"
        val = (religion_max_inf, one, one)
        mycursor.execute(sql, val)

    politic_max = 0
    politic_max_inf = None
    for politic in friend.inference_count["politicalviews"] or friend.attributes['contact and basic']['basic_info']["politicalviews"]!="NA":
        if politic=="no_data":
            continue
        mutual_count = len(friend.inference_count["politicalviews"][politic])
        if mutual_count > politic_max:
            politic_max = mutual_count
            politic_max_inf = politic
        if mutual_count:
            sql = "INSERT INTO politics_inf (friend_url, political_view, mutual_count) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE mutual_count=mutual_count+%s"
            val = (friend.url, politic, mutual_count, mutual_count)
            mycursor.execute(sql, val)
    if politic_max_inf and politic_max_inf != "no_data" and politic_max>1:
        sql = "INSERT INTO attribute_count (attribute, category, inf_count) VALUES (%s, 'politics', %s) ON DUPLICATE KEY UPDATE inf_count=inf_count+%s"
        val = (politic_max_inf, one, one)
        mycursor.execute(sql, val)

    sql = "INSERT INTO friend_inf (friend_url, work_inf, college_inf, high_school_inf, places_lived_inf, religion_inf, politic_inf) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (friend.url, work_max_inf, college_max_inf, hs_max_inf, city_max_inf, religion_max_inf, politic_max_inf)
    mycursor.execute(sql, val)

    mydb.commit()

def insert_attribute_count(mydb, mycursor, attribute, category_name, count):
    sql = "INSERT INTO attribute_count (attribute, category, mutual_count) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE mutual_count=mutual_count+%s"
    val = (attribute, category_name, count, count)
    mycursor.execute(sql, val)
    mydb.commit()

def insert_all_attribute(category_groups, mydb, mycursor):
    for category_name, data in category_groups.items():
        if category_name=="highschool":
            category = "high_school"
        elif category_name=="cities":
            category = "places_lived"
        elif category_name=="religiousviews":
            category = "religion"
        elif category_name=="politicalviews":
            category = "politics"
        else:
            category = category_name
        for attribute, url_list in data.items():
            if "no_data" in attribute:
                continue
            insert_attribute_count(mydb, mycursor, attribute, category, len(url_list))

def make_mutual_count(mydb, mycursor):
    sql = "INSERT INTO mutual_count SELECT * FROM\
        (SELECT friend_url, college_name AS attribute, 'college' AS category, mutual_count FROM college_inf WHERE college_name<>'no_data' UNION ALL\
        SELECT friend_url, hs_name AS attribute, 'high_school' AS category, mutual_count FROM high_school_inf WHERE hs_name<>'no_data' UNION ALL\
        SELECT friend_url, location AS attribute, 'places_lived' AS category, mutual_count FROM places_lived_inf WHERE location<>'no_data' UNION ALL\
        SELECT friend_url, political_view AS attribute, 'politics' AS category, mutual_count FROM politics_inf WHERE political_view<>'no_data' UNION ALL\
        SELECT friend_url, religious_belief AS attribute, 'religion' AS category, mutual_count FROM religion_inf WHERE religious_belief<>'no_data' UNION ALL\
        SELECT friend_url, workplace AS attribute, 'work' AS category, mutual_count FROM work_inf WHERE workplace<>'no_data'\
        ORDER BY mutual_count) a;"
    mycursor.execute(sql)
    mydb.commit()
