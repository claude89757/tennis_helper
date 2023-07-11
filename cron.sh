
# some env setting
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ACCESS_TOKEN=""
SIGN_KEY=""
TENCENT_CLOUD_SECRET_ID=""
TENCENT_CLOUD_SECRET_KEY=""

# run tennis tools
*/5 * * * * /usr/bin/python3 /home/lighthouse/tennis_helper/watcher_for_isz.py --item_name "大沙河" --sales_id "100220" --sales_item_id "100000" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/dsh_$(date +\%Y-\%m-\%d-\%H\%M).log 2>&1
*/5 * * * * /usr/bin/python3 /home/lighthouse/tennis_helper/watcher_for_isz.py --item_name "香蜜体育" --sales_id "101332" --sales_item_id "100341" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/xm_$(date +\%Y-\%m-\%d-\%H\%M).log 2>&1
*/5 * * * * /usr/bin/python3 /home/lighthouse/tennis_helper/watcher_for_isz.py --item_name "深云文体" --sales_id "105057" --sales_item_id "105127" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/sy_$(date +\%Y-\%m-\%d-\%H\%M).log 2>&1
*/5 * * * * /usr/bin/python3 /home/lighthouse/tennis_helper/watcher_for_isz.py --item_name "黄木岗" --sales_id "101333" --sales_item_id "100344" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/hmg_$(date +\%Y-\%m-\%d-\%H\%M).log 2>&1
*/5 * * * * /usr/bin/python3 /home/lighthouse/tennis_helper/watcher_for_isz.py --item_name "深圳湾" --sales_id "104331" --sales_item_id "103715" --watch_days 1 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/szw_$(date +\%Y-\%m-\%d-\%H\%M).log 2>&1
*/5 * * * * /usr/bin/python3 /home/lighthouse/tennis_helper/watcher_for_isz.py --item_name "莲花体育" --sales_id "101335" --sales_item_id "100347" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/lh_$(date +\%Y-\%m-\%d-\%H\%M).log 2>&1
*/5 * * * * /usr/bin/python3 /home/lighthouse/tennis_helper/watcher_for_isz.py --item_name "简上" --sales_id "103909" --sales_item_id "102913" --watch_days 3 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/js_$(date +\%Y-\%m-\%d-\%H\%M).log 2>&1
*/5 * * * * /usr/bin/python3 /home/lighthouse/tennis_helper/watcher_for_isz.py --item_name "华侨城" --sales_id "105143" --sales_item_id "105347" --watch_days 3 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/hqc_$(date +\%Y-\%m-\%d-\%H\%M).log 2>&1
*/5 * * * * /usr/bin/python3 /home/lighthouse/tennis_helper/watcher_for_isz.py --item_name "福田中心" --sales_id "100720" --sales_item_id "100006" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/hqc_$(date +\%Y-\%m-\%d-\%H\%M).log 2>&1
*/5 * * * * /usr/bin/python3 /home/lighthouse/tennis_helper/watcher_for_isz.py --item_name "黄冈公园" --sales_id "100241" --sales_item_id "100003" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/hqc_$(date +\%Y-\%m-\%d-\%H\%M).log 2>&1


# delete old logs everyday
0 1 * * * find /home/lighthouse/tennis_helper/logs -name "*.log" -type f -mtime +3 -delete

# reset count for sms
0 1 * * *  /usr/bin/python3 /home/lighthouse/tennis_helper/reset_count_for_sms.py >> /home/lighthouse/tennis_helper/logs/reset_count_for_sms_$(date +\%Y-\%m-\%d).log 2>&1
