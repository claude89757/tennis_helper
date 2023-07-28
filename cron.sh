# some env setting
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ACCESS_TOKEN=""
SIGN_KEY=""
TENCENT_CLOUD_SECRET_ID=""
TENCENT_CLOUD_SECRET_KEY=""
KS_TOKEN=""
WEDA_ACCESS_TOKEN=""
TENCENT_DOCS_SECRET=""
TENCENT_DOCS_REFRESH_TOKEN=""

# delete too old logs everyday
0 1 * * * timeout 1800 find /home/lighthouse/tennis_helper/logs -name "*.log" -type f -mtime +2 -delete /home/lighthouse/tennis_helper/logs/delete_log_$(date +\%Y-\%m-\%d).log 2>&1

# reset count for sms
0 1 * * *  timeout 1800 /usr/bin/python3 /home/lighthouse/tennis_helper/reset_count_for_sms.py >> /home/lighthouse/tennis_helper/logs/reset_count_for_sms_$(date +\%Y-\%m-\%d).log 2>&1

# git pull for github
0 * * * * timeout 1800 /bin/bash /home/lighthouse/tennis_helper/git_pull.sh /home/lighthouse/tennis_helper/logs/git_pull_$(date +\%Y-\%m-\%d).log 2>&1

# refresh rule status
*/3 * * * * timeout 1800 /usr/bin/python3 /home/lighthouse/tennis_helper/refresh_rule_status.py >> /home/lighthouse/tennis_helper/logs/refresh_rule_status_$(date +\%Y-\%m-\%d).log 2>&1

# refresh rule status
*/10 * * * * timeout 1800 /usr/bin/python3 /home/lighthouse/tennis_helper/update_docs_for_rule.py >> /home/lighthouse/tennis_helper/logs/update_docs_for_rule_$(date +\%Y-\%m-\%d).log 2>&1

# inform rules expired
0 10 * * *  timeout 1800 /usr/bin/python3 /home/lighthouse/tennis_helper/inform_rule_expired.py >> /home/lighthouse/tennis_helper/logs/inform_rule_expired_$(date +\%Y-\%m-\%d).log 2>&1

# check https proxy
0 1 * * *  timeout 43200 /usr/bin/python3 /home/lighthouse/tennis_helper/proxy_watcher.py >> /home/lighthouse/tennis_helper/logs/proxy_watch_$(date +\%Y-\%m-\%d).log 2>&1

# update docs for  tennis tools
*/5 * * * *  timeout 1800 /usr/bin/python3 /home/lighthouse/tennis_helper/update_docs.py >> /home/lighthouse/tennis_helper/logs/update_docs_$(date +\%Y-\%m-\%d).log 2>&1


# run tennis tools for isz
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "ISZ" --court_name "大沙河" --sales_id "100220" --sales_item_id "100000" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/dsh_$(date +\%Y-\%m-\%d).log 2>&1
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "ISZ" --court_name "香蜜体育" --sales_id "101332" --sales_item_id "100341" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/xm_$(date +\%Y-\%m-\%d).log 2>&1
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "ISZ" --court_name "深云文体" --sales_id "105057" --sales_item_id "105127" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/sy_$(date +\%Y-\%m-\%d).log 2>&1
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "ISZ" --court_name "黄木岗" --sales_id "101333" --sales_item_id "100344" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/hmg_$(date +\%Y-\%m-\%d).log 2>&1
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "ISZ" --court_name "深圳湾" --sales_id "104331" --sales_item_id "103715" --watch_days 1 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/szw_$(date +\%Y-\%m-\%d).log 2>&1
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "ISZ" --court_name "莲花体育" --sales_id "101335" --sales_item_id "100347" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/lh_$(date +\%Y-\%m-\%d).log 2>&1
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "ISZ" --court_name "简上" --sales_id "103909" --sales_item_id "102913" --watch_days 3 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/js_$(date +\%Y-\%m-\%d).log 2>&1
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "ISZ" --court_name "华侨城" --sales_id "105143" --sales_item_id "105347" --watch_days 3 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/hqc_$(date +\%Y-\%m-\%d).log 2>&1
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "ISZ" --court_name "福田中心" --sales_id "100720" --sales_item_id "100006" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/ftzx_$(date +\%Y-\%m-\%d).log 2>&1
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "ISZ" --court_name "黄冈公园" --sales_id "100241" --sales_item_id "100003" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/hqgy_$(date +\%Y-\%m-\%d).log 2>&1
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "ISZ" --court_name "北站公园" --sales_id "102911" --sales_item_id "101145" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/bzgy_$(date +\%Y-\%m-\%d).log 2>&1
# run tennis tools for zjclub
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "ZJCLUB" --court_name "郑洁俱乐部" --sales_id "102042" --sales_item_id "100586" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/zjclub_$(date +\%Y-\%m-\%d).log 2>&1
# run tennis tools for hjd
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "HJD" --court_name "金地威新" --watch_days 1 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/jdwx_$(date +\%Y-\%m-\%d).log 2>&1
# run tennis tools for tns
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "TNS" --court_name "泰尼斯香蜜" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/tns_$(date +\%Y-\%m-\%d).log 2>&1
# run tennis tools for kswq
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "KS" --court_name "总裁俱乐部" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/ks_$(date +\%Y-\%m-\%d).log 2>&1
# run tennis tools for wcjq
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "WCJT" --court_name "梅林文体" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/mlwt_$(date +\%Y-\%m-\%d).log 2>&1
# run tennis tools for dsty
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "DSTY" --court_name "莲花二村" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/lh2c_$(date +\%Y-\%m-\%d).log 2>&1
# run tennis tools for shanhua
*/4 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher.py --app_name "SHANHUA" --court_name "山花馆" --watch_days 5 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_shanhua_$(date +\%Y-\%m-\%d).log 2>&1


