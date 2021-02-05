import numpy
import pandas
import db_tool
import re
from tqdm import tqdm
from collections import Counter


class XiaomuchongAnalysis(object):
    def __init__(self):
        self.__session = db_tool.create_mongo_session().get_database('xiaomuchong_db').get_collection('detail')
        self.__all_dicts = list(self.__session.find())

    def get_major_stat(self):
        majors = list(map(lambda o: o['poster_major'], self.__all_dicts))
        major_count = list(Counter(majors).items())
        major_count = sorted(major_count, key=lambda o: o[1], reverse=True)
        print(major_count[:20])

    def get_word_vector(self):


