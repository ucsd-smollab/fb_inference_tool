from time import sleep
from fbdriver import FBdriver
from friend import Friend
import urllib
import random
from collections import Counter
import time
import copy
import pprint

from fbInferences import compute_frequency_category_data, get_list_of_people

# Some helpful resources I consulted:
# https://medium.com/@ali.raza.nisar/crawling-your-facebook-friends-data-31a2d8fc0c6d
# https://medium.com/analytics-vidhya/the-art-of-not-getting-blocked-how-i-used-selenium-python-to-scrape-facebook-and-tiktok-fd6b31dbe85f
# https://selenium-python.readthedocs.io/

def infer(friend, key, value, participant, mutual_friends, total_friends):
    # INPUTS:
    # friend -  Friend object
    # key - string (e.g. "places", "religion")
    # value - string (e.g. "San Diego")
    # participant - Friend object
    # mutual_friends - list of Friend objects (mutuals of participant & friend)
    # total_friends - int (total number of participants' friends),
    # RETURN: True or False
    # (to indicate whether or not we think this friend has lived in San Diego)
    return random.choice([True, False]) # placeholder

# def generate_inferences(friends, participant, key_value_pairs):
#     total_friends = len(friends.keys())
#     inferences = []
#     # this double for loop might be too slow and is not necessarily the best
#     # approach but it's a starting point
#     for k, v in key_value_pairs.items():
#         for friend in friends.values():
#             if infer(friend, k, v, participant, friend.mutual_friends, total_friends):
#                 inferences.append((friend.name, k, v))
#     return inferences

#-------------------------------------------------------------------------------

path_to_chrome_driver = "/Users/aaron/opt/WebDriver/bin/chromedriver"
username = "aaronbroukhim@aol.com"
url = "https://mobile.facebook.com/home.php"

driver = FBdriver(executable_path=path_to_chrome_driver)
driver.set_page_load_timeout(60)
driver.implicitly_wait(10)
driver.login(url, username) # type pw manually

category_groups_template = {
    "work": {
        "no_data": []
    },
    "college": {
        "no_data": []
    },
    "highschool": {
        "no_data": []
    },
    "cities": {
        "no_data": []
    },
    "religiousviews": {
        "no_data": []
    },
    "politicalviews": {
        "no_data": []
    },
    "birthyear": {
        "no_data": []
    },
}

category_groups = copy.deepcopy(category_groups_template)

def populate_category_groups(data, person_url, category_name):
    if data == "NA":
        category_groups[category_name]["no_data"].append(person_url)
        return
    if not isinstance(data, list):
        if data in category_groups[category_name]:
            category_groups[category_name][data].append(person_url)
        else:
            category_groups[category_name][data] = [person_url]
        return
    for entry in data:
        entry_name = entry
        if isinstance(entry, dict):
            entry_name = entry["title"]
        if entry_name in category_groups[category_name]:
            category_groups[category_name][entry_name].append(person_url)
        else:
            category_groups[category_name][entry_name] = [person_url]

