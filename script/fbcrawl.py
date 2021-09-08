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
from fbInferences import get_list_of_people, generate_inferences, generate_inferences_ranking

# Some helpful resources I consulted:
# https://medium.com/@ali.raza.nisar/crawling-your-facebook-friends-data-31a2d8fc0c6d
# https://medium.com/analytics-vidhya/the-art-of-not-getting-blocked-how-i-used-selenium-python-to-scrape-facebook-and-tiktok-fd6b31dbe85f
# https://selenium-python.readthedocs.io/
#-------------------------------------------------------------------------------
#this branch should be refactored to store in a database
path_to_chrome_driver = "/Users/aaron/opt/WebDriver/bin/chromedriver"
username = "aaronbroukhim@aol.com"
url = "https://mobile.facebook.com/home.php"

driver = FBdriver(executable_path=path_to_chrome_driver)
driver.set_page_load_timeout(60)
#5 should work on fast computers, increase if getting unable to locate element errors
driver.implicitly_wait(10)
driver.login(url, username) # type pw manually

#keep track of time
total_time = time.time()

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
    if "category_groups" in old_data:
        category_groups = old_data["category_groups"]

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

#manual override if didnt scrape properly
#prev_friends_scraped = 250
exception_list = []
friends_with_most_data = []
friends_with_least_data = []
num_friends_scraped = 0
num_to_scrape = 15 #len(friends) for all
num_mutual_pages = -1 #-1 for all, otherwise a 8* will be number of friends scraped
num_mutuals_inf = 100 #-1 for all, otherwise sets mutuals to make inferences on
time_df = pd.DataFrame(columns=[str(num_mutual_pages)+" pages", "Word and ed", \
"Places lived", "contact and basic info", "friend total time"])
print(f"friends scraped from pickle: {prev_friends_scraped}")
#scrape friends
for p, f in friends.items():
    try:
        start_time = time.time()
        #update data with old
        if num_friends_scraped < prev_friends_scraped:
            if not f.name or num_friends_scraped>=num_to_scrape:
                continue
            f = old_data["friends"][p]
            # time_df.loc[len(time_df.index)] = f.time_array
            print(num_friends_scraped)        
            print(f.name)
            print(f"Actual Mutual Friends: {f.numMutualFriends}")
            print(f"Scraped Mutual Friends: {len(f.mutual_friends)}")
            print("---------")
            num_friends_scraped+=1

            friends_with_least_data.append([f.url, f.percent_total_complete, f.numMutualFriends])
            friends_with_most_data.append([f.url, f.percent_total_complete, f.numMutualFriends])
            if len(friends_with_least_data) > 5:
                friends_with_least_data = sorted(friends_with_least_data, key=lambda ele: (ele[1], -ele[2]))
                friends_with_least_data.pop(-1)

            if len(friends_with_most_data) > 5:
                friends_with_most_data = sorted(friends_with_most_data, reverse=True, key=lambda ele: (ele[1], ele[2]))
                friends_with_most_data.pop(-1)

            print(f"least: {friends_with_least_data}")
            print(f"most: {friends_with_most_data}")

            #updating local data, breaking after number of friends achieved
            # file = open("file.pkl","wb")
            # formatted_data = {
            #     "count": num_friends_scraped,
            #     "friends": friends,
            #     "participant": participant,
            #     "category_groups": category_groups,
            #     "time_df": time_df
            # }
            # pickle.dump(formatted_data, file)
            continue
        if num_friends_scraped >= num_to_scrape:
            break
        #get current friend data, mutual friends in batches of 8
        f.time_array = scrape_friend_info(f, num_mutual_pages, category_groups, driver)
        if not f.time_array:
            driver.get("http://facebook.com")
            f.name = ""
            continue
        populate_category_groups_funct(f, category_groups)

        friends_with_least_data.append([f.url, f.percent_total_complete, f.numMutualFriends])
        friends_with_most_data.append([f.url, f.percent_total_complete, f.numMutualFriends])
        if len(friends_with_least_data) > 5:
            friends_with_least_data = sorted(friends_with_least_data, key=lambda ele: (ele[1], -ele[2]))
            friends_with_least_data.pop(-1)

        if len(friends_with_most_data) > 5:
            friends_with_most_data = sorted(friends_with_most_data, reverse=True, key=lambda ele: (ele[1], ele[2]))
            friends_with_most_data.pop(-1)
        
        print(f"least: {friends_with_least_data}")
        print(f"most: {friends_with_most_data}")

        # print(num_friends_scraped)
        # print(f.name)
        # print(f"Actual Mutual Friends: {f.numMutualFriends}")
        # print(f"Scraped Mutual Friends: {len(f.mutual_friends)}")
        # print("---------")
        num_friends_scraped+=1
        #print time and append time array to df
        #print("friend total time: "+str(time.time()-start_time))
        #print("-------NEW FRIEND-------")
        f.time_array.append(float(time.time()-start_time))
        time_df.loc[len(time_df.index)] = f.time_array
        #updating local data, breaking after number of friends achieved
        # file = open("file.pkl","wb")
        # formatted_data = {
        #     "count": num_friends_scraped,
        #     "friends": friends,
        #     "participant": participant,
        #     "category_groups": category_groups,
        #     "time_df": time_df
        # }
        # pickle.dump(formatted_data, file)
        # file.close()
    except:
        print(f"exception: {f.url}")
        print("---------")
        exception_list.append(f.url)


