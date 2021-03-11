
限制「CPU」和内存使用量
    # 如果不是想优化程序对内存或 CPU 的使用率，而是想直接将其限制为某个确定的数字，Python 也有一个对应的库可以做到：
    import signal
    import resource

    # To Limit CPU time
    def time_exceeded(signo, frame):
        print("CPU exceeded...")
        raise SystemExit(1)

    def set_max_runtime(seconds):
        # Install the signal handler and set a resource limit
        soft, hard = resource.getrlimit(resource.RLIMIT_CPU)  # 首先获得该特定资源（RLIMIT_CPU）的软限制和硬限制
        resource.setrlimit(resource.RLIMIT_CPU, (seconds, hard))  # 然后使用通过参数指定的秒数和先前检索到的硬限制来进行设置。
        signal.signal(signal.SIGXCPU, time_exceeded)  # 最后，如果 CPU 的运行时间超过了限制，我们将发出系统退出的信号。

    def set_max_memory(size):
        # To limit memory usage
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)  # 检索软限制和硬限制
        resource.setrlimit(resource.RLIMIT_AS, (size, hard))  # 使用带「size」参数的「setrlimit」和先前检索到的硬限制来设置它。


