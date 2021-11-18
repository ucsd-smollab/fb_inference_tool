from friend import Friend
from fbdriver import *
from selenium.common.exceptions import NoSuchElementException

def format_url(friend, sub_path):
    places_url = f'https://facebook.com/{friend.url}'
    if "profile.php" in friend.url:
        return f'{places_url}&sk={sub_path}'
    return f'{places_url}/{sub_path}'

def extract_data(data, formatted_data):
    try:
        splitted_data = data.split("\n")
        correct_data = [split_data for split_data in splitted_data if not "Shared " in split_data and not "Only " in split_data and not "Add " in split_data and not "Friends" in split_data]
        if "gender" in formatted_data:
            for i in range(1, len(correct_data)):
                if "Gender" in correct_data[i] and not correct_data[i-1] in ["Male", "Female", "Agender", "Androgyne", "Androgynous", "Bigender", "Cis", "Cis Female", "Cis Male", "Cis Man", "Cis Woman", "Cisgender"]:
                    correct_data.remove("Gender")
                    break
        #print(f"correct data: {correct_data}")  
        for i in range(1, len(correct_data), 2):
            category = correct_data[i+1].replace(" ", "").lower()
            if category in formatted_data:
                formatted_data[category] = correct_data[i]
        return formatted_data
    except:
        return {}

def generate_list_of_years(string_years, default_year=4):
    '''
    Case 1:
        Date - Present
    Case 2:
        Date - Date
    Case 3:
        Class of Year
    Case 4:
        Starting on Date
    Different Cases on Date Representation:
    Case 1:
        Month Day, Year
    Case 2:
        Month Year
    Case 3:
        Year
    '''
    list_of_years = []
    start_year = 0
    end_year = 0
    if string_years == "NA":
        return "NA"
    # Case 1 and Case 2
    if " - " in string_years:
        separated_dates = string_years.split(" - ")
        start_year = separated_dates[0]
        # Case 1: Date Representation
        if ", " in start_year:
            start_year = int(start_year.split(", ")[1])
        # Case 2: Date Representation
        elif " " in start_year:
            start_year = int(start_year.split(" ")[1])
        # Case 3: Date Representation
        else:
            start_year = int(start_year)
        # Case 2
        if not "Present" in separated_dates[1]:
            end_year = separated_dates[1]
            if ", " in end_year:
                end_year = int(end_year.split(", ")[1])
            elif " " in end_year:
                end_year = int(end_year.split(" ")[1])
            else:
                end_year = int(end_year)
        else:
            end_year = start_year + default_year
    # Case 3
    elif " of " in string_years:
        end_year = int(string_years.split(" of ")[1])
        start_year = end_year - default_year
    # Case 4
    elif " on " in string_years:
        separated_date = string_years.split(" on ")[1]
        separated_date = separated_date.split(", ")[1]
        start_year = int(separated_date)
        end_year = start_year + default_year
    difference = end_year - start_year
    for i in range(difference+1):
        list_of_years.append(f'{start_year+i}')
    return list_of_years

def populate_category_groups(data, person_url, category_name, category_groups):
    if data == "NA":
        category_groups[category_name]["no_data"].append(person_url)
        return
    if not isinstance(data, list):
        data = data
        if data in category_groups[category_name]:
            category_groups[category_name][data].append(person_url)
        else:
            category_groups[category_name][data] = [person_url]
        return
    for entry in data:
        entry_name = entry
        if isinstance(entry, dict):
            entry_name = entry["title"]
        entry_name = entry_name
        if entry_name in category_groups[category_name]:
            category_groups[category_name][entry_name].append(person_url)
        else:
            category_groups[category_name][entry_name] = [person_url]

# scrape participants data and update their profile percent complete
def get_participant_data(category_groups, driver):
    participant = Friend(driver.participant_path)
    participant.name = driver.scrape_participant_name(participant)
    # work_and_ed out of 2
    (count, participant.attributes["work"], participant.attributes["college"], participant.attributes["highschool"], participant.profile_picture_url) = driver.scrape_work_and_ed(participant)
    participant.percent_complete+=count
    populate_category_groups(participant.attributes["work"], participant.url, "work", category_groups)
    populate_category_groups(participant.attributes["college"], participant.url, "college", category_groups)
    populate_category_groups(participant.attributes["highschool"], participant.url, "highschool", category_groups)
    # places_lived out of 1
    (count, participant.attributes["places lived"]) = driver.scrape_places_lived(participant)
    participant.percent_complete+=count
    populate_category_groups(participant.attributes["places lived"]["list_of_cities"], participant.url, "cities", category_groups)
    # contact_and_basic out of 2
    (count, participant.attributes["contact and basic"]) = driver.scrape_contact_and_basic(participant)
    participant.percent_complete+=count
    populate_category_groups(participant.attributes["contact and basic"]["basic_info"]["religiousviews"], participant.url, "religiousviews", category_groups)
    populate_category_groups(participant.attributes["contact and basic"]["basic_info"]["politicalviews"], participant.url, "politicalviews", category_groups)

    participant.percent_complete = round(participant.percent_complete/5, 3)
    participant.percent_total_complete = 0
    return participant

# scrape friends data and update their profile percent complete
def scrape_friend_info(f, num_mutual, category_groups, driver):
    f.name = driver.scrape_name(f)
    driver.full_mutual_friend_list(f, num_mutual)
    (count, f.attributes["work"], f.attributes["college"], f.attributes["highschool"], f.profile_picture_url) = driver.scrape_work_and_ed(f)
    f.percent_complete+=count    
    (count, f.attributes["places lived"]) = driver.scrape_places_lived(f)
    f.percent_complete+=count    
    (count, f.attributes["contact and basic"]) = driver.scrape_contact_and_basic(f)
    f.percent_complete = round(f.percent_complete/5, 3)
    f.percent_total_complete = 0

def populate_category_groups_funct(f, category_groups):
    populate_category_groups(f.attributes["work"], f.url, "work", category_groups)
    populate_category_groups(f.attributes["college"], f.url, "college", category_groups)
    populate_category_groups(f.attributes["highschool"], f.url, "highschool", category_groups)
    populate_category_groups(f.attributes["places lived"]["list_of_cities"], f.url, "cities", category_groups)
    populate_category_groups(f.attributes["contact and basic"]["basic_info"]["religiousviews"], f.url, "religiousviews", category_groups)
    populate_category_groups(f.attributes["contact and basic"]["basic_info"]["politicalviews"], f.url, "politicalviews", category_groups)