import pandas as pd
import time
from pathlib import Path
import os
from bs4 import BeautifulSoup as bs
from datetime import datetime
from math import ceil
import threading
from fn_post_likers_links_img import dispatch_jobs


'''Report DB01: Dataframe with posts links and their types (img or vid)'''


class DB02:
    def __init__(self, username, driver, cookies, root_folder):
        self.username = username
        self.driver = driver
        self.cookies = cookies
        self.root_folder = root_folder

    def fn_post_likers_links_img(self, post_link_list, i):
        username = self.username
        cookies = self.cookies
        driver = self.driver

        followers_link_completo = []
        indice_interno_completo = []
        post_link_completo = []
        post_date_completo = []
        amount_of_likes_completo = []
        followers_names_completo = []

        # Configurando webdrivers
        driver.get('https://www.instagram.com/accounts/onetap/?next=%2F')
        for cookie in cookies:
            driver.add_cookie(cookie)

        current_dir = os.path.dirname(os.path.realpath(__file__))  # accessing report_01_IMG (to delete after processing)
        path = current_dir + '/' + username
        file_name = '/report_01_img_' + str(username)

        try:
            report_02_created = pd.read_csv(
                str(username) + '/report_01_img_' + str(username) + 'v_' + str(i) + '.csv')

        except:
            # criando diretorio para salvar dados por processo
            report_02 = {
                'post_type': 'img',
                'post_link': post_link_completo,
                'post_date': post_date_completo,
                'amount_of_likes': amount_of_likes_completo,
                'followers_links': followers_link_completo,
                'followers_names': followers_names_completo
            }

            report_02 = pd.DataFrame(data=report_02)

            report_02.to_csv(str(username) + '/relatorio_DB02_img_' + str(username) + 'v_' + str(i) + '.csv',
                                  index=False)

            report_02_created = pd.read_csv(
                str(username) + '/relatorio_DB02_img_' + str(username) + 'v_' + str(i) + '.csv')

        print('quantidade total de posts por grupo', len(post_link_list))
        posicao_do_post = 1
        for post_link in post_link_list:
            post_link = str(post_link)

            # acessar pagina a ser pesquisada
            print("Accessing post page to be searched")
            time.sleep(5)
            post_link = post_link
            try:
                driver.get('https://www.instagram.com/' + str(post_link))
            except:
                driver.get('https://www.instagram.com' + str(post_link))
            time.sleep(2)
            print("Post page accessed successfully: ", post_link)

            # print("Getting amount of likes on this post")
            time.sleep(2)
            source = driver.page_source
            data = bs(source, 'html.parser')
            # print(data)

            source = driver.page_source
            data = bs(source, 'html.parser')

            try:
                number_of_followers_specific = driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]/button/span').text
            except:
                number_of_followers_specific = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/div[4]/span').text

            # Precisa somar mais 1 porque o numero de likes que aparece sempre falta 01

            try:
                if number_of_followers_specific.find(','):
                    number_of_followers_specific = int(number_of_followers_specific.replace(',', '')) + 1
                elif number_of_followers_specific.find('.'):
                    number_of_followers_specific = int(number_of_followers_specific.replace('.', '')) + 1
            except:
                number_of_followers_specific = int(number_of_followers_specific) + 1

            print("Amount of likes on this post gotten successfully")

            # Getting post date
            print('Getting post date')
            source = driver.page_source
            data = bs(source, 'html.parser')
            post_date = data.find(class_='_1o9PC Nzb55')
            post_date = post_date['title']
            print('Post date: ', post_date)
            print('Post date gotten successfully')

            # acessing likes page
            print("Accessing likes page")
            button = driver.find_element_by_class_name('Igw0E._56XdI.eGOV_._4EzTm.ItkAi')
            button.click()
            print("Likes page accessed successfully")
            time.sleep(1)

            # Starting scrolldown
            print("Starting scrolldown")
            time.sleep(1)
            try:
                fBody = driver.find_element_by_xpath(
                    '//*[@class="                     Igw0E     IwRSH      eGOV_        vwCYk                                                                            i0EQd                                   "]/div')
            except:
                print("erro no fbody do processo: ", i)
                break

            scroll = 1
            followers_loaded = 0
            items = []
            items_names = []
            index = 0
            index_now = 0
            lista = []
            lista_to_scroll = []  # lista criada para armazenar numero de links capturados (sem duplicados) e considerar no scrolldown
            lista_name = []
            index_interno = []
            lista_de_links = []
            followers_names = []
            scroll_limit = (((number_of_followers_specific - 6) / 5) + 2) * 2
            f = 1
            a = 1
            print('scroll_limit', str(i), str(post_link), scroll_limit)

            while index_now < number_of_followers_specific:
                test_class = driver.find_elements_by_xpath("//*[@class='FPmhX notranslate MBL3Z']")
                # print('test_class', len(test_class))
                test_class = len(test_class)

                tests = driver.find_elements_by_xpath("//*[@class='FPmhX notranslate MBL3Z']")
                # print("tests",tests)
                for test in tests:
                    # print('likers', f)
                    test = test.get_attribute('href')
                    # print('test', test)
                    items.append(test)
                    index += 1

                for a in range(a, test_class + 1):
                    try:
                        followers_name_address = "//*[@class='                     Igw0E     IwRSH      eGOV_        vwCYk                                                                            i0EQd                                   ']//div/div/div[" + str(
                            a) + "]/div[2]/div[2]/div"

                        followers_name = driver.find_element_by_xpath(followers_name_address)
                        followers_name = followers_name.text
                        # print(followers_name_address)
                        # print(followers_name)
                        # print(a)
                    except:
                        followers_name = "n/a_" + str(a)
                        # print(followers_name)
                        # print(a)
                    items_names.append(followers_name)
                lista_name = items_names

                lista = items
                items_index_now = pd.Series(data=lista).drop_duplicates()
                index_now = len(items_index_now)
                print('index_now', str(i), str(posicao_do_post), str(post_link), index_now)

                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                      fBody)
                scroll += 1
                f = 1
                a = 1

                if (scroll > scroll_limit):
                    "alerta de scroll list"

            #     print('scroll', str(i), str(post_link), scroll)
            print('number_of_followers_specific', str(i), str(post_link), number_of_followers_specific)
            print('index_now', str(i), str(post_link), index_now)
            print('scroll', str(i), str(post_link), scroll)
            print('scroll_limit', str(i), str(post_link), scroll_limit)
            # if str(i) == 0:
            # print('data', str(i), str(post_link))
            # print(data.find_all(class_='Igw0E IwRSH YBx95 vwCYk'))

            print("Scrolldown concluded successfully")
            time.sleep(2)

            # Scraping data
            print("Starting scraping")
            source = driver.page_source
            data = bs(source, 'html.parser')
            # print(data)

            counter = 1
            for m in lista:
                followers_link_completo.append(m)
                counter += 1

            for n in lista_name:
                followers_names_completo.append(n)

            for o in range(1, counter):
                post_link_completo.append(post_link)

            # creating post_date list:
            for p in range(1, counter):
                post_date_completo.append(post_date)

            for q in range(1, counter):
                amount_of_likes_completo.append(number_of_followers_specific)

            report_02 = {
                'post_type': 'img',
                'post_link': post_link_completo,
                'post_date': post_date_completo,
                'amount_of_likes': amount_of_likes_completo,
                'followers_links': followers_link_completo,
                'followers_names': followers_names_completo
            }

            report_02 = pd.DataFrame(data=report_02)
            report_02 = report_02.drop_duplicates()

            print('post_link: ', str(i), str(post_link), len(post_link_completo))
            print('post_date: ', str(i), str(post_link), len(post_date_completo))
            print('amount_of_likes: ', str(i), str(post_link), len(amount_of_likes_completo))
            print('followers_links: ', str(i), str(post_link), len(followers_link_completo))
            print('followers_names: ', str(i), str(post_link), len(followers_names_completo))

            path = 'assets_fn_02/' + username

            # report_02_created = pd.read_csv(str(username) + '/relatorio_DB02_img_' + str(username) + '.csv')
            report_02 = report_02_created.append([report_02], ignore_index=True)
            report_02 = report_02.drop_duplicates()
            report_02.to_csv(str(username) + '/relatorio_DB02_img_' + str(username) + 'v_' + str(i) + '.csv',
                                  index=False)
            ''''ATENCAO: caso este diretorio nao exista, ele devera ser criado antes de processar esta funcao. criar este diretorio nesta funcao esta sobreponto os arquivos'''

            # verificar se o item pesquisado foi adicionado na lista de items pesquisados, para apagar da lista original. Se nao foi, nao apaga da lista original.
            # deleting source of data if the post_link was processed
            report_02_post_link = pd.read_csv(
                str(username) + '/relatorio_DB02_img_' + str(username) + 'v_' + str(i) + '.csv')
            report_02_post_link = report_02_post_link['post_link'].tolist()
            item_processed = post_link

            try:
                if report_02_post_link.index(item_processed) >= 0:
                    # deleting source of data
                    doc_source = pd.read_csv(str(username) + str(file_name) + '.csv')
                    doc_source.drop(doc_source.index[doc_source['post_link'] == str(post_link)], inplace=True)
                    doc_source.to_csv(str(username) + str(file_name) + '.csv', index=False)
            except:
                pass
            time.sleep(1)

        posicao_do_post += 1

        print('Final')
        print('post_link: ', len(post_link_completo))
        print('post_date: ', len(post_date_completo))
        print('amount_of_likes: ', len(amount_of_likes_completo))
        print('followers_links: ', len(followers_link_completo))
        print('followers_names: ', len(followers_names_completo))

    def creating_folder_img(self):
        followers_link_completo = []
        indice_interno_completo = []
        post_link_completo = []
        post_date_completo = []
        amount_of_likes_completo = []
        followers_names_completo = []

        # criando diretorio para salvar dados
        report_02 = {
            'post_type': 'img',
            'post_link': post_link_completo,
            'post_date': post_date_completo,
            'amount_of_likes': amount_of_likes_completo,
            'followers_links': followers_link_completo,
            'followers_names': followers_names_completo
        }

        report_02 = pd.DataFrame(data=report_02)
        report_02.to_csv(str(self.username) + '/report_02_img_' + str(self.username) + '.csv', index=False)

        insta_posts_links_img = pd.read_csv(str(self.username) + '/report_01_img_' + str(self.username) + '.csv')
        insta_posts_links_img = insta_posts_links_img['post_link'].tolist()
        return insta_posts_links_img

    def creating_folder_vid(self):
        ###BD02_vid: fn_post_likers_links: elabora relatorio BD02 com lista de quem curtiu os posts_vid (from a posts_likers_links_list = BD01)
        insta_posts_links_vid = pd.read_csv(str(self.username) + '/report_01_vid_' + str(self.username) + '.csv')
        insta_posts_links_vid = insta_posts_links_vid['post_link'].tolist()
        fn_post_likers_links_vid.fn_post_likers_links_vid(insta_posts_links_vid, self.driver, self.username, self.root_folder)

    def creating_folder_vid_and_img(self):
        ###DB02_APPEND: append two dataframes together and sort value indice_interno
        try:
            relatorio_DB02_img = pd.read_csv(str(self.username) + '/report_02_img_' + str(self.username) + '.csv')
            relatorio_DB02_vid = pd.read_csv(str(self.username) + '/report_02_vid_' + str(self.username) + '.csv')
            insta_posts_links_vid_and_img_csv = relatorio_DB02_img.append(relatorio_DB02_vid)
            insta_posts_links_vid_and_img_csv = insta_posts_links_vid_and_img_csv.drop_duplicates()
            # insta_posts_links_vid_and_img_csv = insta_posts_links_vid_and_img_csv.sort_values(by=['indice_interno'])
            # insta_posts_links_vid_and_img_csv = pd.read_csv(str(username) + '/report_02_img_' + str(username) + '.csv')
            # insta_posts_links_vid_and_img_csv = insta_posts_links_vid_and_img_csv.drop_duplicates()
            insta_posts_links_vid_and_img_csv.to_csv(
                str(self.username) + '/report_02_vid_and_img_' + str(self.username) + '.csv',
                index=False)
        except:
            insta_posts_links_vid_and_img_csv = pd.read_csv(
                str(self.username) + '/report_02_img_' + str(self.username) + '.csv')
            insta_posts_links_vid_and_img_csv = insta_posts_links_vid_and_img_csv.drop_duplicates()
            insta_posts_links_vid_and_img_csv.to_csv(
                str(self.username) + '/report_02_vid_and_img_' + str(self.username) + '.csv',
                index=False)

        try:
            os.remove(str(self.username) + '/report_02_vid_' + str(self.username) + '.csv')
            os.remove(str(self.username) + '/report_01_' + str(self.username) + '.csv')
            os.remove(str(self.username) + '/report_01_vid_or_img_' + str(self.username) + '.csv')
            os.remove(str(self.username) + '/report_01_img_' + str(self.username) + '.csv')
            os.remove(str(self.username) + '/report_02_img_' + str(self.username) + '.csv')
            os.remove(str(self.username) + '/report_01_vid_' + str(self.username) + '.csv')
        except:
            os.remove(str(self.username) + '/report_01_' + str(self.username) + '.csv')
            os.remove(str(self.username) + '/report_01_vid_or_img_' + str(self.username) + '.csv')
            os.remove(str(self.username) + '/report_01_img_' + str(self.username) + '.csv')
            os.remove(str(self.username) + '/report_02_img_' + str(self.username) + '.csv')
            os.remove(str(self.username) + '/report_01_vid_' + str(self.username) + '.csv')
        

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

        report_01 = {
            'indice_interno': indice_interno_completo,
            'post_link': lista}

        root_folder = str(root_folder)
        path = root_folder + '/' + str(username)
        report_01 = pd.DataFrame(data=report_01)
        report_01.to_csv(str(username) + '/report_01_' + str(username) + '.csv', index=False)

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

        start = DB02(username, driver, cookies, root_folder)
        insta_posts_links_img = start.creating_folder_img()
        start.fn_post_likers_links_img(insta_posts_links_img)




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
