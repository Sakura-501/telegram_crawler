import pymysql
import pymongo

mysql_telegram_crawler_db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="root",
                                            database="telegram_crawler", charset="utf8mb4")
mysql_cursor = mysql_telegram_crawler_db.cursor()

mongo_client = pymongo.MongoClient(host="127.0.0.1", port=27017, username="darkweb", password="darkweb")
mongo_telegram_crawler_db = mongo_client["telegram_crawler"]

keywords_collection = mongo_telegram_crawler_db["keywords"]
group_channel_collection = mongo_telegram_crawler_db["group_channel"]
history_message_collection = mongo_telegram_crawler_db["history_message"]
external_links_collection = mongo_telegram_crawler_db["external_links"]


# keywords
def keywords():
    print("keywords migrate working!")
    keywords_search_sql = "select bot_name,time_stamp,keyword,search_times from keywords"
    mysql_cursor.execute(keywords_search_sql)
    keywords_search_result = mysql_cursor.fetchall()
    for one_result in keywords_search_result:
        # print(one_result)
        insert_data = {"bot_name": one_result[0], "crawl_time": one_result[1], "keyword": one_result[2],
                       "search_times": one_result[3]}
        keywords_collection.insert_one(insert_data)


def group_channel():
    print("group_channel migrate working!")
    group_channel_sql = "select bot_name,time_stamp,keyword,gc_url,have_searched_times from group_channel"
    mysql_cursor.execute(group_channel_sql)
    group_channel_result = mysql_cursor.fetchall()
    for one_result in group_channel_result:
        # print(one_result)
        insert_data = {"bot_name": one_result[0], "crawl_time": one_result[1], "keyword": one_result[2],
                       "group_channel_url": one_result[3], "have_searched_times": one_result[4]}
        group_channel_collection.insert_one(insert_data)


def history_message():
    print("history_message migrate working!")
    history_message_sql = "select group_channel_url,message_id,message_date,message_text,message,is_application_media from history_message"
    mysql_cursor.execute(history_message_sql)
    history_message_result = mysql_cursor.fetchall()
    print(len(history_message_result))
    for one_result in history_message_result:
        # print(one_result)
        insert_data = {"group_channel_url": one_result[0], "message_id": one_result[1], "message_date": one_result[2],
                       "message_text": one_result[3], "message": one_result[4],
                       "is_application_media": True if one_result[5] else False}
        history_message_collection.insert_one(insert_data)


def external_links():
    print("external_links migrate working!")
    external_links_sql = "select link from external_links"
    mysql_cursor.execute(external_links_sql)
    external_links_result = mysql_cursor.fetchall()
    for one_result in external_links_result:
        # print(one_result)
        insert_data = {"link": one_result[0]}
        external_links_collection.insert_one(insert_data)


keywords()
group_channel()
history_message()
external_links()
