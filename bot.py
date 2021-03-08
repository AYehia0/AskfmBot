from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import time

class Bot:

    def __init__(self):
        self.askfm_url = "https://ask.fm/"
        self.driver = webdriver.Chrome()

    def driver_init(self, id):
        """Init the selenium webdriver with the user_id"""

        self.driver.get("https://google.com/")
        time.sleep(15)
        self.login()
        self.driver.get(self.askfm_url+id)

    def login(self):
        """Login to askFm for only the first time and save the User_data in the same working dir"""
        #time.sleep(50)
        #pickle.dump(self.driver.get_cookies() , open("askfm.pkl","wb")) 
        for cookie in pickle.load(open("askfm.pkl", "rb")): 
            self.driver.add_cookie(cookie) 