print("Begin Postprocessing")
post_time = time.time()
print(f"exception list: {exception_list}")
print(f"number of friends scraped: {num_friends_scraped}")
print("total runtime: "+str(time.time() - total_time))
print("time averages: ")
time_df.loc['mean'] = time_df.mean()
print(time_df.loc['mean'])
time_df.to_csv(str(num_friends_scraped)+"friends_"+str(8*num_mutual_pages)+"mutuals.csv")

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
inference_count_dict = {
    "Not Scraped": 0,
    "Has Ground Truth": {
        "work": {
            "Right": 0,
            "Tie": 0,
            "Wrong": 0,
            "Below Threshold": 0,
            "No Data": 0,
            "Accuracy": 0,
            "Sorted Accuracy": 0,

        },
        "college": {
            "Right": 0,
            "Tie": 0,
            "Wrong": 0,
            "Below Threshold": 0,
            "No Data": 0,
            "Accuracy": 0,
            "Sorted Accuracy": 0,
        },
        "highschool": {
            "Right": 0,
            "Tie": 0,
            "Wrong": 0,
            "Below Threshold": 0,
            "No Data": 0,
            "Accuracy": 0,
            "Sorted Accuracy": 0,
        },
        "cities": {
            "Right": 0,
            "Tie": 0,
            "Wrong": 0,
            "Below Threshold": 0,
            "No Data": 0,
            "Accuracy": 0,
            "Sorted Accuracy": 0,
        },
        "religiousviews": {	
            "Right": 0,
            "Tie": 0,
            "Wrong": 0,
            "Below Threshold": 0,
            "No Data": 0,
            "Accuracy": 0,
            "Sorted Accuracy": 0,
        },
        "politicalviews": {
            "Right": 0,
            "Tie": 0,
            "Wrong": 0,
            "Below Threshold": 0,
            "No Data": 0,
            "Accuracy": 0,
            "Sorted Accuracy": 0,
        },
        "birthyear": {
            "Right": 0,
            "Tie": 0,
            "Wrong": 0,
            "Below Threshold": 0,
            "No Data": 0,
            "Accuracy": 0,
            "Sorted Accuracy": 0,
        },
    },
    "No Ground Truth": {
        "work": {
            "Tie": 0,
            "Below Threshold": 0,
            "No Data": 0,
        },
        "college": {
            "Tie": 0,
            "Below Threshold": 0,
            "No Data": 0,
        },
        "highschool": {
            "Tie": 0,
            "Below Threshold": 0,
            "No Data": 0
        },
        "cities": {
            "Tie": 0,
            "Below Threshold": 0,
            "No Data": 0
        },
        "religiousviews": {	
            "Tie": 0,
            "Below Threshold": 0,
            "No Data": 0
        },
        "politicalviews": {
            "Tie": 0,
            "Below Threshold": 0,
            "No Data": 0
        },
        "birthyear": {
            "Tie": 0,
            "Below Threshold": 0,
            "No Data": 0
        },
    },
    "totals": {
        "total right": 0,
        "total wrong": 0,
        "total tie": 0,
        "total below threshold": 0,
        "total no data": 0,
    },
    "percentages": {
        "total right": 0,
        "total wrong": 0,
        "total tie": 0,
        "total below threshold": 0,
        "total no data": 0,
        "right/rwt": 0,
        "wrong/rwt": 0,
        "tie/rwt": 0,
    },
    "avg confidence percentage": {
        "right": 0,
        "wrong": 0,
    },
}

for url, friend in friends.items():
    category_frequency_data = copy.deepcopy(category_groups_template)
    for category, category_data in category_groups.items():
        for name, list_of_urls in category_data.items():
            category_frequency_data[category][name] = list(set(get_list_of_people(friend.mutual_friends, participant.url, list_of_urls, num_mutuals_inf)))
    friend.inference_count = category_frequency_data

generate_inferences_ranking(friends, participant, inference_count_dict)
pprint.pprint(inference_count_dict)
with open(str(num_friends_scraped)+"friends_"+str(num_mutuals_inf)+"mutuals_inferences.json", "w") as outfile:
    json.dump(inference_count_dict, outfile)

post_time_total = time.time()-post_time
print(f"finished postprocessing{post_time_total}")

inferences = []
data_to_send = {
    "friends": [f.attributes for f in friends.values()],
    "inferences": inferences
}

querystring = urllib.parse.urlencode(data_to_send)
driver.get(f'http://127.0.0.1:5000/go?{querystring}') # flask app

driver.execute_script("alert('Finished!');")