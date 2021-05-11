from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # To set up selenium without show browser
from codes.Login import Login  # Login on instagram
from codes.DB01 import DB01  # To create report 01
from codes.DB02 import DB02  # To create report 02
from codes.DB03 import DB03  # To create report 03

'''Settings'''
headless_option = input("Hello, how are you doing?"
                        "\n Firstly, you have 02 options to operate:"
                        "\n 01 - if you would like to use the headless option, without browser"
                        "\n 02 - if you prefer to see the process, opening your browser"
                        "\n Write here, and press enter >>>: ")
write_login = input('Please, write your instagram profile here >>> : ')
write_password = input('Now, please, write your instagram password here >>> : ')
search_input = input("Finally, write the profile name that you would like to research on Instagram."
                     "\n I.e from https://www.instagram.com/coisandoporai/, just write the end coisandoporai."
                     "\n Write here, and press enter >>>: ")
print('---------------------------')
if headless_option == "01":
    options = Options()
    options.headless = True
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')  # headless
elif headless_option == "02":
    driver = webdriver.Chrome('chromedriver')  # not headless

profile = write_login
password = write_password
Login(driver, profile, password).run()  # login on Instagram

username = search_input
cookies = driver.get_cookies()  # saving cookies for future access
DB01(username, driver, cookies).run()
DB02(username, driver, cookies).run()
DB03(username, driver, cookies).run()

driver.quit()
