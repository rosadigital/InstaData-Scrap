from bs4 import BeautifulSoup as bs
from math import ceil
from multiprocessing import Process, Manager, Lock
import pandas as pd
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from assets_fn_03 import fn_login
import os
import stat

def fn_post_likers_links_img (username, x, groups_of_data,cookies, lock, i):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    followers_link_completo = []
    indice_interno_completo = []
    post_link_completo = []
    post_date_completo = []
    amount_of_likes_completo = []
    followers_names_completo = []

    #Configurando webdrivers
    options = Options()
    options.headless = True
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')
    # driver = webdriver.Chrome('chromedriver')
    driver.get('https://www.instagram.com/accounts/onetap/?next=%2F')
    for cookie in cookies:
        driver.add_cookie(cookie)

    # acessar relatorio DB01_IMG (para deletar apos processamento)
    path = 'assets_fn_02/' + username
    file_name = '/relatorio_DB01_img_' + str(username)

    try:
        relatorio_BD02_created = pd.read_csv(
            str(username) + '/relatorio_DB02_img_' + str(username) + 'v_' + str(i) + '.csv')

    except:
        # criando diretorio para salvar dados por processo
        relatorio_BD02 = {
            'post_type': 'img',
            'post_link': post_link_completo,
            'post_date': post_date_completo,
            'amount_of_likes': amount_of_likes_completo,
            'followers_links': followers_link_completo,
            'followers_names': followers_names_completo
        }

        relatorio_BD02 = pd.DataFrame(data=relatorio_BD02)

        relatorio_BD02.to_csv(str(username) + '/relatorio_DB02_img_' + str(username) + 'v_' + str(i) + '.csv', index=False)

        relatorio_BD02_created = pd.read_csv(
            str(username) + '/relatorio_DB02_img_' + str(username) + 'v_' + str(i) + '.csv')

    # try:
    #     relatorio_BD02_created = pd.read_csv(str(username) + '/relatorio_DB02_img_' + str(username) + '.csv')
    #     relatorio_BD02 = relatorio_BD02_created.append([relatorio_BD02], ignore_index=True)
    #     relatorio_BD02.to_csv(str(username) + '/relatorio_DB02_img_' + str(username) + '.csv', index=False)
    # except:
    #     relatorio_BD02.to_csv(str(username) + '/relatorio_DB02_img_' + str(username) + '.csv',
    #                           index=False)        # relatorio_BD02.to_csv(str(username) + '/relatorio_DB02_img_' + str(username) + '.csv', index=False)


    #acessando posts
    manager = Manager()
    post_link_list = manager.list(groups_of_data)

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
            number_of_followers_specific = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]/button/span').text
        except:
            number_of_followers_specific = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/div[4]/span').text

        # Precisa somar mais 1 porque o numero de likes que aparece sempre falta 01

        try:
            if number_of_followers_specific.find(','):
                number_of_followers_specific = int(number_of_followers_specific.replace(',', '')) + 1
            elif number_of_followers_specific.find('.'):
                number_of_followers_specific = int(number_of_followers_specific.replace('.', '')) + 1
        except:
            number_of_followers_specific = int(number_of_followers_specific) + 1

        # if (number_of_followers_specific.find(',') or number_of_followers_specific.find('.')):
        #     try:
        #         number_of_followers_specific = int(number_of_followers_specific.replace(',', '')) + 1
        #         number_of_followers_specific = int(number_of_followers_specific.replace('.', '')) + 1
        #     except:
        #         number_of_followers_specific = int(number_of_followers_specific) + 1

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
        # try:
        #     fBody = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div")
        # except:
        #     try:
        #         fBody = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div")
        #     except:
        #         try:
        #             fBody = driver.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/div")
        #         except:
        #             print("erro no fbody do processo: ", i)
        #             break

        scroll = 1
        followers_loaded = 0
        items = []
        items_names = []
        index = 0
        index_now = 0
        lista = []
        lista_to_scroll = [] #lista criada para armazenar numero de links capturados (sem duplicados) e considerar no scrolldown
        lista_name = []
        index_interno = []
        lista_de_links = []
        followers_names = []
        scroll_limit = (((number_of_followers_specific - 6) / 5) + 2) * 2
        f = 1
        a = 1
        print('scroll_limit', str(i), str(post_link), scroll_limit)
        ## codigo antigo
        # while (index_now < number_of_followers_specific):
        #     time.sleep(1)
        #     source = driver.page_source
        #     data = bs(source, 'html.parser')
        #     time.sleep(1)
        #
        #     for followers in data.find_all('a', class_='FPmhX notranslate MBL3Z'):
        #         followers_link = followers['href']
        #         items.append(followers_link)
        #         index += 1
        #     lista = items
        #
        #     # removerduplicadosdalista
        #     lista_to_scroll = pd.Series(lista).drop_duplicates()
        #     index_now = len(lista_to_scroll)
        #
        #     for followers_name in data.find_all(class_='Igw0E IwRSH YBx95 vwCYk'):
        #         followers_name = followers_name.find(class_='_7UhW9 xLCgt MMzan _0PwGv uL8Hv')
        #         if followers_name:
        #             followers_name = followers_name.text
        #         else:
        #             followers_name = "n/a"
        #         items_names.append(followers_name)
        #     lista_name = items_names
        #
        #     if index_now < number_of_followers_specific:
        #         index_now = 0
        #         try:
        #             fBody = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div")
        #         except:
        #             try:
        #                 fBody = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div")
        #             except:
        #                 fBody = driver.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/div")
        #
        #         driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        #     scroll += 1
        #
        #     if (scroll > scroll_limit):
        #         break

        while index_now < number_of_followers_specific:
            test_class = driver.find_elements_by_xpath("//*[@class='FPmhX notranslate MBL3Z']")
            # print('test_class', len(test_class))
            test_class = len(test_class)

            # try:

            # try:
            #     for f in range(f, test_class + 1):
            #
            #
            #         # print('likers', f)
            #         # try:
            #         #     test = driver.find_element_by_xpath(
            #         #         "/html/body/div[5]/div/div/div[2]/div/div/div[" + str(f) + "]/div[2]/div[1]/div/span/a")
            #         # except:
            #         #     try:
            #         #         followers_name = driver.find_element_by_xpath(
            #         #             "/html/body/div[4]/div/div/div[2]/div/div/div[" + str(f) + "]/div[2]/div[2]/div/span/a")
            #         #     except:
            #         #         followers_name = driver.find_element_by_xpath(
            #         #             "/html/body/div[5]/div/div/div[2]/div/div/div[" + str(f) + "]/div[1]/div[2]/div/span/a")
            #         test = test.get_attribute('href')
            #         # print('test', test)
            #         items.append(test)
            #         index += 1

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

            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
            scroll += 1
            f = 1
            a = 1

            if (scroll > scroll_limit):
                "alerta de scroll list"
            # except:
            #     print("ainda carregando a pagina", post_link, "no processo", i)





                # f = 1
                # for f in range(f, test_class + 1):
                #     # print('likers', f)
                #     try:
                #         try:
                #             followers_name = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div/div/div[" + str(f) + "]/div[2]/div[2]/div")
                #         except:
                #             try:
                #                 followers_name = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div/div/div[" + str(f) + "]/div[2]/div[2]/div")
                #             except:
                #                 followers_name = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div/div/div[" + str(f) + "]/div[1]/div[2]/div")
                #         followers_name = followers_name.text
                #         # print('followers_name',followers_name)
                #     except:
                #         followers_name = "n/a"
                #         # print('followers_name',followers_name)
                #     items_names.append(followers_name)
                # lista_name = items_names

            #     lista = items
            #     items_index_now = pd.Series(data=lista).drop_duplicates()
            #     index_now = len(items_index_now)
            #     # print('index_now: ', index_now)
            #
            #     driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
            #     scroll += 1
            #     f = 1
            #
            #     if (scroll > scroll_limit):
            #         "alerta de scroll list"
            # except:
            #     print("ainda carregando a pagina", post_link, "no processo", i)


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

        # print(len(post_link_completo))
        # print(len(post_date_completo))
        # print(len(amount_of_likes_completo))
        # print(len(followers_link_completo))
        # print('followers_names_completo',len(followers_names_completo))

        relatorio_BD02 = {
            'post_type': 'img',
            'post_link': post_link_completo,
            'post_date': post_date_completo,
            'amount_of_likes': amount_of_likes_completo,
            'followers_links': followers_link_completo,
            'followers_names': followers_names_completo
        }

        relatorio_BD02 = pd.DataFrame(data=relatorio_BD02)
        relatorio_BD02 = relatorio_BD02.drop_duplicates()

        print('post_link: ', str(i), str(post_link), len(post_link_completo))
        print('post_date: ', str(i), str(post_link), len(post_date_completo))
        print('amount_of_likes: ', str(i), str(post_link), len(amount_of_likes_completo))
        print('followers_links: ', str(i), str(post_link), len(followers_link_completo))
        print('followers_names: ', str(i), str(post_link), len(followers_names_completo))

        path = 'assets_fn_02/' + username

        lock.acquire()
        # relatorio_BD02_created = pd.read_csv(str(username) + '/relatorio_DB02_img_' + str(username) + '.csv')
        relatorio_BD02 = relatorio_BD02_created.append([relatorio_BD02], ignore_index=True)
        relatorio_BD02 = relatorio_BD02.drop_duplicates()
        relatorio_BD02.to_csv(str(username) + '/relatorio_DB02_img_' + str(username) + 'v_' + str(i) + '.csv', index=False)
        ''''ATENCAO: caso este diretorio nao exista, ele devera ser criado antes de processar esta funcao. criar este diretorio nesta funcao esta sobreponto os arquivos'''
        lock.release()

        #verificar se o item pesquisado foi adicionado na lista de items pesquisados, para apagar da lista original. Se nao foi, nao apaga da lista original.
        # deleting source of data if the post_link was processed
        relatorio_BD02_post_link = pd.read_csv(str(username) + '/relatorio_DB02_img_' + str(username) + 'v_' + str(i) + '.csv')
        relatorio_BD02_post_link = relatorio_BD02_post_link['post_link'].tolist()
        item_processed = post_link

        try:
            if relatorio_BD02_post_link.index(item_processed) >= 0:
                # deleting source of data
                lock.acquire()
                doc_source = pd.read_csv(str(username) + str(file_name) + '.csv')
                doc_source.drop(doc_source.index[doc_source['post_link'] == str(post_link)], inplace=True)
                doc_source.to_csv(str(username) + str(file_name) + '.csv', index=False)
                lock.release()
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

    # path = 'assets_fn_02/' + username
    # relatorio_BD02.to_csv(str(username)+'/relatorio_DB02_img_' + str(username) + '.csv', index=False)

