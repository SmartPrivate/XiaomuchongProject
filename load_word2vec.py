import db_tool

session = db_tool.create_mongo_session().get_database('tool_db').get_collection('chinese_word2vec')
reader = open('C:/Users/macha/Downloads/Tencent_AILab_ChineseEmbedding.txt', 'r', encoding='utf-8')
reader.readline()
line_count = 0
total_line_count = 0
word2vec_dicts = []
while True:
    line = reader.readline()
    word = line.split(' ')[0]
    vector = line.split(' ')[1:]
    vector = list(map(lambda o: float(o), vector))
    word2vec_dict = dict(word=word, vector=vector)
    word2vec_dicts.append(word2vec_dict)
    line_count += 1
    total_line_count += 1
    if line_count == 20000:
        session.insert_many(word2vec_dicts)
        word2vec_dicts.clear()
        line_count = 0
        print('已完成{0}行'.format(str(total_line_count)))
