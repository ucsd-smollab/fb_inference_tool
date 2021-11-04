import time
import random
from sys import set_asyncgen_hooks
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from friend import Friend

#kowegkweog

def format_url(friend, sub_path):
    places_url = f'https://facebook.com/{friend.url}'
    if "profile.php" in friend.url:
        return f'{places_url}&sk={sub_path}'
    return f'{places_url}/{sub_path}'

def extract_data(data, formatted_data):
    try:
        splitted_data = data.split("\n")
        correct_data = [split_data for split_data in splitted_data if not "Shared " in split_data and not "Only " in split_data and not "Add " in split_data and not "Friends" in split_data]
        if "gender" in formatted_data:
            for i in range(1, len(correct_data)):
                if "Gender" in correct_data[i] and not correct_data[i-1] in ["Male", "Female", "Agender", "Androgyne", "Androgynous", "Bigender", "Cis", "Cis Female", "Cis Male", "Cis Man", "Cis Woman", "Cisgender"]:
                    correct_data.remove("Gender")
                    break
        #print(f"correct data: {correct_data}")  
        for i in range(1, len(correct_data), 2):
            category = correct_data[i+1].replace(" ", "").lower()
            if category in formatted_data:
                formatted_data[category] = correct_data[i]
        return formatted_data
    except:
        return {}

def generate_list_of_years(string_years, default_year=4):
    '''
    Case 1:
        Date - Present
    Case 2:
        Date - Date
    Case 3:
        Class of Year
    Case 4:
        Starting on Date
    Different Cases on Date Representation:
    Case 1:
        Month Day, Year
    Case 2:
        Month Year
    Case 3:
        Year
    '''
    list_of_years = []
    start_year = 0
    end_year = 0
    if string_years == "NA":
        return "NA"
    # Case 1 and Case 2
    if " - " in string_years:
        separated_dates = string_years.split(" - ")
        start_year = separated_dates[0]
        # Case 1: Date Representation
        if ", " in start_year:
            start_year = int(start_year.split(", ")[1])
        # Case 2: Date Representation
        elif " " in start_year:
            start_year = int(start_year.split(" ")[1])
        # Case 3: Date Representation
        else:
            start_year = int(start_year)
        # Case 2
        if not "Present" in separated_dates[1]:
            end_year = separated_dates[1]
            if ", " in end_year:
                end_year = int(end_year.split(", ")[1])
            elif " " in end_year:
                end_year = int(end_year.split(" ")[1])
            else:
                end_year = int(end_year)
        else:
            end_year = start_year + default_year
    # Case 3
    elif " of " in string_years:
        end_year = int(string_years.split(" of ")[1])
        start_year = end_year - default_year
    # Case 4
    elif " on " in string_years:
        separated_date = string_years.split(" on ")[1]
        separated_date = separated_date.split(", ")[1]
        start_year = int(separated_date)
        end_year = start_year + default_year
    difference = end_year - start_year
    for i in range(difference+1):
        list_of_years.append(f'{start_year+i}')
    return list_of_years