def dispatch_jobs(data, driver, username, cookies,lock):
    print(data)
    total = len(data)
    print('total: ',total)
    amount_of_groups = (ceil(total / 10))

    if total % 10 == 0:
        chunk_size = total / amount_of_groups
    elif total > 100:
        # chunk_size = total / 40 #all items distributed in atleast 50 groups
        # chunk_size = total / 10 #all items distributed in atleast 10 groups
        chunk_size = total / 5 #all items distributed in atleast 10 groups
    else:
        chunk_size = 5  # maximo de itens num grupo
        # chunk_size = total #maximo de itens num grupo

    # insta_posts_links_img_csv = pd.read_csv(str(username) + '/relatorio_DB01_img_' + str(username) + '.csv', index=False)

    # to create chunck
    groups_of_data = chunks(data, int(chunk_size))
    print('slice: ', groups_of_data)
    print('amount_of_groups: ', len(groups_of_data))
    groups = len(groups_of_data)

    t0 = datetime.datetime.now()
    # starting multiprocess
    manager = Manager()
    x = manager.list([[]] * groups)
    n = 0
    p = []

    # i = 0
    # fn_post_likers_links_img(username, x, groups_of_data[0], cookies, lock, i)


    # for i in range(groups):
    #     fn_post_likers_links_img(username, x, groups_of_data[n], cookies, lock, i)
    #     n += 1

    for i in range(groups):
        p.append(Process(target=fn_post_likers_links_img, args=(username, x, groups_of_data[n], cookies, lock, i)))
        print('Starting process: ', i)
        p[i].start()
        n += 1

    for i in range(groups):
        p[i].join()
    t1 = datetime.datetime.now()
    print('Time running multiprocessing: ', t1 - t0)

