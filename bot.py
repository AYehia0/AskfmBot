from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pickle
import time
from os import path
import google_answers
import subprocess


class Bot:

    def __init__(self, id):
        self.askfm_url = "https://ask.fm/"
        self.driver = webdriver.Chrome()
        self.id = id
        self.profile_url = self.askfm_url + self.id
        self.solve_cap = 120  # Time to slove the capatha

    def driver_init(self):
        """Init the selenium webdriver with the user_id"""

        # checking the login status
        if self.login():
            self.driver.get(self.profile_url)
            print("Login keys were found!")

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
            pickle.dump(self.driver.get_cookies(), open(pickle_name, "wb"))

        # it exists : load the cookies
        else:
            # go to google (any website)
            # self.driver.get(self.askfm_url)

            self.driver.get('https://google.com')

            # Load the cookies
            for cookie in pickle.load(open(pickle_name, "rb")):
                self.driver.add_cookie(cookie)
            cookies_exists = True

        return cookies_exists

    def get_num_questions(self, question_no=9):
        """Gets the last question in the inbox"""

        questions = list()
        inbox = "https://ask.fm/account/inbox"
        self.driver.get(inbox)

        # self.toggle_shoutouts()

        time.sleep(5)
        questions_wrapper = self.driver.find_elements_by_xpath(
            '//*[@id="contentArea"]/div/div/section/div[2]/div')
        print("len of questions: ", len(questions_wrapper))
        for i in range(1, question_no):

            # question = question.find_element_by_class_name('streamItem_footer')
            question_header = self.driver.find_element_by_xpath(
                f'//*[@id="contentArea"]/div/div/section/div[2]/div/article[{i}]')
            question_inside = question_header.find_element_by_class_name(
                'streamItem_footer')
            question_url = question_inside.find_element_by_tag_name(
                'a').get_attribute('href')
            questions.append(question_url)

        return questions

    def answer_question(self, question_url):
        """Answers a question with some random shit"""

        # Using js to pass text which contains emojis , since send_keys doesn't work
        JS_ADD_TEXT_TO_INPUT = """
        var elm = arguments[0], txt = arguments[1];
        elm.value += txt;
        elm.dispatchEvent(new Event('change'));
        """

        # opening the link
        self.driver.get(question_url)

        text_area = self.driver.find_element_by_id('question_answer_text')

        # the question
        q_context = self.driver.find_element_by_xpath(
            '/html/body/main/div/div/div[1]').text

        answer = subprocess.getoutput(f"tuxi -r {q_context}")

        print(answer)
        # Clearing the area just in case
        text_area.clear()

        self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, text_area, answer)

        # Sending
        self.driver.find_element_by_class_name('wrap').click()

    def answer_all(self):
        """Answer all fetched questions"""
        to_answer = self.get_num_questions()

        for q in to_answer:
            # checking if questions isn't a threaded on
            if 'threads' not in q:
                self.answer_question(q)
                time.sleep(3)

    def toggle_shoutouts(self):
        """Enable and disable Shoutout"""
        self.driver.find_element_by_class_name('icon-shoutout-pacman').click()
    

    def scroll_to_end(self):
        """Scroll to the end of the page to load all the questions"""
       
        length_page = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
        end_page = False
        while not end_page:
            try:
                page_last_record = length_page
                time.sleep(2)
                length_page = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
                if page_last_record == length_page:
                    end_page=True
            except:
                page_last_record = length_page
                time.sleep(2)
                length_page = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
                if page_last_record == length_page:
                    end_page=True
        

    def delete_all(self):
        """Delete all the answers ,, DANGER"""
        
        #going to home 
        self.driver.get(self.profile_url)


        #Scrolling to the end of the page 
        self.scroll_to_end() 
        
        self.driver.execute_script("var inputs = document.getElementsByClassName('icon-delete');var i = 0, h = inputs.length;function f() {inputs[i].click();i++;if( i < h ){setTimeout( f, 1000 );}}f();")
        gotit = True
        ans_num = 0
        while gotit:
            try:
                WebDriverWait(self.driver, 3).until(EC.alert_is_present())
                obj = self.driver.switch_to.alert
                obj.accept()
                ans_num += 1
            except TimeoutException:
                print("No Questions to delete !!!")
                gotit = False
        print(f"{ans_num} have been deleted !")


    def smart_delete(self):
        """Smarter way to delete answers, probably faster idk"""
        ans_num = 0

        # Loading all the questions/answers
        self.scroll_to_end()
        
        time.sleep(3)
        # looping through all the items 

        page_items = self.driver.find_elements_by_class_name('item-page')
        for item in reversed(page_items):
            questions = item.find_elements_by_class_name('item')

            for question in reversed(questions):
                
                try:
                    delete_question = question.find_element_by_class_name('streamItem_footer')
                    delete_question.find_element_by_class_name('icon-more').click()
                    delete_question.find_element_by_class_name('icon-delete').click()

                    WebDriverWait(self.driver, 6).until(EC.alert_is_present())
                    obj = self.driver.switch_to.alert
                    obj.accept()
                    time.sleep(.5)
                    ans_num += 1
                except:
                    print('Try again, error happend!')
                    self.smart_delete()
        print(f"{ans_num} questions have been deleted!")

#        time.sleep(2)
#        try:
#            while True:
#               #Clicking the menu
#                menu = self.driver.find_element_by_xpath('//*[@id="contentArea"]/div/div/section[2]/div[1]/div/article[1]/div[4]/a[1]')
#                menu.click()
#                self.driver.find_element_by_class_name('icon-delete').click()
#
#                # switching to the alert 
#                WebDriverWait(self.driver, 3).until(EC.alert_is_present())
#                obj = self.driver.switch_to.alert
#                obj.accept()
#                time.sleep(.5)
#                ans_num += 1
#        except Exception as e:
#                print(f"Done: {ans_num} were deleted !!! ", e)
#

