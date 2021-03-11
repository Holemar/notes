
# 打印时间
    import time,datetime
    print(time.strftime('%Y-%m-%d %H:%M:%S')) # time.strftime(format[, tuple]) 将指定的struct_time(默认为当前时间),根据指定的格式化字符串输出,打印如: 2011-04-13 18:30:10
    print(time.strftime('%Y-%m-%d %A %X', time.localtime(time.time()))) # 显示当前日期； 打印如: 2011-04-13 Wednesday 18:30:10
    print(time.strftime("%Y-%m-%d %A %X", time.localtime())) # 显示当前日期； 打印如: 2011-04-13 Wednesday 18:30:10
    print(time.time()) # 以浮点数形式返回自Linux新世纪以来经过的秒数； 打印如: 1302687844.7；  使用 time.localtime(time.time()) 可返转回 time 类型
    print(time.ctime(1150269086.6630149)) #time.ctime([seconds]) 把秒数转换成日期格式的字符串，如果不带参数，则显示当前的时间。打印如: Wed Apr 13 21:13:11 2011
    print(time.gmtime(1150269086.6630149)) # time.gmtime([seconds]) 将一个时间戳转换成一个UTC时区(0时区)的struct_time，如果seconds参数未输入，则以当前时间为转换标准
    print(time.gmtime()) # 打印如： time.struct_time(tm_year=2014, tm_mon=8, tm_mday=27, tm_hour=7, tm_min=28, tm_sec=19, tm_wday=2, tm_yday=239, tm_isdst=0)
    print(time.localtime(1150269086.6630149)) # time.localtime([seconds]) 将一个时间戳转换成一个当前时区的struct_time，如果seconds参数未输入，则以当前时间为转换标准
    print(time.mktime(time.localtime())) # time.mktime(tuple) 将一个以struct_time转换为时间戳(float类型),打印如：1409124869.0

    # 获取当前时间的具体值(年、月、日、时、分、秒)
    print(time.localtime()) # 打印如: time.struct_time(tm_year=2014, tm_mon=8, tm_mday=27, tm_hour=15, tm_min=10, tm_sec=16, tm_wday=2, tm_yday=239, tm_isdst=0)
    print(time.localtime()[:]) # 打印如: (2014, 8, 27, 15, 10, 16, 2, 239, 0)
    # 取上一月月份
    print(time.localtime()[1]-1) # 打印如: 7
    # 取两个月后的月份
    print(time.localtime()[1]+2) # 打印如: 10
    # 取去年年份
    print(time.localtime()[0]-1) # 打印如: 2013


# 时间暂停两秒
    import time
    time.sleep(2)


# 获取今天、昨天、前几或者后几小时(datetime实现)
    import datetime
    # 得到今天的日期
    print(datetime.date.today()) # 打印如: 2011-04-13
    print(datetime.datetime.now().date())
    print(datetime.datetime.today().date()) # 这3句返回的类型都是 <type 'datetime.date'>
    # 得到前一天的日期
    print(datetime.date.today() + datetime.timedelta(days=-1)) # 打印如: 2011-04-12
    print(datetime.date.today() - datetime.timedelta(days=1))  # 打印如: 2011-04-12
    # 得到10天后的时间
    print(datetime.date.today() + datetime.timedelta(days=10)) # 打印如: 2011-04-23
    # 得到10小时后的时间，上面的 days 换成 hours
    print(datetime.datetime.now() + datetime.timedelta(hours=10)) # 打印如: 2011-04-14 04:30:10.189000
    # 获取明天凌晨 1 点的时间
    d1 = datetime.datetime(*time.localtime()[:3]) + datetime.timedelta(days=1) + datetime.timedelta(hours=1) # 打印如: 2011-04-13 01:00:00
    print(time.mktime( d1.timetuple() )) # 获取时间戳打印如： 1409127119.0


    # 根据年月日，获取 time,datetime
    print(datetime.date(2016, 2, 29)) # 获取 datetime.date 类型，打印：2016-02-29
    print(datetime.datetime(2004, 12, 31)) # 获取 datetime.datetime 类型，打印：2004-12-31 00:00:00
    print(datetime.datetime(2004, 12, 31, 15, 31, 8)) # 获取 datetime.datetime 类型，打印：2004-12-31 15:31:08


# 获取今天、昨天、前几或者后几小时(time实现)
    import time
    # 取一天后的当前具体时间
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()+24*60*60)))
    # 取20天后的当前具体时间
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()+20*24*60*60)))
    # 取20天后当前具体时间的前2小时
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()+20*24*60*60-2*60*60)))


#两日期相减(也可以大于、小于来比较):
    import datetime
    # 指定具体时间的参数： datetime.datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])
    d1 = datetime.datetime(2005, 2, 16)
    d2 = datetime.datetime(2004, 12, 31)
    print((d1 - d2).days) # 打印： 47


#运行时间：
    import time,datetime
    starttime = datetime.datetime.now()
    time.sleep(1) # 暂停1秒
    endtime = datetime.datetime.now()
    print((endtime - starttime).seconds) # 秒, 打印： 1
    print((endtime - starttime).microseconds) # 微秒(百万分之一秒)； 打印： 14000

# 精确计算函数的运行时间
    import time
    start = time.clock()
    func(*args, **kwargs) # 运行函数
    end =time.clock()
    print( 'used:' + str(end) ) # 耗时单位:秒

# 精确计算函数的运行时间2(实测发现 time.clock() 计算不严谨,前面用没用过很难确定)
    import time
    start = time.time()
    func(*args, **kwargs) # 运行函数
    end =time.time()
    print( 'used:' + str(end - start) ) # 耗时单位:秒

