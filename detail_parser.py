from bs4 import BeautifulSoup
import os
import re
import db_tool
from tqdm import tqdm
import shutil
import pymongo.errors

detail_session = db_tool.create_mongo_session().get_database('xiaomuchong_db').get_collection('detail')
source_files = os.listdir('E:/Xiaomuchong/DetailPages')
for source_file in tqdm(source_files):
    source_file_name = 'E:/Xiaomuchong/DetailPages/' + source_file
    topic_id = source_file.split('-')[0]
    reader = open(source_file_name, 'r', encoding='utf-8')
    lines = reader.read()
    reader.close()
    soup = BeautifulSoup(lines, 'lxml')
    id_re = re.compile('pid.+')
    content_elements = soup.find_all(attrs={'id': id_re})
    for content_element in content_elements:
        pid = content_element['id'][3:]
        post_id = topic_id + '_' + pid
        post_content_element = content_element.find(class_='t_fsz')
        if not post_content_element:
            continue
        quote_element = post_content_element.find('fieldset')
        quote_pid = 0
        if quote_element:
            quote_text_element = quote_element.find('a')
            if not quote_text_element:
                quote_pid = 0
            else:
                try:
                    quote_pid = int(quote_text_element.text[:-1])
                except ValueError:
                    quote_pid = 0
            quote_element.decompose()
        source_client_element = post_content_element.find(class_='source_client')
        if source_client_element:
            source_client = source_client_element.text
            source_client_element.decompose()
        else:
            source_client = '未知'
        post_content_text_list = post_content_element.text.split('\n')
        post_content_text_list = list(filter(lambda o: o, post_content_text_list))
        post_text = '。'.join(post_content_text_list)
        poster_info = content_element.find(class_='pls_user')
        poster_nick_name = poster_info.h3.a.text
        poster_uid = poster_info.h3.a['href'].split('=')[-1]
        poster_detail_infos = poster_info.find_all('li')
        gender_info = list(filter(lambda o: '性别' in o.text, poster_detail_infos))
        if gender_info:
            gender_code = gender_info[0].text.split(': ')[1]
            if gender_code == 'MM':
                gender = '男'
            else:
                gender = '女'
        else:
            gender = '未知'
        major_info = list(filter(lambda o: '专业' in o.text, poster_detail_infos))
        if major_info:
            major = major_info[0].text.split(': ')[1]
        else:
            major = '未知'
        detail_dict = dict(
            topic_id=topic_id,
            pid=int(pid),
            quote_pid=quote_pid,
            poster_gender=gender,
            poster_major=major,
            post_text=post_text,
            poster_uid=poster_uid,
            poster_nick_name=poster_nick_name,
            source_client=source_client,
            post_id=post_id
        )
        try:
            detail_session.insert_one(detail_dict)
        except pymongo.errors.DuplicateKeyError:
            continue
    shutil.move(source_file_name, 'E:/Xiaomuchong/Parsed/' + source_file)
