import datetime
import pandas as pd
from math import ceil
from bs4 import BeautifulSoup as bs
from multiprocessing import Process, Manager
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from assets_fn_03 import fn_login


def fn_insta_bio(username, x, groups_of_data, cookies, root_folder):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    followers_link_completo = []
    followers_name_completo = []
    followers_bio_completo = []
    followers_amount_of_posts_completo = []
    followers_amount_of_followers_completo = []
    followers_amount_of_following_completo = []
    followers_private_completo = []

    options = Options()
    options.headless = True
    options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')

    driver.get('https://www.instagram.com/accounts/onetap/?next=%2F')
    for cookie in cookies:
        driver.add_cookie(cookie)

    # abrir o arquivo
    root_folder = str(root_folder)
    path = root_folder + '/' + username
    file_name = '/relatorio_DB03_' + str(username)

    try:
        doc_source = pd.read_csv(str(username) + str(file_name) + '.csv')
    except:
        pass

    relatorio_BD03_bio = {
        'followers_links': followers_link_completo,
        'followers_names': followers_name_completo,
        'amount_of_posts': followers_amount_of_posts_completo,
        'amount_of_followers': followers_amount_of_followers_completo,
        'amount_of_following': followers_amount_of_following_completo,
        'private': followers_private_completo,
        'bio': followers_bio_completo
    }

    relatorio_BD03_bio = pd.DataFrame(data=relatorio_BD03_bio)
    relatorio_BD03_bio = relatorio_BD03_bio.drop_duplicates()

    path = root_folder + '/' + username
    try:
        relatorio_BD03_created = pd.read_csv(str(username) + '/relatorio_DB03_bio_' + str(username) + '.csv')
        relatorio_BD03_bio = relatorio_BD03_created.append([relatorio_BD03_bio], ignore_index=True)
        relatorio_BD03_bio = relatorio_BD03_bio.drop_duplicates()
        relatorio_BD03_bio.to_csv(str(username) + '/relatorio_DB03_bio_' + str(username) + '.csv', index=False)
    except:
        relatorio_BD03_bio.to_csv(str(username) + '/relatorio_DB03_bio_' + str(username) + '.csv', index=False)

    manager = Manager()
    insta_followers_links_list = manager.list(groups_of_data)

    #acessar pagina a ser pesquisada
    for insta_followers_links in insta_followers_links_list:
        insta_followers_links = str(insta_followers_links)

        print("Accessing instagram page to be searched")
        driver.get('https://www.instagram.com'+insta_followers_links)
        time.sleep(3)
        # wait = WebDriverWait(driver, 5)
        # element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '-vDIg')))

        print("Starting scrapping")
        source = driver.page_source
        data = bs(source, 'html.parser')

        #followers_link
        followers_link_completo.append(insta_followers_links)

        #followers_name
        try:
            name = data.find(class_='-vDIg').h1.text
            followers_name_completo.append(name)

        except:
            name = str("n/a")
            followers_name_completo.append(name)
        print('name:',name)

        #bio
        try:
            bio = data.find(class_='-vDIg').span.text
            if bio.find("Followed by") == 0:
                bio = str("n/a")
                followers_bio_completo.append(bio)

            else:
                bio = data.find(class_='-vDIg').span.text
                followers_bio_completo.append(bio)

        except:
            bio = str("n/a")
            followers_bio_completo.append(bio)


        #amount_of_posts
        amount_of_posts = data.findAll(class_='g47SY')[0].text

        if (amount_of_posts.find('.') or amount_of_posts.find(',')):
            amount_of_posts = (int(amount_of_posts.replace('.', '')) or int(amount_of_posts.replace(',', '')))
        else:
            amount_of_posts = int(amount_of_posts)

        followers_amount_of_posts_completo.append(amount_of_posts)

        #amount_of_followers
        amount_of_followers = data.findAll(class_='g47SY')[1].text

        try:
            if (amount_of_followers.find('.') or amount_of_followers.find(',')):
                amount_of_followers = (int(amount_of_followers.replace('.', '')) or int(amount_of_followers.replace(',', '')))
            else:
                amount_of_followers = int(amount_of_followers)
        except:
            amount_of_followers = amount_of_followers

        followers_amount_of_followers_completo.append(amount_of_followers)

        #amount_of_following
        amount_of_following = data.findAll(class_='g47SY')[2].text

        if (amount_of_following.find('.') or amount_of_following.find(',')):
            amount_of_following = (int(amount_of_following.replace('.', '')) or int(amount_of_following.replace(',', '')))
        else:
            amount_of_following = int(amount_of_following)

        followers_amount_of_following_completo.append(amount_of_following)

        #is_private
        try:
            is_private = data.find(class_='rkEop').text == 'This Account is Private'
            followers_private_completo.append("1")

            # This Account is Private
        except:
            followers_private_completo.append("0")


        relatorio_BD03_bio = {
                    'followers_links': followers_link_completo,
                    'followers_names': followers_name_completo,
                    'amount_of_posts': followers_amount_of_posts_completo,
                    'amount_of_followers': followers_amount_of_followers_completo,
                    'amount_of_following': followers_amount_of_following_completo,
                    'private': followers_private_completo,
                    'bio': followers_bio_completo
                }

        relatorio_BD03_bio = pd.DataFrame(data=relatorio_BD03_bio)
        relatorio_BD03_bio = relatorio_BD03_bio.drop_duplicates()

        path = root_folder + '/' + username
        try:
            relatorio_BD03_created = pd.read_csv(str(username) + '/relatorio_DB03_bio_' + str(username) + '.csv')
            relatorio_BD03_bio = relatorio_BD03_created.append([relatorio_BD03_bio], ignore_index=True)
            relatorio_BD03_bio = relatorio_BD03_bio.drop_duplicates()
            relatorio_BD03_bio.to_csv(str(username) + '/relatorio_DB03_bio_' + str(username) + '.csv', index=False)
        except:
            relatorio_BD03_bio.to_csv(str(username) + '/relatorio_DB03_bio_' + str(username) + '.csv', index=False)

        # deleting source of data
        try:
            index_followers_link_list = insta_followers_links_list.index(insta_followers_links)
            doc_source = doc_source.drop([index_followers_link_list])
            doc_source = pd.DataFrame(data=doc_source)
            doc_source.to_csv(str(username) + str(file_name) + '.csv', index=False)
        except:
            pass

    relatorio_BD03_bio = pd.read_csv(str(username) + '/relatorio_DB03_bio_' + str(username) + '.csv', float_precision=None)
    relatorio_BD03_bio = relatorio_BD03_bio.drop_duplicates()
    relatorio_BD03_bio.to_csv(str(username) + '/relatorio_DB03_bio_' + str(username) + '.csv', index=False)
    # print(relatorio_BD03_bio)


