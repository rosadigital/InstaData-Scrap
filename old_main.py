import os
import datetime
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from multiprocessing import Process, Manager, Lock

'''Login on instagram'''
import fn_login

# FOCUS ON FEEDS
'''For getting post links from a profile'''
import fn_insta_posts_links

'''For defining if the post link is a video or image'''
import fn_post_vid_img

'''For getting infos (and likers) from posts (images or videos)'''
import fn_post_likers_links_img
import fn_post_likers_links_vid

# FOCUS ON PROFILES AND BIOS
'''For getting a list of followers from a profile'''
import fn_insta_followers_links

'''For getting infos (and bios) from profiles'''
import fn_insta_bio

# DEFINING GENDER FROM IBGE
import fn_ajuste_de_nomes
import fn_multiprocess


# from assets_fn_04_to_github import fn_update_gender_to_DB02_and_DB03

def BD02_img(username, driver, cookies):
    ##GERACAO DE BD02
    ###BD02_img: fn_post_likers_links: elabora relatorio BD02 com lista de quem curtiu os posts_img (from a posts_likers_links_list = BD01)

    followers_link_completo = []
    indice_interno_completo = []
    post_link_completo = []
    post_date_completo = []
    amount_of_likes_completo = []
    followers_names_completo = []

    # criando diretorio para salvar dados
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

    insta_posts_links_img = pd.read_csv(str(username) + '/relatorio_DB01_img_' + str(username) + '.csv')
    insta_posts_links_img = insta_posts_links_img['post_link'].tolist()
    # fn_post_likers_links_img.fn_post_likers_links_img(insta_posts_links_img, driver, username)
    lock = Lock()

    fn_post_likers_links_img.dispatch_jobs(insta_posts_links_img, driver, username, cookies, lock)


def BD02_vid(username, driver, root_folder):
    ###BD02_vid: fn_post_likers_links: elabora relatorio BD02 com lista de quem curtiu os posts_vid (from a posts_likers_links_list = BD01)
    insta_posts_links_vid = pd.read_csv(str(username) + '/relatorio_DB01_vid_' + str(username) + '.csv')
    insta_posts_links_vid = insta_posts_links_vid['post_link'].tolist()
    fn_post_likers_links_vid.fn_post_likers_links_vid(insta_posts_links_vid, driver, username, root_folder)


def BD02_img_and_vid(username, driver):
    ###DB02_APPEND: append two dataframes together and sort value indice_interno
    try:
        relatorio_DB02_img = pd.read_csv(str(username) + '/relatorio_DB02_img_' + str(username) + '.csv')
        relatorio_DB02_vid = pd.read_csv(str(username) + '/relatorio_DB02_vid_' + str(username) + '.csv')
        insta_posts_links_vid_and_img_csv = relatorio_DB02_img.append(relatorio_DB02_vid)
        insta_posts_links_vid_and_img_csv = insta_posts_links_vid_and_img_csv.drop_duplicates()
        # insta_posts_links_vid_and_img_csv = insta_posts_links_vid_and_img_csv.sort_values(by=['indice_interno'])
        # insta_posts_links_vid_and_img_csv = pd.read_csv(str(username) + '/relatorio_DB02_img_' + str(username) + '.csv')
        # insta_posts_links_vid_and_img_csv = insta_posts_links_vid_and_img_csv.drop_duplicates()
        insta_posts_links_vid_and_img_csv.to_csv(
            str(username) + '/relatorio_DB02_vid_and_img_' + str(username) + '.csv',
            index=False)
    except:
        insta_posts_links_vid_and_img_csv = pd.read_csv(str(username) + '/relatorio_DB02_img_' + str(username) + '.csv')
        insta_posts_links_vid_and_img_csv = insta_posts_links_vid_and_img_csv.drop_duplicates()
        insta_posts_links_vid_and_img_csv.to_csv(
            str(username) + '/relatorio_DB02_vid_and_img_' + str(username) + '.csv',
            index=False)

    try:
        os.remove(str(username) + '/relatorio_DB02_vid_' + str(username) + '.csv')
        os.remove(str(username) + '/relatorio_DB01_' + str(username) + '.csv')
        os.remove(str(username) + '/relatorio_DB01_vid_or_img_' + str(username) + '.csv')
        os.remove(str(username) + '/relatorio_DB01_img_' + str(username) + '.csv')
        os.remove(str(username) + '/relatorio_DB02_img_' + str(username) + '.csv')
        os.remove(str(username) + '/relatorio_DB01_vid_' + str(username) + '.csv')
    except:
        os.remove(str(username) + '/relatorio_DB01_' + str(username) + '.csv')
        os.remove(str(username) + '/relatorio_DB01_vid_or_img_' + str(username) + '.csv')
        os.remove(str(username) + '/relatorio_DB01_img_' + str(username) + '.csv')
        os.remove(str(username) + '/relatorio_DB02_img_' + str(username) + '.csv')
        os.remove(str(username) + '/relatorio_DB01_vid_' + str(username) + '.csv')


def BD03(username, driver, root_folder):
    ##GERACAO DE BD03
    ###DB03: fn_insta_followers_links: elabora relatorio BD03 com lista de followers (from an username)
    fn_insta_followers_links.fn_followers_link(username, driver, root_folder)


