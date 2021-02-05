import db_tool

session = db_tool.create_mongo_session()
topic_session = session.get_database('xiaomuchong').get_collection('topic')
detail_session = session.get_database('xiaomuchong').get_collection('detail')
no_major = list(detail_session.find({'poster_major': '未知'}))
print(len(no_major))
