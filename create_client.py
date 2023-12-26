import socks
from telethon import TelegramClient
from config import config_all

config_all=config_all()

class telegram_client():
    def __init__(self):
        self.session_name=config_all.session_name
        self.api_id=config_all.api_id
        self.api_hash=config_all.api_hash

        self.client=TelegramClient(self.session_name,self.api_id,self.api_hash,proxy=(socks.SOCKS5,config_all.proxy_ip,config_all.proxy_port)).start()

    # def start(self):
    #     print('(Press Ctrl+C to stop this)')
    #     self.client.run_until_disconnected()