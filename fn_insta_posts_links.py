from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import datetime

#to create new folder and login at the unitario
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from assets_fn_03 import fn_login

from pathlib import Path
import os


#Create a post link list from an username
def fn_post_link_list(username, driver,root_folder):
    #acessar pagina a ser pesquisada
    print("Accessing instagram page to be searched")
    time.sleep(10)
    driver.get('https://www.instagram.com/'+username)
    time.sleep(10)

    try:
        total_of_posts = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/ul/li[1]/span/span").text
    except:
        total_of_posts = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text

    # print(total_of_posts)
    total_of_posts = int(total_of_posts.replace(',', ''))
    numbers_of_scroll = round(((((total_of_posts)-24)/12)*2)+2+1)
    # round(((((((total_of)-24)/12)*2)+2+1))))
    print("---------------------------")
    print("Amount of posts: ", total_of_posts)

    #Starting ScrollDown
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

        #Deciding if the scrolldown continues or stops
        if index_now < total_of_posts:
            index_now = 0
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            scroll += 1
    print('Scrolldown concluded')

    #Inserting data into report
    print('Getting posts links')
    source = driver.page_source
    data = bs(source, 'html.parser')

    #creating index
    indice_interno_completo = []
    for x in range(1, len(lista)+1):
        indice_interno_completo.append(x)

    relatorio_BD01 = {
        'indice_interno': indice_interno_completo,
        'post_link': lista}

    root_folder = str(root_folder)
    path = root_folder + '/' + str(username)
    relatorio_BD01 = pd.DataFrame(data=relatorio_BD01)
    relatorio_BD01.to_csv(str(username)+'/relatorio_DB01_'+str(username)+'.csv', index=False)

    print("---------------------------")
    print("Report:")
    print("Amount of posts posted: ", total_of_posts)
    print("Amount of posts loaded: ", index_now)
    print("---------------------------")



if __name__ == '__main__':
    t0 = datetime.datetime.now()
    username = 'meutrailer'

    try:
        # creating folder
        print('Creating folder')
        root_folder = Path(__file__).parents[0]
        os.chdir(root_folder)
        folder = str(username)
        os.mkdir(folder)
        print('Folder created successfully')
    except:
        pass

    options = Options()
    options.headless = True
    options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')
    print("Headless Chrome Initialized")

    fn_login.access('feliperosa_oficial','16107166', driver)

    root_folder = 'assets_fn_03'

    fn_post_link_list(username, driver, root_folder)

    t1 = datetime.datetime.now()
    time_running = t1 - t0
    print('time_running: ',time_running)