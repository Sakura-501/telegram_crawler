import datetime
import json
import os.path
import time

from config import config_all

config_all = config_all()

# 默认查询最新获取的3960个group_channel_url（最后去重）
def get_all_group_channel_url():
    all_url=[]
    # 测试阶段为limit 1，正式爬取数据需要改为预设值；
    search_url_sql="select gc_url from group_channel order by have_searched_times asc, id desc limit {}".format(config_all.history_message_use_url_limit)
    # search_url_sql="select gc_url from group_channel order by have_searched_times desc, id desc  limit 1"
    cursor.execute(search_url_sql)
    all_url_tmp=cursor.fetchall()
    if not all_url_tmp:
        print("No group_channel_urls!!! Please add some urls in step 2!")
        exit()
    else:
        for url in all_url_tmp:
            all_url.append(url[0])
    return list(set(all_url))

async def get_one_url_history_message(one_url):
    try:
        url_entity=await client.get_entity(one_url)
    except Exception as e:
        print(e)
        return False, {}

    histroy_message={}
    # 默认取最新的消息1000条，下面limit记得修改
    # 奥，可以字典嵌套数组：id作为键，然后值是一个列表[message.date,message.text, str(message), is_media]
    async for message in client.iter_messages(one_url,limit=config_all.history_message_limit):
        tmp_result=[]
        tmp_result.append(str(message.date))
        tmp_result.append(str(message.text))
        tmp_result.append(str(message))

        try:
            if hasattr(message.media,"document"):
                # 判断是否有media同时类型是否为apk或者exe，是的话直接打标记
                if ("application/vnd.android.package-archive" in message.media.document.mime_type) | (
                        "application/x-msdownload" in message.media.document.mime_type):
                    tmp_result.append(True)
                else:
                    tmp_result.append(False)
            else:
                tmp_result.append(False)
            histroy_message[str(message.id)]=tmp_result
        except Exception as e:
            print(e)
            return False, {}

    return True,histroy_message

# 奥，可以字典嵌套数组：id作为键，然后值是一个列表[date,str(message),is_media]
def write_one_url_message_file(one_url_name,histroy_message):
    current_date=str(datetime.date.today())
    history_message_dir=config_all.history_message_dir+"/"+current_date+"/"
    if not os.path.exists(history_message_dir):
        os.makedirs(history_message_dir)

    filename=one_url_name+".json"
    with open(history_message_dir+filename,"w",encoding="utf-8") as file:
        json.dump(histroy_message,file)

def write_one_url_message_table(one_url,history_message):
    insert_history_message_sql="insert into history_message(group_channel_url,message_id,message_date,message_text,message,is_application_media) values (%s,%s,%s,%s,%s,%s)"
    try:
        for id,list in history_message.items():
            # 我觉得先要做一波插入前检测，如果该条群组的消息已经存在数据库中了，那么就不要插入了；发现这个还挺费时间的，对很慢！！！
            before_insert_search_sql="select id from history_message where group_channel_url=%s and message_id=%s"
            cursor.execute(before_insert_search_sql,(one_url,id))
            if not cursor.fetchone():
                # 插入
                cursor.execute(insert_history_message_sql,(one_url,id,list[0],list[1],list[2],list[3]))
                db.commit()
    except Exception as e:
        print(e)
        db.rollback()

def searched_times_plus_one(one_url):
    update_times_sql="update group_channel set have_searched_times=have_searched_times + 1 where gc_url=%s"
    try:
        cursor.execute(update_times_sql,(one_url))
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)

async def get_history_message(mysql_instance,client_instance):
    global client, db, cursor
    client = client_instance.client
    db = mysql_instance.db
    cursor = mysql_instance.cursor

    # 首先获取上一步爬取的group/channel，默认取最新的3960条
    all_group_channel_url=get_all_group_channel_url()

    for i in range(len(all_group_channel_url)):
        begin_time=time.time()
        one_url=all_group_channel_url[i]
        print("{} get_history_message in: {}".format(i+1, one_url))
        one_url_name = one_url.replace("https://t.me/", "")
        flag, history_message = await get_one_url_history_message(one_url)
        # print(history_message)

        if flag:
            # 如果获取历史信息成功，要将group_channel_table里面的have_searched_times+1
            searched_times_plus_one(one_url)

            write_one_url_message_file(one_url_name, history_message)

            write_one_url_message_table(one_url, history_message)

        time.sleep(10)
        # 计算一个url使用的时间
        end_time=time.time()
        use_time=end_time-begin_time
        print("usetime: {:.2f}min".format(use_time/60))



