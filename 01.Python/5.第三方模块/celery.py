

启动 Celery Worker ，通过delay() 或 apply_async() 将任务发布到broker 
(delay 方法封装了 apply_async, apply_async支持更多的参数 )



apply_async 指定时间的参数如下：
    * countdown：延迟多少秒后执行任务，不指定则默认立即执行
    * eta (estimated time of arrival)：指定任务被调度的具体时间，参数类型是 datetime
    当这两个参数同时存在时， countdown 优先。

celery 指定时间执行 / 延期特定时间执行
    task_name.apply_async(args=None, kwargs=None, eta=None)
    task_name.apply_async(args=(2, 3), countdown=5) # 5 秒后执行任务

    # 当前 UTC 时间再加 10 秒后执行任务
    from datetime import datetime, timedelta
    task1.multiply.apply_async(args=[3, 7], eta=datetime.utcnow() + timedelta(seconds=10))


常用配置
    # -*- coding:utf-8 -*-
    from datetime import timedelta
    from settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB_NUM

    # 某个程序中出现的队列，在broker中不存在，则立刻创建它
    CELERY_CREATE_MISSING_QUEUES = True

    CELERY_IMPORTS = ("async_task.tasks", "async_task.notify")

    # 使用redis 作为任务队列
    BROKER_URL = 'redis://:' + REDIS_PASSWORD + '@' + REDIS_HOST + ':' + str(REDIS_PORT) + '/' + str(REDIS_DB_NUM)

    #CELERY_RESULT_BACKEND = 'redis://:' + REDIS_PASSWORD + '@' + REDIS_HOST + ':' + str(REDIS_PORT) + '/10'

    CELERYD_CONCURRENCY = 20  # 并发worker数

    CELERY_TIMEZONE = 'Asia/Shanghai'

    CELERYD_FORCE_EXECV = True    # 非常重要,有些情况下可以防止死锁

    CELERYD_PREFETCH_MULTIPLIER = 1

    CELERYD_MAX_TASKS_PER_CHILD = 100    # 每个worker最多执行万100个任务就会被销毁，可防止内存泄露
    # CELERYD_TASK_TIME_LIMIT = 60    # 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死 
    # BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 90}
    # 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
    CELERY_DISABLE_RATE_LIMITS = True   

    # 定时任务
    CELERYBEAT_SCHEDULE = {
        'msg_notify': {
            'task': 'async_task.notify.msg_notify',
            'schedule': timedelta(seconds=10),
            #'args': (redis_db),
            'options' : {'queue':'my_period_task'}
        },
        'report_result': {
            'task': 'async_task.tasks.report_result',
            'schedule': timedelta(seconds=10),
          #'args': (redis_db),
            'options' : {'queue':'my_period_task'}
        },
        #'report_retry': {
        #    'task': 'async_task.tasks.report_retry',
        #    'schedule': timedelta(seconds=60),
        #    'options' : {'queue':'my_period_task'}
        #},
    }


启动worker的命令
    # *** 定时器 ***
    nohup celery beat -s /var/log/boas/celerybeat-schedule  --logfile=/var/log/boas/celerybeat.log  -l info &
    # *** worker ***
    nohup celery worker -f /var/log/boas/boas_celery.log -l INFO &


超时机制
    celery是自带超时机制的，主要分两种：

    软超时(soft_time_limit)

        @celery.task(soft_time_limit=360)
        def soft_time_out_try(args,url_array):
            pass

        在这种情况下，就算超时了，也是平滑过渡不会报错，推荐优先考虑。
        但是这种情况有个问题，在该机制下，如果函数中含有容易超时的第三方模块，是可能存在软超时以后，任务继续卡住的情况的。
        笔者在测试时使用的是celery v3，在升级v4后暂时没遇到这种情况。

    硬超时(time_limit)

        @celery.task(time_limit=40)
        def hard_time_out_try(args,url_array):
            pass

        在此情况下，超时阻断效果很给力，基本不会出现卡住的情况下。
        但是这种模式会直接抛出异常，不是特别友好。

    另外，在 chord 和 group 之类等聚合链路模式下，如果单个链路超时，会直接导致整体聚合失败，不会得到最终结果，也调用不了callback，比如下面的chord_return_value函数：

        results = chord( (hard_time_out_try_single.s(path, PASSWORD_DIC, host, port) for port in service_ports for path in plugin_www_paths ), chord_return_value.s(sys._getframe().f_code.co_name , url) )().get()


celery实践建议

1.用好celery beat
    如果你想更好的管理项目的定时任务，可以用celery beat代替crontab管理。
    celery不仅支持动态的异步任务(通过delay调用)，也支持定时任务执行。
    当然我们可以用crontab实现任务的定时执行，但是crontab是与项目代码隔离的，为了更方便地管理定时任务用celery beat代替也是一个不错的选择。
    celery beat是celery额外起的一个进程，具体命令行：

        celery -A yourApp beat

    该进程开启后会根据配置定期的发送任务到broker中，最终任务的执行还是由worker执行

