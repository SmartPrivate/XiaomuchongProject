import requests
import time
from tqdm import tqdm

cookies = {'_discuz_uid': '24724882', '_discuz_pw': '789cb43e40ab0032'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'}

for page in tqdm(range(1, 21, 1)):
    topic_page_url = 'http://muchong.com/f-198-{0}-typeid-1255'.format(str(page))
    r = requests.get(url=topic_page_url, cookies=cookies, headers=headers)
    with open('topic_pages/page_{0}.html'.format(str(page)), 'w+', encoding='utf-8') as f:
        f.write(r.text)
    time.sleep(1)
