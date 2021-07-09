from time import sleep
from fbdriver import FBdriver
from friend import Friend
import urllib
import random
from collections import Counter

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

path_to_chrome_driver = "C:\\Users\\tanst\\chromedriver.exe"
username = "sttan@ucsd.edu"
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

# fetching all url paths to the user's friends' profiles
friends = driver.full_friend_lookup_table()

for p, f in friends.items():
    f.name = driver.scrape_name(f)
    f.mutual_friends = driver.full_mutual_friend_list(f)
    (f.attributes["work"], f.attributes["college"], f.attributes["highschool"], f.profile_picture_url) = driver.scrape_work_and_ed(f)
    #key_value_pairs["work and ed"].extend(f.attributes["work and ed"])
    f.attributes["places lived"] = driver.scrape_places_lived(f)
    #key_value_pairs["places lived"].extend(f.attributes["places lived"])
    f.attributes["contact and basic"] = driver.scrape_contact_and_basic(f)
    #key_value_pairs["contact and basic"].extend(f.attributes["contact and basic"])
    f.attributes["family and rel"] = driver.scrape_family_and_rel(f)
    #key_value_pairs["family and rel"].extend(f.attributes["family and rel"])
participant = Friend(driver.participant_path)
participant.attributes["work and ed"] = driver.scrape_work_and_ed(participant)
#key_value_pairs["work and ed"].extend(participant.attributes["work and ed"])
participant.attributes["places lived"] = driver.scrape_places_lived(participant)
#key_value_pairs["places lived"].extend(participant.attributes["places lived"])
participant.attributes["contact and basic"] = driver.scrape_contact_and_basic(participant)
#key_value_pairs["contact and basic"].extend(participant.attributes["work and ed"])
participant.attributes["family and rel"] = driver.scrape_family_and_rel(participant)
#key_value_pairs["family and rel"].extend(participant.attributes["family and rel"])

# keep key value pairs that appear at least 3 times
place_counts = Counter(key_value_pairs["places lived"])
key_value_pairs["places lived"] = []
for place, count in place_counts.items():
    if count >= 3 and place is not None:
        key_value_pairs["places lived"].append(place)

inferences = generate_inferences(friends, participant, key_value_pairs)

data_to_send = {
    "friends": [f.attributes for f in friends.values()],
    "inferences": inferences
}

querystring = urllib.parse.urlencode(data_to_send)
driver.get(f'http://127.0.0.1:5000/go?{querystring}') # flask app

driver.execute_script("alert('Finished!');")
