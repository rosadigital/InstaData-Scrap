import pandas as pd
import time
import os
from datetime import datetime
from math import ceil
import threading
import glob

'''Report DB02: Dataframe with posts links and their details'''

class DB02:
    def __init__(self, username, driver, cookies):
        self.username = username
        self.driver = driver
        self.cookies = cookies

    def post_likes_links_img(self, post_link_list, group_number):
        username = self.username
        cookies = self.cookies
        driver = self.driver

        indice_interno_completo = []
        likers_link_completo = []
        likers_names_completo = []
        post_link_completo = []
        post_date_completo = []
        amount_of_likes_completo = []

        current_dir = os.path.dirname(os.path.realpath(__file__))  # accessing report_01_IMG (to delete processed rows)
        path = current_dir + '/' + username
        file_name = '/report_01_img_' + str(username)

        print('Amount of posts by group: ', len(post_link_list))  # print amount of links to be searched
        print('----------------------------------')
        posicao_do_post = 1

        driver.get('https://www.instagram.com/accounts/onetap/?next=%2F')
        for cookie in cookies:
            driver.add_cookie(cookie)

        for post_link in post_link_list:
            indice_interno_completo = []
            likers_link_completo = []
            likers_names_completo = []
            post_link_completo = []
            post_date_completo = []
            amount_of_likes_completo = []
            try:
                post_link = str(post_link)
                try:
                    driver.get('https://www.instagram.com' + str(post_link))  # try for post link without slash
                except:
                    driver.get('https://www.instagram.com/' + str(post_link))  # try again if post link already had slash
                print("Post page accessed successfully: ", post_link)  # print post link

                time.sleep(5)
                try:  # searching for number of liker
                    number_of_likes = driver.find_element_by_xpath('//div[contains(@class, "Nm9Fw")]/a/span').text
                except:
                    number_of_likes = driver.find_element_by_xpath(
                        '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]/a/span').text

                try:
                    if number_of_likes.find(','):  # remove comma from number of followers
                        number_of_likes = int(number_of_likes.replace(',', ''))
                        number_of_likes = number_of_likes
                    elif number_of_likes.find('.'):  # remove dot from number of followers
                        number_of_likes = int(number_of_likes.replace('.', ''))
                        number_of_likes = number_of_likes
                except:
                    number_of_likes = int(number_of_likes)
                number_of_likes = number_of_likes + 1  # Note: need to add up one because the amount of links shows total less one
                print("Total amount of likes on this post: ", number_of_likes)

                # getting post date
                post_date = driver.find_element_by_xpath('//time[contains(@class, "_1o9PC Nzb55")]').get_attribute('title')
                print('Post date: ', post_date)

                # print("Accessing likes page")  # accessing likes page
                try:
                    button = driver.find_element_by_class_name('zV_Nj')
                except:
                    try:
                        button = driver.find_element_by_class_name('Igw0E._56XdI.eGOV_._4EzTm.ItkAi')
                    except:
                        button = driver.find_element_by_class_name('KcRNL mOBkM    ')
                button.click()

                time.sleep(1)

                try:  # Getting screen info to scroll down
                    fbody = driver.find_element_by_xpath(
                        '//*[@class="                     Igw0E     IwRSH      eGOV_        vwCYk                                                                            i0EQd                                   "]/div')
                except:
                    try:
                        fbody = driver.find_element_by_xpath('//*[contains(@class, "_1XyCr")]/div[2]/div')
                    except:
                        print("error finding xpath to scroll down: ", group_number)
                        break

                scroll = 1
                followers_loaded = 0
                items = []
                items_names = []
                index = 0
                index_now = 0
                lista = []
                lista_to_scroll = []  # list created to save amount of links scrapped (without duplicates) and consider on scroll down action
                lista_name = []
                index_interno = []
                lista_de_links = []
                likers_names = []
                scroll_limit = (((number_of_likes - 6) / 5) + 2) * 2  # limit for scroll down action
                f = 1
                a = 1
                liker_name_number_for_error = 0
                print('Expected limit for scroll down action: ', str(group_number), str(post_link), scroll_limit)

                while index_now < number_of_likes:  # while scrapped likes are lesser than total amount of likes expected
                    like_class = driver.find_elements_by_xpath("//*[@class='FPmhX notranslate MBL3Z']")
                    like_class = len(like_class)

                    # getting liker profile link
                    likes = driver.find_elements_by_xpath("//*[@class='FPmhX notranslate MBL3Z']")
                    liker_link_number_for_error = 0
                    for like in likes:
                        try:
                            liker_link = like.get_attribute('href')
                        except:
                            liker_link = "n/a_" + str(liker_link_number_for_error)
                            liker_link_number_for_error += 1
                        items.append(liker_link)
                        index += 1

                    # getting liker names
                    liker_name_number_for_error = 0
                    for likers_name_position in range(1, like_class + 1):
                        try:
                            likers_name = driver.find_element_by_xpath("//*[@class='_1XyCr']//div/div/div[" + str(likers_name_position) + "]/div[2]/div[2]/div")
                            likers_name = likers_name.text
                            '/html/body/div[6]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div'
                        except:
                            likers_name = "n/a_" + str(liker_name_number_for_error)
                            liker_name_number_for_error += 1
                        items_names.append(likers_name)

                    # dropping duplicated links
                    lista = items
                    items_index_now = pd.Series(data=lista).drop_duplicates()
                    index_now = len(items_index_now)

                    # scrolling down
                    driver.execute_script(
                        'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                        fbody)
                    scroll += 1
                    print("Scrolling down: ", scroll, 'Current amount of likes already gotten: ', str(group_number),
                          str(posicao_do_post), str(post_link), index_now)

                    # setting limit to scroll down action
                    if scroll > scroll_limit:
                        print("The limit of scroll down was reached. Stopping scroll down. Total of scrolls: ", scroll)
                        break

                time.sleep(2)

                print("Starting save scrapped data")
                for m in lista:  # likers links
                    likers_link_completo.append(m)
                likers_link_completo = list(dict.fromkeys(likers_link_completo))

                for n in items_names:  # likers names
                    likers_names_completo.append(n)
                likers_names_completo = list(dict.fromkeys(likers_names_completo))

                post_link_completo = []
                post_date_completo = []
                amount_of_likes_completo = []

                counter = len(likers_link_completo) + 1
                for o in range(1, counter):
                    post_link_completo.append(post_link)  # post link
                    post_date_completo.append(post_date)  # post date
                    amount_of_likes_completo.append(len(likers_link_completo))  # amount of likes on this post

                print('Amount of post_link:       ', str(group_number), str(post_link), len(post_link_completo))
                print('Amount of post_date:       ', str(group_number), str(post_link), len(post_date_completo))
                print('Amount of amount_of_likes: ', str(group_number), str(post_link), len(amount_of_likes_completo))
                print('Amount of likers_links:    ', str(group_number), str(post_link), len(likers_link_completo))
                print('Amount of Amount of likers_names:    ', str(group_number), str(post_link), len(likers_names_completo))

                # saving data in the dataframe
                report_02 = {
                    'post_type': 'img',
                    'post_link': post_link_completo,
                    'post_date': post_date_completo,
                    'amount_of_likes': amount_of_likes_completo,
                    'likers_links': likers_link_completo,
                    'likers_names': likers_names_completo
                }
                report_02 = pd.DataFrame(data=report_02)
                report_02 = report_02.drop_duplicates()
                report_02_created = pd.read_csv(str(username) + '/report_02_img_' + str(username) + '_v_' + str(group_number) + '.csv')
                report_02 = report_02_created.append([report_02], ignore_index=True)
                report_02 = report_02.drop_duplicates()
                report_02.to_csv(str(username) + '/report_02_img_' + str(username) + '_v_' + str(group_number) + '.csv', index=False)  # Attention: if this directory does not exist, it has to be created before process this function. Otherwise, this function will continuously overwrite all scrapped data

                # deleting source of data if the post_link was processed
                report_02_post_link = pd.read_csv(str(username) + '/report_02_img_' + str(username) + '_v_' + str(group_number) + '.csv')
                report_02_post_link = report_02_post_link['post_link'].tolist()
                item_processed = post_link
                try:
                    if report_02_post_link.index(item_processed) >= 0:
                        doc_source = pd.read_csv(str(username) + str(file_name) + '.csv')  # deleting source of data
                        doc_source.drop(doc_source.index[doc_source['post_link'] == str(post_link)], inplace=True)
                        doc_source.to_csv(str(username) + str(file_name) + '.csv', index=False)
                except:
                    pass
                time.sleep(1)
            # If some fatal error occurs, and its not possible to get the data,
            # the function will keep the link on the report 01,
            # and try to scrap the next link
            except:
                pass
        posicao_do_post += 1

    def post_likes_links_vid(self, post_link_list, group_number):
        username = self.username
        cookies = self.cookies
        driver = self.driver

        indice_interno_completo = []
        likers_link_completo = []
        likers_names_completo = []
        post_link_completo = []
        post_date_completo = []
        amount_of_likes_completo = []

        current_dir = os.path.dirname(os.path.realpath(__file__))  # accessing report_01_vid (to delete processed rows)
        path = current_dir + '/' + username
        file_name = '/report_01_vid_' + str(username)

        print('Amount of posts by group: ', len(post_link_list))  # print amount of links to be searched
        posicao_do_post = 1

        driver.get('https://www.instagram.com/accounts/onetap/?next=%2F')
        for cookie in cookies:
            driver.add_cookie(cookie)

        for post_link in post_link_list:
            indice_interno_completo = []
            likers_link_completo = []
            likers_names_completo = []
            post_link_completo = []
            post_date_completo = []
            amount_of_likes_completo = []
            try:
                post_link = str(post_link)
                print('----------------------------------')
                try:
                    driver.get('https://www.instagram.com/' + str(post_link))  # try for post link without slash
                except:
                    driver.get('https://www.instagram.com' + str(post_link))  # try again if post link already had slash
                print("Post page accessed successfully: ", post_link)  # print post link

                time.sleep(5)

                post_date = driver.find_element_by_xpath('//time[contains(@class, "_1o9PC Nzb55")]').get_attribute('title')
                print('Post date: ', post_date)

                likers_link_completo.append("n/a")

                post_link_completo.append(post_link)

                post_date_completo.append(post_date)

                likers_names_completo.append("n/a")

                # video_likes_button = driver.find_element_by_xpath('//span[contains(@class, "vcOH2")]/span').text
                video_likes_button = driver.find_element_by_xpath('//span[contains(@class, "vcOH2")]')
                video_likes_button.click()
                time.sleep(1)
                amount_of_likes_video = driver.find_element_by_xpath('//div[contains(@class, "vJRqr")]/span').text
                amount_of_likes_completo.append(amount_of_likes_video)
                time.sleep(2)

                print("Starting save scrapped data")

                print('Amount of post_link:       ', str(group_number), str(post_link), len(post_link_completo))
                print('Amount of post_date:       ', str(group_number), str(post_link), len(post_date_completo))
                print('Amount of amount_of_likes: ', str(group_number), str(post_link), len(amount_of_likes_completo))
                print('Amount of likers_links:    ', str(group_number), str(post_link), len(likers_link_completo))
                print('Amount of Amount of likers_names:    ', str(group_number), str(post_link),
                      len(likers_names_completo))

                report_02 = {
                    'post_type': 'vid',
                    'post_link': post_link_completo,
                    'post_date': post_date_completo,
                    'amount_of_likes': amount_of_likes_completo,
                    'likers_links': likers_link_completo,
                    'likers_names': likers_names_completo
                }

                # saving data in the dataframe
                report_02 = pd.DataFrame(data=report_02)
                report_02 = report_02.drop_duplicates()
                report_02_created = pd.read_csv(str(username) + '/report_02_vid_' + str(username) + '_v_' + str(group_number) + '.csv')
                report_02 = report_02_created.append([report_02], ignore_index=True)
                report_02 = report_02.drop_duplicates()
                report_02.to_csv(str(username) + '/report_02_vid_' + str(username) + '_v_' + str(group_number) + '.csv',
                                 index=False)

                # deleting source of data if the post_link was processed
                report_02_post_link = pd.read_csv(str(username) + '/report_02_vid_' + str(username) + '_v_' + str(group_number) + '.csv')
                report_02_post_link = report_02_post_link['post_link'].tolist()
                item_processed = post_link
                try:
                    if report_02_post_link.index(item_processed) >= 0:
                        doc_source = pd.read_csv(str(username) + str(file_name) + '.csv')
                        doc_source.drop(doc_source.index[doc_source['post_link'] == str(post_link)], inplace=True)
                        doc_source.to_csv(str(username) + str(file_name) + '.csv', index=False)
                except:
                    pass
                time.sleep(1)
            # If some fatal error occurs, and its not possible to get the data,
            # the function will keep the link on the report 01,
            # and try to scrap the next link
            except:
                pass
        posicao_do_post += 1

    def img_link_list(self):
        insta_posts_links_img = pd.read_csv(str(self.username) + '/report_01_img_' + str(self.username) + '.csv')
        insta_posts_links_img = insta_posts_links_img['post_link'].tolist()
        return insta_posts_links_img

    def vid_link_list(self):
        insta_posts_links_vid = pd.read_csv(str(self.username) + '/report_01_vid_' + str(self.username) + '.csv')
        insta_posts_links_vid = insta_posts_links_vid['post_link'].tolist()
        return insta_posts_links_vid

    @staticmethod
    def slicing_lists_to_groups(post_link_list):
        # defining amount of groups to slice
        total = len(post_link_list)
        amount_of_groups = (ceil(total / 10))

        if total % 10 == 0:
            chunk_size = total / amount_of_groups
        else:
            chunk_size = 45  # maximo de itens num grupo
        # print('Chunk size: ', chunk_size)
        return chunk_size

    @staticmethod
    def creating_chunks(post_link_list, chunk_size):
        # creating chunks of data
        chunk_size = int(chunk_size)
        x = range(0, len(post_link_list), chunk_size)
        groups_of_data = [post_link_list[i:i + chunk_size] for i in x]
        # print('slice: ', groups_of_data)
        # print('amount_of_groups: ', len(groups_of_data))
        groups = len(groups_of_data)
        return groups, groups_of_data

    def starting_threading(self, start, groups_of_data, type):
        group_number = 1
        indice_interno_completo = []
        likers_link_completo = []
        likers_names_completo = []
        post_link_completo = []
        post_date_completo = []
        amount_of_likes_completo = []

        if type == "img":
            for each_group_of_data in groups_of_data:
                try:
                    pd.read_csv(
                        str(self.username) + '/report_02_img_' + str(self.username) + '_v_' + str(group_number) + '.csv')
                except:
                    report_02 = {
                        'post_type': 'img',
                        'post_link': post_link_completo,
                        'post_date': post_date_completo,
                        'amount_of_likes': amount_of_likes_completo,
                        'likers_links': likers_link_completo,
                        'likers_names': likers_names_completo
                    }
                    report_02 = pd.DataFrame(data=report_02)
                    report_02.to_csv(
                        str(self.username) + '/report_02_img_' + str(self.username) + '_v_' + str(group_number) + '.csv',
                        index=False)

                start_threading = threading.Thread(target=start.post_likes_links_img(each_group_of_data, group_number))
                start_threading.start()
                group_number += 1

        if type == 'vid':
            for each_group_of_data in groups_of_data:
                try:
                    pd.read_csv(
                        str(self.username) + '/report_02_vid_' + str(self.username) + '_v_' + str(
                            group_number) + '.csv')
                except:
                    report_02 = {
                        'post_type': 'vid',
                        'post_link': post_link_completo,
                        'post_date': post_date_completo,
                        'amount_of_likes': amount_of_likes_completo,
                        'likers_links': likers_link_completo,
                        'likers_names': likers_names_completo
                    }
                    report_02 = pd.DataFrame(data=report_02)
                    report_02.to_csv(
                        str(self.username) + '/report_02_vid_' + str(self.username) + '_v_' + str(
                            group_number) + '.csv',
                        index=False)

                start_threading = threading.Thread(target=start.post_likes_links_vid(each_group_of_data, group_number))
                start_threading.start()
                group_number += 1

    @staticmethod
    def merging_report_02_img_and_vid(username, key_word_for_report):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        path = current_dir + '\\' + username + "\\" + '*' + key_word_for_report + '*'

        report_db02_img_and_vid = pd.DataFrame()
        for report_02 in glob.glob(path):
            report_02_data = pd.read_csv(report_02)
            report_db02_img_and_vid = report_db02_img_and_vid.append(report_02_data, ignore_index=True)
            os.remove(report_02)

        report_db02_img_and_vid = report_db02_img_and_vid.drop_duplicates()
        report_db02_img_and_vid.to_csv(str(username) + '/report_02_' + str(username) + '.csv',
                                       index=False)  # save report 02 img and vid already merged

    @staticmethod
    def delete_file_by_key_name(username, key_word_for_file):
        current_dir = os.path.dirname(os.path.realpath(__file__))  # accessing report_01_IMG (to delete processed rows)
        path = current_dir + '\\' + username + "\\" + '*' + key_word_for_file + '*'
        for file_to_delete in glob.glob(path):
            os.remove(file_to_delete)

    @staticmethod
    def report_01_from_report_02(username):
        report02 = pd.read_csv(str(username) + '/report_02_' + str(username) + '.csv')
        new_report_01 = report02[['post_link', 'post_date', 'amount_of_likes', 'post_type']].drop_duplicates().reset_index(drop=True)
        new_report_01 = pd.DataFrame(new_report_01)
        new_report_01.to_csv(str(username) + '/report_01_' + str(username) + '.csv')

    def run(self):
        print('Starting to create report 02')
        username = self.username
        driver = self.driver
        cookies = self.cookies

        start = DB02(username, driver, cookies)

        try:  # create: a dataframe db02img; returns a list of img_links
            img_link_list = start.img_link_list()
            # if len(img_link_list) > 0:
            while len(img_link_list) > 0:
                chunk_size = start.slicing_lists_to_groups(
                    img_link_list)  # defines amount of groups to slice; returns chuck size
                groups, groups_of_data = start.creating_chunks(img_link_list,
                                                               chunk_size)  # returns groups, groups_of_data

                print('----------------------------------'
                      '\nStarting threading'
                      '\ngroups: ', groups,
                      '\n----------------------------------')
                time_starting = datetime.now()
                start.starting_threading(start, groups_of_data, 'img')  # running threading to get data for db02img
                time_finishing = datetime.now()
                time_running = time_finishing - time_starting
                print('time_running: ', time_running)
                print('\n----------------------------------')
                img_link_list = start.img_link_list()
        except:
            pass

        try:  # create: a dataframe db02img; returns a list of img_links
            vid_link_list = start.vid_link_list()
            # if len(vid_link_list) > 0:
            while len(vid_link_list) > 0:
                chunk_size = start.slicing_lists_to_groups(
                    vid_link_list)  # defines amount of groups to slice; returns chuck size
                groups, groups_of_data = start.creating_chunks(vid_link_list,
                                                               chunk_size)  # returns groups, groups_of_data

                print('----------------------------------'
                      '\nStarting threading'
                      '\ngroups: ', groups,
                      '\n----------------------------------')
                time_starting = datetime.now()
                start.starting_threading(start, groups_of_data, 'vid')  # running threading to get data for db02img
                time_finishing = datetime.now()
                time_running = time_finishing - time_starting
                print('time_running: ', time_running)
                print('\n----------------------------------')
                vid_link_list = start.vid_link_list()
        except:
            pass

        try:
            # deleting report 01 after the whole process:
            img_link_list = start.img_link_list()  # create: a dataframe db02img; returns a list of img_links
            if len(img_link_list) == 0:
                key_word_for_file = 'report_01_img'
                start.delete_file_by_key_name(username, key_word_for_file)

            vid_link_list = start.vid_link_list()  # create: a dataframe db02img; returns a list of img_links
            if len(vid_link_list) == 0:
                key_word_for_file = 'report_01_vid'
                start.delete_file_by_key_name(username, key_word_for_file)
        except:
            pass

        try:
            key_word_for_report = 'report_02'
            start.merging_report_02_img_and_vid(username, key_word_for_report)  # merge then delete reports 02 merged
        except:
            pass

        start.report_01_from_report_02(username)  # brings to report 01 type, date, amount of likes, from report 02

        print('Process "Report 02" concluded.')

