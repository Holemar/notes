#!/usr/bin/env bash

cd ~/notes/notes_web
server="notes"

export PYTHONDONTWRITEBYTECODE=x  # 不生成 pyc 文件
export PORT=8080  # 设置端口号

filename="$server".py
if [ ! -f "$filename" ]; then filename="$filename"c;fi

echo "清理旧程序"
ps aux | grep "$server" | grep -v -w grep | awk '{print $2}' | xargs kill -9

echo "启动 web 程序"
nohup python3 "$filename" > /dev/null 2>&1 &

echo "查看程序启动情况"
ps aux | grep "$server"

echo "ps aux | grep $server"