def BD03_bio(username, driver, cookies, root_folder):
    ##GERACAO DE BD03_bio
    insta_followers_links_list = pd.read_csv(str(username) + '/relatorio_DB03_' + str(username) + '.csv')
    insta_followers_links_list = insta_followers_links_list['followers_links'].tolist()
    # fn_insta_bio.fn_insta_bio(insta_followers_links_list, driver, username)

    fn_insta_bio.dispatch_jobs(insta_followers_links_list, driver, username, cookies, root_folder)

    # os.remove(str(username) + '/relatorio_DB03_' + str(username) + '.csv')


##NEXT STEPS (ALWAYS):
# fn_ajuste_de_nomes (editar nomes que precisam ser ajustados)
# fn_gender_search_brasil #pesquisar genero com base no nome
# fn_update_gender #update DB02 e DB03 com gender

def DB04_ajuste_de_nomes(username):
    fn_ajuste_de_nomes.fn_ajuste_de_nomes(username)


# def DB04_multiprocess(username,root_folder):
#     fn_multiprocess.fn_multiprocess(username,root_folder)

# def update_gender_to_DB02_and_DB03(username):
#     fn_update_gender_to_DB02_and_DB03.update_gender_to_DB02_andDB03(username)


if __name__ == '__main__':
    username = 'renovesergipe'
    root_folder = 'assets_fn_04_to_github'

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Starting headless Chrome
    # options = Options()
    # options.headless = True
    # options.add_argument('--headless')
    # options.add_argument('window-size=1920x1080')
    # driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')
    driver = webdriver.Chrome('chromedriver')
    print("Headless Chrome Initialized")

    '''Logging into Instagram'''
    fn_login.access('feliperosa_oficial', '16107166', driver)
    # fn_login.access('keziawbr','f220912k', driver)

    cookies = driver.get_cookies()

    '''Creating folder'''
    try:
        t0 = datetime.datetime.now()
        creating_folder(username, driver)
        t1 = datetime.datetime.now()
        time_creating_folder = t1 - t0
    except:
        pass

    '''Getting post links'''
    t0 = datetime.datetime.now()
    BD01(username, driver, cookies, root_folder)
    t1 = datetime.datetime.now()
    time_running_DB01 = t1 - t0

    '''Getting post (image) likers'''
    t0 = datetime.datetime.now()
    BD02_img(username, driver, cookies)
    # print('total_of_likes_on_all_posts_img:', 0)
    t1 = datetime.datetime.now()
    time_running_DB02_img = t1 - t0

    '''Getting post (videos) likers'''
    try:
        t0 = datetime.datetime.now()
        BD02_vid(username, driver, root_folder)
        # print('total_of_likes_on_all_posts_vids:', 0)
        t1 = datetime.datetime.now()
        time_running_DB02_vid = t1 - t0
    except:
        pass

    t0 = datetime.datetime.now()
    BD02_img_and_vid(username, driver)
    t1 = datetime.datetime.now()
    time_running_DB02_img_and_vid = t1 - t0

    '''Getting a followers list'''
    t0 = datetime.datetime.now()
    BD03(username, driver, root_folder)
    t1 = datetime.datetime.now()
    time_running_DB03 = t1 - t0

    '''Getting followers infos (and bios)'''
    t0 = datetime.datetime.now()
    BD03_bio(username, driver, cookies, root_folder)
    t1 = datetime.datetime.now()
    time_running_DB03_bio = t1 - t0

    '''Separating first name from each likers (DB02) and followers (DB03)'''
    t0 = datetime.datetime.now()
    DB04_ajuste_de_nomes(username)
    t1 = datetime.datetime.now()
    time_running_DB04_ajuste_de_nomes = t1 - t0

    # t0 = datetime.datetime.now()
    # DB04_multiprocess(username, root_folder)
    # t1 = datetime.datetime.now()
    # time_running_DB04_multiprocess = t1 - t0

    # t0 = datetime.datetime.now()
    # update_gender_to_DB02_and_DB03(username)
    # t1 = datetime.datetime.now()
    # time_running_update_gender_to_DB02_and_DB03 = t1 - t0

    try:
        print('---------------------')
        print('Time running summary:', datetime.date.today())
        try:
            print('time_creating_folder:', time_creating_folder)
        except:
            pass
        try:
            print('time_running_DB01:', time_running_DB01)
            # print('total_of_posts_teste:', total_of_posts)
        except:
            pass
        try:
            print('time_running_DB02_img:', time_running_DB02_img)
        except:
            pass
        try:
            print('time_running_DB02_vid:', time_running_DB02_vid)
        except:
            pass
        try:
            print('time_running_DB02_img_and_vid:', time_running_DB02_img_and_vid)
        except:
            pass
        try:
            print('time_running_DB03:', time_running_DB03)
        except:
            pass
        try:
            print('time_running_DB03_bio:', time_running_DB03_bio)
        except:
            pass
        try:
            print('time_running_DB04_ajuste_de_nomes:', time_running_DB04_ajuste_de_nomes)
        except:
            pass
        # try:
        #     print('time_running_DB04_multiprocess:', time_running_DB04_multiprocess)
        # except:
        #     pass
        # try:
        #     print('time_running_update_gender_to_DB02_and_DB03:', time_running_update_gender_to_DB02_and_DB03)
        # except:
        #     pass
    except:
        pass