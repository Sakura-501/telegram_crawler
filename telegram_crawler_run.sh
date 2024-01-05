#!/bin/bash
echo "Stop last telegram_crawler_run.sh first, Please wait for a moment!"
pkill -f "telegram_crawler_run.sh"
while [ 1 ]; do
    #nohup command > output.log 2>&1 &
    echo "1. 首先获取99个keywords"
    python ${PWD}/main.py keywords
    sleep 5;
    echo "2.1 从数据库获取关键字（默认99个），去查询group/channel"
    python ${PWD}/main.py search_group_channel from_table
    sleep 5;
    echo "2.2 从config.ini获取关键字（需自行添加），去查询group/channel"
    python ${PWD}/main.py search_group_channel from_config
    sleep 5;
    echo "3. 从数据库获取group/channel，查询历史消息（默认200个，每个1000条）"
    nohup python ${PWD}/main.py history_message > telegram_crawler.log 2>&1 &
    # 12个小时
    sleep 43200;
    echo "4. 从数据库获取历史消息，过滤出外链（默认20w条）"
    python ${PWD}/main.py external_links
    sleep 5;
done