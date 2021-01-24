import spider_main

spider = spider_main.Spider(account=1)
spider.start_detail_page_spider(start_index=1, batch_size=50)
