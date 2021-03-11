
一.queue队列
    1.python3中的队列模块是 queue, python2中是Queue
    2.一般涉及到同步，多线程之类用到队列模块
    3.定义了 queue.Queue 类，以及继承它的 queue.LifoQueue 类 和 queue.PriorityQueue 类 和 queue.SimpleQueue 类
    4.分别对应队列类（FIFO先进先出），LIFO后进先出队列类，优先队列，无边界FIFO简单队列类
    5.还有两个异常：对满和队空


二.队列queue公共方法
    try:
        from Queue import Queue  # py2 的写法
    except:
        from queue import Queue  # py3 的写法

    # 创建基本队列
    # queue.Queue(maxsize=0)创建一个队列对象（队列容量），若maxsize小于或者等于0，队列大小没有限制
    Q = Queue(10)
    print(Q)  # py2 打印: <Queue.Queue instance at 0x10ace47a0>  py3 打印:<queue.Queue object at 0x1092ad7f0>
    print(type(Q))  # py2 打印: <type 'instance'>  py3 打印:<class 'queue.Queue'>
    print('---')

    # 1.基本方法
    print(Q.queue)  # 查看队列中所有元素， 这里打印: deque([])
    print(Q.qsize())  # 返回队列的大小， 返回 int 类型大于等于 0 的值, 这里打印: 0
    print(Q.empty())  # 判断队空，返回 True/False
    print(Q.full())  # 判断队满，返回 True/False
    print('---')

    # 2.放入队列
    # Queue.put(item，block=True，timeout=None)将对象放入队列，阻塞调用（block=False抛异常），timeout等待时间
    for i in range(5):
        Q.put(i)
    # Queue.put_nowait(item)相当于 put(item, False).


    # 3.读队列
    # Queue.get(block=True, timeout=None)读出队列的一个元素，block阻塞调用，timeout等待时间
    while not Q.empty():
        print(Q.get())  # 打印 0~5, 这里是先进先出
    # Queue.get_nowait()相当于get(False).取数据，如果没数据抛queue.Empty异常
    '''当一个队列为空的时候如果再用 get() 取则会堵塞。
    所以取队列的时候一般是用到 get_nowait()方法，这种方法在向一个空队列取值的时候会抛一个Empty异常。
    所以更常用的方法是先判断一个队列是否为空，如果不为空则取值
    '''


    # 4.另两种涉及等待排队任务的方法
    # Queue.task_done()在完成一项工作后，向任务已经完成的队列发送一个信号
    #   意味着之前入队的一个任务已经完成。由队列的消费者线程调用。每一个get()调用得到一个任务，接下来的task_done()调用告诉队列该任务已经处理完毕。
    # Queue.join()阻止直到队列中的所有项目都被获取并处理。即等到队列为空再执行别的操作


三.队列queue各子类
    try:
        from Queue import Queue, LifoQueue, PriorityQueue  # py2 的写法
    except:
        from queue import Queue, LifoQueue, PriorityQueue  # py3 的写法
    # print(help(Queue))

    # Queue 类实现了一个基本的先进先出(FIFO)容器，使用put()将元素添加到序列尾端，get()从队列尾部移除元素。
    q = Queue()
    for i in range(3):
        q.put(i)

    while not q.empty():
        print(q.get())  # 打印 0~2
    print("---")

    # 与标准FIFO实现Queue不同的是，LifoQueue使用后进先出序（会关联一个栈数据结构）。
    q1 = LifoQueue()
    for i in range(3):
        q1.put(i)
    while not q1.empty():
        print(q1.get())  # 打印 2~0
    print("---")

    # 除了按元素入列顺序外，有时需要根据队列中元素的特性来决定元素的处理顺序。
    # 例如，老板的打印任务可能比研发的打印任务优先级更高。PriorityQueue依据队列中内容的排序顺序(sort order)来决定那个元素将被检索。
    class Job(object):
        def __init__(self, priority, description):
            self.priority = priority
            self.description = description
            print('New job:', description)
            return

        def __lt__(self, other):
            return self.priority < other.priority

    q2 = PriorityQueue()
    q2.put(Job(5, 'Mid-level job'))
    q2.put(Job(10, 'Low-level job'))
    q2.put(Job(1, 'Important job'))  # 数字越小，优先级越高

    while not q2.empty():
        next_job = q2.get()  # 可根据优先级取序列
        print('Processing job', next_job.description)