class FBdriver(webdriver.Chrome):
    def __init__(self, executable_path, options=None):
        if options is None:
            options = Options()
            option = webdriver.ChromeOptions()
            chrome_prefs = {}
            option.experimental_options["prefs"] = chrome_prefs
            options.add_argument(" - window-size=1920x1080")
            chrome_prefs["profile.default_content_settings"] = {"images": 2}
            chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
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

    def scroll(self, time):
        #remove if not testing
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # r = random.randint(5, 2*time-5)/10
        # sleep(r)
        sleep(time)
        return 0

    def get_link_and_mutual_friends(self, f):
        full_text = f.get_attribute("innerText")
        href = f.find_element_by_css_selector("._5pxa ._5pxc a").get_attribute("href")
        if not href:
            return ("", 0, False)
        href = href.split("/")[-1]
        if "mutual friends" in full_text:
            formatted_text = full_text.split(" ")
            for i in range(len(formatted_text)):
                if formatted_text[i] == "mutual":
                    total_mutual_friends = int(formatted_text[i-1].split("\n")[-1])
                    return (href, total_mutual_friends, True)
        return (href, 0, True)

    def full_friend_lookup_table(self, to_load=-1):
        start_time = time.time()
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
        print(f"{len(friend_urls)} friends: "+str(time.time() - start_time))
        #print("-------BEGIN FRIENDS-------")
        return friend_lookup_table

    def full_mutual_friend_list_mobile(self, friend):
        start_time = time.time()
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
                #print(f"{len(mutual_friends_urls)} mutual friends: "+str(time.time() - start_time))
                mutual_tries-=1
                to_return = float(time.time() - start_time)
            except Exception:
                mutual_tries-=1
                to_return = float(time.time() - start_time)
        return to_return

    def scrape_name(self, friend):
        #load friends facebook page
        self.get("https://facebook.com/" + friend.url)
        #find name element by css selector and return attribute string value
        elt = self.find_elements_by_css_selector("h1.gmql0nx0.l94mrbxd.p1ri9a11.lzcic4wl")
        if len(elt) > 1:
            elt = elt[1]
        else:
            elt = elt[0]
        name = elt.get_attribute("innerText")
        #print(name)
        return name

    def scrape_participant_name(self, participant):
        #load friends facebook page
        self.get("https://mobile.facebook.com/" + participant.url)
        #find name element by css selector and return attribute string value
        elt = self.find_element_by_css_selector("h3._6x2x")
        # if len(elt) > 1:
        #     elt = elt[1]
        # else:
        #     elt = elt[0]
        name = elt.get_attribute("innerText")
        #print(name)
        return name

    def scrape_work_and_ed(self, friend):
        start_time = time.time()
        self.get(format_url(friend, "about_work_and_education"))

        # getting profile image url
        profile_picture_section = self.find_element_by_class_name("q9uorilb.l9j0dhe7.pzggbiyp.du4w35lb")
        # profile_picture_section = self.find_element_by_class_name("b3onmgus.e5nlhep0.ph5uu5jm.ecm0bbzt.spb7xbtv.bkmhp75w.emlxlaya.s45kfl79.cwj9ozl2")
        profile_picture_image = profile_picture_section.find_element_by_tag_name("image")
        profile_picture_url = profile_picture_image.get_attribute("xlink:href")

        #work scraping
        sections = self.find_elements_by_css_selector(".dati1w0a.tu1s4ah4.f7vcsfb0.discj3wi > div")
        workList = []
        work = sections[0]
        for w in work.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt"):
            workName = "NA"
            dateOrLocationName = "NA"
            locationName = "NA"
            facebookPageUrl = "NA"
            list_of_years = "NA"

            if not "Add a " in w.get_attribute("innerText") and not " to show" in w.get_attribute("innerText"):
                workElement = w.find_element_by_css_selector(".ii04i59q.a3bd9o3v.jq4qci2q.oo9gr5id")
                workName = workElement.get_attribute("innerText")
                # workUrlElement = workElement.find_elements_by_css_selector("[role='link']")
                # if workUrlElement:
                #     facebookPageUrl = workUrlElement[0].get_attribute("href")
                dateOrLocations = w.find_elements_by_class_name("j5wam9gi.e9vueds3.m9osqain")
                if len(dateOrLocations) > 1:
                    dateOrLocationName = dateOrLocations[0].get_attribute("innerText")
                    locationName = dateOrLocations[1].get_attribute("innerText")
                elif len(dateOrLocations) == 1:
                    dateOrLocationName = dateOrLocations[0].get_attribute("innerText")
            else:
                continue
            
            if locationName == "NA":
                if not any(str.isdigit(c) for c in dateOrLocationName):
                    locationName = dateOrLocationName
                    dateOrLocationName = "NA"
                else:
                    list_of_years = generate_list_of_years(dateOrLocationName, 0)
            else:
                list_of_years = generate_list_of_years(dateOrLocationName, 0)
            if " at " in workName:
                workName = workName.split("at ")[1]
            tempDict = {
                "title": workName,
                "date": dateOrLocationName,
                "list_of_years": list_of_years,
                "location": locationName,
                "workUrl": facebookPageUrl
            }
            workList.append(tempDict)

        #college scraping
        college = sections[1]
        collegeList = []
        for c in college.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt"):
            schoolName = "NA"
            year = "NA"
            list_of_years = []
            facebookPageUrlC = "NA"

            if not "Add a " in c.get_attribute("innerText") and not " to show" in c.get_attribute("innerText"):
                schoolElement = c.find_element_by_css_selector(".ii04i59q.a3bd9o3v.jq4qci2q.oo9gr5id")
                schoolName = schoolElement.get_attribute("innerText")
                # schoolUrlElement = schoolElement.find_elements_by_css_selector("[role='link']")
                # if schoolUrlElement:
                #     facebookPageUrlC = schoolUrlElement[0].get_attribute("href")
                elements = c.find_elements_by_css_selector(".j5wam9gi.e9vueds3.m9osqain")

                if len(elements) == 1:
                    year = elements[0].get_attribute("innerText")
                elif len(elements) == 3:
                    year = elements[2].get_attribute("innerText")
                elif len(elements) == 5:
                    year = elements[4].get_attribute("innerText")
            else:
                continue

            if not any(str.isdigit(c) for c in year): 
                year = "NA" 
                
            if " at " in schoolName:
                schoolName = schoolName.split("at ")[1]
            list_of_years = generate_list_of_years(year)
            tempDict = {
                "title": schoolName,
                "list_of_years": list_of_years,
                "year": year,
                "collegeUrl": facebookPageUrlC
            }
            collegeList.append(tempDict)

        #high school scraping
        highSchool = sections[2]
        highSchoolList = []
        for h in highSchool.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt"):
            hSchoolName = "NA"
            hSYear = "NA"
            facebookPageUrlH = "NA"
            list_of_years = []

            if not "Add a " in h.get_attribute("innerText") and not " to show" in h.get_attribute("innerText"):
                hSchoolElement = h.find_element_by_css_selector(".ii04i59q.a3bd9o3v.jq4qci2q.oo9gr5id")
                hSchoolName = hSchoolElement.get_attribute("innerText")
                # hSchoolUrlElement = hSchoolElement.find_elements_by_css_selector("[role='link']")
                # if hSchoolUrlElement:
                #     facebookPageUrlH = hSchoolUrlElement[0].get_attribute("href")
                hSYear_element = h.find_elements_by_css_selector(".j5wam9gi.e9vueds3.m9osqain")
                if hSYear_element:
                    hSYear = hSYear_element[0].get_attribute("innerText")
            else:
                continue

            if " at " in hSchoolName:
                hSchoolName = hSchoolName.split(" at ")[1]
            if " to " in hSchoolName:
                hSchoolName = hSchoolName.split(" to ")[1]
            list_of_years = generate_list_of_years(hSYear)
            tempDict = {
                "title": hSchoolName,
                "list_of_years": list_of_years,
                "year": hSYear,
                "highSchoolUrl": facebookPageUrlH
            }
            highSchoolList.append(tempDict)

        #update profile completion counts
        completionCount = 3
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
        #print("Work and ed: "+str(time.time() - start_time))
        return (completionCount, workList, collegeList, highSchoolList, profile_picture_url, float(time.time() - start_time))

    def scrape_places_lived(self, friend):
        start_time = time.time()
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
        #print("Places lived: "+str(time.time() - start_time))
        return completionCount, places_lived, float(time.time() - start_time)

    def scrape_contact_and_basic(self, friend):
        start_time = time.time()
        self.get(format_url(friend, "about_contact_and_basic_info"))
        elts = self.find_elements_by_css_selector(".dati1w0a.tu1s4ah4.f7vcsfb0.discj3wi > div")
        text_elements = []
        for i in elts:
            text_elements.append(i.get_attribute("innerText"))

        contact_info = {
            "address": "NA",
            "mobile": "NA",
            "email": "NA"
        }
        websites = []
        social_links = []
        basic_info = {
            "languages": [],
            "religiousviews": "NA",
            "politicalviews": "NA",
            "interestedin": "NA",
            "gender": "NA",
            "birthdate": "NA",
            "birthyear": "NA"
        }
    
        # getting contact_info
        if not "No contact info to show" in text_elements[0]:
            contact_info = extract_data(text_elements[0], contact_info)
        
        # getting website and social media links
        if not "No links to show" in text_elements[1]:
            all_links = text_elements[1].split("\n")
            links = [link for link in all_links if not "Shared " in link and not "Only " in link and not "Add a " in link]
            for i in range(1, len(links), 2):
                if "Website" in links[i+1]:
                    websites.append(links[i])
                else:
                    social_links.append({
                        "platform": links[i+1], 
                        "identifier": links[i] 
                    })
        
        # getting basic info
        basic_info = extract_data(text_elements[2], basic_info)

        #format for consistency - NA
        if not basic_info:
            basic_info["languages"] = "NA"
            basic_info["religiousviews"] = "NA"
            basic_info["politicalviews"] = "NA"
            basic_info["birthyear"] = "NA"
            basic_info["interestedin"] = "NA"
            basic_info["gender"] = "NA"
            websites = "NA"
            social_links = "NA"
        else:
            if not basic_info["languages"]:
                basic_info["languages"] = "NA"
            if not websites:
                websites = "NA"
            if not social_links:
                social_links = "NA"
        contact_and_basic_info = {
            "contact_info": contact_info,
            "websites": websites,
            "social_links": social_links,
            "basic_info": basic_info
        }

        #update profile percentage counts
        completionCount = 4
        if basic_info["languages"] == "NA":
            completionCount-=1
        if basic_info["religiousviews"] == "NA":
            completionCount-=1
        if basic_info["politicalviews"] == "NA":
            completionCount-=1
        if basic_info["birthyear"] == "NA":
            completionCount-=1
        totalCount = 5
        if basic_info["interestedin"] == "NA":
            totalCount-=1
        if basic_info["gender"] == "NA":
            totalCount-=1
        if contact_info["address"] == "NA":
            totalCount-=1
        if contact_info["mobile"] == "NA":
            totalCount-=1
        if contact_info["email"] == "NA":
            totalCount-=1

        #print("contact and basic info: "+str(time.time()-start_time))
        return totalCount, completionCount, contact_and_basic_info, float(time.time()-start_time)

    # def scrape_family_and_rel(self, friend):
    #     start_time = time.time()
    #     self.get(format_url(friend, "about_family_and_relationships"))
    #     sections = self.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt")
    #     rel = sections[0]

    #     #scrape relationship
    #     relStatus = rel.get_attribute("innerText")
    #     if "No relationship info to show" in relStatus or "Add a " in relStatus:
    #         relStatus = "NA"
    #     else:
    #         relStatus = rel.get_attribute("innerText")
        
    #     #scrape family
    #     fam = sections[1:]
    #     famList = []
    #     for f in fam:
    #         famPart = f.get_attribute("innerText").partition('\n')
    #         famName = famPart[0]
    #         if "No family" in famName:
    #             famList = "NA"
    #             break
    #         elif "Add a " in famName:
    #             continue
    #         famRel = famPart[2]
    #         famUrl = "NA"

    #         famUrlElement = f.find_elements_by_css_selector("[role='link']")

    #         if famUrlElement:
    #             famUrl = famUrlElement[0].get_attribute("href").split("/")[-1]

    #         famList.append(
    #             {
    #                 "relation": famRel,
    #                 "name": famName,
    #                 "url": famUrl
    #             }
    #         )

    #     relAndFamDict = {
    #         "relationship": relStatus,
    #         "family members": famList
    #     }
    #     completionCount = 1
    #     if famList == "NA":
    #         completionCount-=1
    #     totalCount = 1
    #     if relStatus == "NA":
    #         totalCount-=1
    #     #print("relationship and family: "+str(time.time()-start_time))
    #     return totalCount, completionCount, relAndFamDict, float(time.time()-start_time)

