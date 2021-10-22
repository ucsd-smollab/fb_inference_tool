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
    # pprint.pprint(friend.inference_count)
    for work in friend.inference_count["work"]:
        mutual_count = len(friend.inference_count["work"][work])
        if mutual_count:
            sql = "INSERT INTO work_inf (friend_url, workplace, mutual_count) VALUES (%s, %s, %s)"
            val = (friend.url, work, mutual_count)
            mycursor.execute(sql, val)

    for college in friend.inference_count["college"]:
        mutual_count = len(friend.inference_count["college"][college])
        if mutual_count:
            sql = "INSERT INTO college_inf (friend_url, college_name, mutual_count) VALUES (%s, %s, %s)"
            print(friend.url, college, mutual_count)
            val = (friend.url, college, mutual_count)
            mycursor.execute(sql, val)

    for hs in friend.inference_count["highschool"]:
        mutual_count = len(friend.inference_count["highschool"][hs])
        if mutual_count:
            sql = "INSERT INTO high_school_inf (friend_url, hs_name, mutual_count) VALUES (%s, %s, %s)"
            val = (friend.url, hs, mutual_count)
            mycursor.execute(sql, val)

    for city in friend.inference_count["cities"]:
        mutual_count = len(friend.inference_count["cities"][city])
        if mutual_count:
            sql = "INSERT INTO places_lived_inf (friend_url, location, mutual_count) VALUES (%s, %s, %s)"
            val = (friend.url, city, mutual_count)
            mycursor.execute(sql, val)

    for religion in friend.inference_count["religiousviews"]:
        mutual_count = len(friend.inference_count["religiousviews"][religion])
        if mutual_count:
            sql = "INSERT INTO religion_inf (friend_url, religious_belief, mutual_count) VALUES (%s, %s, %s)"
            val = (friend.url, religion, mutual_count)
            mycursor.execute(sql, val)

    for politic in friend.inference_count["politicalviews"]:
        mutual_count = len(friend.inference_count["politicalviews"][politic])
        if mutual_count:
            sql = "INSERT INTO politics_inf (friend_url, political_view, mutual_count) VALUES (%s, %s, %s)"
            val = (friend.url, politic, mutual_count)
            mycursor.execute(sql, val)
    mydb.commit()