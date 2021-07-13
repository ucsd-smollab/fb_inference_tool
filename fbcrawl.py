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

path_to_chrome_driver = "C:\\Users\\tanst\\chromedriver"
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

# fetching all url paths to the user's friends' profiles
friends = driver.full_friend_lookup_table()

for p, f in friends.items():
    #completion count is out of 9
    f.name = driver.scrape_name(f)
    f.mutual_friends = driver.full_mutual_friend_list(f)
    (count, f.attributes["work"], f.attributes["college"], f.attributes["highschool"], f.profile_picture_url) = driver.scrape_work_and_ed(f)
    f.percent_complete+=count    
    populate_category_groups(f.attributes["work"], f.url, "work")
    populate_category_groups(f.attributes["college"], f.url, "college")
    populate_category_groups(f.attributes["highschool"], f.url, "highschool")
    #key_value_pairs["work and ed"].extend(f.attributes["work and ed"])
    (count, f.attributes["places lived"]) = driver.scrape_places_lived(f)
    f.percent_complete+=count    
    populate_category_groups(f.attributes["places lived"]["list_of_cities"], f.url, "cities")
    #key_value_pairs["places lived"].extend(f.attributes["places lived"])
    (count, f.attributes["contact and basic"]) = driver.scrape_contact_and_basic(f)
    f.percent_complete+=count    
    populate_category_groups(f.attributes["contact and basic"]["basic_info"]["religiousviews"], f.url, "religious_views")
    populate_category_groups(f.attributes["contact and basic"]["basic_info"]["politicalviews"], f.url, "political_views")
    populate_category_groups(f.attributes["contact and basic"]["basic_info"]["birthyear"], f.url, "birthyear")
    #key_value_pairs["contact and basic"].extend(f.attributes["contact and basic"])
    #(count, f.attributes["family and rel"]) = driver.scrape_family_and_rel(f)
    f.percent_complete+=count
    f.percent_complete/=9
    print(f'{f.name} - {f.percent_complete}%')
    #key_value_pairs["family and rel"].extend(f.attributes["family and rel"])


participant = Friend(driver.participant_path)
(count, participant.attributes["work"], participant.attributes["college"], participant.attributes["highschool"], participant.profile_picture_url) = driver.scrape_work_and_ed(participant)
participant.percent_complete+=count
populate_category_groups(participant.attributes["work"], participant.url, "work")
populate_category_groups(participant.attributes["college"], participant.url, "college")
populate_category_groups(participant.attributes["highschool"], participant.url, "highschool")
#key_value_pairs["work and ed"].extend(participant.attributes["work and ed"])
(count, participant.attributes["places lived"]) = driver.scrape_places_lived(participant)
participant.percent_complete+=count
populate_category_groups(participant.attributes["places lived"]["list_of_cities"], participant.url, "cities")
#key_value_pairs["places lived"].extend(participant.attributes["places lived"])
(count, participant.attributes["contact and basic"]) = driver.scrape_contact_and_basic(participant)
participant.percent_complete+=count
populate_category_groups(participant.attributes["contact and basic"]["basic_info"]["religiousviews"], participant.url, "religious_views")
populate_category_groups(participant.attributes["contact and basic"]["basic_info"]["politicalviews"], participant.url, "political_views")
populate_category_groups(participant.attributes["contact and basic"]["basic_info"]["birthyear"], participant.url, "birthyear")
#key_value_pairs["contact and basic"].extend(participant.attributes["work and ed"])
(count, participant.attributes["family and rel"]) = driver.scrape_family_and_rel(participant)
participant.percent_complete+=count
participant.percent_complete/=9
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