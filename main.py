import spider_main


#
# def start_main_spider():
#     account_num = 4
#     for i in range(account_num):
#         spider = spider_main.Spider(account=i)
#         spider.start_detail_page_spider(start_index=1, batch_size=50)

def start_user_page_spider():
    account_num = 4
    for i in range(account_num):
        spider = spider_main.Spider(account=i)
        spider.start_user_page_spider(batch_size=50)
