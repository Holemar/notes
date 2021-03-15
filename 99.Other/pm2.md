
# 安装 pm2 的过程

1. 先下载安装 node.js ，找官方下载包安装即可。  
    <https://nodejs.org/en/download/>

2. 装完之后有了 npm 命令  
    这时候可以使用命令直接安装 pm2:  
    `npm install pm2 -g`

3. 我本机安装 pm2 失败，使用 sudo 再执行安装依然失败  
    网上说先清缓存：  
    `npm cache clean --force`

4. 执行清缓存后再安装，依然失败  
    网上有说，可能是下载失败导致问题，要重试。但我翻墙重试很多次都失败了。  
    见到网上有使用淘宝镜像地址的做法，试了一下依然失败：  
    `npm config set registry "https://registry.npm.taobao.org"`

5. 安装 cnpm 镜像  
    `npm install -g cnpm --registry=https://registry.npm.taobao.org`  
    我这里创建目录导致失败，所以加上 `sudo` 之后正常安装

6. 使用 cnpm 安装  
    `cnpm install -g pm2`  
    再次文件权限导致失败，加上 `sudo` 之后正常。


使用说明官方文档：  
    <https://pm2.keymetrics.io/docs/usage/pm2-doc-single-page/>


- ## 安装
    ```shell script
    npm install pm2 -g # 安装pm2
    pm2 update # 更新pm2
    pm2 uninstall pm2 # 移除pm2
    ```

- ## 开启
    ```shell script
    pm2 start server.js # 启动server.js进程
    pm2 start server.js -i 4 # cluster mode 启动4个server.js进程(4个应用程序会自动进行负载均衡)
    pm2 start server.js --name="api" # 启动应用程序并命名为 "api"
    pm2 start server.js --watch # 当文件变化时自动重启应用
    pm2 start script.sh # 启动 bash 脚本
    pm2 start ecosystem.config.js --only worker-app # Start only the app named worker-app
    ```

    ```text
    启动参数说明:
    --watch: 监听应用目录的变化，一旦发生变化，自动重启。如果要精确监听、不同的目录，最好通过配置文件。
    -i --instances: 启用多少个实例，可用于负载均衡。如果配置 0 或者 max，则根据当前机器核数确定实例数目。配置 -1 表示当前机器核数 -1。
    --ignore-watch: 排除监听的目录/文件，可以是特定的文件名，也可以是正则。比如--ignore-watch="test node_modules"
    -n --name: 应用的名称。查看应用信息的时候可以用到。
    -o --output <path>: 标准输出日志文件的路径。
    -e --error <path>: 错误输出日志文件的路径。
    --interpreter <interpreter>: 用来执行的程序名称, 如: bash, python...。
    --max-memory-restart <200MB>:  Set memory threshold for app reload
    --log <log_path>: Specify log file
    -- arg1 arg2 arg3: Pass extra arguments to the script
    --restart-delay <delay in ms>: Delay between automatic restarts
    --time: Prefix logs with time
    --no-autorestart: Do not auto restart app
    --cron <cron_pattern>: Specify cron for forced restart
    --no-daemon: Attach to application log
    ```

- ## 重启/关闭
    ```shell script
    pm2 restart all/app_name/ID/server.js # 重启进程
    pm2 restart all --update-env # 重启，且使用新的环境变量
    pm2 reload  all/app_name/ID/server.js # 重启应用
    pm2 stop    all/app_name/ID/server.js # 停止应用程序
    pm2 delete  all/app_name/ID/server.js # 关闭并删除应用

    pm2 scale api 10 # 把名字叫api的应用添加或者删除实例到 10 个
    pm2 scale app +3 # 把名字叫app的应用添加 3 个实例
    pm2 reset [app-name] # 重置重启数量
    ```

- ## 其它
    ```shell script
    pm2 startup # 创建开机自启动命令
    pm2 save # 保存当前应用列表
    pm2 resurrect # 重新加载保存的应用列表
    pm2 update # Save processes, kill PM2 and restore processes
    pm2 updatePM2 # Update in memory pm2
    pm2 generate # Generate a sample json configuration file
    pm2 start app.js --node-args="--max-old-space-size=1024"
    pm2 gracefulReload all # Graceful reload all apps in cluster mode
    pm2 web # 运行健壮的 computer API endpoint (http://localhost:9615)
    pm2 ping # Ensure pm2 daemon has been launched
    pm2 sendSignal SIGUSR2 my-app # Send system signal to script
    ```

