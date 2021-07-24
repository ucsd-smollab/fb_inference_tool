from friend import Friend

def get_number_of_people(mutual_friends, current_friend, participant, category, specified_data, category_group_data):
    list_of_friends = category_group_data[category][specified_data]
    total_people = mutual_friends.append(participant).append(current_friend)
    list_of_intersected_friends = [friend for friend in list_of_friends if friend in total_people]
    return len(list_of_intersected_friends)


def compute_frequency_category_data(category_data):
    frequency_category_data = category_data.copy()
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