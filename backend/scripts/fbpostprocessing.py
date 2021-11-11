import copy

from fbInferences import get_list_of_people

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
    "birthyear": {
        "no_data": []
    },
}

# pull friends from database

# pull category groups ?

# pull participant url 


# pull num of mutual inferences
num_mutuals_inf = 20
for url, friend in friends.items():
    category_frequency_data = copy.deepcopy(category_groups_template)
    for category, category_data in category_groups.items():
        for name, list_of_urls in category_data.items():
            category_frequency_data[category][name] = list(set(get_list_of_people(friend.mutual_friends, participant.url, list_of_urls, num_mutuals_inf)))
    friend.inference_count = category_frequency_data