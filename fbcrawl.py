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
    "places": [],
    "religion": [],
}

# fetching all url paths to the user's friends' profiles
friends = driver.full_friend_lookup_table()

for p, f in friends.items():
    f.attributes["places"] = driver.scrape_places_lived(f)
    f.attributes["religion"] = driver.scrape_religion(f)
    key_value_pairs["places"].extend(f.attributes["places"])
    key_value_pairs["religion"].append(f.attributes["religion"])
    f.mutual_friends = driver.full_mutual_friend_list(f)
    f.name = driver.scrape_name(f)
participant = Friend(driver.participant_path)
participant.attributes["places"] = driver.scrape_places_lived(participant)
participant.attributes["religion"] = driver.scrape_religion(participant)
key_value_pairs["places"].extend(participant.attributes["places"])
key_value_pairs["religion"].append(participant.attributes["religion"])

# keep key value pairs that appear at least 3 times
place_counts = Counter(key_value_pairs["places"])
key_value_pairs["places"] = []
for place, count in place_counts.items():
    if count >= 3 and place is not None:
        key_value_pairs["places"].append(place)
religion_counts = Counter(key_value_pairs["religion"])
key_value_pairs["religion"] = []
for religion, count in religion_counts.items():
    if count >= 3 and religion is not None:
        key_value_pairs["religion"].append(religion)

inferences = generate_inferences(friends, participant, key_value_pairs)

data_to_send = {
    "friends": [f.attributes for f in friends.values()],
    "inferences": inferences
}

querystring = urllib.parse.urlencode(data_to_send)
driver.get(f'http://127.0.0.1:5000/go?{querystring}') # flask app

driver.execute_script("alert('Finished!');")
