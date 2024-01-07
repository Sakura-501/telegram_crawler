import datetime
import os.path
import re
import time

from tools.config import config_all
from tools.create_client import telegram_client
from tools.create_mongo import mongo_latest

config_all = config_all()

mongo_instance = mongo_latest()
db = mongo_instance.db
now_collection = db[config_all.mongo_keywords_collection_name]


async def click_button(bot_entity, word):
    async for message in client.iter_messages(bot_entity, limit=1):
        if message.buttons:
            for sub_list in message.buttons:
                for keyword in sub_list:
                    if word in keyword.text:
                        await keyword.click()


def keyword_write_file(bot_name, keyword_result):
    print("keyword_write_file")
    current_date = str(datetime.date.today())
    keyword_folder_path = config_all.keyword_dir + "/"
    if not os.path.exists(keyword_folder_path):
        os.makedirs(keyword_folder_path)
    filename = current_date + "-" + bot_name + ".txt"
    with open(keyword_folder_path + filename, "w", encoding="utf-8") as file:
        for keyword in keyword_result:
            if "返回" in keyword:
                continue
            file.write(keyword + "\n")


def seperate_keyword(keyword):
    pattern = r"(.+?)\((.+?)\)"
    match = re.findall(pattern, keyword)
    return match[0][0], int(match[0][1])


def keyword_write_sql(bot_name, keyword_result):
    print("keyword_write_sql")
    # insert_keyword_sql = "insert into keywords(bot_name,time_stamp,keyword,search_times) values ( %s,%s,%s,%s )"
    for keyword in keyword_result:
        if "返回" in keyword:
            continue
        try:
            key, times = seperate_keyword(keyword)
            current_time = datetime.datetime.now()
            # cursor.execute(insert_keyword_sql,(bot_name,current_time,key,times))
            insert_data = {"bot_name": bot_name, "crawl_time": current_time, "keyword": key, "search_times": times}
            now_collection.insert_one(insert_data)
        except Exception as e:
            print(e)


async def get_keywords(bot,client_instance):
    global client
    client=client_instance.client

    bot_name = bot.replace("https://t.me/", "")
    bot_entity = await client.get_entity(bot)

    await client.send_message(bot_entity, "频道")
    time.sleep(3)
    await click_button(bot_entity, "购买广告")
    time.sleep(3)
    await click_button(bot_entity, "关键词排名广告")
    time.sleep(3)
    await click_button(bot_entity, "热门词排行")
    async for message in client.iter_messages(bot_entity, limit=1):
        keyword_result = []
        if message.buttons:
            for sub_list in message.buttons:
                for keyword in sub_list:
                    keyword_result.append(keyword.text)

        # keywords结果写到./keywords/202x-x-x-bot.txt文件中
        keyword_write_file(bot_name, keyword_result)
        # keywords结果写到keywords表中
        keyword_write_sql(bot_name, keyword_result)