2.参数传递
    大多数场景下传递任意数据时可行的，但是如果数据内容本身是可变的，那么这时候就要仔细考虑了。
    假定参数是一个对象，这个对象映射到数据库中的一行数据，如果任务在等待执行的过程中该行数据有改变，那么在任务执行的时候，使用到的这个对象就是一个过期数据。
    所以尽量传递不变(这里的不变与python不可变数据类型不是一个概念)的参数。

3.序列化方式
    celery支持多种序列化方式，但是每种序列化方式产生的数据大小是不同的，如果在broker吞吐量存在瓶颈的情况下，可以选择产生数据较小的序列化方式

4.使用计划任务
    假定有这样一个场景，用户创建了订单，减少了商品库存，但是还未支付，这时候需要给用户一个限定的支付时间如半个小时，如果半个小时之后这笔订单还未支付，那么就撤销该订单，重置商品库存。这个时候可以用到celery的计划任务，也就是任务发出后并不会马上执行，会在指定的时间点执行。
    我们可以用countdown或者eta参数实现该功能：

        task.apply_async(countdown=300)
        task.apply_async(eta=datetime.now() + timedelta(minutes=30) - timedelta(hours=8))

    eta给到的时间有时区的问题，所以我在上述代码中减去了八个小时。

5.任务优先级
    如果执行的任务相同，但是这些相同的任务会有不同的优先级，如果想使某个任务具有更高的优先级，那么可以使用priority参数来完成。

        task.apply_async(priority=9)

    这里会存在一个问题。redis broker的priority只支持0、3、6、9四个级别，底层的实现方式是用不同的队列来实现的。
    大致的做法是为每个优先的任务生成一个队列，更高优先级的任务投递到更高优先级的队列，worker工作的时候更倾向于从高优先级队列获取任务。

6.broker的选择
    不要使用mysql作为broker。虽然celery支持mysql作为broker，但我们还是不要用mysql，因为如果任务量一旦上来，mysql会存在大量的磁盘io，不利于任务系统良好的运行。
    rabbitmq是官方推荐的broker，也是完全实现了amqp协议的broker。
    相比较而言，redis更轻量级，但也是一个较好的选择。

7.worker命名
    给celery worker指定一个唯一的名字，可以让我们更好的区分不同的worker。
    可以用-n参数指定name

8.为不同的队列开启不同的worker
    我们尽量给不同的任务指定不同的队列，有的任务具有更高的优先级，有的反而没那么重要，所以分开来是有必要的。
    在开启的worker的时候指定队列，执行一组相同的任务。

9.选择合适的并发方式
    celery提供了几种并发方式，包括prefork、gevent、eventlet等
    如果执行的任务是cpu密集型的可以选择prefork的方式，如果是网络io密集型的可以选择gevent或者eventlet，这两者都用到了io多路复用的技术。
    选择恰当的并发方式可能可以极大的提升处理能力。
    并发数的选择也需要考虑一下，并不是越多越好，多了需要处理大量的上下文切换，少了不能明显提高性能，这里可能需要一个测试。

10.执行的幂等性
    对于broker而言，任务重复下发是存在的，虽然这种可能性微乎其微。
    所以对于同一个任务，即使多次执行，不会也不应该产生数据异常。这需要在代码层面实现。

11.小心使用retry
    在我工作初期，因为不当地使用retry，导致任务指数级的增长，最终整个broker塞满了消息。大致是因为任务失败后同时retry了两次，并且下一次执行还是失败，继续两次retry(此时总的是4次retry)，如此指数增长。
    retry是在任务异常时重试，可以指定延迟执行以及重试次数。其实也相当于重新抛出一个异步任务，同样地会写入任务队列。

12.给任务设置timeout
    如果不给单个任务设置超时时间，一旦某个任务卡死(比如产生死锁)，整个worker将一直不可用，除非重启。
    可以使用--time-limit参数指定超时时间。

13.接入sentry
    接入sentry可以让我们快速定位错误，解决问题。

14.backend设置
    celery的backend是指任务执行结果的存储服务，一般用redis作为backend即可。
    执行task.apply_async()方法后生成一个result对象，调用result.get()可以从backend中读取结果。
    当然如果对执行的结果不关心可以配置celery为ignore result，此时不会存储结果。
    如果需要存储结果，也需要给结果设置一定的超时时间。

15.flower监控
    flower是celery的一个可视化监控工具。
    我们可以从上面看到如worker工作情况、队列长度等信息，也可以执行远程控制等操作。
    出现问题时，celery监控系统可能会帮助使用者更快的定位问题。






