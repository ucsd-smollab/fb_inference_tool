from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from friend import Friend

class FBdriver(webdriver.Chrome):
    def __init__(self, executable_path, options=None):
        if options is None:
            options = Options()
            options.add_argument(" - window-size=1920x1080")
        self.friend_lookup_table = None
        super(FBdriver, self).__init__(executable_path=executable_path, options=options)

    def login(self, url, username=""):
        self.get(url)
        if username:
            username_box = self.find_element_by_id("m_login_email")
            username_box.send_keys(username)
            password_box = self.find_element_by_id("m_login_password")
            password_box.send_keys("")
        retry = 10
        logged_in = False
        while retry > 0 and not logged_in:
            if len(self.find_elements_by_css_selector("#rootcontainer")) > 0:
                logged_in = True
            else:
                retry -= 1
        if not(logged_in):
            raise Exception("Login failed.")
        elt = self.find_element_by_css_selector("[role=button]")
        url = elt.get_attribute("href")
        self.participant_path = url.split("?")[0].split("/")[-1]

    def scroll(self):
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(0.5)

    def full_friend_lookup_table(self):
        if self.friend_lookup_table:
            return friend_lookup
        url = "https://mobile.facebook.com/{}/friends".format(self.participant_path)
        self.get(url)
        all_friends_loaded = False
        last_height = self.execute_script("return document.body.scrollHeight;")
        while (not all_friends_loaded):
            self.scroll()
            new_height = self.execute_script("return document.body.scrollHeight;")
            if new_height == last_height:
                all_friends_loaded = True
            last_height = new_height
        friend_elements = self.find_elements_by_css_selector("._52jh > a")
        friend_urls = [f.get_attribute("href") for f in friend_elements]
        friend_paths = [f.split("/")[-1] for f in friend_urls if f]
        friend_lookup_table = {p:Friend(p) for p in friend_paths}
        self.friend_lookup_table = friend_lookup_table
        return friend_lookup_table

    def full_mutual_friend_list(self, friend):
        # TO DO
        # scrape list of mutual friends
        # (scrape friend paths and then use lookup table to get Friend objects)
        # return list of Friends
        return []

    def scrape_places_lived(self, friend):
        self.get("https://facebook.com/" + friend.path + "/about_places")
        sleep(0.2)
        try:
            elts = self.find_elements_by_css_selector(".aahdfvyu.sej5wr8e ~ div")
            place_texts  = [elt.get_attribute("innerText") for elt in elts[7:]]
            places = [p.split("\n")[0] for p in place_texts if p != "No places to show"]
            return places
        except Exception:
            return None

    def scrape_religion(self, friend):
        return "TO DO"

    def scrape_name(self, friend):
        return "TO DO"