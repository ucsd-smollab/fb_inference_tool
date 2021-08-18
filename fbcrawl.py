from time import sleep
from pandas.core.indexes.base import Index
from fbdriver import *
from friend import Friend
import urllib
import random
from collections import Counter
import time
import copy
import pprint
import json
import pickle
import pandas as pd
from fbInferences import compute_frequency_category_data, get_list_of_people, generate_inferences, infer

# Some helpful resources I consulted:
# https://medium.com/@ali.raza.nisar/crawling-your-facebook-friends-data-31a2d8fc0c6d
# https://medium.com/analytics-vidhya/the-art-of-not-getting-blocked-how-i-used-selenium-python-to-scrape-facebook-and-tiktok-fd6b31dbe85f
# https://selenium-python.readthedocs.io/
#-------------------------------------------------------------------------------

path_to_chrome_driver = "C:\\Users\\tanst\\chromedriver.exe"
username = "aaronbroukhim@aol.com"
url = "https://mobile.facebook.com/home.php"

driver = FBdriver(executable_path=path_to_chrome_driver)
driver.set_page_load_timeout(60)
#5 should work on fast computers, increase if getting Unable to locate element errors
driver.implicitly_wait(5)
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

inference_count_dict = {
    "Right": 0,
    "Wrong": 0,
    "Tie": 0,
    "No Data": 0,
    "Not Scraped": 0,
    "Below Threshold": 0
}

#keep track of time
total_time = time.time()

#load in previously scraped data
objects = []
try:
    with (open("file.pkl", "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    print("Found pickle file")
except:
    print("No pickle file")
old_data = {}
prev_friends_scraped = 0
if objects:
    old_data = objects[0]
    if "count" in old_data:
        prev_friends_scraped = old_data["count"]

#scrape user info
if not old_data and not "participant" in old_data:
    participant = get_participant_data(category_groups, driver)
else:
    participant = old_data["participant"]

#fetching all url paths to the user's friends' profiles
if not old_data and not "friends" in old_data:
    #change value to limit number of pages loaded for friends
    friends = driver.full_friend_lookup_table(-1)
else:
    friends = old_data["friends"]

#table of times
time_df = pd.DataFrame(columns=["mutual friends", "Word and ed", "Places lived", \
"contact and basic info", "relationship and family", "total time"])

num_friends_scraped = 0
num_to_scrape = 1000
#manual override if didnt scrape properly
#prev_friends_scraped = 60
num_mutual_pages = -1 #-1 for all, otherwise a 8* will be number of friends scraped
time_df = pd.DataFrame(columns=[str(num_mutual_pages*8)+" mutual friends", "Word and ed", \
"Places lived", "contact and basic info", "friend total time"])
print(f"friends scraped from pickle: {prev_friends_scraped}")
#scrape friends
for p, f in friends.items():
    start_time = time.time()
    #update data with old
    if num_friends_scraped < prev_friends_scraped:
        f = old_data["friends"][p]
        print(num_friends_scraped)        
        print(f.name)
        # print(f.url)
        print(f"Actual Mutual Friends: {f.numMutualFriends}")
        print(f"Scraped Mutual Friends: {len(f.mutual_friends)}")
        # pprint.pprint(f.attributes)
        # print("---------")
        num_friends_scraped+=1
        continue
    if num_friends_scraped >= num_to_scrape:
        break
    #get current friend data, mutual friends in batches of 8
    time_array = scrape_friend_info(f, num_mutual_pages, category_groups, driver)
    mutual_tries = 0
    if f.numMutualFriends > 0:
        while len(f.mutual_friends)/f.numMutualFriends < 0.6:
            if mutual_tries >= 10:
                break
            f.mutual_friends, temp = driver.full_mutual_friend_list(f, num_mutual_pages)
            mutual_tries+=1
    print(num_friends_scraped)
    print(f.name)
    print(f"Actual Mutual Friends: {f.numMutualFriends}")
    print(f"Scraped Mutual Friends: {len(f.mutual_friends)}")
    num_friends_scraped+=1
    #print time and append time array to df
    #print("friend total time: "+str(time.time()-start_time))
    #print("-------NEW FRIEND-------")
    time_array.append(float(time.time()-start_time))
    time_df.loc[len(time_df.index)] = time_array
    #updating local data, breaking after number of friends achieved
    file = open("file.pkl","wb")
    formatted_data = {
        "count": num_friends_scraped,
        "friends": friends,
        "participant": participant
    }
    pickle.dump(formatted_data, file)
    file.close()

print(f"number of friends scraped: {num_friends_scraped}")
print("total runtime: "+str(time.time() - total_time))
print("time averages: ")
time_df.loc['mean'] = time_df.mean()
print(time_df.loc['mean'])
time_df.to_csv("20friends_160mutual_nourls.csv")

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
            category_frequency_data[category][name] = get_list_of_people(friend.mutual_friends, participant.url, list_of_urls)
    friend.inference_count = category_frequency_data

generate_inferences(friends, participant, inference_count_dict)
pprint.pprint(inference_count_dict)

#inferences = generate_inferences(friends, participant, key_value_pairs)
inferences = []
data_to_send = {
    "friends": [f.attributes for f in friends.values()],
    "inferences": inferences
}

querystring = urllib.parse.urlencode(data_to_send)
driver.get(f'http://127.0.0.1:5000/go?{querystring}') # flask app

driver.execute_script("alert('Finished!');")