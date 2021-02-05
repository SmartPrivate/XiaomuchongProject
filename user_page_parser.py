from bs4 import BeautifulSoup
import os
import re
import db_tool
from tqdm import tqdm

files = os.listdir('E:/Xiaomuchong/UserPages')
for file in files:
    abs_filename = 'E:/Xiaomuchong/UserPages/' + file
    # reader = open(abs_filename, 'r', encoding='gbk')
    reader = open('test.html', 'r', encoding='gbk')
    soup = BeautifulSoup(reader.read(), 'lxml')
    text_contents = soup.find_all('td')
    for text_content in text_contents:
        print(text_content.text)

