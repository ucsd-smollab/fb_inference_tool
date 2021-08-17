from friend import Friend
import copy

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

def get_list_of_people(mutual_friends, participant, list_of_urls):
    if not list_of_urls or not mutual_friends:
        return []
    total_people = copy.deepcopy(mutual_friends)
    if not participant in mutual_friends:
        total_people.append(participant)
    # print("------------------------------------------------------")
    # print(f'total people: {total_people}')
    list_of_intersected_friends = [friend for friend in list_of_urls if friend in total_people]
    # print(f'intersected friends: {list_of_intersected_friends}')
    # print("------------------------------------------------------")
    return list_of_intersected_friends

def compute_frequency_category_data(category_data):
    frequency_category_data = copy.deepcopy(category_data)
    for category, data in category_data.items():
        for k, list_of_urls in data.items():
            frequency_category_data[category][k] = len(list_of_urls)
    return frequency_category_data

def generate_inferences(friends, participant, inference_count_dict):
    for p, f in friends.items():
        if not f.attributes:
            inference_count_dict["Not Scraped"]+=1
            continue
        c = -1
        for category, category_data in f.inference_count.items():
            c+=1
            #initilize temp variables
            temp_count = 5 #sets threshold
            threshold = 5 #for printing purposes
            temp_name = "threshold"
            tie = False
            to_predict = []
            #get data
            #print(f"category: {category}, Count: {c}")
            if c < 3:
                #print(f.attributes)
                if f.attributes[category] == "NA":
                    inference_count_dict["No Data"] += 1
                    continue
                for cat in f.attributes[category]:
                    to_predict.append(cat["title"])
            elif c == 3:
                if f.attributes["places lived"]["list_of_cities"] == "NA":
                    inference_count_dict["No Data"] += 1
                    continue
                to_predict = f.attributes["places lived"]["list_of_cities"]
            else:
                if f.attributes["contact and basic"]["basic_info"][category] == "NA":
                    inference_count_dict["No Data"] += 1
                    continue
                to_predict = f.attributes["contact and basic"]["basic_info"][category]
            #iterate through dict and compare most frequent values to make inferences
            for name, data_entries in category_data.items():
                if name == "no_data":
                    continue
                #get most frequent data value
                count = len(data_entries)
                #print(name, count)
                if count > temp_count:
                    temp_count = count
                    temp_name = name
                    tie = False
                elif count == temp_count:
                    tie = True
            #update accuracy counts
            if tie == True:
                inference_count_dict["Tie"]+=1
            elif temp_name == "threshold":
                inference_count_dict["Below Threshold"]+=1
            else:
                if temp_name in to_predict:
                    inference_count_dict["Right"]+=1
                else:
                    inference_count_dict["Wrong"]+=1
            print(f"guess: {temp_name}")
            print(f"actual: {to_predict}")
    print(f"threshold: {threshold}")

'''

category_groups = {
    "work": {
        "no_data": 20
        ""
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
'''