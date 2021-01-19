from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import db_tool
from tqdm import tqdm


def start_detail_spider(account, start_index):
    mongo = db_tool.create_mongo_session()
    detail_session = mongo.get_database('xiaomuchong_db').get_collection('detail')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path='webdriver/chromedriver.exe', options=chrome_options)
    main_page = 'http://muchong.com/bbs/'
    driver.get(url=main_page)
    if account == 1:
        driver.add_cookie({'name': '_discuz_uid', 'value': '24725517'})
    else:
        driver.add_cookie({'name': '_discuz_uid', 'value': '24724882'})
    driver.add_cookie({'name': '_discuz_pw', 'value': '789cb43e40ab0032'})
