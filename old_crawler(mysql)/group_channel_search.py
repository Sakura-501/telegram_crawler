import datetime
import os.path
import re
import time

from config import config_all

config_all = config_all()


# 默认查询最新获取的99个keywords
def get_all_keywords():
    all_keywords = []
    search_keywords_sql = "select keyword from keywords order by id desc limit {}".format(
        config_all.keyword_search_limit)
    cursor.execute(search_keywords_sql)
    all_keywords_tmp = cursor.fetchall()
    if not all_keywords_tmp:
        print("No keywords!!! Please add some keywords in step 1!")
        exit()
    else:
        for keyword in all_keywords_tmp:
            all_keywords.append(keyword[0])

    return list(set(all_keywords))


async def click_button(message_id, button_word):
    async for message in client.iter_messages(bot_entity, ids=message_id):
        if message.buttons:
            for button in message.buttons:
                for real_button in button:
                    if button_word in real_button.text:
                        await real_button.click()
                        return True
    return False


# 一般开头和结尾的url是广告。
def message_filter_url(message_text):
    find = re.findall("\((https://t\.me.*?)\)", message_text)
    return find[1:-1]


def write_group_channel_to_file(results, keyword):
    current_date = str(datetime.date.today())
    group_channel_dir = config_all.group_channel_dir + "/" + current_date + "-" + bot_name + "/"
    if not os.path.exists(group_channel_dir):
        os.makedirs(group_channel_dir)

    filename = keyword + ".txt"
    with open(group_channel_dir + filename, "w", encoding="utf-8") as file:
        for result in results:
            file.write(result + "\n")


def write_group_channel_to_table(results, keyword):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    is_url_in_table_sql="select * from group_channel where gc_url=%s";

    insert_group_channel_sql = "insert into group_channel(bot_name,time_stamp,keyword,gc_url,have_searched_times) values (%s,%s,%s,%s,%s)"
    try:
        for result in results:
            cursor.execute(is_url_in_table_sql,(result))
            if not cursor.fetchone():
                cursor.execute(insert_group_channel_sql, (bot_name, current_time, keyword, result,0))
                db.commit()
    except Exception as e:
        db.rollback()
        print(e)


async def use_keywords_search(keywords):
    print("一共{}个keywords：{}".format(len(keywords),keywords))
    for keyword in keywords:
        print("search keyword: {} in group: {}".format(keyword, group_name))
        results = []
        # 发送关键词，获取group OR channel，然后点击下一页继续获取
        try:
            message_id = 1318370
            # （PS：正式启用，这里需要修改）
            await client.send_message(bot_entity, keyword)
            time.sleep(3)

            # 首先获取返回消息的id，防止被其他人刷屏了
            async for message in client.iter_messages(bot_entity, limit=1):
                # （PS：正式启用，这里需要修改）
                message_id = message.id

            # 第一次返回的结果先保存，后面再判断点不点击下一页！
            async for message in client.iter_messages(bot_entity, ids=message_id):
                finds = message_filter_url(message.text)
                results.extend(finds)

            # 点击下一页模块，可根据需要进行注释！
            # （PS：正式启用，这里需要修改）
            # 一页有20个，测试为1次共40个,正式爬取可以设置大一点
            click_times = config_all.group_channel_click_times
            for i in range(click_times):
                flag = await click_button(message_id, "下一页")
                if flag:
                    time.sleep(2)
                    async for message in client.iter_messages(bot_entity, ids=message_id):
                        finds = message_filter_url(message.text)
                        results.extend(finds)
            # print(results)
        except Exception as e:
            print(e)

        # 写入文件
        write_group_channel_to_file(results, keyword)

        # 写入group_channel数据库
        write_group_channel_to_table(results, keyword)

        # 查询完一个keyword休息一下，防止被群组封了（
        time.sleep(20)


async def get_group_channel(option, bot, mysql_instance, client_instance):
    global client, db, cursor, bot_entity, bot_name, group_name
    client = client_instance.client
    db = mysql_instance.db
    cursor = mysql_instance.cursor
    group_name = bot

    bot_name = bot.replace("https://t.me/", "")
    bot_entity = await client.get_entity(bot)

    all_keywords = []
    # 从数据库中获取keywords
    if option == "from_table":
        all_keywords = get_all_keywords()
    # 从config.ini获取keywords
    elif option == "from_config":
        all_keywords = config_all.keywords
        # print(all_keywords)

    # （PS：正式启用，这里需要修改）
    # 测试一个keyword,正式启用时把one_keyword换成all_keywords
    await use_keywords_search(all_keywords)
