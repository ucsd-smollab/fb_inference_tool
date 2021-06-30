from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from friend import Friend

def format_url(friend, sub_path):
    places_url = f'https://facebook.com/{friend.path}'
    if "profile.php" in friend.path:
        return f'{places_url}&sk={sub_path}'
    return f'{places_url}/{sub_path}'

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
        #remove if not testing
        #self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(0.5)

    def full_friend_lookup_table(self):
        if self.friend_lookup_table:
            return self.friend_lookup_table

        # navigating to user profile
        profile_url = f'https://mobile.facebook.com/{self.participant_path}'
        self.get(profile_url)

        # navigating to friends list
        friends_btn_element = self.find_element_by_css_selector("[data-sigil=expanded-context-log]")
        friends_list_url = friends_btn_element.get_attribute("href")
        self.get(friends_list_url)

        # getting all of user's friends loaded on screen
        all_friends_loaded = False
        last_height = self.execute_script("return document.body.scrollHeight;")
        while (not all_friends_loaded):
            self.scroll()
            new_height = self.execute_script("return document.body.scrollHeight;")
            if new_height == last_height:
                all_friends_loaded = True
            last_height = new_height
        
        # getting all url to friends
        friend_elements = self.find_elements_by_css_selector("._5pxa ._5pxc a")
        friend_urls = [f.get_attribute("href") for f in friend_elements]
        friend_paths = [f.split("/")[-1] for f in friend_urls if f]
        friend_lookup_table = {p:Friend(p) for p in friend_paths}
        self.friend_lookup_table = friend_lookup_table
        return friend_lookup_table

    def full_mutual_friend_list(self, friend):
        self.get(format_url(friend, "friends_mutual"))
        sleep(0.2)
        try:
            mutual_friends_elements = self.find_element_by_css_selector("[data-pagelet='ProfileAppSection_0']")
            if mutual_friends_elements.text.contains("No friends"):
                raise Exception
            mutual_friends_anchors = mutual_friends_elements.find_elements_by_css_selector("[tabindex='-1']")
            mutual_friends_urls = [anchor.get_attribute("href") for anchor in mutual_friends_anchors]
            mutual_friends_paths = [path.split("/")[-1] for path in mutual_friends_urls]
            print(mutual_friends_paths)
            return mutual_friends_paths
        except Exception:
            return None

    def scrape_name(self, friend):
        #load friends facebook page
        self.get("https://facebook.com/" + friend.path)
        #find name element by css selector and return attribute string value
        elt = self.find_element_by_css_selector("h1.gmql0nx0.l94mrbxd.p1ri9a11.lzcic4wl")
        name = elt.get_attribute("innerText")
        print(name)
        return name

    def scrape_work_and_ed(self, friend):
        self.get(format_url(friend, "about_work_and_education"))
        elts = self.find_elements_by_css_selector(".dati1w0a.tu1s4ah4.f7vcsfb0.discj3wi > div")
        workAndEd = []
        for i in elts:
            workAndEd.append(i.get_attribute("innerText"))
        print(workAndEd)
        return workAndEd

    def scrape_places_lived(self, friend):
        self.get(format_url(friend, "about_places"))
        sleep(0.2)
        try:
            elts = self.find_elements_by_css_selector(".aahdfvyu.sej5wr8e ~ div")
            place_texts  = [elt.get_attribute("innerText") for elt in elts[7:]]
            places = [p.split("\n")[0] for p in place_texts if p != "No places to show"]
            print(places)
            return places
        except Exception:
            return None
    
    def scrape_contact_and_basic(self, friend):
        self.get(format_url(friend, "about_contact_and_basic_info"))
        elts = self.find_elements_by_css_selector(".dati1w0a.tu1s4ah4.f7vcsfb0.discj3wi > div")
        contactAndBasic = []
        for i in elts:
            contactAndBasic.append(i.get_attribute("innerText"))
        print(contactAndBasic)
        return contactAndBasic

    def scrape_family_and_rel(self, friend):
        self.get(format_url(friend, "about_family_and_relationships"))
        elts = self.find_elements_by_css_selector(".aahdfvyu.sej5wr8e ~ div")
        familyAndRel = []
        for i in elts[7:]:
            familyAndRel.append(i.get_attribute("innerText"))
        print(familyAndRel)
        return familyAndRel

    def scrape_life_events(self, friend):
        self.get(format_url(friend, "about_life_events"))
        elts = self.find_elements_by_css_selector(".dati1w0a.tu1s4ah4.f7vcsfb0.discj3wi")
        lifeEvents = []
        for i in elts:
            lifeEvents.append(i.get_attribute("innerText"))
        print(lifeEvents)
        return lifeEvents
