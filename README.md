## 业务监控项目

此项目作为简单的监控项目，主要分为监控和预警两部分，可自定义监控项和报警模版

###说明：

- 项目定时任务的执行，这里用centos crontab功能实现，每天每隔5分钟执行一次。
  配置可设置为：
    ```
    */5 * * * * {user} {command}
    ```
    写web的话，通过celery的beat实现定时任务。ps: 推荐写web实现

- 修改config.py 文件中的配置项，配置监控项MONITOR_DICT，和报警项ALARM_DICT


### 使用方法：

以下为在centos上使用说明：
  
    # 通过git 将项目clone到/home 下
    cd /home
    git clone http://git.yaobili.com/gitlab/operation/Bussiness-Monitoring.git
    vim /etc/crontab   
    # 修改定时任务配置文件，添加下面内容即可
    */5 * * * * root /usr/bin/python36 /home/Bussiness-Monitoring/monitoring.py check
