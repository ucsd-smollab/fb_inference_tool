from sys import set_asyncgen_hooks
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import time
from friend import Friend
import random

def format_url(friend, sub_path):
    places_url = f'https://facebook.com/{friend.url}'
    if "profile.php" in friend.url:
        return f'{places_url}&sk={sub_path}'
    return f'{places_url}/{sub_path}'

def extract_data(data, formatted_data):
    splitted_data = data.split("\n")
    correct_data = [split_data for split_data in splitted_data if not "Shared " in split_data and not "Only " in split_data and not "Add a" in split_data and not "Friends" in split_data]
    print(f"correct data: {correct_data}")
    for i in range(1, len(correct_data), 2):
        category = correct_data[i+1].replace(" ", "").lower()
        if category in formatted_data:
            formatted_data[category] = correct_data[i]
    return formatted_data

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
        #self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(time)

    def full_friend_lookup_table(self):
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
        while (not all_friends_loaded):
            for i in range(0, 5):
                r = random.randint(0, 5)/10
                self.scroll(0.5+r)
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
        # print("friends")
        # print(len(friend_urls))
        # print("--- %s seconds ---" % (time.time() - start_time))
        return friend_lookup_table

    def full_mutual_friend_list(self, friend):
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
                r = random.randint(0, 5)/10
                self.scroll(0.5+r)
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
        # print("mutual friends")
        # print(len(friend_paths))
        # print("--- %s seconds ---" % (time.time() - start_time))
        return friend_paths

    def scrape_name(self, friend):
        #load friends facebook page
        self.get("https://facebook.com/" + friend.url)
        #find name element by css selector and return attribute string value
        elt = self.find_element_by_css_selector("h1.gmql0nx0.l94mrbxd.p1ri9a11.lzcic4wl")
        name = elt.get_attribute("innerText")
        #print(name)
        return name

    def scrape_work_and_ed(self, friend):
        self.get(format_url(friend, "about_work_and_education"))

        # getting profile image url
        profile_picture_section = self.find_element_by_class_name("oajrlxb2.gs1a9yip.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.nhd2j8a9.q9uorilb.mg4g778l.btwxx1t3.pfnyh3mw.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.lzcic4wl.abiwlrkh.p8dawk7l.oo9gr5id")
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
                workUrlElement = workElement.find_elements_by_css_selector("[role='link']")
                if workUrlElement:
                    facebookPageUrl = workUrlElement[0].get_attribute("href")
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
        #print(workList)

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
                schoolUrlElement = schoolElement.find_elements_by_css_selector("[role='link']")
                if schoolUrlElement:
                    facebookPageUrlC = schoolUrlElement[0].get_attribute("href")
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
        #print(collegeList)

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
                hSchoolUrlElement = hSchoolElement.find_elements_by_css_selector("[role='link']")
                if hSchoolUrlElement:
                    facebookPageUrlH = hSchoolUrlElement[0].get_attribute("href")
                hSYear_element = h.find_elements_by_css_selector(".j5wam9gi.e9vueds3.m9osqain")
                if hSYear_element:
                    hSYear = hSYear_element[0].get_attribute("innerText")
                    #print(hSYear)
            else:
                continue

            if " at " in hSchoolName:
                hSchoolName = hSchoolName.split(" at ")[1]
            if " to " in hSchoolName:
                hSchoolName = hSchoolName.split(" to ")[1]
            #print(f'hsYear: {hSYear}')
            list_of_years = generate_list_of_years(hSYear)
            tempDict = {
                "title": hSchoolName,
                "list_of_years": list_of_years,
                "year": hSYear,
                "highSchoolUrl": facebookPageUrlH
            }
            highSchoolList.append(tempDict)
        
        #print(highSchoolList)

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
        #print("work")
        #print(workList)
        #print("college")
        #print(collegeList)
        #print("high school")
        #print(highSchoolList)
        return (completionCount, workList, collegeList, highSchoolList, profile_picture_url)

    def scrape_places_lived(self, friend):
        self.get(format_url(friend, "about_places"))
        sleep(0.2)
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
        #print("places lived")
        #print(places_lived)
        return completionCount, places_lived

    def scrape_contact_and_basic(self, friend):
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

        #print("contact and basic info")
        #print(contact_and_basic_info)
        return totalCount, completionCount, contact_and_basic_info

    def scrape_family_and_rel(self, friend):
        self.get(format_url(friend, "about_family_and_relationships"))
        sections = self.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt")
        rel = sections[0]

        #scrape relationship
        relStatus = rel.get_attribute("innerText")
        if "No relationship info to show" in relStatus or "Add a " in relStatus:
            relStatus = "NA"
        else:
            relStatus = rel.get_attribute("innerText")
        
        #scrape family
        fam = sections[1:]
        famList = []
        for f in fam:
            famPart = f.get_attribute("innerText").partition('\n')
            famName = famPart[0]
            if "No family" in famName:
                famList = "NA"
                break
            elif "Add a " in famName:
                continue
            famRel = famPart[2]
            famUrl = "NA"

            famUrlElement = f.find_elements_by_css_selector("[role='link']")

            if famUrlElement:
                famUrl = famUrlElement[0].get_attribute("href").split("/")[-1]

            famList.append(
                {
                    "relation": famRel,
                    "name": famName,
                    "url": famUrl
                }
            )

        relAndFamDict = {
            "relationship": relStatus,
            "family members": famList
        }
        completionCount = 1
        if famList == "NA":
            completionCount-=1
        totalCount = 1
        if relStatus == "NA":
            totalCount-=1
        #print("relationship and family")
        #print(relAndFamDict)
        return totalCount, completionCount, relAndFamDict