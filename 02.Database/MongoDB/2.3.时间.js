
MongoDB 时间处理

1、$dateFromString (aggregation)
    { $dateFromString: {
         dateString: <dateStringExpression>,    // 要转换的时间字符串
         format: <formatStringExpression>,    // 转换的格式，'%Y-%m-%dT%H:%M:%S.%LZ'
         timezone: <tzExpression>,    // 指定的时区
         onError: <onErrorExpression>,    // 报错时输出
         onNull: <onNullExpression>    // null时输出
    } }

    // 例1
    { $dateFromString: {
        dateString: "2017-02-08T12:10:40.787"
    } }
    // 结果：ISODate("2017-02-08T12:10:40.787Z")

    // 例2(实测不通过，可能与版本有关)
    { $dateFromString: {
        dateString: "15-06-2018",
        format: "%d-%m-%Y"
    } }
    // 结果：ISODate("2018-06-15T00:00:00Z")


2、$dateToString (aggregation)
    { $dateToString: {
        date: <dateExpression>,  // ISODate日期，或者日期字段
        format: <formatString>,  // 转换的格式
        timezone: <tzExpression>, // 指定的时区
        onNull: <expression>  // null时输出
    } }

    // 例: {"date" : ISODate("2014-01-01T08:15:39.736Z")}
    db.sales.aggregate([
        {$project: {
            yearMonthDayUTC: { $dateToString: { format: "%Y-%m-%d", date: "$date" } },
            timewithOffsetNY: { $dateToString: { format: "%H:%M:%S:%L%z", date: "$date", timezone: "America/New_York"} },
            timewithOffset430: { $dateToString: { format: "%H:%M:%S:%L%z", date: "$date", timezone: "+04:30" } },
            minutesOffsetNY: { $dateToString: { format: "%Z", date: "$date", timezone: "America/New_York" } },
            minutesOffset430: { $dateToString: { format: "%Z", date: "$date", timezone: "+04:30" } }
        }}
    ])
    /* 结果：
    {
       "_id" : 1,
       "yearMonthDayUTC" : "2014-01-01",
       "timewithOffsetNY" : "03:15:39:736-0500",
       "timewithOffset430" : "12:45:39:736+0430",
       "minutesOffsetNY" : "-300",
       "minutesOffset430" : "270"
    } */


3、toDate (aggregation)
    {
       $toDate: <expression>
    }

    // 例：
    语句：{$toDate: 120000000000.5}
    结果：ISODate("1973-10-20T21:20:00Z")

    语句：{$toDate:  "2018-03-03"}
    结果：ISODate("2018-03-03T00:00:00Z")


4、其它获取时间的函数
	$year, $month, $dayOfMonth, $hour, $minute, $second, $dayOfYear, $dayOfWeek
	其中 $dayOfMonth: 1-31, $dayOfYear: 1-365, $dayOfWeek: 1-7


日期格式化符号:
    %d = 01-31        // 月内中的一天(1-31)
    %G = 0000-9999    // 当前星期所在的年份(0000-9999)。如 %Y 的"2019-12-31", %G 显示的是"2020-12-31"
    %H = 00-23        // 24进制小时数(0-23)
    %L = 000-999      // 毫秒数(000-999)
    %m = 01-12        // 月份(01-12)
    %M = 00-59        // 分钟(00-59)
    %S = 00-60        // 秒钟(00-59)
    %u = 1-7          // 星期(1-7),星期天是7
    %V = 1-53         // 年里的星期数(1-53),星期一为星期的开始。如"2019-12-29"显示为52, "2019-12-31"显示为1
    %Y = 0000-9999    // 当天所在的年(000-9999)
    %z = +/-[hh][mm]  // 当前时区,在中国显示为: +0800
    %Z = +/-mmm       // 当前时区,在中国显示为: 480
    %% = %            // %号本身