- ## 配置启动信息
- 创建 ecosystem.config.js，内容如下
    ```shell script
    # 全局环境变量
    const sharedEnv = {
        "REDIS_HOST":"127.0.0.1",
        "REDIS_PASSWORD":"12345678",
        "BROKER_MODE":"redis",
        "BROKER_HEALTH_CHECK":"redis",
    };
    module.exports = {
      "apps" : [{
        name: 'worker',  # App name, 应用名称
        cwd: 'main.py',  # 可配置 "./" 表示当前工作路径
        interpreter: 'python3.6',
        args: '-m worker -Q fetch_uids_queue,belloai_inbox_sync --logfile ../logs/worker.log',
        instances: 3, # 启用多少个实例
        autorestart: false,
        watch: false,
        max_memory_restart: '1G',
        error_file: "./logs/worker.error.log", # 错误日志路径
        out_file: "./logs/worker.out.log", # 普通日志路径
        env: sharedEnv # 环境参数
      }, {
        "name"        : "fis-receiver",  # 应用名称
        "script"      : "./bin/www",  # 实际启动脚本
        "cwd"         : "./",  # 当前工作路径
        "watch": ["bin", "routers"],  # 监控变化的目录，一旦变化，自动重启
        "ignore_watch" : ["node_modules", "logs", "public"], # 从监控目录中排除
        "watch_options": {
          "followSymlinks": false
        },
        "error_file" : "./logs/app-err.log",
        "out_file" : "./logs/app-out.log",
        "instances" : "max",   # 启用多少个实例，可用于负载均衡。如果配置 0 或者 max，则根据当前机器核数确定实例数目。配置 -1 表示当前机器核数 -1。
        "exec_mode" : "cluster" #  可选：fork(服务器单核推荐) cluster(多核推荐)
        "env": sharedEnv # 环境参数
      }]
    };

    pm2 start ecosystem.config.js
    pm2 [start|restart|stop|delete] ecosystem.config.js
    ```
    注: 配置文件的 `instances` 数量修改，`restart/reload` 重启不会生效，需要先 `pm2 delete` 再 `pm2 start` 才生效。

    Field | Example | Description
    --- | --- | ---
    name | “my-api” | application name (default to script filename without extension)
    script | ”./api/app.js” | script path relative to pm2 start
    cwd | “/var/www/” | the directory from which your app will be launched
    args | “-a 13 -b 12” | string containing all arguments passed via CLI to script
    interpreter | “/usr/bin/python” | interpreter absolute path (default to node)
    interpreter_args | ”–harmony” | option to pass to the interpreter
    node_args |  | alias to interpreter_args

    在应用中，可以启动命令读取不同的环境变量。
    ```json
    {
        "env": { "NODE_ENV": "production", "REMOTE_ADDR": "http://www.example.com/" },
        "env_dev": { "NODE_ENV": "development", "REMOTE_ADDR": "http://wdev.example.com/" },
        "env_test": { "NODE_ENV": "test", "REMOTE_ADDR": "http://wtest.example.com/" }
    }
    ```
    启动指明环境变量:
    `pm2 start app.js --env dev`

- ## 查看进程
    ```shell script
    pm2 [list|ls|status] # 列表 PM2 启动的所有的应用程序
    pm2 show 0 # 查看执行编号为0的进程
    pm2 show [app-name] # 显示应用程序的所有信息
    pm2 jlist  # 用 JSON 形式打印程序信息
    pm2 prettylist  # 以人容易阅读的 JSON 形式打印程序信息
    pm2 describe 0 # Display all informations about a specific process
    ```

- ## 实时监控
    ```shell script
    pm2 monit # 显示每个应用程序的CPU和内存占用情况
    pm2 monit 0 # 监控批评行ID为0的进程
    pm2 monit server.js # 监控名称为server.js的进程
    ```

- ## 日志
    ```shell script
    pm2 logs # 显示所有日志
    pm2 logs 0 # 显示执行编号为0的日志(0是id，不是pid)
    pm2 logs [app-name] # 显示指定应用程序的日志
    pm2 logs server.js # 显示名称为 server.js 的进程
    pm2 flush  # Empty all log files[注：我没有试出来效果]
    pm2 reloadLogs # Reload all logs
    ```

