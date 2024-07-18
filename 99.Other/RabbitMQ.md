
# RabbitMQ

# 安装
Ubuntu 上安装 RabbitMQ
1. `sudo apt update`
2. `sudo apt install rabbitmq-server`

# 其他命令
1. 启动服务：`systemctl start rabbitmq-server` / `service rabbitmq-server start`
2. 停止服务：`systemctl stop rabbitmq-server` / `service rabbitmq-server stop`
3. 重启服务：`systemctl restart rabbitmq-server` / `service rabbitmq-server restart`
4. 查看服务状态：`systemctl status rabbitmq-server` / `service rabbitmq-server status`
5. 开机自启：`systemctl enable rabbitmq-server`
6. 访问RabbitMQ管理界面（可选，重启生效）: `sudo apt install rabbitmq-plugins-management` / `rabbitmq-plugins enable rabbitmq_management`
7. 访问 Web 管理界面：http://localhost:15672   默认登录用户名：guest，密码：guest
8. 列出用户：`rabbitmqctl list_users`
9. 创建用户：`rabbitmqctl add_user username password`
10. 设置管理员权限：`rabbitmqctl set_user_tags username administrator`
11. 设置mq用户的权限，指定允许访问的vhost以及write/read权限：`rabbitmqctl set_permissions -p "/vhost" username ".*" ".*" ".*"`
12. 查看vhost（/）允许哪些用户访问：`rabbitmqctl list_permissions -p /`



