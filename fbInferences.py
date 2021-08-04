from friend import Friend
import copy

def get_list_of_people(mutual_friends, current_friend, participant, category, specified_data, list_of_urls):
    if not list_of_urls or not mutual_friends:
        return []
    if not mutual_friends:
        print("empty list")
    total_people = copy.deepcopy(mutual_friends)
    if not participant in total_people:
        total_people.append(participant)

    list_of_intersected_friends = [friend for friend in list_of_urls if friend in total_people]
    print(list_of_intersected_friends)
    return list_of_intersected_friends

def compute_frequency_category_data(category_data):
    frequency_category_data = copy.deepcopy(category_data)
    for category, data in category_data.items():
        for k, list_of_urls in data.items():
            frequency_category_data[category][k] = len(list_of_urls)
    return frequency_category_data


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