四.跨进程通信队列
  1. multiprocessing.Process 多进程
    '''
    1.from queue import Queue  # 是进程内非阻塞队列
    这个是普通的队列模式，类似于普通列表，先进先出模式，get方法会阻塞请求，直到有数据get出来为止

    2.from multiprocessing import Queue # 是跨进程通信队列(各子进程共有)
    这个是多进程并发的Queue队列，用于解决多进程间的通信问题。普通Queue实现不了。
    例如跑多进程对一批IP列表进行运算，运算后的结果都存到Queue队列里面，这个就必须使用multiprocessing提供的Queue来实现
    '''

    import time, random
    from multiprocessing import Process, Queue  # py2, py3 写法一样。但换成普通的 queue.Queue 就没法实现跨进程通信了

    def write(q):
        for value in ['a', 'b', 'c']:
            print('put %s to queue...' % value)
            q.put(value)
            # time.sleep(random.random())
            time.sleep(0.1)

    def read(q):
        while True:
            # time.sleep(random.random())
            time.sleep(0.1)
            if not q.empty():
                value = q.get()
                print('Get %s from queue' % value)
            else:
                break

    if __name__ == '__main__':
        q = Queue()  # 换成普通的 queue.Queue 就没法实现跨进程通信了
        pw = Process(target=write, args=(q,))
        pr = Process(target=read, args=(q,))
        pw.start()
        pr.start()
        pw.join()
        pr.join()
        # 使用 random 读取是不确定的，所以有可能未写完，但已经读取完了
        print('all datas have been writen and been read')


  2. multiprocessing.Pool 进程池
    '''
    如果需要多个子进程时可以考虑使用进程池(pool)来管理
    pool创建子进程的方法与Process不同，是通过 p.apply_async(func,args=(args)) 实现，一个池子里能同时运行的任务是取决你电脑的cpu数量。
    如我的电脑现在是有4个cpu，那会子进程task0,task1,task2,task3可以同时启动，task4则在之前的一个某个进程结束后才开始
    '''
    import os, time
    from multiprocessing import Pool

    def long_time_task(name):
        print('Run task %s (%s)...' % (name, os.getpid()))
        start = time.time()
        time.sleep(0.1)
        end = time.time()
        print('Task %s runs %0.2f seconds.' % (name, (end - start)))

    if __name__ == '__main__':
        print('Parent process %s.' % os.getpid())
        p = Pool()  # 如果指定 p=Pool(5) 那么就可以同时执行5个子进程，不指定则默认使用CPU的数量作为同时执行数量
        for i in range(10):
            p.apply_async(long_time_task, args=(i,))

        print('Waiting for all subprocesses done...')
        p.close()  # 关掉进程池子，不再向里面添加进程了。调用 close() 之后就不能继续添加新的 Process 了。
        p.join()  # 等待所有子进程执行完毕，调用 join() 之前必须先调用 close()。

        print('All subprocesses done.')


  3. multiprocessing.Pool 进程池间通信
    '''
    multiprocessing.Queue 队列对象不能在进程池(pool)间通信，如果想要在进程池中使用队列则要使用 multiprocess.Manager 类
    父进程创建 Manager().Queue()，并传给各个子进程。这个队列对象就可以在父进程与子进程间通信，不用池则不需要 Manager
    '''
    import time
    from multiprocessing import Pool, Manager, Queue  # py2, py3 写法一样

    def write(q):
        for value in ['a', 'b', 'c']:
            print('put %s to queue...' % value)
            q.put(value)
            time.sleep(0.1)

    def read(q):
        while True:
            time.sleep(0.1)
            if not q.empty():
                value = q.get()
                print('Get %s from queue' % value)
            else:
                break

    if __name__ == '__main__':
        q = Manager().Queue()  # 父进程创建Queue，并传给各个子进程
        # q = Queue()  # multiprocessing.Queue 队列对象不能在进程池(pool)间通信
        p = Pool()  # 如果指定 p=Pool(5) 那么就可以同时执行5个子进程，不指定则默认使用CPU的数量作为同时执行数量
        pw = p.apply_async(write, args=(q,))
        pr = p.apply_async(read, args=(q,))
        p.close()  # 关掉进程池子，不再向里面添加进程了。调用 close() 之后就不能继续添加新的 Process 了。
        p.join()  # 等待所有子进程执行完毕，调用 join() 之前必须先调用 close()。
        print('all datas have been writen and been read')


  4. multiprocessing.Pool 进程池间加锁
    '''
    关于锁的应用，在不同程序间如果有同时对同一个队列操作的时候，为了避免错误，可以在某个函数操作队列的时候给它加把锁。
    这样在同一个时间内则只能有一个子进程对队列进行操作，锁也要在 manager 对象中的锁
    '''
    import time, random
    from multiprocessing import Manager, Pool

    # 写数据进程执行的代码:
    def write(q, lock):
        lock.acquire()  # 加上锁
        for value in ['A', 'B', 'C']:
            print('put %s to queue...' % value)
            q.put(value)
        lock.release()  # 释放锁
        # 不想自己写 加锁、释放锁 的代码，可用 with
        with lock:
            pass  # 要执行的代码

    # 读数据进程执行的代码:
    def read(q):
        time.sleep(random.random())
        while True:
            if not q.empty():
                value = q.get(False)
                print('Get %s from queue' % value)
            else:
                break

    if __name__ == '__main__':
        manager = Manager()
        q = manager.Queue()  # 父进程创建Queue，并传给各个子进程
        results = manager.dict()  # 可用于多进程传参的 dict, 因为 queue 类似于 list, 有些场景 queue 不够用。
        lock = manager.Lock()  # 初始化一把锁
        p = Pool()
        pw = p.apply_async(write, args=(q, lock))
        pr = p.apply_async(read, args=(q,))
        p.close()
        p.join()
        print('所有数据都写入并且读完')


