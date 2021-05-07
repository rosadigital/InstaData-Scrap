from bs4 import BeautifulSoup as bs
from math import ceil
from multiprocessing import Process, Manager
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#to create new folder and login at the unitario
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from assets_fn_03 import fn_login

from pathlib import Path
import os


def fn_post_vid_img (username, x, groups_of_data,cookies,root_folder):
    followers_link_completo = []
    indice_interno_completo = []
    post_link_completo = []
    post_date_completo = []
    amount_of_likes_completo = []
    followers_names_completo = []
    post_link_type_completo = []
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    options = Options()
    options.headless = True
    options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')

    driver.get('https://www.instagram.com/accounts/onetap/?next=%2F')
    for cookie in cookies:
        driver.add_cookie(cookie)

    manager = Manager()
    post_link_list = manager.list(groups_of_data)

    relatorio_BD01_vid_or_img = {
        'indice_interno': indice_interno_completo,
        'post_link': post_link_completo,
        'post_link_type': post_link_type_completo
    }

    relatorio_BD01_vid_or_img = pd.DataFrame(data=relatorio_BD01_vid_or_img)

    try:
        relatorio_BD01_vid_or_img_final = pd.read_csv(
            str(username) + '/relatorio_DB01_vid_or_img_' + str(username) + '.csv')
        relatorio_BD01_vid_or_img_final = relatorio_BD01_vid_or_img_final.append([relatorio_BD01_vid_or_img],
                                                                                 ignore_index=True)
        relatorio_BD01_vid_or_img_final.to_csv(str(username) + '/relatorio_DB01_vid_or_img_' + str(username) + '.csv',
                                               index=False)

    except:
        relatorio_BD01_vid_or_img.to_csv(str(username) + '/relatorio_DB01_vid_or_img_' + str(username) + '.csv',
                                     index=False)

    for post_link in post_link_list:
        post_link = str(post_link)

        # acessar pagina a ser pesquisada
        # print("Accessing post page to be searched")

        post_link = post_link
        driver.get('https://www.instagram.com' + str(post_link))
        print("Post page accessed successfully: ", post_link)
        # print("Getting amount of likes on this post")

        url_now = driver.current_url
        print(url_now)
        source = driver.page_source
        data = bs(source, 'html.parser')
        # print(data)

        try:
            video = data.find(class_='eo2As')
            # print(video)

            if (data.find(class_='eo2As').find(text=' views') == ' views' or data.find(class_='eo2As').find(text=' visualizações') == ' visualizações'):
                # data.find(type="video/mp4")['type'] == 'video/mp4'

                # source = driver.page_source
                # data = bs(source, 'html.parser')

                # # creating post_link list:
                post_link_completo.append(post_link)

                post_link_type_completo.append('vid')
                print("This post is a video")

            else:
                # # creating post_link list:
                post_link_completo.append(post_link)

                post_link_type_completo.append('img')
                print("This post is an img")

        except:
            # # creating post_link list:
            post_link_completo.append(post_link)

            post_link_type_completo.append('img')
            print("This post is an img")


        # creating index
    indice_interno_completo = []
    for y in range(1, len(post_link_type_completo)+1):
        indice_interno_completo.append(y)

    relatorio_BD01_vid_or_img = {
            'indice_interno': indice_interno_completo,
            'post_link': post_link_completo,
            'post_link_type': post_link_type_completo
        }

    root_folder = str(root_folder)
    path = root_folder + '/' + username
    relatorio_BD01_vid_or_img = pd.DataFrame(data=relatorio_BD01_vid_or_img)
    # print(relatorio_BD01_vid_or_img)

    relatorio_BD01_vid_or_img_final = pd.read_csv(str(username) + '/relatorio_DB01_vid_or_img_' + str(username) + '.csv')
    relatorio_BD01_vid_or_img_final = relatorio_BD01_vid_or_img_final.append([relatorio_BD01_vid_or_img], ignore_index=True)
    relatorio_BD01_vid_or_img_final = relatorio_BD01_vid_or_img_final.drop_duplicates()
    relatorio_BD01_vid_or_img_final.to_csv(str(username) + '/relatorio_DB01_vid_or_img_' + str(username) + '.csv',
                                        index=False)

#slicing into groups
def dispatch_jobs(data, driver, username, cookies,root_folder):
    print(data)
    total = len(data)
    amount_of_groups = (ceil(total/10))

    if total % 10 == 0:
        chunk_size = total / amount_of_groups
    else:
        chunk_size = 5 #maximo de itens num grupo
        # chunk_size = total #maximo de itens num grupo

    #to create chunck
    groups_of_data = chunks(data, int(chunk_size))
    print('slice: ',groups_of_data)
    print('amount_of_groups: ',len(groups_of_data))
    groups = len(groups_of_data)

    #starting multiprocess
    t0 = datetime.datetime.now()
    manager = Manager()
    x = manager.list([[]] * groups)
    n = 0
    p = []
    for i in range(groups):
        p.append(Process(target=fn_post_vid_img, args=(username, x, groups_of_data[n],cookies,root_folder)))
        p[i].start()
        n += 1

    for i in range(groups):
        p[i].join()
    t1 = datetime.datetime.now()
    print('Time running multiprocessing: ',t1-t0)

#defining chunks
def chunks(data, chunk_size):
    # print('------------')
    # print('chuncks')
    # print('L: ', data)
    # print('N: ', chunk_size)
    x = range(0, len(data), chunk_size)
    # print('x_range',x)
    # print('amount of groups: ',len(x))
    return [data[i:i+chunk_size] for i in x]



if __name__ == '__main__':
    t0 = datetime.datetime.now()
    username = 'meutrailer'

    # post_link = ['/p/CHvUhLGFFwLfoferL5J5BV4n2-ABMEhAMPEhkE0/']

    #for a list of images
    post_link = pd.read_csv(str(username) + '/relatorio_DB01_' + str(username) + '.csv')
    post_link = post_link['post_link'].tolist()

    #starting login
    options = Options()
    options.headless = True
    options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')
    print("Headless Chrome Initialized")

    fn_login.access('feliperosa_oficial','16107166', driver)
    # fn_login.access('keziawbr','f220912k', driver)


    root_folder = 'assets_fn_03'

    groups = len(post_link)
    manager = Manager()
    x = manager.list([[]] * groups)
    cookies = driver.get_cookies()

    fn_post_vid_img(username, x, post_link, cookies, root_folder)

    t1 = datetime.datetime.now()
    time_running = t1-t0
    print('time_running: ',time_running)