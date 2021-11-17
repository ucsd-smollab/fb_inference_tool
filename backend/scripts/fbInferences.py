from friend import Friend
from time import sleep
import random
import copy
import pprint
import bisect 
import pandas as pd


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
    total = 0
    total_rwt = 0
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
            total+=1
            if No_Data:
                inference_count_dict[truth][category]["No Data"]+=1
                inference_count_dict["totals"]["total no data"]+=1
            elif temp_name=="Threshold":
                inference_count_dict[truth][category]["Below Threshold"]+=1
                inference_count_dict["totals"]["total below threshold"]+=1
            elif tie:
                inference_count_dict[truth][category]["Tie"]+=1
                inference_count_dict["totals"]["total tie"]+=1
                total_rwt+=1
            elif truth=="Has Ground Truth":
                if (isinstance(attribute_data, list) and temp_name in attribute_data) or temp_name == attribute_data:
                    inference_count_dict[truth][category]["Right"]+=1
                    inference_count_dict["totals"]["total right"]+=1
                else:
                    inference_count_dict[truth][category]["Wrong"]+=1
                    inference_count_dict["totals"]["total wrong"]+=1
                total_rwt+=1
            # print(f"prediction: {temp_name}")
            # print("------------------")
            # sleep(10)
    c = 0
    dict_cat = ["total right", "total wrong", "total tie", "total below threshold", "total no data",
        "right/rwt", "wrong/rwt", "tie/rwt"]
    for key in dict_cat:
        if c > 4:
            inference_count_dict["percentages"][key] = round(100*inference_count_dict["totals"]["total "+ key[:-4]]/total_rwt, 2)
            continue
        inference_count_dict["percentages"][key] = round(100*inference_count_dict["totals"][key]/total, 2)
        c+=1
    
