from config import config_all
from create_mysql import mysql_latest
from create_client import telegram_client
import sys
import asyncio
from keywords import get_keywords
from group_channel_search import get_group_channel
from history_message import get_history_message
from external_links import get_external_links

config_all = config_all()

# # 数据库初始化
mysql_instance = mysql_latest()

# #telegram客户端初始化
client_instance = telegram_client()

async def run_get_keywords():
    print("run_get_keywords")
    for bot in config_all.keyword_search_bot:
        print("search_keywords in bot: {}".format(bot))
        await get_keywords(bot, mysql_instance, client_instance)


async def run_get_group_channel(option):
    print("run_get_group_channel")
    for bot in config_all.group_channel_search_bot:
        print("search_group_channel in bot: {}".format(bot))
        await get_group_channel(option, bot, mysql_instance, client_instance)


async def run_get_history_message():
    print("run_get_history_message")
    await get_history_message(mysql_instance, client_instance)


def run_get_external_links():
    print("run_get_external_links")
    get_external_links(mysql_instance)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "usage: 1. python main.py keywords\n"
            "       2. - python main.py search_group_channel from_table\n"
            "          - python main.py search_group_channel from_config\n"
            "       3. python main.py history_message\n"
            "       4. python main.py external_links")

    elif sys.argv[1] == "keywords":
        # 先检查keywords表是否存在
        mysql_instance.create_keyword_table()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_get_keywords())

    elif sys.argv[1] == "search_group_channel":
        # 从数据库提取keyword去查询group_channel | # 从config.ini获取查询的关键词
        if sys.argv[2] == "from_table" or sys.argv[2] == "from_config":
            print("search_group_channel from_table")
            # 先检查group_channel表是否存在
            mysql_instance.create_group_channel_table()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(run_get_group_channel(sys.argv[2]))

    elif sys.argv[1] == "history_message":
        # 先检查history_message表是否存在
        mysql_instance.create_history_message_table()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_get_history_message())

    elif sys.argv[1] == "external_links":
        # 先检查external_links是否存在
        mysql_instance.create_external_links_table()
        run_get_external_links()

    else:
        print(
            "usage: 1. python main.py keywords\n"
            "       2. - python main.py search_group_channel from_table\n"
            "          - python main.py search_group_channel from_config\n"
            "       3. python main.py history_message\n"
            "       4. python main.py external_links")
