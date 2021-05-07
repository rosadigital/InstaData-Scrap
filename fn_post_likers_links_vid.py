from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from multiprocessing import Process, Manager


#to create new folder and login at the unitario
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from assets_fn_03 import fn_login

from pathlib import Path
import os

def fn_post_likers_links_vid (post_link_list, driver, username,root_folder):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    followers_link_completo = []
    indice_interno_completo = []
    post_link_completo = []
    post_date_completo = []
    amount_of_likes_completo = []
    followers_names_completo = []

    # abrir o arquivo
    root_folder = str(root_folder)
    path = root_folder + '/' + username
    file_name = '/relatorio_DB01_vid_' + str(username)
    doc_source = pd.read_csv(str(username) + str(file_name) + '.csv')

    for post_link in post_link_list:
        post_link = str(post_link)

        # acessar pagina a ser pesquisada
        print("Accessing post page to be searched")
        time.sleep(5)
        post_link = post_link
        driver.get('https://www.instagram.com' + str(post_link))
        time.sleep(2)
        print("Post page accessed successfully: ", post_link)

        # print("Getting amount of likes on this post")
        time.sleep(2)
        source = driver.page_source
        data = bs(source, 'html.parser')
        # print(data)

        # Scraping data
        print("Starting scraping:", post_link)

        # Getting post date
        print('Getting post date')
        source = driver.page_source
        data = bs(source, 'html.parser')
        post_date = data.find(class_='_1o9PC Nzb55')
        post_date = post_date['title']
        print('Post date: ', post_date)
        print('Post date gotten successfully')

        # creating followers_links list:
        followers_link = []
        followers_link_completo.append("n/a")

        # # creating post_link list:
        post_link_completo.append(post_link)

        # creating amount of likes:
        video_likes_button = driver.find_element_by_class_name('vcOH2')
        video_likes_button.click()
        time.sleep(1)
        source = driver.page_source
        data = bs(source, 'html.parser')
        amount_of_likes_video = data.find(class_='vJRqr').span.text
        amount_of_likes_completo.append(amount_of_likes_video)

        # creating post_date list:
        post_date_completo.append(post_date)

        # creating followers_names list:
        followers_names_completo.append("n/a")

        time.sleep(2)

        relatorio_BD02 = {
            'post_type': 'vid',
            'post_link': post_link_completo,
            'post_date': post_date_completo,
            'amount_of_likes': amount_of_likes_completo,
            'followers_links': followers_link_completo,
            'followers_names': followers_names_completo
        }

        relatorio_BD02 = pd.DataFrame(data=relatorio_BD02)

        print('post_link: ', len(post_link_completo))
        print('post_date: ', len(post_date_completo))
        print('amount_of_likes: ', len(amount_of_likes_completo))
        print('followers_links: ', len(followers_link_completo))
        print('followers_names: ', len(followers_names_completo))

        index_post_link_list = post_link_list.index(post_link)
        doc_source = doc_source.drop([index_post_link_list])

        # deleting source of data
        doc_source = pd.DataFrame(data=doc_source)
        doc_source.to_csv(str(username) + str(file_name) + '.csv', index=False)

        path = 'assets_fn_02/' + username
        relatorio_BD02.to_csv(str(username) + '/relatorio_DB02_vid_' + str(username) + '.csv', index=False)

    print('Final')
    print('post_link: ', len(post_link_completo))
    print('post_date: ', len(post_date_completo))
    print('amount_of_likes: ', len(amount_of_likes_completo))
    print('followers_links: ', len(followers_link_completo))
    print('followers_names: ', len(followers_names_completo))


if __name__ == '__main__':
    username = 'feliperosa_oficial'

    # #for only one video
    # groups_of_data = ['p/CHvUhLGFFwLfoferL5J5BV4n2-ABMEhAMPEhkE0/']

    # #for a list of videos
    # groups_of_data = pd.read_csv(str(username) + '/relatorio_DB01_vid_' + str(username) + '.csv')
    # groups_of_data = groups_of_data['post_link'].tolist()

    #starting login
    options = Options()
    options.headless = True
    options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')
    print("Headless Chrome Initialized")

    fn_login.access('feliperosa_oficial','16107166', driver)

    root_folder = 'assets_fn_03'
    manager = Manager()
    x = manager.list([[]] * 1)
    cookies = driver.get_cookies()

    fn_post_likers_links_vid(groups_of_data, driver, username, root_folder)