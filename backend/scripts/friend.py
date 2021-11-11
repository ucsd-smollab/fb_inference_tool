class Friend:
    def __init__(self, path, numMutualFriends=0):
        self.numMutualFriends = numMutualFriends
        self.url = path
        self.attributes = {}
        self.percent_complete = 0
        self.percent_total_complete = 0
        self.profile_picture_url = ""
        self.mutual_friends = None
        self.name = None
        self.inference_count = None
        self.time_array = []