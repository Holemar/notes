
取得系统时间: Calendar
java.util.Calendar
   Calendar cal = Calendar.getInstance();
   int year = cal.get(Calendar.YEAR);
   int month = cal.get(Calendar.MONTH) + 1; //注：月份从0开始
   int date = cal.get(Calendar.DATE); //取得当前的日期
   int day = cal.get(Calendar.DAY_OF_WEEK); //取得当前是星期几。周日是1，周六是7
   int hour = cal.get(Calendar.HOUR_OF_DAY);
   int min = cal.get(Calendar.MINUTE);
   int sec = cal.get(Calendar.SECOND);
   System.out.println("今天是："+year+"年"+month+"月"+date+"日");
   System.out.println("现在是："+hour+"时"+min+"分"+sec+"秒");


Calendar 的 after、before、equals方法，比较两个时间
   after():  Calendar现在的时刻比参数的Calendar时刻晚，则true；否则false
   before():  Calendar现在的时刻比参数的Calendar时刻早，则true；否则false
   equals():  Calendar现在的时刻跟参数的Calendar时刻相等，则true；否则false
   例： Calendar Date1 = Calendar.getInstance();
        Date1.set(2001,11,10);
    Calendar Date2 = Calendar.getInstance();
        Date2.set(2001,11,11);
    System.out.println(Date1.after(Date2)); //结果false


Calendar 的 Setlenient方法，检查日期是否存在
   当Setlenient方法的参数设置成false时，会进行检查。抛出illegalArgumentException异常


求程序执行时间：
java.util.Date
   long sTime = new Date().getTime(); //当前时间的毫秒数，最小毫秒
   long bs = Calendar.getInstance().getTimeInMillis(); //很精确


获取格式化的时间：
    import java.util.Date;
    import java.text.SimpleDateFormat;
    Date date = new Date();  // 此时date为当前的时间
    System.out.println(date);  // 打印如：Sat May 07 16:34:03 CST 2022
    SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");  // 设置当前时间的格式，为 年-月-日
    System.out.println(dateFormat.format(date));  // 打印如：2022-05-07
    SimpleDateFormat dateFormat_min = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");  // 设置当前时间的格式，为 年/月/日 时:分:秒
    System.out.println(dateFormat_min.format(date));  // 打印如：2022/05/07 16:34:03

