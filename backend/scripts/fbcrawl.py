import time
import copy
import pickle
import requests
import pandas as pd
import mysql.connector

from fbdriver import *
from fbscrape_helpers import *
from fbInferences import get_list_of_people
from sql import *
from selenium.webdriver.chrome.options import Options

# connect to database and initialize schemas
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="privacy_admin",
  password="kristenisthebest",
)
mycursor = mydb.cursor()
sql_file = open("./backend/initialize_db.sql")
sql_as_string = sql_file.read()
sqlCommands = sql_as_string.strip().split(';')
for command in sqlCommands:
    try:
        mycursor.execute(command)
    except Exception as e:
        print(f"Command skipped: {command}")
        print(e)
mydb.commit()
sql_file.close()

# hacky
response = None

# connect to chromedriver for scraping
path_to_chrome_driver = '/Users/aaron/bin/Selenium/chromedriver'
# path_to_chrome_driver = "/Users/aaron/opt/WebDriver/bin/chromedriver"
# path_to_chrome_driver = "/Users/masmart/Downloads/chromedriver"
url = "https://mobile.facebook.com/home.php"

driver = FBdriver(executable_path=path_to_chrome_driver)
driver.set_page_load_timeout(60)
driver.implicitly_wait(10) # 5 should work on fast computers, increase if getting unable to locate element errors
driver.maximize_window()
driver.login(url) # type pw manually

# keep track of time
total_time = time.time()

# dict to keep track of each element and the mutual friends that correspond to each
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
}

category_groups = copy.deepcopy(category_groups_template)

# load in previously scraped data from pickle file
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

# scrape participant info if not in pickle
if not old_data and not "friends" in old_data:
    participant = get_participant_data(category_groups, driver)
else:
    participant = old_data["participant"]
insert_scraped_into_database(participant, mydb, mycursor, True)

# fetching all url paths to the user's friends' profiles
if not old_data and not "friends" in old_data:
    # change value to limit number of pages loaded for friends
    friends = driver.full_friend_lookup_table(-1)
else:
    friends = old_data["friends"]


# manual override if didnt scrape properly
#prev_friends_scraped = 250
exception_list = []
friends_with_most_data = []
friends_with_least_data = []
num_friends_scraped = 0
num_to_scrape = 300 # len(friends) for all
num_mutual_pages = 3 # -1 for all, otherwise a 8* will be number of friends scraped
num_mutuals_inf = -1 # -1 for all, otherwise sets mutuals to make inferences on
print(f"friends scraped from pickle: {prev_friends_scraped}")
for p, f in friends.items():
    # start_time = time.time()
    try:
        # use backup pickle if present else scrape normally
        if num_friends_scraped < prev_friends_scraped:
            if not f.name or num_friends_scraped>=num_to_scrape:
                continue
            f = old_data["friends"][p]
        else:
            if num_friends_scraped >= num_to_scrape:
                break
            # get current friend data, mutual friends in batches of 8
            scrape_friend_info(f, num_mutual_pages, category_groups, driver)
            populate_category_groups_funct(f, category_groups)

        num_friends_scraped+=1

        # updating local data, breaking after number of friends achieved
        file = open("file.pkl","wb")
        formatted_data = {
            "count": num_friends_scraped,
            "friends": friends,
            "participant": participant,
            "category_groups": category_groups,
        }
        pickle.dump(formatted_data, file)
        file.close()

        insert_scraped_into_database(f, mydb, mycursor)

        print(num_friends_scraped)
        print(f.name)
        print(f"Actual Mutual Friends: {f.numMutualFriends}")
        print(f"Scraped Mutual Friends: {len(f.mutual_friends)}")

        # STOP SCRAPING
        url = 'http://127.0.0.1:5000/stop_scraper'
        response = requests.get(url)
        if (response is not None) and (response.status_code == 200):
            print("starting stage four, inserting inferences into database")
            insert_all_attribute(category_groups, mydb, mycursor)
            for url, friend in friends.items():
                if friend.name is not None:
                    category_frequency_data = copy.deepcopy(category_groups_template)
                    for category, category_data in category_groups.items():
                        for name, list_of_urls in category_data.items():
                            category_frequency_data[category][name] = list(set(get_list_of_people(friend.mutual_friends, participant.url, list_of_urls, num_mutuals_inf)))
                    friend.inference_count = category_frequency_data
                    insert_inf_into_database(friend, mydb, mycursor)
            make_mutual_count(mydb, mycursor)
            break

    except Exception as e:
        print(f"Command skipped: {command}")
        print(f"Reason: {e}")
        print(e)
        if (response is not None) and (response.status_code == 200):
            print('Aborting...')
            break


mydb.close()
print(f"exception list: {exception_list}")
print(f"number of friends scraped: {num_friends_scraped}")
print("total runtime: "+str(time.time() - total_time))
