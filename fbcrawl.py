from time import sleep
from fbdriver import FBdriver
from friend import Friend
import urllib
import random
from collections import Counter
import time
import pprint

from fbInferences import compute_frequency_category_data

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

def generate_inferences(friends, participant, key_value_pairs):
    total_friends = len(friends.keys())
    inferences = []
    # this double for loop might be too slow and is not necessarily the best
    # approach but it's a starting point
    for k, v in key_value_pairs.items():
        for friend in friends.values():
            if infer(friend, k, v, participant, friend.mutual_friends, total_friends):
                inferences.append((friend.name, k, v))
    return inferences

#-------------------------------------------------------------------------------

path_to_chrome_driver = "/Users/aaron/opt/WebDriver/bin/chromedriver"
username = "aaronbroukhim@aol.com"
url = "https://mobile.facebook.com/home.php"

driver = FBdriver(executable_path=path_to_chrome_driver)
driver.set_page_load_timeout(60)
driver.implicitly_wait(10)
driver.login(url, username) # type pw manually

key_value_pairs = {
    "work and ed": [],
    "places lived": [],
    "contact and basic": [],
    "family and rel": []
}

category_groups = {
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
    "religious_views": {
        "no_data": []
    },
    "political_views": {
        "no_data": []
    },
    "birthyear": {
        "no_data": []
    },
}

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

total_time = time.time()
# fetching all url paths to the user's friends' profiles
friends = driver.full_friend_lookup_table()
#scrape users friends info
c = 0
for p, f in friends.items():
    try:
        #to check runtime
        start_time = time.time()
        #completion count is out of 8
        #total count is out of 14
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
        populate_category_groups(f.attributes["contact and basic"]["basic_info"]["religiousviews"], f.url, "religious_views")
        populate_category_groups(f.attributes["contact and basic"]["basic_info"]["politicalviews"], f.url, "political_views")
        populate_category_groups(f.attributes["contact and basic"]["basic_info"]["birthyear"], f.url, "birthyear")
        (tempCount, count, f.attributes["family and rel"]) = driver.scrape_family_and_rel(f)
        f.percent_complete+=count
        f.percent_total_complete+=f.percent_complete
        f.percent_total_complete+=tempCount
        f.percent_complete = round(f.percent_complete/8, 3)
        f.percent_total_complete = round(f.percent_total_complete/14, 3)
        print(f.name)
        print(f.percent_complete, f.percent_total_complete)
        print(len(f.mutual_friends))
        print("--- %s seconds ---" % (time.time() - start_time))
        c+=1
        if c == 2:
            pprint.pprint(compute_frequency_category_data(category_groups))
            break
    except:
        print(compute_frequency_category_data(category_groups))
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
populate_category_groups(participant.attributes["contact and basic"]["basic_info"]["religiousviews"], participant.url, "religious_views")
populate_category_groups(participant.attributes["contact and basic"]["basic_info"]["politicalviews"], participant.url, "political_views")
populate_category_groups(participant.attributes["contact and basic"]["basic_info"]["birthyear"], participant.url, "birthyear")
(tempCount, count, participant.attributes["family and rel"]) = driver.scrape_family_and_rel(participant)
participant.percent_total_complete+=tempCount
participant.percent_complete+=count
participant.percent_total_complete+=participant.percent_complete
participant.percent_complete/=9
participant.percent_complete = round(participant.percent_complete/8, 3)
participant.percent_total_complete = round(participant.percent_total_complete/14, 3)
#print(category_groups)
print("total runtime")
print("--- %s seconds ---" % (time.time() - total_time))

# keep key value pairs that appear at least 3 times
#place_counts = Counter(key_value_pairs["places lived"])
#key_value_pairs["places lived"] = []
#for place, count in place_counts.items():
#    if count >= 3 and place is not None:
#        key_value_pairs["places lived"].append(place)

inferences = generate_inferences(friends, participant, key_value_pairs)

data_to_send = {
    "friends": [f.attributes for f in friends.values()],
    "inferences": inferences
}

querystring = urllib.parse.urlencode(data_to_send)
driver.get(f'http://127.0.0.1:5000/go?{querystring}') # flask app

driver.execute_script("alert('Finished!');")