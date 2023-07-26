# tennis_helper
(深圳网球场守望者) 网球场预定小助手后台代码

## 脚本结构
- logs: 缓存定时任务运行的日志文件夹
- common.py: 通用的函数集合
- config.py: 静态的变量集合
- cron.sh: 定时任务的相关配置命令
- sms.py: 腾讯云短信服务相关的函数
- weda.py: 腾讯云微搭服务相关的函数
- tennis_court_watcher.py: 网球场守望者的主函数
- reset_count_for_sms.py: 每条订阅的今日短信提示次数置零
- refresh_rule_status.py: 更新订阅的状态
- tencent_docs.py: 腾讯文档相关的函数方法
- update_docs.py: 更新在线表格的任务
- proxy_watcher.py: 巡检代理的任务
