from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from assets_fn_03 import fn_login

import csv
import time
import pandas as pd
from bs4 import BeautifulSoup as bs

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
from pathlib import Path

def fn_followers_link (username, driver,root_folder):
    #acessar pagina a ser pesquisada
    print("Accessing instagram page to be searched")
    # time.sleep(10)
    username = username
    driver.get('https://www.instagram.com/'+username)
    wait = WebDriverWait(driver, 10)
    try:
        element = wait.until(EC.presence_of_element_located(((By.PARTIAL_LINK_TEXT, 'follower'))))
    except:
        element = wait.until(EC.presence_of_element_located(((By.PARTIAL_LINK_TEXT, 'seguidor'))))
    # time.sleep(2)
    print("Accessing followers page")
    try:
        driver.find_element_by_partial_link_text("follower").click()
    except:
        driver.find_element_by_partial_link_text("seguidor").click()
    get_url = driver.current_url
    # print(get_url)
    print("Followers page accessed successfully")

    try:
        element = wait.until(EC.presence_of_element_located(((By.XPATH, "//*[@id='react-root']/section/main/div/ul/li[2]/a/span"))))
    except:
        element = wait.until(EC.presence_of_element_located(((By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span'))))

    try:
        total_followers = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/ul/li[2]/a/span").text
        total_followers = total_followers.replace('.', '')
        total_followers = total_followers.replace(',', '')
    except:
        total_followers = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text
        total_followers = total_followers.replace('.', '')
        total_followers = total_followers.replace(',', '')


    if total_followers.find('k') == True:
        total_followers = total_followers.replace('k', '')
        total_followers = int(float(total_followers))*100
        print("Total number of followers approximately: ", total_followers)
    else:
        total_followers = int(float(total_followers))
        print("Total number of followers: ", total_followers)

    # numbers_of_scroll = round(int(total_followers)/6)
    print("---------------------------")
    print("Amount of followers: ", total_followers)
    # print("Amount of scrolldown: ", numbers_of_scroll)

    fBody = driver.find_element_by_xpath("//div[@class='isgrP']")
    scroll = 1
    followers_loaded = 0
    items = []
    index = 0
    index_now = 0
    lista = []
    while index_now < int(float(total_followers)):
        time.sleep(1)
        # element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'FPmhX notranslate _0imsa')))
        source = driver.page_source
        data = bs(source, 'html.parser')

        for followers in data.find_all('a', class_='FPmhX notranslate _0imsa'):
            followers_link = followers['href']
            items.append(followers_link)
            index += 1
        lista = items
        lista = pd.Series(lista).drop_duplicates()  # removerduplicadosdalista

        index_now = len(lista)
        print("total de followers_now",index_now)

        if index_now < int(total_followers):
            index_now = 0
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
            time.sleep(1)
            # element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='isgrP']//li")))
            fList = driver.find_elements_by_xpath("//div[@class='isgrP']//li")
            # print(scroll, " - fList len is {}".format(len(fList)))
            # print(scroll)
            scroll += 1

    print("---- Process Concluded ----")
    print("---------------------------")
    print("----- Showing results -----")
    print("Amount of followers found: ",len(fList))
    print("Amount of ScrollDown done: ",scroll)
    print("---------------------------")
    print("----- Processing data -----")
    #soup of data
    source = driver.page_source
    data = bs(source, 'html.parser')
    # print(data)
    # print()
    # name_of_followers = data.find(Class_= "FPmhX notranslate  _0imsa")
    # print(name_of_followers.text)
    # seguidores = data.find_all(span='Jv7Aj mArmR MqpiF  ')
    # print(seguidores)

    #creating csv
    print("------ Creating CSV ------")
    root_folder = str(root_folder)
    path = root_folder + '/' + username
    csv_file = open(str(username)+'/relatorio_DB03_'+str(username)+'.csv', 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['index', 'followers_links', 'followers_names'])

    #scrape followers links and names from data
    print("Scraping followers links and names from data")
    index=0
    for followers in data.find_all('a', class_='FPmhX notranslate _0imsa'):
        index = index+1
        # print(index)
        #extraction of followers_links
        followers_links = followers['href']
        # print(followers_links)

        #extraction of followers_names
        followers_names = followers.text
        # print(followers_names)

        csv_writer.writerow([index, followers_links, followers_names])

    #close csv
    csv_file.close()

    print("---------------------------")
    print("Report:")
    print("Amount of followers: ", int(total_followers))
    print("Amount of followers loaded: ", index_now)
    print("---------------------------")

if __name__ == '__main__':
    username = 'maisautonomo'

    # creating folder
    print('Creating folder')
    try:
        root_folder = Path(__file__).parents[0]
        os.chdir(root_folder)
        folder = str(username)
        os.mkdir(folder)
        print('Folder created successfully')
    except:
        print('Folder already created successfully')
        pass



    #starting login
    # options = Options()
    # options.headless = True
    # options.add_argument('--headless')
    # options.add_argument('window-size=1920x1080')
    # driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')
    driver = webdriver.Chrome('chromedriver')
    print("Headless Chrome Initialized")

    fn_login.access('feliperosa_oficial','16107166', driver)

    root_folder = 'assets_fn_03'

    fn_followers_link(username, driver,root_folder)