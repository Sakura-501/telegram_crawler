import argparse
import traceback

from tools.config import config_all
import asyncio
from keywords import get_keywords
from group_channel_search import get_group_channel
from history_message import get_history_message
from external_links import get_external_links
from tools.create_client import telegram_client

config_all = config_all()
client_instance = telegram_client()
client = client_instance.client

async def run_get_keywords():
    print("run_get_keywords")
    for bot in config_all.keyword_search_bot:
        print("search_keywords in bot: {}".format(bot))
        await get_keywords(bot,client_instance)


async def run_get_group_channel(option):
    print("run_get_group_channel")
    for bot in config_all.group_channel_search_bot:
        print("search_group_channel in bot: {}".format(bot))
        await get_group_channel(option, bot,client_instance)


async def run_get_history_message():
    print("run_get_history_message")
    await get_history_message(client_instance)


def run_get_external_links():
    print("run_get_external_links")
    get_external_links()


def get_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="a bot for telegram_crawler.")
    parser.add_argument("-k", "--keywords", type=str, choices=["from_config"],
                        help="crawl 99 keywords from bot in config.ini.")
    parser.add_argument("-s", "--search_group_channel", type=str, choices=["from_collection", "from_config"],
                        help="crawl group/channel by sending keywords from collection/config.ini.")
    parser.add_argument("-m", "--history_message", type=str, choices=["from_collection"],
                        help="crawl history_message from group/channel which is in collection.(最少访问优先爬取原则)")
    parser.add_argument("-e", "--external_links", type=str, choices=["from_collection"],
                        help="extract external_links from history_message in collection.")
    return parser


def all_run(args):
    loop = asyncio.get_event_loop()
    if args.keywords == "from_config":
        loop.run_until_complete(run_get_keywords())
    elif args.search_group_channel == "from_collection" or args.search_group_channel == "from_config":
        loop.run_until_complete(run_get_group_channel(args.search_group_channel))
    elif args.history_message == "from_collection":
        loop.run_until_complete(run_get_history_message())
    elif args.external_links == "from_collection":
        get_external_links()
    else:
        args_parser.print_help()


if __name__ == "__main__":
    try:
        args_parser = get_argparse()
        args = args_parser.parse_args()
        try:
            all_run(args)
        except Exception as e:
            traceback.print_exc()
            print("Please check your problems!!!")

    except KeyboardInterrupt:
        print("\nInterrupt received! Exit now!")