def populate_category_groups(data, person_url, category_name, category_groups):
    if data == "NA":
        category_groups[category_name]["no_data"].append(person_url)
        return
    if not isinstance(data, list):
        data = data
        if data in category_groups[category_name]:
            category_groups[category_name][data].append(person_url)
        else:
            category_groups[category_name][data] = [person_url]
        return
    for entry in data:
        entry_name = entry
        if isinstance(entry, dict):
            entry_name = entry["title"]
        entry_name = entry_name
        if entry_name in category_groups[category_name]:
            category_groups[category_name][entry_name].append(person_url)
        else:
            category_groups[category_name][entry_name] = [person_url]

def get_participant_data(category_groups, driver):
    #scrape user info
    participant = Friend(driver.participant_path)
    participant.name = driver.scrape_participant_name(participant)
    (count, participant.attributes["work"], participant.attributes["college"], participant.attributes["highschool"], participant.profile_picture_url, time) = driver.scrape_work_and_ed(participant)
    participant.percent_complete+=count
    populate_category_groups(participant.attributes["work"], participant.url, "work", category_groups)
    populate_category_groups(participant.attributes["college"], participant.url, "college", category_groups)
    populate_category_groups(participant.attributes["highschool"], participant.url, "highschool", category_groups)
    (count, participant.attributes["places lived"], time) = driver.scrape_places_lived(participant)
    participant.percent_complete+=count
    populate_category_groups(participant.attributes["places lived"]["list_of_cities"], participant.url, "cities", category_groups)
    (participant.percent_total_complete, count, participant.attributes["contact and basic"], time) = driver.scrape_contact_and_basic(participant)
    participant.percent_complete+=count
    populate_category_groups(participant.attributes["contact and basic"]["basic_info"]["religiousviews"], participant.url, "religiousviews", category_groups)
    populate_category_groups(participant.attributes["contact and basic"]["basic_info"]["politicalviews"], participant.url, "politicalviews", category_groups)
    #populate_category_groups(participant.attributes["contact and basic"]["basic_info"]["birthyear"], participant.url, "birthyear", category_groups)
    #(tempCount, count, participant.attributes["family and rel"], time) = driver.scrape_family_and_rel(participant)
    #participant.percent_total_complete+=tempCount
    participant.percent_complete+=count
    participant.percent_total_complete+=participant.percent_complete
    participant.percent_complete = round(participant.percent_complete/7, 3)
    participant.percent_total_complete = round(participant.percent_total_complete/13, 3)
    return participant

