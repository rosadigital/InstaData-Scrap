import time
import pickle  # To work with cookies
import json
from selenium.webdriver.support.wait import WebDriverWait


class Login():
    def __init__(self, driver, profile, password):
        self.profile = profile
        self.driver = driver
        self.password = password

    def run(self):
        self.driver.get('https://www.instagram.com/')  # open and logging without cookies
        self.driver.implicitly_wait(20)
        print("Logging into instagram")
        self.driver.find_element_by_name('username').send_keys(self.profile)  # passing username to logging
        self.driver.find_element_by_name('password').send_keys(self.password)  # passing password to logging
        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
        print("Logging successfully completed")
        time.sleep(5)
