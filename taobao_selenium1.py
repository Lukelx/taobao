# _*_ coding: utf-8 _*_

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import  By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq


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
    # driver.delete_all_cookies()
    return driver

def get_products(driver):
    # scroll_down()
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

def page_select(page, url, driver):
    wait = WebDriverWait(driver, 10)
    try:
        driver.get(url)
        if page > 1:
            # locate page num input box
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            # locate page num submit button
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit'))
            )
            input.clear()
            input.send_keys(page)
            submit.click()
        # confirm current page active
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'),
                str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
    except TimeoutException:
        page_select(page, url, driver)


keyword = '笔记本电脑'
start_url = 'https://s.taobao.com/search?q=' + quote(keyword)
driver = create_driver()
page_num = 2
for num in range(1, page_num + 1):
    page_select(num, start_url, driver)
    products = get_products(driver)
    print(products)
driver.quit()