def dispatch_jobs(data, driver, username, cookies, root_folder):
    print(data)
    total = len(data)
    print('amount of profiles for bio: ', total)
    amount_of_groups = (ceil(total / 10))

    if total % 10 == 0:
        chunk_size = total / amount_of_groups
    elif total > 100:
        chunk_size = 100
    else:
        chunk_size = total  # maximo de itens num grupo
        # chunk_size = total #maximo de itens num grupo

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
    for i in range(groups):
        p.append(Process(target=fn_insta_bio, args=(username, x, groups_of_data[n], cookies, root_folder)))
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
    username = 'maisautonomo'

    initialization_options = input('Write 1 for one profile, 2 for DB02, 3 for DB03: ')

    if initialization_options == str(1):
        #bio from one profile
        print('Starting bio from one profile')
        groups_of_data = ['/afb_santos/']

    elif initialization_options == str(2):
        #DB02: bio from people who liked a post (run fn_post_likers_links_img before)
        print('Starting DB02 bio from people who liked a post')
        groups_of_data = pd.read_csv(str(username) + '/relatorio_DB02_img_' + str(username) + '.csv')
        groups_of_data = groups_of_data['followers_links'].tolist()

    elif initialization_options == str(3):
        print('Starting DB03 bio from people who followed a profile')
        #DB03: bio from people who followed a profile (run fn_insta_followers_links before)
        groups_of_data = pd.read_csv(str(username) + '/relatorio_DB03_' + str(username) + '.csv')
        groups_of_data = groups_of_data['followers_links'].tolist()

    #starting login
    # options = Options()
    # options.headless = True
    # options.add_argument('--headless')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--no-sandbox')
    # options.add_argument('window-size=1920x1080')
    # driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')
    driver = webdriver.Chrome('chromedriver')
    print("Headless Chrome Initialized")

    fn_login.access('feliperosa_oficial','16107166', driver)
    # fn_login.access('keziawbr','f220912k', driver)

    root_folder = 'assets_fn_03'
    manager = Manager()
    x = manager.list([[]] * 1)
    cookies = driver.get_cookies()

    dispatch_jobs(groups_of_data, driver, username, cookies, root_folder)