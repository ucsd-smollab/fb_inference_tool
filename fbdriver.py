from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from friend import Friend

def format_url(friend, sub_path):
    places_url = f'https://facebook.com/{friend.path}'
    if "profile.php" in friend.path:
        return f'{places_url}&sk={sub_path}'
    return f'{places_url}/{sub_path}'

def extract_data(data, formatted_data):
    splitted_data = data.split("\n")
    correct_data = [split_data for split_data in splitted_data if not "Shared " in split_data and not "Only " in split_data]
    for i in range(1, len(correct_data), 2):
        category = correct_data[i+1].replace(" ", "").lower()
        formatted_data[category] = correct_data[i]
    return formatted_data

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
            return mutual_friends_paths
        except Exception:
            return None

    def scrape_name(self, friend):
        #load friends facebook page
        self.get("https://facebook.com/" + friend.path)
        #find name element by css selector and return attribute string value
        elt = self.find_element_by_css_selector("h1.gmql0nx0.l94mrbxd.p1ri9a11.lzcic4wl")
        name = elt.get_attribute("innerText")
        return name

    def scrape_work_and_ed(self, friend):
        self.get(format_url(friend, "about_work_and_education"))
        sections = self.find_elements_by_css_selector(".dati1w0a.tu1s4ah4.f7vcsfb0.discj3wi > div")
        workList = []
        work = sections[0]
        for w in work.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt"):
            workName = ""
            dateOrLocationName = ""
            locationName = ""
            facebookPageUrl = ""
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

            if not locationName and dateOrLocationName:
                if not any(str.isdigit(c) for c in dateOrLocationName):
                    locationName = dateOrLocationName
                    dateOrLocationName = ""
            elif locationName and dateOrLocationName:
                dateOrLocationName = dateOrLocationName[:-2]
            tempDict = {
                "title": workName,
                "date": dateOrLocationName,
                "location": locationName,
                "workUrl": facebookPageUrl
            }
            workList.append(tempDict)

        college = sections[1]
        collegeList = []
        for c in college.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt"):
            schoolName = ""
            degree = ""
            otherConcentrations = ""
            year = ""
            facebookPageUrlC = ""
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
                    degree = ""
                elif degree[:4]=="Also" and otherConcentrations:
                    otherConcentrations = degree
                    degree = ""
                elif degree[:4]=="Also" and otherConcentrations:
                    year = otherConcentrations
                    otherConcentrations = degree
                    degree = ""
                elif any(str.isdigit(c) for c in otherConcentrations):
                    year = otherConcentrations
                    otherConcentrations = ""
            tempDict = {
                "schoolTitle": schoolName,
                "degree": degree.replace("\n", ""),
                "concentrations": otherConcentrations.replace("\n", ""),
                "year": year,
                "collegeUrl": facebookPageUrlC
            }
            collegeList.append(tempDict)

        highSchool = sections[2]
        highSchoolList = []
        for h in highSchool.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt"):
            hSchoolName = ""
            hSYear = ""
            facebookPageUrlH = ""
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
            tempDict = {
                "schoolName": hSchoolName,
                "year": hSYear,
                "highSchoolUrl": facebookPageUrlH
            }
            highSchoolList.append(tempDict)
        work_and_ed = {
            "work": workList,
            "college": collegeList,
            "highschool": highSchoolList
        }
        return work_and_ed

    def scrape_places_lived(self, friend):
        self.get(format_url(friend, "about_places"))
        sleep(0.2)
        places_lived = {
            "hometown": "",
            "currentCity": "",
            "otherCities": []
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
            elif "Hometown" in place_info[-1]:
                places_lived["hometown"] = place_info[index_city]
            else:
                otherPlace = {
                    "dateMove": "",
                    "city": place_info[index_city]
                }
                if "Only " in place_info[-1]:
                    index_city = -2
                else:
                    index_city = -1
                if any(str.isdigit(c) for c in place_info[index_city]):
                    otherPlace["dateMove"] = place_info[index_city]
                places_lived["otherCities"].append(otherPlace)
        return places_lived

    def scrape_contact_and_basic(self, friend):
        self.get(format_url(friend, "about_contact_and_basic_info"))
        elts = self.find_elements_by_css_selector(".dati1w0a.tu1s4ah4.f7vcsfb0.discj3wi > div")
        text_elements = []
        for i in elts:
            text_elements.append(i.get_attribute("innerText"))

        contact_info = {
            "address": "",
            "mobile": "",
            "email": ""
        }
        websites = []
        social_links = []
        basic_info = {
            "languages": [],
            "religiousviews": "",
            "politicalviews": "",
            "interestedin": "",
            "gender": "",
            "birthdate": "",
            "birthyear": ""
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
        contact_and_basic_info = {
            "contact_info": contact_info,
            "websites": websites,
            "social_links": social_links,
            "basic_info": basic_info
        }
        return contact_and_basic_info

    def scrape_family_and_rel(self, friend):
        self.get(format_url(friend, "about_family_and_relationships"))
        sections = self.find_elements_by_css_selector(".rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.o8rfisnq.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt")
        rel = sections[0]
        tempDictRel = {}
        relName = ""
        relUrl = ""
        relDescription = ""

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
            famRel = famPart[2]
            famUrl = ""
            try:
                famUrl = f.find_elements_by_css_selector("* > div > a")[0].get_attribute("href")
            except:
                pass
            if famRel:
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
        return relAndFamDict
