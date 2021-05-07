import time

class Login():
    def __init__(self, driver, profile, password):
        self.profile = profile
        self.driver = driver
        self.password = password

    def run(self):
        #abrir e logar
        self.driver.get('https://www.instagram.com/')
        self.driver.implicitly_wait(20)
        print("Logging into instagram")
        #ajustar para esperar por https://www.instagram.com/accounts/onetap/?next=%2F
        self.driver.find_element_by_name('username').send_keys(self.profile)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
        print("Logging concluded successfully")
        time.sleep(5)