def generate_inferences_ranking(friends, participant, inference_count_dict):
    total = 0
    total_rwt = 0
    conf_perc_right = 0
    conf_perc_wrong = 0
    pred_df = pd.DataFrame(columns=["category", "Right/Wrong", "Conf Pred Right", "Actual", "Max", "Ranking Array"])
    df_dict = {
        "work": pd.DataFrame(columns=["Right/Wrong", "Conf Pred Right", "Actual", "Max", "Ranking Array"]),
        "college": pd.DataFrame(columns=["Right/Wrong", "Conf Pred Right", "Actual", "Max", "Ranking Array"]),
        "highschool": pd.DataFrame(columns=["Right/Wrong", "Conf Pred Right", "Actual", "Max", "Ranking Array"]),
        "cities": pd.DataFrame(columns=["Right/Wrong", "Conf Pred Right", "Actual", "Max", "Ranking Array"]),
        "politicalviews": pd.DataFrame(columns=["Right/Wrong", "Conf Pred Right", "Actual", "Max", "Ranking Array"]),
        "religiousviews": pd.DataFrame(columns=["Right/Wrong", "Conf Pred Right", "Actual", "Max", "Ranking Array"])
    }
    for p, f in friends.items():
        if not f.attributes:
            inference_count_dict["Not Scraped"]+=1
            continue
        threshold = 1
        for category, category_data in f.inference_count.items():
            # temporary removal of biirthyear, need to completely remove on finalization
            if category=="birthyear":
                continue
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
            cat_count = 0
            cat_dict = {}
            # check if no data, below threshold, tied, right or wrong
            for name, url_list in category_data.items():
                if not url_list or name=="no_data":
                    continue
                if category=="religiousviews" and name=="other":
                    continue
                No_Data = False
                cat_dict[name] = len(url_list)
                cat_count+=len(url_list)
                if len(url_list) > temp_max:
                    temp_max = len(url_list)
                    temp_name = name
                    tie = False
                elif len(url_list) == temp_max:
                    tie = True

            # update counts
            total+=1
            temp_bool = False
            if No_Data:
                inference_count_dict[truth][category]["No Data"]+=1
                inference_count_dict["totals"]["total no data"]+=1
            elif temp_name=="Threshold":
                inference_count_dict[truth][category]["Below Threshold"]+=1
                inference_count_dict["totals"]["total below threshold"]+=1
            elif tie:
                inference_count_dict[truth][category]["Tie"]+=1
                inference_count_dict["totals"]["total tie"]+=1
                total_rwt+=1
            elif truth=="Has Ground Truth":
                if cat_count:
                    temp_conf = round((temp_max/cat_count)*100, 2)
                cat_dict = {k: v for k, v in sorted(cat_dict.items(), key=lambda item: item[1])}
                cat_dict = list(cat_dict.items())
                cat_dict.reverse()
                if len(cat_dict)>=10:
                    cat_dict = cat_dict[:10]
                if (isinstance(attribute_data, list) and temp_name in attribute_data) or temp_name == attribute_data:
                    inference_count_dict[truth][category]["Right"]+=1
                    inference_count_dict["totals"]["total right"]+=1
                    if cat_count:
                        conf_perc_right += (temp_max/cat_count)
                    pred_df.loc[len(pred_df.index)] = [category, "Right", temp_conf, attribute_data, temp_max, cat_dict]
                    df_dict[category].loc[len(pred_df.index)] = ["Right", temp_conf, attribute_data, temp_max, cat_dict]
                else:
                    inference_count_dict[truth][category]["Wrong"]+=1
                    inference_count_dict["totals"]["total wrong"]+=1
                    if cat_count:
                        conf_perc_wrong += (temp_max/cat_count)
                    pred_df.loc[len(pred_df.index)] = [category, "Wrong", temp_conf, attribute_data, temp_max, cat_dict]
                    df_dict[category].loc[len(pred_df.index)] = ["Wrong", temp_conf, attribute_data, temp_max, cat_dict]
                total_rwt+=1
            # print(f"prediction: {temp_name}")
            # print("------------------")
            # sleep(10)
    if inference_count_dict["totals"]["total right"]:
        inference_count_dict["avg confidence percentage"]["right"] = round(conf_perc_right/inference_count_dict["totals"]["total right"]*100, 2)
    if inference_count_dict["totals"]["total wrong"]:
        inference_count_dict["avg confidence percentage"]["wrong"] = round(conf_perc_wrong/inference_count_dict["totals"]["total wrong"]*100, 2)

    c = 0
    dict_cat = ["total right", "total wrong", "total tie", "total below threshold", "total no data",
        "right/rwt", "wrong/rwt", "tie/rwt"]
    for key in dict_cat:
        if c > 4:
            if total_rwt:
                inference_count_dict["percentages"][key] = round(100*inference_count_dict["totals"]["total "+ key[:-4]]/total_rwt, 2)
            continue
        if total:
            inference_count_dict["percentages"][key] = round(100*inference_count_dict["totals"][key]/total, 2)
        c+=1
    # pred_df.to_csv("predRanking.csv", index=False)
    truth="Has Ground Truth"
    for key in df_dict:
        # sort by max value & take the top 10
        df_dict[key] = df_dict[key].sort_values(by=["Max", "Conf Pred Right"], ascending=False)
        df_dict[key] = df_dict[key].head(10)
        # then sort by confidence percentage
        df_dict[key] = df_dict[key].sort_values(by=["Conf Pred Right"], ascending=False)
        # export to csv
        # df_dict[key].to_csv(str(key)+"Ranking.csv", index=False)
        if (inference_count_dict[truth][key]["Right"]+inference_count_dict[truth][key]["Wrong"]):
            inference_count_dict[truth][key]["Accuracy"] = round(inference_count_dict[truth][key]["Right"]/(inference_count_dict[truth][key]["Right"]+inference_count_dict[truth][key]["Wrong"])*100, 2)

        try:
            right = df_dict[key]["Right/Wrong"].value_counts().Right
            inference_count_dict[truth][key]["Sorted Accuracy"] = int(right*10)
        except:
            print("sorted accuracy failure")
        
"""
CSV File Structure

PredictionConfidence Prediction [(key, value) () ()]

"""