#keep track of time
total_time = time.time()
# fetching all url paths to the user's friends' profiles
friends = driver.full_friend_lookup_table()
#scrape users friends info
c = 0
for p, f in friends.items():
    f.name = driver.scrape_name(f)
    f.mutual_friends = driver.full_mutual_friend_list(f)
    try:
        # to check runtime
        start_time = time.time()
        # completion count is out of 8
        # total count is out of 14
        count = 0
        f.name = driver.scrape_name(f)
        f.mutual_friends = driver.full_mutual_friend_list(f)
        (count, f.attributes["work"], f.attributes["college"], f.attributes["highschool"], f.profile_picture_url) = driver.scrape_work_and_ed(f)
        f.percent_complete+=count    
        populate_category_groups(f.attributes["work"], f.url, "work")
        populate_category_groups(f.attributes["college"], f.url, "college")
        populate_category_groups(f.attributes["highschool"], f.url, "highschool")
        (count, f.attributes["places lived"]) = driver.scrape_places_lived(f)
        f.percent_complete+=count    
        populate_category_groups(f.attributes["places lived"]["list_of_cities"], f.url, "cities")
        (f.percent_total_complete, count, f.attributes["contact and basic"]) = driver.scrape_contact_and_basic(f)
        populate_category_groups(f.attributes["contact and basic"]["basic_info"]["religiousviews"], f.url, "religiousviews")
        populate_category_groups(f.attributes["contact and basic"]["basic_info"]["politicalviews"], f.url, "politicalviews")
        populate_category_groups(f.attributes["contact and basic"]["basic_info"]["birthyear"], f.url, "birthyear")
        (tempCount, count, f.attributes["family and rel"]) = driver.scrape_family_and_rel(f)
        f.percent_complete+=count
        f.percent_total_complete+=f.percent_complete
        f.percent_total_complete+=tempCount
        f.percent_complete = round(f.percent_complete/8, 3)
        f.percent_total_complete = round(f.percent_total_complete/14, 3)
        #print("name")
        #print(f.name)
        #print("inference complete, total complete")
        #print(f.percent_complete, f.percent_total_complete)
        #print(len(f.mutual_friends))
        #print(f.mutual_friends)
        #print("--- %s seconds ---" % (time.time() - start_time))
        c+=1
        if c == 1:
            #pprint.pprint(compute_frequency_category_data(category_groups))
            break
    except:
        print("exception error")
        print(f.name)
        break

#scrape user info
participant = Friend(driver.participant_path)
(count, participant.attributes["work"], participant.attributes["college"], participant.attributes["highschool"], participant.profile_picture_url) = driver.scrape_work_and_ed(participant)
participant.percent_complete+=count
populate_category_groups(participant.attributes["work"], participant.url, "work")
populate_category_groups(participant.attributes["college"], participant.url, "college")
populate_category_groups(participant.attributes["highschool"], participant.url, "highschool")
(count, participant.attributes["places lived"]) = driver.scrape_places_lived(participant)
participant.percent_complete+=count
populate_category_groups(participant.attributes["places lived"]["list_of_cities"], participant.url, "cities")
(participant.percent_total_complete, count, participant.attributes["contact and basic"]) = driver.scrape_contact_and_basic(participant)
participant.percent_complete+=count
populate_category_groups(participant.attributes["contact and basic"]["basic_info"]["religiousviews"], participant.url, "religiousviews")
populate_category_groups(participant.attributes["contact and basic"]["basic_info"]["politicalviews"], participant.url, "politicalviews")
populate_category_groups(participant.attributes["contact and basic"]["basic_info"]["birthyear"], participant.url, "birthyear")
#(tempCount, count, participant.attributes["family and rel"]) = driver.scrape_family_and_rel(participant)
#participant.percent_total_complete+=tempCount
participant.percent_complete+=count
participant.percent_total_complete+=participant.percent_complete
participant.percent_complete = round(participant.percent_complete/8, 3)
participant.percent_total_complete = round(participant.percent_total_complete/14, 3)
# print(category_groups)
# print(f"number of freinds: {c}")
# print("total runtime")
# print("--- %s seconds ---" % (time.time() - total_time))

#make inferences

'''
look through each friends dcitionary
 - key/value pair is url/friend object pair
    create a temp category groups object
 - go thru each category section and finding the length of the lists where the friend's 
    mutual friends list intersects with the value list for that specific category data
 - make inferences after the calculating frequency of intersected data for each category

for in friends
    initialize temp category obj
    for category in category groups
        for dataentry in category
            add mutual friend url to category
'''
for url, friend in friends.items():
    category_frequency_data = copy.deepcopy(category_groups_template)
    for category, category_data in category_groups.items():
        for name, list_of_urls in category_data.items():
            category_frequency_data[category][name] = get_list_of_people(friend.mutual_friends, url, participant.url, category, name, list_of_urls)
    friend.inference_count = category_frequency_data
#print(friends['danielnewman21'].inference_count)


#inferences = generate_inferences(friends, participant, key_value_pairs)
inferences = []
data_to_send = {
    "friends": [f.attributes for f in friends.values()],
    "inferences": inferences
}

querystring = urllib.parse.urlencode(data_to_send)
driver.get(f'http://127.0.0.1:5000/go?{querystring}') # flask app

driver.execute_script("alert('Finished!');")