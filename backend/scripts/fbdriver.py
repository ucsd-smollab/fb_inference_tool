import time
import re
from time import sleep
from friend import Friend
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fbscrape_helpers import *

class FBdriver(webdriver.Chrome):
    # initialize driver
    def __init__(self, executable_path, options=None):
        if options is None:
            options = Options()
            options.add_argument("--incognito")
            option = webdriver.ChromeOptions()
            chrome_prefs = {}
            option.experimental_options["prefs"] = chrome_prefs
            options.add_argument(" - window-size=1920x1080")
            options.add_experimental_option("detach", True)
            chrome_prefs["profile.default_content_settings"] = {"images": 2}
            chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        self.friend_lookup_table = None
        super(FBdriver, self).__init__(executable_path=executable_path, options=options)

    # go to facebook login page and reattempt login until successful
    def login(self, url, username=""):
        self.get(url)
        if username:
            username_box = self.find_element_by_id("m_login_email")
            username_box.send_keys(username)
            password_box = self.find_element_by_id("m_login_password")
            password_box.send_keys("")
        retry = 60
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
        if ".php" in url:
            self.get("https://www.facebook.com/profile")
            url = self.current_url
            self.participant_path = url.split("/")[-1]
        else:
            self.participant_path = url.split("?")[0].split("/")[-1]

    # scroll to bottom of the page
    def scroll(self, time):
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(time)

    # get a friends url and number of mutual friends
    def get_link_and_mutual_friends(self, f):
        full_text = f.get_attribute("innerText")
        href = f.find_element_by_css_selector("._5pxa ._5pxc a").get_attribute("href")
        if not href:
            return ("", 0, False)
        href = href.split("/")[-1]
        href = re.sub('\?refid=[0-9]+', '', href)
        if "mutual friends" in full_text:
            formatted_text = full_text.split(" ")
            for i in range(len(formatted_text)):
                if formatted_text[i] == "mutual":
                    total_mutual_friends = int(formatted_text[i-1].split("\n")[-1])
                    return (href, total_mutual_friends, True)
        return (href, 0, True)

    # get participants friends list and return as list of friends objects
    def full_friend_lookup_table(self, to_load=-1):
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
        load_num = 0
        while (not all_friends_loaded):
            if load_num==to_load:
                 break
            for i in range(0, 3*4):
                self.scroll(0.25)
                new_height = self.execute_script("return document.body.scrollHeight;")
                if new_height != last_height:
                    all_friends_loaded = False
                    load_num+=1
                    break
                else:
                     all_friends_loaded = True
            last_height = new_height

        # getting all url to friends
        friend_elements = self.find_elements_by_css_selector("._55wp._7om2._5pxa._8yo0")

        friend_urls = [self.get_link_and_mutual_friends(f) for f in friend_elements]
        friend_lookup_table = {p:Friend(p, num) for (p, num, doesExist) in friend_urls if doesExist}
        self.friend_lookup_table = friend_lookup_table
        print(f"participant has {len(friend_urls)} friends")
        return friend_lookup_table

    # get a friends mutual friends list and return as list of friend urls, done through mobile layout
    def full_mutual_friend_list_mobile(self, friend):
        if "profile.php" in friend.url:
            url = f"https://m.facebook.com/{friend.url}&v=friends&mutual=1"
        else:
            url = f"https://m.facebook.com/{friend.url}/friends?mutual=1"
        self.get(url)

        # getting all of user's friends loaded on screen
        all_friends_loaded = False
        last_height = self.execute_script("return document.body.scrollHeight;")
        while (not all_friends_loaded):
            for i in range(0, 5):
                self.scroll(0.5)
                new_height = self.execute_script("return document.body.scrollHeight;")
                if new_height == last_height:
                    all_friends_loaded = True
            last_height = new_height

        # getting all url to friends
        friend_elements = self.find_elements_by_css_selector("._5pxa ._5pxc a")
        if not friend_elements:
            return []
        friend_urls = [f.get_attribute("href") for f in friend_elements]
        friend_paths = []
        for f in friend_urls:
            if not f:
                continue
            path = f.split("/")[-1]
            if not "profile.php" in path:
                path = path.split("?")[0]
            friend_paths.append(path)
        return friend_paths

    # get a friends mutual friends list and return as list of friend urls
    def full_mutual_friend_list(self, friend, to_load=-1):
        start_time = time.time()
        self.get(format_url(friend, "friends_mutual"))

        if friend.numMutualFriends == 0:
            return "NA", 0

        mutual_tries = 3
        while not friend.mutual_friends or (to_load==-1 and len(friend.mutual_friends)/friend.numMutualFriends < 0.6) or (to_load!=-1 and len(friend.mutual_friends)*0.6<to_load*8):
            if mutual_tries == 0:
                break

            # getting all of user's friends loaded on screen
            all_friends_loaded = False
            last_height = self.execute_script("return document.body.scrollHeight;")
            load_num = 0
            while (not all_friends_loaded):
                if load_num==to_load:
                    break
                for i in range(0, 7*4):
                    self.scroll(0.25)
                    new_height = self.execute_script("return document.body.scrollHeight;")
                    if new_height != last_height:
                        all_friends_loaded = False
                        load_num+=1
                        break
                    #elif load_num*8/friend.numMutualFriends > 0.6:
                    else:
                        all_friends_loaded = True
                last_height = new_height

            try:
                mutual_friends_elements = self.find_element_by_class_name("j83agx80.btwxx1t3.lhclo0ds.i1fnvgqd")
                mutual_friends_anchors = mutual_friends_elements.find_elements_by_css_selector("[tabindex='-1']")
                mutual_friends_urls = [anchor.get_attribute("href") for anchor in mutual_friends_anchors]
                friend.mutual_friends = [path.split("/")[-1] for path in mutual_friends_urls]
                mutual_tries-=1
                to_return = float(time.time() - start_time)
            except Exception:
                mutual_tries-=1
                to_return = float(time.time() - start_time)
        return to_return

    def scrape_name(self, friend):
        # load friends facebook page
        self.get("https://facebook.com/" + friend.url)
        # find name element by css selector and return attribute string value
        elts = self.find_elements_by_css_selector("h1.gmql0nx0.l94mrbxd.p1ri9a11.lzcic4wl")
        names = [elt.get_attribute('innerText') for elt in elts]
        if len(names) > 1:
            names = [name for name in names if name not in ['Messenger', 'Notifications']]
            name = names[0]
        else:
            name = names[0]
        return name

    def scrape_participant_name(self, participant):
        # load friends facebook page
        self.get("https://mobile.facebook.com/" + participant.url)
        # find name element by css selector and return attribute string value
        elt = self.find_element_by_css_selector("h3._6x2x")
        name = elt.get_attribute("innerText")
        return name

    def scrape_work_and_ed(self, friend):
        self.get(format_url(friend, "about_work_and_education"))

        try:
            # getting profile image url
            profile_picture_section = self.find_element_by_class_name("b3onmgus.e5nlhep0.ph5uu5jm.ecm0bbzt.spb7xbtv.bkmhp75w.emlxlaya.s45kfl79.cwj9ozl2")
            profile_picture_image = profile_picture_section.find_element_by_tag_name("image")
            profile_picture_url = profile_picture_image.get_attribute("xlink:href")
        except Exception as e:
            print('Failed to scrape profile picture. Error:', e)
            profile_picture_url = ''

        # work scraping
        retries = 1
        while retries>=0:
            retries -= 1
            try:
                sections = self.find_elements_by_css_selector(".dati1w0a.tu1s4ah4.f7vcsfb0.discj3wi > div")
                workList = []
                work = sections[0]
                for w in work.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt"):
                    workName = "NA"
                    if not "Add a " in w.get_attribute("innerText") and not " to show" in w.get_attribute("innerText"):
                        workElement = w.find_element_by_css_selector(".ii04i59q.a3bd9o3v.jq4qci2q.oo9gr5id")
                        workName = workElement.get_attribute("innerText")
                    else:
                        continue
                    if " at " in workName:
                        workName = workName.split("at ")[1]
                    tempDict = {
                        "title": workName,
                    }
                    workList.append(tempDict)
                uniqueWorkList = list({v['title']:v for v in workList}.values())
                workList = uniqueWorkList
            except Exception as e:
                print('Failed to scrape work. Error:', e)

        # college scraping
        retries = 1
        while retries>=0:
            retries -= 1
            try:
                college = sections[1]
                collegeList = []
                for c in college.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt"):
                    schoolName = "NA"

                    if not "Add a " in c.get_attribute("innerText") and not " to show" in c.get_attribute("innerText"):
                        schoolElement = c.find_element_by_css_selector(".ii04i59q.a3bd9o3v.jq4qci2q.oo9gr5id")
                        schoolName = schoolElement.get_attribute("innerText")
                        # schoolUrlElement = schoolElement.find_elements_by_css_selector("[role='link']")
                        # if schoolUrlElement:
                        #     facebookPageUrlC = schoolUrlElement[0].get_attribute("href")
                    else:
                        continue

                    if " at " in schoolName:
                        schoolName = schoolName.split("at ")[1]
                    tempDict = {
                        "title": schoolName,
                    }
                    collegeList.append(tempDict)
                uniqueCollegeList = list({v['title']:v for v in collegeList}.values())
                collegeList = uniqueCollegeList
            except Exception as e:
                print('Failed to scrape college. Error:', e)

        # high school scraping
        retries = 1
        while retries>=0:
            retries -= 1
            try:
                highSchool = sections[2]
                highSchoolList = []
                for h in highSchool.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt"):
                    hSchoolName = "NA"

                    if not "Add a " in h.get_attribute("innerText") and not " to show" in h.get_attribute("innerText"):
                        hSchoolElement = h.find_element_by_css_selector(".ii04i59q.a3bd9o3v.jq4qci2q.oo9gr5id")
                        hSchoolName = hSchoolElement.get_attribute("innerText")
                    else:
                        continue

                    if " at " in hSchoolName:
                        hSchoolName = hSchoolName.split(" at ")[1]
                    if " to " in hSchoolName:
                        hSchoolName = hSchoolName.split(" to ")[1]
                    tempDict = {
                        "title": hSchoolName,
                    }
                    highSchoolList.append(tempDict)
                uniqueHighSchoolList = list({v['title']:v for v in highSchoolList}.values())
                highSchoolList = uniqueHighSchoolList
            except Exception as e:
                print('Failed to scrape highschool. Error:', e)

        # update profile completion counts
        completionCount = 2
        if not workList:
            workList = "NA"
            completionCount-=1
        if not collegeList and not highSchoolList:
            completionCount-=1
        if not collegeList:
            collegeList = "NA"
        if not highSchoolList:
            highSchoolList = "NA"
        return (completionCount, workList, collegeList, highSchoolList, profile_picture_url)

    def scrape_places_lived(self, friend):
        self.get(format_url(friend, "about_places"))
        places_lived = {
            "hometown": "NA",
            "currentCity": "NA",
            "otherCities": [],
            "list_of_cities": [],
        }
        elts = self.find_elements_by_css_selector(".aahdfvyu.sej5wr8e ~ div")
        place_texts  = [elt.get_attribute("innerText") for elt in elts[7:]]
        for place in place_texts:
            index_city = 0
            if "no places to show" in place.lower():
                break
            place_info = place.split("\n")[:2]
            if "Add " in place_info[-1] or "Shared " in place_info[index_city] or "Only " in place_info[index_city]:
                continue
            elif "Current" in place_info[-1]:
                places_lived["currentCity"] = place_info[index_city]
                if places_lived["hometown"] != places_lived["currentCity"]:
                    places_lived["list_of_cities"].append(place_info[index_city])
            elif "Hometown" in place_info[-1]:
                places_lived["hometown"] = place_info[index_city]
                if places_lived["hometown"] != places_lived["currentCity"]:
                    places_lived["list_of_cities"].append(place_info[index_city])
            else:
                otherPlace = {
                    "dateMove": "NA",
                    "city": place_info[index_city]
                }
                if "Only " in place_info[-1]:
                    index_city = -2
                else:
                    index_city = -1
                if any(str.isdigit(c) for c in place_info[index_city]):
                    otherPlace["dateMove"] = place_info[index_city]
                if place_info[index_city] != places_lived["hometown"] and place_info[index_city] != places_lived["currentCity"]:
                    places_lived["list_of_cities"].append(place_info[index_city])
                places_lived["otherCities"].append(otherPlace)
        if not places_lived["otherCities"]:
            places_lived["otherCities"] = "NA"
        if not places_lived["list_of_cities"]:
            places_lived["list_of_cities"] = "NA"
        completionCount = 1
        if all(value == "NA" for value in places_lived.values()):
            completionCount = 0
        return completionCount, places_lived

    def scrape_contact_and_basic(self, friend):
        self.get(format_url(friend, "about_contact_and_basic_info"))
        elts = self.find_elements_by_css_selector(".dati1w0a.tu1s4ah4.f7vcsfb0.discj3wi > div")
        text_elements = []
        for i in elts:
            text_elements.append(i.get_attribute("innerText"))

        basic_info = {
            "religiousviews": "NA",
            "politicalviews": "NA",
        }

        # getting basic info
        basic_info = extract_data(text_elements[2], basic_info)

        # format for consistency - NA
        if not basic_info:
            basic_info["religiousviews"] = "NA"
            basic_info["politicalviews"] = "NA"

        contact_and_basic_info = {
            "basic_info": basic_info
        }

        # update profile percentage counts
        completionCount = 2
        if basic_info["religiousviews"] == "NA":
            completionCount-=1
        if basic_info["politicalviews"] == "NA":
            completionCount-=1

        return completionCount, contact_and_basic_info
