import pandas as pd
import time
from pathlib import Path
import os
from bs4 import BeautifulSoup as bs
from datetime import datetime
from math import ceil
import threading


'''Report DB01: Dataframe with posts links and their types (img or vid)'''


class DB01:
    def __init__(self, username, driver, cookies, root_folder):
        self.username = username
        self.driver = driver
        self.cookies = cookies
        self.root_folder = root_folder

    def creating_folder(self):
        print('Creating folder')
        root_folder = Path(__file__).parents[0]
        os.chdir(root_folder)
        folder = str(self.username)
        if not os.path.exists(folder):
            os.mkdir(folder)
            print('Folder created successfully')

    def get_posts_links(self):  # getting posts links
        username = self.username
        driver = self.driver
        root_folder = self.root_folder

        # Accessing instagram page to be searched
        print("Accessing instagram page to be searched")
        time.sleep(10)
        driver.get('https://www.instagram.com/' + username)
        time.sleep(10)

        try:
            total_of_posts = driver.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/ul/li[1]/span/span").text
        except:
            total_of_posts = driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text

        total_of_posts = int(total_of_posts.replace(',', ''))
        numbers_of_scroll = round(((((total_of_posts) - 24) / 12) * 2) + 2 + 1)
        print("---------------------------")
        print("Amount of posts: ", total_of_posts)

        # Starting ScrollDown
        print("Starting scrolldown")
        scroll = 0
        index = 0
        index_now = 0
        items = []
        lista = []
        while index_now < total_of_posts:
            time.sleep(1)
            source = driver.page_source
            data = bs(source, 'html.parser')

            for posts in data.find_all("div", class_="v1Nh3 kIKUG _bz0w"):
                posts_link = posts.a['href']
                items.append(posts_link)
                index += 1
            lista = items

            # removerduplicadosdalista
            lista = pd.Series(lista).drop_duplicates()
            index_now = len(lista)

            # Deciding if the scrolldown continues or stops
            if index_now < total_of_posts:
                index_now = 0
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                scroll += 1
        print('Scrolldown concluded')

        # Inserting data into report
        print('Getting posts links')
        source = driver.page_source
        data = bs(source, 'html.parser')

        # creating index
        indice_interno_completo = []
        for x in range(1, len(lista) + 1):
            indice_interno_completo.append(x)

        relatorio_BD01 = {
            'indice_interno': indice_interno_completo,
            'post_link': lista}

        root_folder = str(root_folder)
        path = root_folder + '/' + str(username)
        relatorio_BD01 = pd.DataFrame(data=relatorio_BD01)
        relatorio_BD01.to_csv(str(username) + '/report_01_' + str(username) + '.csv', index=False)

        print("---------------------------")
        print("Report:")
        print("Amount of posts posted: ", total_of_posts)
        print("Amount of posts loaded: ", index_now)
        print("---------------------------")

    def get_posts_vid_or_img_links(self, post_link_list):
        username = self.username
        driver = self.driver
        root_folder = self.root_folder
        cookies = self.cookies

        followers_link_completo = []
        indice_interno_completo = []
        post_link_completo = []
        post_date_completo = []
        amount_of_likes_completo = []
        followers_names_completo = []
        post_link_type_completo = []
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        driver.get('https://www.instagram.com/accounts/onetap/?next=%2F')
        for cookie in cookies:
            driver.add_cookie(cookie)

        relatorio_db01_vid_or_img = {
            'indice_interno': indice_interno_completo,
            'post_link': post_link_completo,
            'post_link_type': post_link_type_completo
        }

        relatorio_db01_vid_or_img = pd.DataFrame(data=relatorio_db01_vid_or_img)

        try:
            relatorio_db01_vid_or_img_final = pd.read_csv(
                str(username) + '/report_01_vid_or_img_' + str(username) + '.csv')
            relatorio_db01_vid_or_img_final = relatorio_db01_vid_or_img_final.append([relatorio_db01_vid_or_img],
                                                                                     ignore_index=True)
            relatorio_db01_vid_or_img_final.to_csv(
                str(username) + '/report_01_vid_or_img_' + str(username) + '.csv',
                index=False)

        except:
            relatorio_db01_vid_or_img.to_csv(str(username) + '/report_01_vid_or_img_' + str(username) + '.csv',
                                             index=False)

        for post_link in post_link_list:
            post_link = str(post_link)
            driver.get('https://www.instagram.com' + str(post_link))  # Accessing page to search
            post_info = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]').text
            matches = ["views", "visualizações"]

            if any(x in post_info for x in matches):  # Identifying if the post is video or img
                post_link_completo.append(post_link)
                post_link_type_completo.append('vid')
            else:
                post_link_completo.append(post_link)
                post_link_type_completo.append('img')

        indice_interno_completo = []  # creating index
        for y in range(1, len(post_link_type_completo) + 1):
            indice_interno_completo.append(y)

        relatorio_db01_vid_or_img = {
            'indice_interno': indice_interno_completo,
            'post_link': post_link_completo,
            'post_link_type': post_link_type_completo
        }

        root_folder = str(root_folder)
        path = root_folder + '/' + username
        relatorio_db01_vid_or_img = pd.DataFrame(data=relatorio_db01_vid_or_img)

        relatorio_db01_vid_or_img_final = pd.read_csv(
            str(username) + '/report_01_vid_or_img_' + str(username) + '.csv')
        relatorio_db01_vid_or_img_final = relatorio_db01_vid_or_img_final.append([relatorio_db01_vid_or_img],
                                                                                 ignore_index=True)
        relatorio_db01_vid_or_img_final = relatorio_db01_vid_or_img_final.drop_duplicates()
        relatorio_db01_vid_or_img_final.to_csv(str(username) + '/report_01_vid_or_img_' + str(username) + '.csv',
                                               index=False)

    def data_to_multiprocess(self):
        insta_posts_links_vid_or_img = pd.read_csv(str(self.username) + '/report_01_' + str(self.username) + '.csv')
        insta_posts_links_vid_or_img = insta_posts_links_vid_or_img['post_link'].tolist()
        post_link_list = insta_posts_links_vid_or_img
        return post_link_list

    def slicing_lists_to_groups(self, post_link_list):
        # defining amount of groups to slice
        total = len(post_link_list)
        amount_of_groups = (ceil(total / 10))

        if total % 10 == 0:
            chunk_size = total / amount_of_groups
        else:
            chunk_size = 45  # maximo de itens num grupo
        # print('Chunk size: ', chunk_size)
        return chunk_size

    def creating_chunks(self, post_link_list, chunk_size):
        # creating chunks of data
        x = range(0, len(post_link_list), chunk_size)
        groups_of_data = [post_link_list[i:i + chunk_size] for i in x]
        # print('slice: ', groups_of_data)
        # print('amount_of_groups: ', len(groups_of_data))
        groups = len(groups_of_data)
        return groups, groups_of_data

    def starting_threading(self, start, groups_of_data):
        for each_group_of_data in groups_of_data:
            start_threading = threading.Thread(target=start.get_posts_vid_or_img_links(each_group_of_data))
            start_threading.start()

    def spliting_report_01_img_or_vid(self):
        # separar BD01_vid_or_img_em dois arquivos (img e vid)
        insta_posts_links_vid_or_img_csv = pd.read_csv(
            str(self.username) + '/report_01_vid_or_img_' + str(self.username) + '.csv')
        insta_posts_links_vid_or_img_csv = pd.DataFrame(data=insta_posts_links_vid_or_img_csv)

        # gerando arquivo de img
        insta_posts_links_img_csv = insta_posts_links_vid_or_img_csv.loc[
            insta_posts_links_vid_or_img_csv['post_link_type'] == 'img']
        insta_posts_links_img_csv.to_csv(str(self.username) + '/report_01_img_' + str(self.username) + '.csv',
                                         index=False)

        # gerando arquivo de vid
        insta_posts_links_vid_csv = insta_posts_links_vid_or_img_csv.loc[
            insta_posts_links_vid_or_img_csv['post_link_type'] == 'vid']
        insta_posts_links_vid_csv.to_csv(str(self.username) + '/report_01_vid_' + str(self.username) + '.csv',
                                         index=False)
        return insta_posts_links_img_csv, insta_posts_links_vid_csv

    def run(self):
        username = self.username
        driver = self.driver
        root_folder = self.root_folder
        cookies = self.cookies

        start = DB01(username, driver, cookies, root_folder)
        start.creating_folder()  # creates folder to reports
        start.get_posts_links()  # generate report_DB01 with links
        post_link_list = start.data_to_multiprocess()  # access data to multiprocess

        chunk_size = start.slicing_lists_to_groups(post_link_list)  # defining amount of groups to slice
        groups = start.creating_chunks(post_link_list, chunk_size)[0]  # creating chunks of data
        groups_of_data = start.creating_chunks(post_link_list, chunk_size)[1]  # creating chunks of data

        print('Starting threading')
        print('groups: ', groups)
        time_starting = datetime.now()
        start.starting_threading(start, groups_of_data)  # running threading
        time_finishing = datetime.now()
        time_running = time_finishing - time_starting
        print(groups, time_running)
        print('\n----------------------------------')

        start.spliting_report_01_img_or_vid()
