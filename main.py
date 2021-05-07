import os
import datetime
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from multiprocessing import Process, Manager, Lock
from fn_login import Login  #Login on instagram
from fn_DB01 import DB01
from fn_DB02 import DB02

'''Settings'''
# Starting headless Chrome
options = Options()
options.headless = True
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')  # headless
# driver = webdriver.Chrome('chromedriver')  # not headless
profile = 'feliperosa_oficial'
password = 'f220912k'
Login(driver, profile, password).run() #login on Instagram

username = 'renovesergipe'
cookies = driver.get_cookies() #saving cookies for future access
root_folder = 'assets_fn_04_to_github'
DB01(username, driver, cookies, root_folder).run()
DB02(username, driver, cookies, root_folder).run()

driver.quit()

