from sys import set_asyncgen_hooks
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from friend import Friend

def format_url(friend, sub_path):
    places_url = f'https://facebook.com/{friend.url}'
    if "profile.php" in friend.url:
        return f'{places_url}&sk={sub_path}'
    return f'{places_url}/{sub_path}'

def extract_data(data, formatted_data):
    splitted_data = data.split("\n")
    correct_data = [split_data for split_data in splitted_data if not "Shared " in split_data and not "Only " in split_data]
    for i in range(1, len(correct_data), 2):
        category = correct_data[i+1].replace(" ", "").lower()
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
    if not string_years:
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
            mutual_friends_elements = self.find_element_by_class_name("j83agx80.btwxx1t3.lhclo0ds.i1fnvgqd")
            if "No friends" in mutual_friends_elements.get_attribute("innerText"):
                return "NA"
            mutual_friends_anchors = mutual_friends_elements.find_elements_by_css_selector("[tabindex='-1']")
            mutual_friends_urls = [anchor.get_attribute("href") for anchor in mutual_friends_anchors]
            mutual_friends_paths = [path.split("/")[-1] for path in mutual_friends_urls]
            return mutual_friends_paths
        except Exception:
            return "NA"

    def scrape_name(self, friend):
        #load friends facebook page
        self.get("https://facebook.com/" + friend.url)
        #find name element by css selector and return attribute string value
        elt = self.find_element_by_css_selector("h1.gmql0nx0.l94mrbxd.p1ri9a11.lzcic4wl")
        name = elt.get_attribute("innerText")
        return name

    def scrape_work_and_ed(self, friend):
        self.get(format_url(friend, "about_work_and_education"))

        # getting profile image url
        profile_picture_section = self.find_element_by_class_name("oajrlxb2.gs1a9yip.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.nhd2j8a9.q9uorilb.mg4g778l.btwxx1t3.pfnyh3mw.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.lzcic4wl.abiwlrkh.p8dawk7l.oo9gr5id")
        profile_picture_image = profile_picture_section.find_element_by_tag_name("image")
        profile_picture_url = profile_picture_image.get_attribute("xlink:href")

        sections = self.find_elements_by_css_selector(".dati1w0a.tu1s4ah4.f7vcsfb0.discj3wi > div")
        workList = []
        work = sections[0]
        for w in work.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt"):
            workName = "NA"
            dateOrLocationName = "NA"
            locationName = "NA"
            facebookPageUrl = "NA"
            list_of_years = "NA"
            try:
                workName = w.find_elements_by_css_selector("* > div")[0].get_attribute("innerText")
                try:
                    facebookPageUrl = w.find_elements_by_css_selector("* > div > a")[0].get_attribute("href")
                except:
                    pass
                try:
                    dateOrLocationName = w.find_elements_by_css_selector("* > div + div > div > span")[0].get_attribute("innerText")
                    try:
                        locationName = w.find_elements_by_css_selector("* > div + div > div > span + span")[0].get_attribute("innerText")
                    except:
                        pass
                except:
                    pass
            except:
                continue

            if locationName == "NA" and dateOrLocationName == "NA":
                if not any(str.isdigit(c) for c in dateOrLocationName):
                    locationName = dateOrLocationName
                    dateOrLocationName = "NA"
                else:
                    list_of_years = generate_list_of_years(dateOrLocationName, 0)
            elif locationName != "NA" and dateOrLocationName != "NA":
                dateOrLocationName = dateOrLocationName[:-2]
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

        college = sections[1]
        collegeList = []
        for c in college.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt"):
            schoolName = "NA"
            degree = "NA"
            otherConcentrations = "NA"
            year = "NA"
            list_of_years = []
            facebookPageUrlC = "NA"
            try:
                schoolName = c.find_elements_by_css_selector("* > div")[0].get_attribute("innerText")
                try:
                    facebookPageUrlC = c.find_elements_by_css_selector("* > div > a")[0].get_attribute("href")
                except:
                    pass
                try:
                    degree = c.find_elements_by_css_selector("* > div + div > div > span")[0].get_attribute("innerText")
                    try:
                        otherConcentrations = c.find_elements_by_css_selector("* > div + div > div > span + span")[0].get_attribute("innerText")
                        try:
                            year = c.find_elements_by_css_selector("* > div + div > div > span + span + span")[0].get_attribute("innerText")
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
            except:
                continue          
            if degree and not any(str.isdigit(c) for c in year):  
                if any(str.isdigit(c) for c in degree):
                    year = degree
                    degree = "NA"
                elif degree[:4]=="Also" and otherConcentrations:
                    otherConcentrations = degree
                    degree = "NA"
                elif degree[:4]=="Also" and otherConcentrations:
                    year = otherConcentrations
                    otherConcentrations = degree
                    degree = "NA"
                elif any(str.isdigit(c) for c in otherConcentrations):
                    year = otherConcentrations
                    otherConcentrations = "NA"
            if " at " in schoolName:
                schoolName = schoolName.split("at ")[1]
            list_of_years = generate_list_of_years(year)
            tempDict = {
                "schoolTitle": schoolName,
                "degree": degree.replace("\n", ""),
                "concentrations": otherConcentrations.replace("\n", ""),
                "list_of_years": list_of_years,
                "year": year,
                "collegeUrl": facebookPageUrlC
            }
            collegeList.append(tempDict)

        highSchool = sections[2]
        highSchoolList = []
        for h in highSchool.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt"):
            hSchoolName = "NA"
            hSYear = "NA"
            facebookPageUrlH = "NA"
            list_of_years = []
            try:
                hSchoolName = h.find_elements_by_css_selector("* > div")[0].get_attribute("innerText")
                try:
                    facebookPageUrlH = h.find_elements_by_css_selector("* > div > a")[0].get_attribute("href")
                except:
                    pass
                try:
                    hSYear = h.find_elements_by_css_selector("* > div + div > div > span")[0].get_attribute("innerText")
                except:
                    pass
            except:
                continue
            if " at " in hSchoolName:
                hSchoolName = hSchoolName.split(" at ")[1]
            if " to " in hSchoolName:
                hSchoolName = hSchoolName.split(" to ")[1]
            list_of_years = generate_list_of_years(hSYear)
            tempDict = {
                "schoolName": hSchoolName,
                "list_of_years": list_of_years,
                "year": hSYear,
                "highSchoolUrl": facebookPageUrlH
            }
            highSchoolList.append(tempDict)
        completionCount = 3
        if not workList:
            workList = "NA"
            completionCount-=1
        if not collegeList:
            collegeList = "NA"
            completionCount-=1
        if not highSchoolList:
            highSchoolList = "NA"
            completionCount-=1
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
            place_info = place.split("\n")
            if "Add " in place_info[index_city]:
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
        #print(places_lived["list_of_cities"])
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

        if not basic_info["languages"]:
            basic_info["languages"] = "NA"
        contact_and_basic_info = {
            "contact_info": contact_info,
            "websites": websites,
            "social_links": social_links,
            "basic_info": basic_info
        }
        completionCount = 4
        if basic_info["languages"] == "NA":
            completionCount-=1
        if basic_info["religiousviews"] == "NA":
            completionCount-=1
        if basic_info["politicalviews"] == "NA":
            completionCount-=1
        if basic_info["birthyear"] == "NA":
            completionCount-=1
        return completionCount, contact_and_basic_info

    def scrape_family_and_rel(self, friend):
        self.get(format_url(friend, "about_family_and_relationships"))
        sections = self.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt")
        rel = sections[0]
        tempDictRel = {}
        relName = "NA"
        relUrl = "NA"
        relDescription = "NA"

        try:
            relStatus = rel.find_elements_by_css_selector("* > div")[0].get_attribute("innerText")
            if relStatus != "Single":
                relName = relStatus
                try:
                    relUrl = rel.find_elements_by_css_selector("* > div > a")[0].get_attribute("href")
                except:
                    pass
                try:
                    relDescription = rel.find_elements_by_css_selector("* > div + div")[0].get_attribute("innerText")
                except:
                    pass
                tempDictRel = {
                    "name": relName,
                    "url": relUrl,
                    "description": relDescription
                }
            else:
                tempDictRel = "NA"
        except:
            pass

        tempDictRel = {
            "name": relName,
            "url": relUrl,
            "description": relDescription
        }
        
        fam = sections[1:]
        famList = []
        for f in fam:
            famPart = f.get_attribute("innerText").partition('\n')
            famName = famPart[0]
            if "No family" in famName:
                famList = "NA"
                break
            famRel = famPart[2]
            famUrl = "NA"
            try:
                famUrl = f.find_elements_by_css_selector("* > div > a")[0].get_attribute("href")
            except:
                pass
            if famRel == "NA":
                continue   
            famList.append(
                {
                    "relation": famRel,
                    "name": famName,
                    "url": famUrl
                }
            )

        relAndFamDict = {
            "relationship": tempDictRel,
            "family members": famList
        }
        completionCount = 1
        if famList == "NA":
            completionCount-=1
        print(relAndFamDict)
        return completionCount, relAndFamDict