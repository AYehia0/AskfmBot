from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import time
from os import path

class Bot:

    def __init__(self, id):
        self.askfm_url = "https://ask.fm/"
        self.driver = webdriver.Chrome()
        self.id = id
        self.profile_url = self.askfm_url + self.id
        self.solve_cap = 120 # Time to slove the capatha

    def driver_init(self):
        """Init the selenium webdriver with the user_id"""

        # checking the login status
        if self.login():
            self.driver.get(self.profile_url)
            print("Success")

    def login(self):
        """Login to askFm for only the first time and save the User_data in the same working dir"""
        pickle_name = f"askfm_{self.id}"
        cookies_exists = False
        # checking if pickles exists
        if not path.exists(pickle_name):
            # wait for signin 
            print("Please SignIn")

            self.driver.get(self.profile_url)
            
            # enough time to solve stupid capatha
            time.sleep(self.solve_cap)

            # dumping the pickle cookies
            pickle.dump(self.driver.get_cookies() , open(pickle_name,"wb"))
            
        # it exists : load the cookies
        else:
            # go to google (any website)
            self.driver.get("https://google.com/")

            # Load the cookies
            for cookie in pickle.load(open(pickle_name, "rb")): 
                self.driver.add_cookie(cookie) 
            cookies_exists = True

        return cookies_exists

    def get_last_question(self):
        """Gets the last question in the inbox"""

        inbox = "https://ask.fm/account/inbox"
        self.driver.get(inbox)

        time.sleep(5)
        questions_wrapper = self.driver.find_elements_by_xpath('//*[@id="contentArea"]/div/div/section/div[2]/div')
        print("len of questions: ", len(questions_wrapper))
        for i in range(1,6):

            # question = question.find_element_by_class_name('streamItem_footer')
            question_header = self.driver.find_element_by_xpath(f'//*[@id="contentArea"]/div/div/section/div[2]/div/article[{i}]')
            question_inside = question_header.find_element_by_class_name('streamItem_footer')
            question_url = question_inside.find_element_by_tag_name('a').get_attribute('href')
            print(f"Question no : {i}",question_url)

    def toggle_shoutouts(self):
        """Enable and disable Shoutout"""
        self.driver.find_element_by_class_name('icon-shoutout-pacman').click()
