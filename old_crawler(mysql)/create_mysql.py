import pymysql
from config import config_all

config_all = config_all()


class mysql_latest:
    def __init__(self):
        self.db = pymysql.connect(host=config_all.mysql_host, port=config_all.mysql_port, user=config_all.mysql_user,
                                  password=config_all.mysql_password, database=config_all.mysql_database,
                                  charset=config_all.mysql_charset)
        self.cursor = self.db.cursor()

    def create_keyword_table(self):
        # print("create_keyword_table")
        try:
            show_table_keyword_sql = "show tables like 'keywords'"
            self.cursor.execute(show_table_keyword_sql)
            if not self.cursor.fetchone():
                create_table_keyword_sql = """create table keywords(
                id int auto_increment primary key ,
                bot_name varchar(255),
                time_stamp timestamp default current_timestamp on update current_timestamp,
                keyword varchar(255) ,
                search_times int
                )"""
                self.cursor.execute(create_table_keyword_sql)
            else:
                pass
        except Exception as e:
            print(e)

    def create_group_channel_table(self):
        # print("create_group_channel_table")
        try:
            show_table_group_channel_sql = "show tables like 'group_channel'"
            self.cursor.execute(show_table_group_channel_sql)
            if not self.cursor.fetchone():
                create_table_group_channel_sql = """create table group_channel(
                id int auto_increment primary key ,
                bot_name varchar(255),
                time_stamp timestamp default current_timestamp on update current_timestamp,
                keyword varchar(255) ,
                gc_url varchar(255) ,
                have_searched_times int
                )"""
                self.cursor.execute(create_table_group_channel_sql)
            else:
                pass
        except Exception as e:
            print(e)

    def create_history_message_table(self):
        try:
            show_table_group_channel_sql = "show tables like 'history_message'"
            self.cursor.execute(show_table_group_channel_sql)
            if not self.cursor.fetchone():
                create_table_group_channel_sql = """create table history_message(
                id int auto_increment primary key ,
                group_channel_url varchar(255),
                message_id int ,
                message_date timestamp default current_timestamp on update current_timestamp,
                message_text text,
                message text,
                is_application_media tinyint(1)
                )"""
                self.cursor.execute(create_table_group_channel_sql)
            else:
                pass
        except Exception as e:
            print(e)

    def create_external_links_table(self):
        try:
            show_table_external_links_sql = "show tables like 'external_links'"
            self.cursor.execute(show_table_external_links_sql)
            if not self.cursor.fetchone():
                create_table_external_links_sql = """create table external_links(
                id int auto_increment primary key ,
                gc_url varchar(1024) ,
                link varchar(2048) 
                )"""
                self.cursor.execute(create_table_external_links_sql)
            else:
                pass
        except Exception as e:
            print(e)
