#!/bin/sh

OUT_DIR=/data/db/mongodb_bak/temp # 临时备份目录

TAR_DIR=/data/db/mongodb_bak/bak_list # 备份存放路径

DB_URI="mongodb://admin:belloai@127.0.0.1:57017/?authSource=admin" # 数据库连接字符串

DAYS=15 # DAYS=15代表删除15天前的备份，即只保留最近15天的备份

DATE=`date +%Y_%m_%d` # 获取当前系统时间

TAR_BAK="mongodb_bak_$DATE.tar.gz" # 最终保存的数据库备份文件名


### 下面正式执行 ###

cd $OUT_DIR

rm -rf $OUT_DIR/*

mkdir -p $OUT_DIR/$DATE

mongodump --uri $DB_URI -o $OUT_DIR/$DATE # 备份全部数据库

tar -zcvf $TAR_DIR/$TAR_BAK ./$DATE # 压缩为 .tar.gz 格式

find $TAR_DIR/ -mtime +$DAYS -delete # 删除 $DAYS 天前的备份文件

rm -rf $OUT_DIR/$DATE  # 删除已压缩的内容


### 后续操作 ###

# 1. 加执行权限
# chmod +x /home/crontab/mongod_bak.sh

# 2. 加定时任务, 修改/etc/crontab
# m h dom mon dow user  command
# 23 2    * * 6   root    /data/mongo_bak.sh

# 3. 重新启动crond使设置生效
# sudo service cron restart # 重新载入配置。自从ubutu 16.04 改名 cron, 不再是 crond
# /sbin/service crond reload # 重新载入配置。旧写法，现已没法使用。
# chkconfig --level 35 crond on  #加入开机自动启动:
# /sbin/service crond start   #启动服务
# crontab -l #列出crontab文件
