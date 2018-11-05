# _*_ coding: utf-8 _*_

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.parse import quote
import time
from pyquery import PyQuery as pq
import csv


def create_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins-discovery")

    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
    driver.start_client()
    driver.delete_all_cookies()
    return driver

def login(driver, username, password):
    login_url = 'https://login.taobao.com/member/login.jhtml'
    driver.get(login_url)
    driver.execute_script("document.getElementById('J_Quick2Static').click()")
    driver.execute_script("document.getElementById('TPL_username_1').value = '{}'".format(username))
    driver.execute_script("document.getElementById('TPL_password_1').value = '{}'".format(password))
    driver.execute_script("document.getElementById('J_SubmitStatic').click()")

def scroll_down():
    html_page = driver.find_element_by_tag_name('html')
    html_page.send_keys(Keys.END)
    time.sleep(1)

# def organize_url(keyword):
#     offset_number = [x * 44 for x in range(1, 3)]
#     page_urls = []
#     for num in offset_number:
#         page_url = f'https://s.taobao.com/search?q={keyword}&bcoffset=4&p4ppushleft=%2C48&ntoffset=4&s={num}'
#         page_urls.append(page_url)
#     return page_urls

def get_products(driver):
    html = driver.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    products = []
    for item in items:
        product = {
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'product_link': item.find('.pic .a').attr('href'),
            'shop': item.find('.shop').text(),
            'shop_link': item.find('.shop .a').attr('href'),
            'location': item.find('.location').text()
        }
        products.append(product)
    return products


keyword = '笔记本电脑'
driver = create_driver()
# username = 'lxwhat@vip.sina.com'
# password = '***'
# login(driver, username, password)
# time.sleep(2)
start_url = 'https://s.taobao.com/search?q=' + quote(keyword)
driver.get(start_url)
time.sleep(2)
scroll_down()
for i in range(1, 4):
    products = get_products(driver)
    time.sleep(1)
    driver.find_element_by_css_selector('#mainsrp-pager li.item.next a').click()
    scroll_down()
driver.quit()




