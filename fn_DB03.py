import time
import pandas as pd
from bs4 import BeautifulSoup as bs

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import glob
import os
from pathlib import Path


'''Report DB03: Dataframe with followers and theirs bios'''


class DB03:
    def __init__(self, username, driver, cookies):
        self.username = username
        self.driver = driver
        self.cookies = cookies

    def create_report(self):
        print('Creating folder')
        root_folder = Path(__file__).parents[0]
        os.chdir(root_folder)
        folder = str(self.username)
        if not os.path.exists(folder):
            os.mkdir(folder)
            print('Folder created successfully')

        try:
            pd.read_csv(str(self.username) + '/report_03_list_' + str(self.username) + '.csv')
        except:
            report_03 = {
                'index': [],
                'followers_links': [],
                'followers_names': []
            }
            report_03 = pd.DataFrame(data=report_03)
            report_03.to_csv(str(self.username) + '/report_03_list_' + str(self.username) + '.csv', index=False)

    def followers_link(self):
        username = self.username
        driver = self.driver
        cookies = self.cookies

        driver.get('https://www.instagram.com/accounts/onetap/?next=%2F')
        for cookie in cookies:
            driver.add_cookie(cookie)

        print("Accessing instagram page to be searched")  # accessing page to be searched
        driver.get('https://www.instagram.com/' + username)
        wait = WebDriverWait(driver, 10)
        try:
            wait.until(EC.presence_of_element_located(((By.PARTIAL_LINK_TEXT, 'follower'))))
        except:
            wait.until(EC.presence_of_element_located(((By.PARTIAL_LINK_TEXT, 'seguidor'))))

        print("Accessing followers page")
        try:
            driver.find_element_by_partial_link_text("follower").click()
        except:
            driver.find_element_by_partial_link_text("seguidor").click()
        print("Followers page accessed successfully")

        try:  # waiting page to be loaded
            wait.until(
                EC.presence_of_element_located(((By.XPATH, "//*[@id='react-root']/section/main/div/ul/li[2]/a/span"))))
        except:
            wait.until(EC.presence_of_element_located(
                ((By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span'))))

        try:  # getting total amount of followers
            total_followers = driver.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/ul/li[2]/a/span").text
            total_followers = total_followers.replace('.', '')
            total_followers = total_followers.replace(',', '')
        except:
            total_followers = driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text
            total_followers = total_followers.replace('.', '')
            total_followers = total_followers.replace(',', '')

        if total_followers.find('k') == True:
            total_followers = total_followers.replace('k', '')
            total_followers = int(float(total_followers)) * 100
            print("Total number of followers approximately: ", total_followers)
        else:
            total_followers = int(float(total_followers))
            print("Total number of followers: ", total_followers)

        print("---------------------------")
        print("Amount of followers: ", total_followers)

        fbody = driver.find_element_by_xpath("//div[@class='isgrP']")  # Getting screen info to scroll down
        scroll = 1
        followers_loaded = 0
        items = []
        items_names = []
        index = 0
        index_now = 0
        lista = []
        while index_now < int(float(total_followers)):  # while the amount of followers scrapped is lesser than the total of followers.
            time.sleep(1)
            followers_on_screen = driver.find_elements_by_xpath('//a[contains(@class, "FPmhX notranslate  _0imsa ")]')
            for follower_on_screen in followers_on_screen:
                items.append(follower_on_screen.get_attribute('href'))  # getting followers_link
                index += 1

            lista = items  # removing duplicates links found from list
            lista = pd.Series(lista).drop_duplicates()
            index_now = len(lista)
            print("Total amount of followers now: ", index_now)

            if index_now < int(total_followers):  # if the amount of scrapped followers is lesser than the total of followers.
                index_now = 0  # resetting the amount of scrapped followers
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                      fbody)  # does scroll down action
                time.sleep(1)
                fList = driver.find_elements_by_xpath("//div[@class='isgrP']//li")  # Amount of followers found
                scroll += 1

        print("---- Process Concluded ----")
        print("---------------------------")
        print("----- Showing results -----")
        print("Amount of followers found: ", len(fList))
        print("Amount of ScrollDown done: ", scroll)
        print("---------------------------")
        print("----- Processing data -----")

        # scrape followers links and names from data using BS and CSV (without Selenium and Pandas)
        print("Scraping followers links and names from data")
        source = driver.page_source
        data = bs(source, 'html.parser')
        index_now = 0
        index = []
        followers_links = []
        followers_names = []
        for followers in data.find_all('a', class_='FPmhX notranslate _0imsa'):
            index.append(index_now + 1)
            followers_links.append(followers['href'])  # extraction of followers_links
            followers_names.append(followers.text)  # extraction of followers_names

        report_03_list = {
                'index': index,
                'followers_links': followers_links,
                'followers_names': followers_names
            }
        report_03_list = pd.DataFrame(data=report_03_list)
        report_03_list = report_03_list.drop_duplicates()
        report_03_list = report_03_list.drop_duplicates()
        report_03_list.to_csv(str(username) + '/report_03_list_' + str(username) + '.csv', index=False)

        print("---------------------------")
        print("Report:")
        print("Amount of followers: ", int(total_followers))
        print("Amount of followers loaded: ", index_now)
        print("---------------------------")

    def followers_link_list(self):
        followers_link_list = pd.read_csv(str(self.username) + '/report_03_list_' + str(self.username) + '.csv')
        followers_link_list = followers_link_list['followers_links'].tolist()
        return followers_link_list

    def followers_bios(self, followers_links_list):
        username = self.username
        driver = self.driver
        
        followers_link_completed = []
        followers_name_completed = []
        followers_bio_completed = []
        followers_amount_of_posts_completed = []
        followers_amount_of_followers_completed = []
        followers_amount_of_following_completed = []
        followers_private_completed = []

        report_03_bio = {
            'followers_links': followers_link_completed,
            'followers_names': followers_name_completed,
            'amount_of_posts': followers_amount_of_posts_completed,
            'amount_of_followers': followers_amount_of_followers_completed,
            'amount_of_following': followers_amount_of_following_completed,
            'private': followers_private_completed,
            'bio': followers_bio_completed
        }

        report_03_bio = pd.DataFrame(data=report_03_bio)
        report_03_bio = report_03_bio.drop_duplicates()

        try:
            report_03_created = pd.read_csv(str(username) + '/report_03_bio_' + str(username) + '.csv')
            report_03_bio = report_03_created.append([report_03_bio], ignore_index=True)
            report_03_bio = report_03_bio.drop_duplicates()
            report_03_bio.to_csv(str(username) + '/report_03_bio_' + str(username) + '.csv', index=False)
        except:
            report_03_bio.to_csv(str(username) + '/report_03_bio_' + str(username) + '.csv', index=False)

        try:
            for insta_followers_links in followers_links_list:  # accessing page to be searched
                try:
                    insta_followers_links = str(insta_followers_links)

                    print("Accessing instagram page to be searched")
                    driver.get('https://www.instagram.com' + insta_followers_links)
                    time.sleep(3)

                    print("Starting scrapping")
                    source = driver.page_source
                    data = bs(source, 'html.parser')

                    # followers_link
                    followers_link_completed.append(insta_followers_links)

                    # followers_name
                    try:
                        name = data.find(class_='-vDIg').h1.text
                        followers_name_completed.append(name)
                    except:
                        name = str("n/a")
                        followers_name_completed.append(name)
                    print('name:', name)

                    # bio
                    try:
                        bio = data.find(class_='-vDIg').span.text
                        if bio.find("Followed by") == 0:
                            bio = str("n/a")
                            followers_bio_completed.append(bio)
                        else:
                            bio = data.find(class_='-vDIg').text
                            followers_bio_completed.append(bio)
                    except:
                        bio = str("n/a")
                        followers_bio_completed.append(bio)

                    # amount_of_posts
                    amount_of_posts = data.findAll(class_='g47SY')[0].text
                    try:
                        if (amount_of_posts.find('.') or amount_of_posts.find(',')):
                            amount_of_posts = amount_of_posts.replace(',', '')
                            amount_of_posts = amount_of_posts.replace('.', '')
                            amount_of_posts = int(amount_of_posts)
                        else:
                            amount_of_posts = int(amount_of_posts)
                    except:
                        amount_of_posts = amount_of_posts
                    followers_amount_of_posts_completed.append(amount_of_posts)

                    # amount_of_followers
                    amount_of_followers = data.findAll(class_='g47SY')[1].text
                    try:
                        if (amount_of_followers.find('.') or amount_of_followers.find(',')):
                            amount_of_followers = amount_of_followers.replace(',', '')
                            amount_of_followers = amount_of_followers.replace('.', '')
                            amount_of_followers = int(amount_of_followers)
                        else:
                            amount_of_followers = int(amount_of_followers)
                    except:
                        amount_of_followers = amount_of_followers
                    followers_amount_of_followers_completed.append(amount_of_followers)

                    # amount_of_following
                    amount_of_following = data.findAll(class_='g47SY')[2].text
                    if amount_of_following.find('.') or amount_of_following.find(','):
                        amount_of_following = amount_of_following.replace('.', '')
                        amount_of_following = amount_of_following.replace(',', '')
                        amount_of_following = int(amount_of_following)
                    else:
                        amount_of_following = int(amount_of_following)
                    followers_amount_of_following_completed.append(amount_of_following)

                    # is_private
                    try:
                        is_private = data.find(class_='rkEop').text == 'This Account is Private'
                        followers_private_completed.append("1")  # This Account is Private
                    except:
                        followers_private_completed.append("0")

                    report_03_bio = {
                        'followers_links': followers_link_completed,
                        'followers_names': followers_name_completed,
                        'amount_of_posts': followers_amount_of_posts_completed,
                        'amount_of_followers': followers_amount_of_followers_completed,
                        'amount_of_following': followers_amount_of_following_completed,
                        'private': followers_private_completed,
                        'bio': followers_bio_completed
                    }

                    report_03_bio = pd.DataFrame(data=report_03_bio)
                    report_03_bio = report_03_bio.drop_duplicates()
                    try:
                        report_03_created = pd.read_csv(str(username) + '/report_03_bio_' + str(username) + '.csv')
                        report_03_bio = report_03_created.append([report_03_bio], ignore_index=True)
                        report_03_bio = report_03_bio.drop_duplicates()
                        report_03_bio.to_csv(str(username) + '/report_03_bio_' + str(username) + '.csv', index=False)
                    except:
                        report_03_bio.to_csv(str(username) + '/report_03_bio_' + str(username) + '.csv', index=False)

                    # deleting source of data if the post_link was processed
                    report_03_link_list = pd.read_csv(str(username) + '/report_03_bio_' + str(username) + '.csv')
                    report_03_link_list = report_03_link_list['followers_links'].tolist()

                    item_processed = insta_followers_links
                    try:
                        if report_03_link_list.index(item_processed) >= 0:
                            doc_source = pd.read_csv(str(username) + '/report_03_list_' + str(username) + '.csv')  # deleting source of data
                            doc_source.drop(doc_source.index[doc_source['followers_links'] == str(insta_followers_links)], inplace=True)
                            doc_source.to_csv(str(username) + '/report_03_list_' + str(username) + '.csv', index=False)
                    except:
                        pass
                except:
                    pass
        except:
            pass

    @staticmethod
    def delete_file_by_key_name(username, key_word_for_file):
        current_dir = os.path.dirname(os.path.realpath(__file__))  # accessing report_01_IMG (to delete processed rows)
        path = current_dir + '\\' + username + "\\" + '*' + key_word_for_file + '*'
        for file_to_delete in glob.glob(path):
            os.remove(file_to_delete)

        report_03_bio = pd.read_csv(str(username) + '/report_03_bio_' + str(username) + '.csv')
        report_03_bio.to_csv(str(username) + '/report_03_' + str(username) + '.csv', index=False)  # save report_03_bio as report_03
        os.remove(str(username) + '/report_03_bio_' + str(username) + '.csv')  # delete report_03_bio

    def run(self):
        print('Starting to create report 03')
        username = self.username
        driver = self.driver
        cookies = self.cookies

        start = DB03(username, driver, cookies)
        start.create_report()
        start.followers_link()
        followers_link_list = start.followers_link_list()
        start.followers_bios(followers_link_list)

        # deleting report 01 without after whole process:
        followers_link_list = start.followers_link_list()  # create: a dataframe db02img; returns a list of img_links
        if len(followers_link_list) == 0:
            key_word_for_file = 'report_03_list'
            start.delete_file_by_key_name(username, key_word_for_file)

        print('Process "Report 03" concluded.')

