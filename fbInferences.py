from friend import Friend
from time import sleep
import random
import copy
import pprint

def get_list_of_people(mutual_friends, participant, list_of_urls, num_mutuals = None):
    if "NA" == mutual_friends or not list_of_urls or not mutual_friends:
        return []
    if num_mutuals == -1:
        total_people = copy.deepcopy(mutual_friends)
    else:
        total_people = copy.deepcopy(mutual_friends)[:num_mutuals]
    if not participant in mutual_friends:
        total_people.append(participant)
    list_of_intersected_friends = [friend for friend in list_of_urls if friend in total_people]
    return list_of_intersected_friends

def generate_inferences(friends, participant, inference_count_dict):
    for p, f in friends.items():
        if not f.attributes:
            inference_count_dict["Not Scraped"]+=1
            continue
        threshold = 1
        for category, category_data in f.inference_count.items():
            # get ground truth
            if category=="cities":
                attribute_data = f.attributes["places lived"]["list_of_cities"]
            elif category in ["religiousviews", "politicalviews", "birthyear"]:
                attribute_data = f.attributes["contact and basic"]["basic_info"][category]
            else:
                attribute_data = f.attributes[category]
                if isinstance(attribute_data, list):
                    attribute_data = [data["title"] for data in attribute_data]
            # print(f.name)
            # pprint.pprint(attribute_data)
            # pprint.pprint(category_data)
            #initialize variables
            temp_max = threshold
            temp_name = "Threshold"
            tie = False
            No_Data = True
            if attribute_data == "NA":
                truth = "No Ground Truth"
            else:
                truth = "Has Ground Truth"
            # check if no data, below threshold, tied, right or wrong
            for name, url_list in category_data.items():
                if not url_list or name=="no_data":
                    continue
                No_Data = False
                if len(url_list) > temp_max:
                    temp_max = len(url_list)
                    temp_name = name
                    tie = False
                elif len(url_list) == temp_max:
                    tie = True
            # update counts
            if No_Data:
                inference_count_dict[truth][category]["No Data"]+=1
            elif temp_name=="Threshold":
                inference_count_dict[truth][category]["Below Threshold"]+=1
            elif tie:
                inference_count_dict[truth][category]["Tie"]+=1
            elif truth=="Has Ground Truth":
                if (isinstance(attribute_data, list) and temp_name in attribute_data) or temp_name == attribute_data:
                    inference_count_dict[truth][category]["Right"]+=1
                else:
                    inference_count_dict[truth][category]["Wrong"]+=1
            # print(f"prediction: {temp_name}")
            # print("------------------")
            # sleep(10)