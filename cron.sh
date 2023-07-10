
# some env setting
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ACCESS_TOKEN=""
SIGN_KEY=""
TENCENT_CLOUD_SECRET_ID=""
TENCENT_CLOUD_SECRET_KEY=""

# run tennis tools
*/5 * * * * /usr/bin/python3 /home/lighthouse/tennis_helper/watcher_for_isz.py --item_name "大沙河" --sales_id "100220" --sales_item_id "100000" --watch_days 7 --send_sms 1 >> /home/lighthouse/logs/dsh_$(date +\%Y-\%m-\%d-\%H\%M).log 2>&1
*/5 * * * * /usr/bin/python3 /home/lighthouse/tennis_helper/watcher_for_isz.py --item_name "香蜜公园" --sales_id "101332" --sales_item_id "100341" --watch_days 2 --send_sms 1 >> /home/lighthouse/logs/xm_$(date +\%Y-\%m-\%d-\%H\%M).log 2>&1
*/5 * * * * /usr/bin/python3 /home/lighthouse/tennis_helper/watcher_for_isz.py --item_name "深云文体" --sales_id "105057" --sales_item_id "105127" --watch_days 2 --send_sms 1 >> /home/lighthouse/logs/sy_$(date +\%Y-\%m-\%d-\%H\%M).log 2>&1
*/5 * * * * /usr/bin/python3 /home/lighthouse/tennis_helper/watcher_for_isz.py --item_name "黄木岗" --sales_id "101333" --sales_item_id "100344" --watch_days 2 --send_sms 1 >> /home/lighthouse/logs/hmg_$(date +\%Y-\%m-\%d-\%H\%M).log 2>&1


# delete old logs everyday
0 1 * * * find /home/lighthouse/logs -name "*.log" -type f -mtime +3 -delete