# time.clock() 用法
    clock() -> floating point number
    该函数有两个功能，
    在第一次调用的时候，返回的是程序运行的实际时间；
    以第二次之后的调用，返回的是自第一次调用后,到这次调用的时间间隔

    import time
    time.sleep(1)
    print "clock1:%s" % time.clock() # 打印如: clock1:2.17698990094e-06
    time.sleep(1)
    print "clock2:%s" % time.clock() # 打印如: clock2:1.00699529055
    time.sleep(1)
    print "clock3:%s" % time.clock() # 打印如: clock3:2.00698720459



# 字符串 转成 时间 time
    import time
    s2='2012-02-16';
    a=time.strptime(s2,'%Y-%m-%d')
    print a # time.struct_time(tm_year=2012, tm_mon=2, tm_mday=16, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=47, tm_isdst=-1)
    print type(a) # <type 'time.struct_time'>
    print repr(a) # time.struct_time(tm_year=2012, tm_mon=2, tm_mday=16, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=47, tm_isdst=-1)

# 字符串 转成 时间 datetime
    import datetime
    date_str = "2008-11-10 17:53:59"
    dt_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    print dt_obj # 2008-11-10 17:53:59
    print dt_obj.strftime('%Y-%m-%d %H:%M:%S') # 2008-11-10 17:53:59
    print type(dt_obj) # <type 'datetime.datetime'>
    print repr(dt_obj) # datetime.datetime(2008, 11, 10, 17, 53, 59)

# timestamp to time tuple in UTC
    import time
    timestamp = 1226527167.595983
    time_tuple = time.gmtime(timestamp)
    print repr(time_tuple) # time.struct_time(tm_year=2008, tm_mon=11, tm_mday=12, tm_hour=21, tm_min=59, tm_sec=27, tm_wday=2, tm_yday=317, tm_isdst=0)
    print time.strftime('%Y-%m-%d %H:%M:%S', time_tuple) # 2008-11-12 21:59:27

# timestamp to time tuple in local time (返转 time.time() 生成的时间戳)
    import time
    timestamp = 1226527167.595983
    time_tuple = time.localtime(timestamp)
    print repr(time_tuple) # time.struct_time(tm_year=2008, tm_mon=11, tm_mday=13, tm_hour=5, tm_min=59, tm_sec=27, tm_wday=3, tm_yday=318, tm_isdst=0)
    print time.strftime('%Y-%m-%d %H:%M:%S', time_tuple) # 2008-11-13 05:59:27

# datetime 转成 time
    import time, datetime
    # datetime 的 timetuple 函数可直接转成 time.struct_time
    print(datetime.datetime.now().timetuple())
    # 上行打印如：time.struct_time(tm_year=2014, tm_mon=8, tm_mday=27, tm_hour=16, tm_min=7, tm_sec=37, tm_wday=2, tm_yday=239, tm_isdst=-1)
    print(time.localtime())
    # 上行打印如：time.struct_time(tm_year=2014, tm_mon=8, tm_mday=27, tm_hour=16, tm_min=7, tm_sec=37, tm_wday=2, tm_yday=239, tm_isdst=0)

# datetime 转成 date
    import datetime
    # 比较简单，直接使用datetime_object.date()即可
    a = datetime.datetime(2015, 6, 5, 11, 45, 45, 393548)
    b = a.date() # datetime.date(2016, 6, 5)
    print(b) # 打印: 2015-06-05
    print(type(b)) # 打印: <type 'datetime.date'>

# date 转成 datetime
    import datetime
    n_date = datetime.date(2015, 9, 8)
    b = datetime.datetime.combine(n_date, datetime.datetime.min.time()) # datetime.datetime(2015, 9, 8, 0, 0)
    print(b) # 打印: 2015-09-08 00:00:00
    print(type(b)) # 打印: <type 'datetime.datetime'>


# 获取时间戳
    import time, datetime
    print(time.time()) # 打印如： 1409127119.16
    print(long(time.time())) # 打印如： 1409127119
    print(time.mktime( datetime.datetime.now().timetuple() )) # 打印如： 1409127119.0
    print(long(time.mktime(time.strptime('2014-03-25 19:25:33', '%Y-%m-%d %H:%M:%S')))) # 打印如：1395746733



日期格式化符号:
%%: %号本身
%A: 本地星期(全称),如:Tuesday   %a: 本地星期(简称),如:Tue
%B: 本地月份(全称),如:February  %b: 本地月份(简称),如:Feb
                                %c: 本地相应的日期表示和时间表示,如:02/15/11 16:50:57
                                %d: 月内中的一天(0-31),如:15
                                %f: 微秒数值(仅 datetime 类型有, time 类型用会报错)
%H: 24进制小时数(0-23)
%I: 12进制小时数(01-12)
                                %j: 年内的一天(001-366),如:046
%M: 分钟(00-59),如:50           %m: 月份(01-12),如:02
                                %p: 上下午(本地A.M.或P.M.的等价符),如:PM
%S: 秒钟(00-59),如:57
%X: 本地的时间,如:16:50:57      %x: 本地的日期,如:02/15/11
%Y: 四位的年(000-9999)          %y: 两位数的年份表示(00-99)

%U: 年里的星期数(00-53)从星期天开始,如:07
%W: 年里的星期数(00-53)从星期一开始,如:07
%w: 星期(0-6),星期天为星期的开始,如:2 (星期天为0)
%Z: 当前时区的名称,如:中国标准时间
%z: 当前时区的名称,如:中国标准时间

