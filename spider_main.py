from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import db_tool
from tqdm import tqdm
import time
import selenium.common.exceptions


class Spider(object):
    def __init__(self, account):
        self.__mongo = db_tool.create_mongo_session()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.__driver = webdriver.Chrome(executable_path='webdriver/chromedriver.exe', options=chrome_options)
        main_page = 'http://muchong.com/bbs/'
        self.__driver.get(url=main_page)
        if account == 1:
            self.__driver.add_cookie({'name': '_discuz_uid', 'value': '6111795'})
        else:
            self.__driver.add_cookie({'name': '_discuz_uid', 'value': '24724882'})
        self.__driver.add_cookie({'name': '_discuz_pw', 'value': '789cb43e40ab0032'})

    def start_topic_page_spider(self, start_index):
        topic_session = self.__mongo.get_database('xiaomuchong_db').get_collection('topic')
        for page_index in tqdm(range(start_index, start_index + 20, 1)):
            topic_dicts = []
            topic_page_url = 'http://muchong.com/f-198-{0}-typeid-1255'.format(str(page_index))
            self.__driver.get(url=topic_page_url)
            topic_items = self.__driver.find_elements_by_class_name(name='forum_list')
            for topic_item in topic_items:
                topic_main_item = topic_item.find_element_by_class_name(name='thread-name')
                topic_info_item = topic_main_item.find_element_by_class_name(name='a_subject')
                topic_url = topic_info_item.get_attribute(name='href')
                try:
                    topic_id = topic_url.split('-')[1]
                except IndexError:
                    continue
                topic_all_text = topic_main_item.text
                re_result = re.findall('\([0-9]+?\/[0-9]+\)', topic_all_text)[0][1:-1]
                reply_count = int(re_result.split('/')[0])
                view_count = int(re_result.split('/')[1])
                topic_name = topic_info_item.text
                poster_info_items = topic_item.find_elements_by_class_name(name='by')
                poster_info_item = poster_info_items[0]
                poster_profile_page_url = poster_info_item.find_element_by_tag_name(name='a').get_attribute(name='href')
                last_update_info_item = poster_info_items[1]
                last_editor_profile_page_url = last_update_info_item.find_element_by_tag_name(name='a').get_attribute(name='href')
                poster_info_text = poster_info_item.text
                poster_id = poster_info_text.split('\n')[0]
                post_date = poster_info_text.split('\n')[1]
                last_edit_text = last_update_info_item.text
                last_edit_time = last_edit_text.split('\n')[0]
                last_editor_id = last_edit_text.split('\n')[1].split(' ')[1]
                topic_dict = dict(
                    topic_id=topic_id,
                    topic_name=topic_name,
                    poster_id=poster_id,
                    post_date=post_date,
                    last_edit_time=last_edit_time,
                    last_editor_id=last_editor_id,
                    reply_count=reply_count,
                    view_count=view_count,
                    topic_url=topic_url,
                    poster_profile_page_url=poster_profile_page_url,
                    last_editor_profile_page_url=last_editor_profile_page_url
                )
                if topic_session.find_one({'topic_id': topic_id}):
                    continue
                topic_dicts.append(topic_dict)
            topic_session.insert_many(topic_dicts)

    def start_detail_page_spider(self, start_index, batch_size):
        topic_session = self.__mongo.get_database('xiaomuchong_db').get_collection('topic')
        topic_dicts = list(topic_session.find())
        for i in tqdm(range(start_index, start_index + batch_size, 1)):
            topic_dict = topic_dicts[i]
            topic_id = topic_dict['topic_id']
            detail_first_page_url = 'http://muchong.com/t-{0}-1'.format(topic_id)
            self.__driver.get(detail_first_page_url)
            with open('E:/Xiaomuchong/DetailPages/{0}-1.html'.format(topic_id), 'w+', encoding='utf-8') as first_write:
                first_write.write(self.__driver.page_source)
            try:
                page_count_element = self.__driver.find_element_by_class_name(name='smalltxt')
            except selenium.common.exceptions.NoSuchElementException:
                print(detail_first_page_url)
                continue
            page_count = page_count_element.text.split(' ')[1]
            all_page_count = int(page_count.split('/')[1])
            for next_page in range(2, all_page_count + 1, 1):
                page_url = 'http://muchong.com/t-{0}-{1}'.format(topic_id, str(next_page))
                self.__driver.get(page_url)
                with open('E:/Xiaomuchong/DetailPages/{0}-{1}.html'.format(topic_id, str(next_page)), 'w+', encoding='utf-8') as f:
                    f.write(self.__driver.page_source)
                time.sleep(1)
            topic_session.delete_one({'topic_id': topic_id})
            time.sleep(1)