def chunks(data, chunk_size):
    # print('------------')
    # print('chuncks')
    # print('L: ', data)
    # print('N: ', chunk_size)
    x = range(0, len(data), chunk_size)
    # print('x_range',x)
    # print('amount of groups: ',len(x))
    return [data[i:i + chunk_size] for i in x]


if __name__ == '__main__':
    t0 = datetime.datetime.now()
    username = 'nasasasdocondor'
    # username = 'meutrailer' #186 posts

    # #for only one link of image
    # username = 'clinicadesaudemelhorar' #186 posts
    # groups_of_data = ['p/CJrfXTyl8Z8/']

    followers_link_completo = []
    indice_interno_completo = []
    post_link_completo = []
    post_date_completo = []
    amount_of_likes_completo = []
    followers_names_completo = []

    #criando diretorio para salvar dados
    relatorio_BD02 = {
        'post_type': 'img',
        'post_link': post_link_completo,
        'post_date': post_date_completo,
        'amount_of_likes': amount_of_likes_completo,
        'followers_links': followers_link_completo,
        'followers_names': followers_names_completo
    }

    relatorio_BD02 = pd.DataFrame(data=relatorio_BD02)
    relatorio_BD02.to_csv(str(username) + '/relatorio_DB02_img_' + str(username) + '.csv', index=False)
    # os.chmod(str(username) + '/relatorio_DB02_img_' + str(username) + '.csv', stat.S_IRWXO)  # makesfile Read, write, and execute by others.

    try:
        groups_of_data = pd.read_csv(str(username) + '/relatorio_DB01_img_' + str(username) + '.csv')
        groups_of_data = groups_of_data['post_link'].tolist()
    except:
        #for a list of images
        insta_posts_links_vid_or_img_csv = pd.read_csv(str(username) + '/relatorio_DB01_vid_or_img_' + str(username) + '.csv')
        insta_posts_links_vid_or_img_csv = pd.DataFrame(data=insta_posts_links_vid_or_img_csv)
        insta_posts_links_img_csv = insta_posts_links_vid_or_img_csv.loc[insta_posts_links_vid_or_img_csv['post_link_type'] == 'img']
        insta_posts_links_img_csv.to_csv(str(username) + '/relatorio_DB01_img_' + str(username) + '.csv', index=False)

        groups_of_data = pd.read_csv(str(username) + '/relatorio_DB01_img_' + str(username) + '.csv')
        groups_of_data = groups_of_data['post_link'].tolist()

    #starting login
    options = Options()
    options.headless = True
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')
    # driver = webdriver.Chrome('chromedriver')
    print("Headless Chrome Initialized")

    fn_login.access('feliperosa_oficial','16107166', driver)
    # fn_login.access('keziawbr','f220912k', driver)

    root_folder = 'assets_fn_03'
    manager = Manager()
    x = manager.list([[]] * 1)
    cookies = driver.get_cookies()
    lock = Lock()
    # fn_post_likers_links_img(username, x, groups_of_data, cookies)
    dispatch_jobs(groups_of_data, driver, username, cookies,lock)


    t1 = datetime.datetime.now()
    time_running = t1 - t0
    print('time_running: ',time_running)