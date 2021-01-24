import db_tool

session = db_tool.create_mongo_session()
topic_session = session.get_database('xiaomuchong').get_collection('topic')

