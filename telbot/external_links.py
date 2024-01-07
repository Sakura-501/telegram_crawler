import datetime
import os.path

from tools.config import config_all
from tools.create_mongo import mongo_latest
import re
import pymongo

config_all = config_all()
mongo_instance=mongo_latest()
db=mongo_instance.db
history_message_collection=db[config_all.mongo_history_message_collection_name]
external_links_collection=db[config_all.mongo_external_links_collection_name]

# 提取url，过滤掉t.me域名
def message_filter_url(message):
    url_pattern = r"https?://[^\s),'\"]+"
    urls = re.findall(url_pattern, message)
    # print(urls)
    filtered_urls = [url for url in urls if not (url.startswith("https://t.me/") | url.startswith("http://t.me/"))]

    return list(set(filtered_urls))


def grep_external_links():
    result_links = []
    # search_sql="select message from history_message order by id desc limit 10000"
    # search_sql = "select message from history_message order by id desc limit {}".format(config_all.message_from_table_limit)

    try:
        # cursor.execute(search_sql)
        # all_message_tmp = cursor.fetchall()
        all_message_tmp=history_message_collection.find({},{"_id":0,"message":1}).sort("_id",pymongo.DESCENDING).limit(config_all.message_from_table_limit)
        all_message_tmp=list(all_message_tmp)
        if not all_message_tmp:
            print("No messages!!! Please add some messages in step 3!")
            # exit()
        else:
            for message in all_message_tmp:
                # 将\n字符串替换成空格，后面方便剔除
                links = message_filter_url(message["message"].replace(r"\n", " "))
                result_links.extend(links)
                result_links = list(set(result_links))

    except Exception as e:
        print(e)

    return result_links


# def write_external_links_file(external_links):
#     current_date = str(datetime.datetime.now().date())
#     max_message_id = 1
#     max_message_id_search_sql = "select id from history_message order by id desc limit 1"
#     try:
#         cursor.execute(max_message_id_search_sql)
#         max_message_id = cursor.fetchall()[0][0]
#     except Exception as e:
#         print(e)
#
#     external_links_dir = config_all.external_links_dir + "/"
#     if not os.path.exists(external_links_dir):
#         os.makedirs(external_links_dir)
#     filename = current_date + "_" + "max-message-id-" + str(max_message_id) + ".txt"
#     with open(external_links_dir + filename, "w", encoding="utf-8") as file:
#         for link in external_links:
#             file.write(link + "\n")


def write_external_links_table(external_links):
    # insert_external_links_sql = "insert into external_links(link) values (%s)"
    # before_search_external_links_sql = "select id from external_links where link=%s"

    try:
        for link in external_links:
            # 如果数据库不存在这条link才插入
            # cursor.execute(before_search_external_links_sql, (link))
            # if not cursor.fetchone():
            #     cursor.execute(insert_external_links_sql, (link))
            #     db.commit()
            before_search_data={"link":link}
            if not external_links_collection.find_one(before_search_data):
                insert_data={"link":link}
                external_links_collection.insert_one(insert_data)
    except Exception as e:
        # db.rollback()
        print(e)


def get_external_links():

    external_links = grep_external_links()
    # print(external_links)

    # 写文件暂时不需要了。
    # write_external_links_file(external_links)

    write_external_links_table(external_links)