# run tennis tools for isz (vip)
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "ISZ" --court_name "大沙河" --sales_id "100220" --sales_item_id "100000" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_dsh_$(date +\%Y-\%m-\%d).log 2>&1
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "ISZ" --court_name "香蜜体育" --sales_id "101332" --sales_item_id "100341" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_xm_$(date +\%Y-\%m-\%d).log 2>&1
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "ISZ" --court_name "深云文体" --sales_id "105057" --sales_item_id "105127" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_sy_$(date +\%Y-\%m-\%d).log 2>&1
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "ISZ" --court_name "黄木岗" --sales_id "101333" --sales_item_id "100344" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_hmg_$(date +\%Y-\%m-\%d).log 2>&1
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "ISZ" --court_name "深圳湾" --sales_id "104331" --sales_item_id "103715" --watch_days 1 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_szw_$(date +\%Y-\%m-\%d).log 2>&1
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "ISZ" --court_name "莲花体育" --sales_id "101335" --sales_item_id "100347" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_lh_$(date +\%Y-\%m-\%d).log 2>&1
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "ISZ" --court_name "简上" --sales_id "103909" --sales_item_id "102913" --watch_days 3 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_js_$(date +\%Y-\%m-\%d).log 2>&1
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "ISZ" --court_name "华侨城" --sales_id "105143" --sales_item_id "105347" --watch_days 3 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_hqc_$(date +\%Y-\%m-\%d).log 2>&1
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "ISZ" --court_name "福田中心" --sales_id "100720" --sales_item_id "100006" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_ftzx_$(date +\%Y-\%m-\%d).log 2>&1
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "ISZ" --court_name "黄冈公园" --sales_id "100241" --sales_item_id "100003" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_hqgy_$(date +\%Y-\%m-\%d).log 2>&1
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "ISZ" --court_name "北站公园" --sales_id "102911" --sales_item_id "101145" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_bzgy_$(date +\%Y-\%m-\%d).log 2>&1
# run tennis tools for zjclub(vip)
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "ZJCLUB" --court_name "郑洁俱乐部" --sales_id "102042" --sales_item_id "100586" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_zjclub_$(date +\%Y-\%m-\%d).log 2>&1
# run tennis tools for hjd(vip)
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "HJD" --court_name "金地威新" --watch_days 1 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_jdwx_$(date +\%Y-\%m-\%d).log 2>&1
# run tennis tools for tns(vip)
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "TNS" --court_name "泰尼斯香蜜" --watch_days 2 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_tns_$(date +\%Y-\%m-\%d).log 2>&1
# run tennis tools for kswq(vip)
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "KS" --court_name "总裁俱乐部" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_ks_$(date +\%Y-\%m-\%d).log 2>&1
# run tennis tools for wcjq
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "WCJT" --court_name "梅林文体" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_mlwt_$(date +\%Y-\%m-\%d).log 2>&1
# run tennis tools for dsty
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "DSTY" --court_name "莲花二村" --watch_days 7 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_lh2c_$(date +\%Y-\%m-\%d).log 2>&1
# run tennis tools for shanhua
*/2 * * * * timeout 600 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_vip.py --app_name "SHANHUA" --court_name "山花馆" --watch_days 5 --send_sms 1 >> /home/lighthouse/tennis_helper/logs/vip_shanhua_$(date +\%Y-\%m-\%d).log 2>&1
