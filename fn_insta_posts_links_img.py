from bs4 import BeautifulSoup as bs
import time
import pandas as pd

# driver = fn_login.open_driver()

# def access (login, senha):
#     #abrir e logar
#     driver.get('https://www.instagram.com/')
#     driver.implicitly_wait(20)
#     print("Logging into instagram")
#     #ajustar para esperar por https://www.instagram.com/accounts/onetap/?next=%2F
#     driver.find_element_by_name('username').send_keys(login)
#     driver.find_element_by_name('password').send_keys(senha)
#     driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
#     print("Logging concluded successfully")

#Create a post link list from an username
def fn_post_link_list_img(username, driver):
    #acessar pagina a ser pesquisada
    print("Accessing instagram page to be searched")
    time.sleep(10)
    driver.get('https://www.instagram.com/'+username)
    time.sleep(5)

    #Getting amount of posts
    total_of_posts = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/ul/li[1]/span/span").text
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

    path = 'assets_fn/' + username
    relatorio_BD01 = pd.DataFrame(data=relatorio_BD01)
    relatorio_BD01.to_csv(path+'/relatorio_DB01_'+str(username)+'.csv', index=False)

    print("---------------------------")
    print("Report:")
    print("Amount of posts posted: ", total_of_posts)
    print("Amount of posts loaded: ", index_now)
    print("---------------------------")