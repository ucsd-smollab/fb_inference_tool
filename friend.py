class Friend:
    def __init__(self, path):
        self.url = path
        self.attributes = {}
        self.percent_complete = 0
        self.profile_picture_url = ""
        self.mutual_friends = None
        self.name = None