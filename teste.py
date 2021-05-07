# from selenium import webdriver
# import time
#
# driver = webdriver.Chrome('chromedriver')  # not headless
# profile = 'feliperosa_oficial'
# password = 'f220912k'
# post_link = 'CMKPJXSBQc_'
#
# # abrir e logar
# driver.get('https://www.instagram.com/')
# driver.implicitly_wait(20)
# print("Logging into instagram")
# # ajustar para esperar por https://www.instagram.com/accounts/onetap/?next=%2F
# driver.find_element_by_name('username').send_keys(profile)
# driver.find_element_by_name('password').send_keys(password)
# driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
# print("Logging concluded successfully")
# time.sleep(5)
#
# driver.get('https://www.instagram.com/p/' + str(post_link))  # accessing post link
#
# print('teste 01')
# if ('views' or 'visualizações') in driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]').text:
#     print('video')
# else:
#     print('img')
#
# print('teste 02')
# post_info = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]').text
# if str(post_info).find(('views' or 'visualizações')):
#     print('video')
# else:
#     print('img')
#
# # link_info = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]')
# # print(link_info)
# # print(link_info.text)


texto = "views  asd"
matches = ["views", "visualizações"]

if any(x in texto for x in matches):
    print('video')
else:
    print('img')