def scrape_friend_info(f, num_mutual, category_groups, driver):
    try:
        time_array = []
        f.name = driver.scrape_name(f)
        time = driver.full_mutual_friend_list(f, num_mutual)
        time_array.append(time)
        (count, f.attributes["work"], f.attributes["college"], f.attributes["highschool"], f.profile_picture_url, time) = driver.scrape_work_and_ed(f)
        time_array.append(time)
        f.percent_complete+=count    
        (count, f.attributes["places lived"], time) = driver.scrape_places_lived(f)
        time_array.append(time)
        f.percent_complete+=count    
        (f.percent_total_complete, count, f.attributes["contact and basic"], time) = driver.scrape_contact_and_basic(f)
        time_array.append(time)
        #(tempCount, count, f.attributes["family and rel"], time) = driver.scrape_family_and_rel(f)
        #time_array.append(time)
        #f.percent_complete+=count
        f.percent_total_complete+=f.percent_complete
        #f.percent_total_complete+=tempCount
        f.percent_complete = round(f.percent_complete/7, 3)
        f.percent_total_complete = round(f.percent_total_complete/13, 3)
        return time_array
    except NoSuchElementException:
        return None
def populate_category_groups_funct(f, category_groups):
    populate_category_groups(f.attributes["work"], f.url, "work", category_groups)
    populate_category_groups(f.attributes["college"], f.url, "college", category_groups)
    populate_category_groups(f.attributes["highschool"], f.url, "highschool", category_groups)
    populate_category_groups(f.attributes["places lived"]["list_of_cities"], f.url, "cities", category_groups)
    populate_category_groups(f.attributes["contact and basic"]["basic_info"]["religiousviews"], f.url, "religiousviews", category_groups)
    populate_category_groups(f.attributes["contact and basic"]["basic_info"]["politicalviews"], f.url, "politicalviews", category_groups)
    populate_category_groups(f.attributes["contact and basic"]["basic_info"]["birthyear"], f.url, "birthyear", category_groups)

