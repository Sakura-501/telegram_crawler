import json
from configparser import ConfigParser

class config_all:
    def __init__(self):
        config=ConfigParser()
        # 配置文件路径
        config.read("config.ini",encoding="utf-8")
        # 详细配置
        self.api_id = int(config["telegram_config"]["api_id"])
        self.api_hash=config["telegram_config"]["api_hash"]
        self.session_name=config["telegram_config"]["session_name"]

        self.mysql_host=config["mysql"]["host"]
        self.mysql_port = int(config["mysql"]["port"])
        self.mysql_user = config["mysql"]["user"]
        self.mysql_password = config["mysql"]["password"]
        self.mysql_database = config["mysql"]["database"]
        self.mysql_charset = config["mysql"]["charset"]
        self.mysql_table_keyword = config["mysql"]["table_keyword"]

        self.proxy_ip=config["proxy"]["ip"]
        self.proxy_port = int(config["proxy"]["port"])

        self.keyword_dir=config["download_dir"]["keyword_dir"]
        self.group_channel_dir=config["download_dir"]["group_channel_dir"]
        self.history_message_dir=config["download_dir"]["history_message_dir"]
        self.application_media_dir=config["download_dir"]["application_media_dir"]
        self.external_links_dir=config["download_dir"]["external_links_dir"]

        self.keyword_search_bot=json.loads(config["bot_channel_group"]["keyword_search_bot"])
        self.group_channel_search_bot=json.loads(config["bot_channel_group"]["group_channel_search_bot"])

        self.keyword_search_limit=int(config["settings"]["keyword_search_limit"])
        self.group_channel_click_times=int(config["settings"]["group_channel_click_times"])
        self.history_message_limit = int(config["settings"]["history_message_limit"])
        self.history_message_use_url_limit=int(config["settings"]["history_message_use_url_limit"])
        self.message_from_table_limit=int(config["settings"]["message_from_table_limit"])
        self.keywords=list(set(json.loads(config["settings"]["keywords"])))



# conf=config_all()
# value=getattr(conf,"api_id")
# print(value)