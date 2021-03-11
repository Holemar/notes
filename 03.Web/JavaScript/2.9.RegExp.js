﻿
RegExp 正则表达式：

一、产生正则表达式的方式
    1. var re = new RegExp("pattern",["flags"]); // 这种方式比较好
       pattern :正则表达式字符串 // 注意这是字符串,里面的反斜杠("\")需要连写两个来表示一个,因为会转义,如 new RegExp("\\d") 匹配一个数字
       flags: // flags 可以多个一起使用, 如 new RegExp("\\w", 'gm')
            g global (全文查找出现的所有 pattern)
            i ignoreCase (忽略大小写)
            m multiLine (多行查找)

    2. 使用 正斜杠("/") 括起来
       var re = /pattern/flags
       pattern 和 flags 的含义跟 new RegExp 的一样。
       只不过,这里的 pattern 不是字符串,不会转义,所以里面的反斜杠("\")不需要连写两个。如 /\d/ 表示匹配一个数字
       这两种方式产生的正则表达式都是一样的，如 new RegExp("(f+)d+(s+)") 也可以写成： /(f+)d+(s+)/

    正则表达式的常用函数：
       re.exec(字符串); // 返回匹配数组(下标0是整个匹配到的字符串,下标1是第1个捕获组,下标2是第2个捕获组...),没有匹配时返回 null
       re.test(字符串); // 返回 true, 或者 false,表示是否匹配
    另外,字符串也有可运用正则表达式的：
       字符串.replace(正则表达式, 要替换的字符串); // 要替换的字符串里面,也可以使用 $1, $2 作为捕获组
       字符串.match(正则表达式); // 同 re.exec,返回匹配数组,无法匹配则返回null,[0]是匹配的整个字符串,[1]是匹配的第一个捕获组,[2]是第二个捕获组...

    RegExp 的属性
        $1, ..., $9  捕获组,$1是匹配的第一个捕获组(即第一个用小括号括起来的内容),$2是第二个捕获组... 如：
            if ( new RegExp("(f+)d+(s+)").test("ddfffdddsss") ) {
               alert(RegExp.$1 + ", " + RegExp.$2); // 提示出： fff, sss
            }
        $_, input  返回输入的内容
            如: /^1((3\d)|(5[036789])|(8[89]))\d{8}$/.exec("13595044124"); alert(RegExp.$_); alert(RegExp.input); // 提示出: 13595044124



二、常用的正则表达式 元字符
    \          转义符
    .          匹配除换行符以外的任意字符
    |          或符号
    \w         匹配字母或数字或下划线 (大写的通常是小写的反义)
    \W         匹配任意不是字母,数字,下划线的字符
    \s         匹配任意的空白符
    \S         匹配任意不是空白符的字符
    \d         匹配数字
    \D         匹配任意非数字的字符
    \b         匹配单词的开始或结束
    \B         匹配不是单词开头或结束的位置
    ^          匹配字符串的开始
    $          匹配字符串的结束
    [^x]       匹配除了x以外的任意字符
    [^aeiou]   匹配除了aeiou这几个字母以外的任意字符
    \数字      表示捕获组,要求与第几个捕获组相同
  常用的限定符
    *          重复零次或多次
    +          重复一次或多次
    ?          重复零次或一次
    {n}        重复n次
    {n,}       重复n次或更多次
    {n,m}      重复n到m次


三、常用正则表达式
    /^[-]?\d+([.]?\d*)$/                  //数字
    /^[-]?\d+$/                           //整数
    /^[0-9a-zA-Z]{5,16}$/                 //用户名(区分大小写，5-16位)
    /^[\u4e00-\u9fa5]+$/                  //中文
    /^(\w){6,20}$/;                       //校验密码：只能输入6-20个字母、数字、下划线
    //电话号码(手機號碼):像(010)88886666，022-22334455，029 1234-5678，010 3523922轉259，3523922。04-36018188/23051418 等
    /^([(（]?0\d{1,6}[）) -]?)?(\d{5,30}|((\d{4}[ -]){1,7}\d{1,4}))([ -#(（轉转]?\d{1,6}[）)]?)?$/;
    /^#?([a-f0-9]{6}|[a-f0-9]{3})$/       //十六进制值
    /^([a-zA-Z\d_\.-]+)@([a-zA-Z\d]+\.)+[a-zA-Z\d]{2,6}$/                     //电子邮箱
    /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/          //URL
    //下句是 IP 地址: 1.0.0.1 到 255.255.255.255,每段不能用“0”打头
    /^([1-9]|([1-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5])))\.(([\d]|([1-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5])))\.){2}([1-9]|([1-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5])))$/
    /^<([a-z]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)$/           //HTML 标签

     "str".replace(/(^\s*)|(\s*$)/g, ""); // 去除前后空格

     //校验登录名：只能输入5-20个以字母开头、可带数字、“_”、“.”的字符串
     function isRegisterUserName(s) {
         var patrn = /^[a-zA-Z]{1}([a-zA-Z0-9]|[._]){4,19}$/;
         return !!(patrn.exec(s));    //返回匹配数组,没有匹配时返回null;所以非两次以返回boolean值
     }
     //防止SQL注入，返回true表示通过验证，返回false表示验证不通过
     function IsValid( oField ) {
         re= /select|update|delete|exec|count|'|"|=|;|>|<|%/i;
         $sMsg = "请您不要在参数中输入特殊字符和SQL关键字！";
         if ( re.test(oField.value) ) {
              alert( $sMsg );
              return false;
         }
         return true;
     }
     // 日期检查
     function strDateTime(str)
     {
        var r = str.match(/^(\d{1,4})(-|\/)?(\d{1,2})\2(\d{1,2})$/); // 注意里面的“\2”，表示要求与第2个捕获组“(-|\/)?”的值相同
        if ( r == null ) return false;
        var d = new Date(r[1], r[3]-1, r[4]);
        return (d.getFullYear()==r[1] && (d.getMonth()+1)==r[3] && d.getDate()==r[4]);
     }
