
/*
var ga = document.createElement('script');
 ga.type = 'text/javascript';
 ga.async = true;
 ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
 var s = document.getElementsByTagName('script')[0];
 s.parentNode.insertBefore(ga, s);

上面谷歌分析代码就采用了异步调用方式，动态创建了script元素，加快载入时间。这是异步调用js组件的其中一种方法。

《黑客与画家》IT男8年前就该读的励志超浓缩鸡精
*/

/**
 * 创建 c$ 类别, 此类别的所有方法和属性都在它里面
 * 如果名称有冲突，请将此档案的 c$ 都替换成想要的名称。这是此工具类别唯一占用的关键词
 */
c$ = window.c$ = c$ || {};

// 废弃
/**
 * 运行平台判断(是否 windows)
 * @return 如果是 windows 平台则为“true”，其它平台则返回“false”
 * @example if (c$.isWin) alert('这是 window 平台'); // 注意,这个是值,不是函数
 */
c$.isWin = (window.navigator.appVersion.toLowerCase().indexOf("win") != -1);


/**
 * 郵件信箱檢查
 * @param checkStr 需檢查的字串
 * @param name 不符合時，需提示的訊息的名稱，不寫則不提示
 * @param isMust 是否必須填寫，為true則必須寫，為其他則可不寫
 * @return 字串是郵件信箱，傳回true；否則傳回false
 */
c$.isEmail = function ( checkStr, name, isMust )
{
	var minlength = 5;
	var maxlength = 50;
    var repx = /^([a-zA-Z\d_\.-]+)@([a-zA-Z\d]+\.)+[a-zA-Z\d]{2,6}$/;
    return this.isValid( checkStr, name, minlength, maxlength, isMust, repx );
};

/**
 * 電話號碼檢查，判斷物件是否是符合要求的電話號碼
 * @param checkStr 需檢查的字串
 * @param name 不符合時，需提示的訊息的名稱，不寫則不提示
 * @param isMust 是否必須填寫，為true則必須寫，為其他則可不寫
 * @return 字串是電話號碼，傳回true；否則傳回false
 */
c$.isTel = function ( checkStr, name, isMust )
{
	var minlength = 4;
	var maxlength = 50;
    var repx = /^(([(（]?0\d{1,6}[）)\s\-]?)?(\d+[\s\-])+([\s#\-(（轉转\*]?\d+[）)]?)?([\\/;]?))+$/;
    return this.isValid( checkStr, name, minlength, maxlength, isMust, repx );
};

/**
 * 字串檢查，判斷物件是否符合要求
 * @param checkStr 需檢查的字串
 * @param name 不符合時，需提示的訊息的名稱，不寫則不提示
 * @param minlength 需檢查的字串的最小長度
 * @param maxlength 需檢查的字串的最大長度
 * @param isMust 是否必須填寫，為true則必須寫，為其他則可不寫
 * @param repx 需檢查的字串的正規表示式
 * @return 如果字串符合要求，傳回true；否則傳回false
 */
c$.isValid = function ( checkStr, name, minlength, maxlength, isMust, repx )
{
    //如果需檢查的字串為空
    if ( !checkStr )
    {
		//如果允許為空
        if ( !"true".is(isMust) )
            return true;
        //如果有要求提示的訊息，提示：name 還未輸入!
        if ( name )
            alert( name + unescape("%20%u9084%u672A%u8F38%u5165%21") );
		//不允許為空
        return false;
    }
    //如果需要正規表示式驗證，且物件的值不符合要求
    if ( repx && !repx.exec(checkStr) )
    {
        //如果有要求提示的訊息，提示：name 不正確!
        if ( name )
            alert( name + unescape("%20%u4E0D%u6B63%u78BA%21") );
        return false;
    }
    //如果需要判斷最小長度，提示：name 的長度必須 minlength 碼以上
    if ( minlength !== null && "" !== minlength && parseInt(minlength) > checkStr.length )
    {
        if ( name )
            alert( unescape(name + "%20%u7684%u9577%u5EA6%u5FC5%u9808%20" + minlength + "%20%u78BC%u4EE5%u4E0A") );
        return false;
    }
    //如果需要判斷最大長度，提示：name 的長度不能超過 maxlength 碼
    if ( maxlength !== null && "" !== maxlength && parseInt(maxlength) < checkStr.length )
    {
        if ( name )
            alert( unescape(name + "%20%u7684%u9577%u5EA6%u4E0D%u80FD%u8D85%u904E%20" + maxlength + "%20%u78BC") );
        return false;
    }
    return true;
};

/**
 * 資料重置(並非清空)
 * @param form Form表單
 * @return 無
 */
c$.resetForm = function( form )
{
	// 防呆
	if ( !form )
		return;
	var tem_elements = [];
    //儲存不需要重置的欄位
    $("input[type='button'], input[type='submit'], input[type='reset'], input[type='hidden']").each(function(i){
        tem_elements[i] = this.value;
    });
	//重置表單
	form.reset();
    //還原不需要重置的欄位
    $("input[type='button'], input[type='submit'], input[type='reset'], input[type='hidden']").each(function(i){
        this.value = tem_elements[i];
    });
};

// 去掉执行顺序的维护,这写法消耗比较大,且不能完全保证(直接写 window.onload 时无法保证其顺序)
/**
 * 添加 onload 事件(多次调用此函数时会保证各函数的执行顺序)
 * @param fun 要添加到 onload 事件的函数
 * @param win 要添加 onload 事件的窗口对象,默认为 window
 * @return c$ 对象本身，以支持连缀
 */
c$.addOnloadFun = function(fun, win) {
    if (!fun || typeof fun !== 'function') return this;
    win = win || window;

    var thisFun = arguments.callee;
    // thisFun.funList 作为本函数的全局变量,保证多次调用本函数时可以共用
    thisFun.funList = thisFun.funList || [];
    thisFun.funList.push(fun);
    if (thisFun.funList.length > 1) return this;

    var doReady = function () {
        var fn,  i = 0,  readyList;
        if (thisFun.funList) {
            // 为了减少变量查询带来的性能损耗，将它赋值给本地变量
            readyList = thisFun.funList;
            // 释放引用
            thisFun.funList = null;
            while ( (fn = readyList[ i++ ]) ){
                fn.call( win );
            }
        }
    };
    // IE
    if (win.attachEvent) {
        win.attachEvent('onload', doReady);
    }
    // firfox
    else if (win.addEventListener) {
        win.addEventListener('load', doReady, false);
    }

    return this;
};

// 改写了
/**
 * 全部替换字符串中的指定内容(非正则表达式替换)
 * @param regexp 把字符串里的regexp内容替换成newSubStr
 * @param newSubStr 把字符串里的regexp内容替换成newSubStr
 * @return 替换后的字符串。注意：当regexp为空时，字符串的每个字前面都会加上newSubStr
 * @example
 *  "add dda".replaceAllStr('a', '55')  // 返回: "55dd dd55"
 *  "add+dda".replaceAllStr('+', ' ')   // 不支持正则表达式的字符串替换,返回: "55dd dd55"
 */
String.prototype.replaceAllStr = function(regexp, newSubStr) {
    regexp = regexp || '';
    // 过滤掉正则表达式的符号
    regexp = regexp.
        replace(new RegExp("\\\\", 'gm'), "\\\\").
        replace(new RegExp("\\[", 'gm'), "\\[").
        replace(new RegExp("\\]", 'gm'), "\\]").
        replace(new RegExp("\\/", 'gm'), "\\/").
        replace(new RegExp("\\.", 'gm'), "\\.").
        replace(new RegExp("\\{", 'gm'), "\\{").
        replace(new RegExp("\\}", 'gm'), "\\}").
        replace(new RegExp("\\(", 'gm'), "\\(").
        replace(new RegExp("\\)", 'gm'), "\\)").
        replace(new RegExp("\\|", 'gm'), "\\|").
        replace(new RegExp("\\^", 'gm'), "\\^").
        replace(new RegExp("\\$", 'gm'), "\\$").
        replace(new RegExp("\\*", 'gm'), "\\*").
        replace(new RegExp("\\+", 'gm'), "\\+").
        replace(new RegExp("\\?", 'gm'), "\\?");
    newSubStr = newSubStr || '';
    var raRegExp = new RegExp("" + regexp, 'gm');
    return this.replace(raRegExp, "" + newSubStr);
};


// 这函数依然使用,只为了方便下面的理解
/**
 * 全部替换字符串中的指定内容
 * @param regexp 把字符串里的regexp内容替换成newSubStr
 * @param newSubStr 把字符串里的regexp内容替换成newSubStr
 * @return 替换后的字符串。注意：当regexp为空时，字符串的每个字前面都会加上newSubStr
 * @example  "add dda".replaceAll('a', '55')  // 返回: "55dd dd55"
 */
String.prototype.replaceAll = function(regexp, newSubStr) {
    regexp = regexp || '';
    newSubStr = newSubStr || '';
    var raRegExp = new RegExp("" + regexp, "gm");
    return this.replace(raRegExp, "" + newSubStr);
};

// 这函数被换以新的写法
/**
 * 转换字符串成 Html 页面上显示的编码
 * @return 转换后的字符串
 * @example "<div>".toHtmlCode() 返回: "&lt;div&gt;"
 */
String.prototype.toHtmlCode = function() {
    var html = this;
    // 以下逐一转换
    html = html.replaceAll("&", "&amp;");
    html = html.replaceAll("%", "&#37;");
    html = html.replaceAll("<", "&lt;");
    html = html.replaceAll(">", "&gt;");
    html = html.replaceAll("\n", "\n<br/>");
    html = html.replaceAll('"', "&quot;");
    html = html.replaceAll(" ", "&nbsp;");
    html = html.replaceAll("'", "&#39;");
    html = html.replaceAll("[+]", "&#43;");
    return html;
};

// 写法已优化,见下面
/**
 * 转换字符串由 Html 页面上显示的编码变回正常编码(以上面的函数对应)
 * @return 转换后的字符串
 * @example "&nbsp;".toTextCode() 返回: " "
 */
String.prototype.toTextCode = function() {
    var sour = this;
    // 以下逐一转换
    // 先转换百分号
    sour = sour.replaceAll("&#37;", "%");
    // 小于号,有三种写法
    sour = sour.replaceAll("&lt;", "<");
    sour = sour.replaceAll("&LT;", "<");
    sour = sour.replaceAll("&#60;", "<");
    // 大于号,有三种写法
    sour = sour.replaceAll("&gt;", ">");
    sour = sour.replaceAll("&GT;", ">");
    sour = sour.replaceAll("&#62;", ">");
    // 单引号
    sour = sour.replaceAll("&#39;", "'");
    sour = sour.replaceAll("&#43;", "+");
    // 转换换行符号
    sour = sour.replaceAll("\n?<[Bb][Rr]\\s*/?>\n?", "\n");
    // 双引号号,有三种写法
    sour = sour.replaceAll("&quot;", '"');
    sour = sour.replaceAll("&QUOT;", '"');
    sour = sour.replaceAll("&#34;", '"');
    // 空格,只有两种写法, &NBSP; 浏览器不承认
    sour = sour.replaceAll("&nbsp;", " ");
    sour = sour.replaceAll("&#160;", " ");
    // & 符号,最后才转换
    sour = sour.replaceAll("&amp;", "&");
    sour = sour.replaceAll("&AMP;", "&");
    sour = sour.replaceAll("&#38;", "&");
    return sour;
};
// 这函数被换以新的写法
/**
 * 转换字符串由 Html 页面上显示的编码变回正常编码(与 toHtml 函数对应)
 * @return 转换后的字符串
 * @example "&nbsp;".toText() // 返回: " "
 */
String.prototype.toTextCode = function() {
    // 以下逐一转换
    var sour = this.
        replaceAll("&#37;", "%"). // 百分号
        replaceAll("&lt;", "<", "gim").replaceAll("&#60;", "<"). // 小于号
        replaceAll("&gt;", ">", "gim").replaceAll("&#62;", ">"). // 大于号
        replaceAll("&#39;", "'"). // 单引号
        replaceAll("&#43;", "+"). // 加号
        replaceAll("\n?<br\\s*/?>\n?", "\n", "gim"). // 换行符
        replaceAll("&quot;", '"', "gim").replaceAll("&#34;", '"'). // 双引号
        replaceAll("&nbsp;", " ", "gim").replaceAll("&#160;", " "). // 空格
        replaceAll("(&amp;)|(&#38;)", "&", "gim"); // & 符号,为避免二次转换,最后才转换
    return sour;
};
// 废弃了,由新的 toTextCode 完成
/**
 * 清除HTML标签
 * @return 清除标签后的内容
 * @example "<div>haha</div>".removeHtmlTag() 返回: "haha"
 */
String.prototype.removeHtmlTag = function() {
    var text = this.trim().
        replaceAll("<!--.*-->", "").  // 清除注释
        replaceAll("</title>", "\n", "gim"). // 标题换行: </title> ==> 换行符
        replaceAll("</tr>", "\n", "gim"). // tr换行: </tr> ==> 换行符
        replaceAll("<[^>]+>", ""). // html标签清除
        toText(); // 转换字符串由 Html 页面上显示的编码变回正常编码
    return text;
};

// 换用新写法，以提高效率
/**
 * 转换字符串成 Unicode 编码
 * @param needChangeChinese 是否需要转换中文，为true则转换，否则不转换
 * @return 转换后的字符串
 * @example "哈哈".toUnicode(true) 返回: "\u54C8\u54C8"
 */
String.prototype.toUnicode = function(needChangeChinese) {
    var retValue = "";
    //逐字转换
    for (var i = 0; i < this.length; i++) {
        var tem = this.charAt(i);
        var StrLength = escape(tem).length;
        //如果是中文
        if (StrLength >= 6) {
            retValue += needChangeChinese ? escape(tem).replace("%", "\\") : tem;
        }
        //如果是符号。注，不会编码的字符： @ * / +
        else if (StrLength > 1) {
            var repaceStr = "\\u";
            //补上0
            for (var j = 0; j < 5 - StrLength; j++) {
                repaceStr += "0";
            }
            retValue += escape(tem).replace("%", repaceStr);
        }
        //如果是字母
        else retValue += tem;
    }
    return retValue;
};

// 改写了
/**
 * 检查字符串是否包含中文，是则返回true，否则返回false (注:空字符串返回 false)
 * @param isAllChinese 是否要求全部都为中文
 * @return 不填 isAllChinese，或者 isAllChinese 为 false 时，只要包含有中文即返回true，不包含一个中文则返回false
 * @return 当 isAllChinese 为 true 时，要求字符串全部都为中文则返回 true，如果有一个不为中文则返回false
 *
 * @example
 *  "aa哈哈".hasChinese() // 返回: true
 *  "aa哈哈".hasChinese(true) // 返回: false
 */
String.prototype.hasChinese = function(isAllChinese) {
    if ("" === this) return false;
    // \u4E00-\u9FA5 是汉字, \uFE30-\uFFA0 是全角符号, \u3002 是句号， \u201C \u201D 是双引号
    var clearChineseLength = this.replace(new RegExp('([\u4E00-\u9FA5]|[\uFE30-\uFFA0]|[\u3002\u201C\u201D])', 'gm'), "").length;
    // 要求全部都为中文
    if (true === isAllChinese) return (0 === clearChineseLength);
    return (this.length !== clearChineseLength);
};

// 改写了
/**
 * 检查字符串是否为日期和时间格式 (形如: 2003/12/05 13:04:06)
 * @return boolean 符合返回true,否则返回false (注:空字符串返回 false)
 */
String.prototype.isDateTime = function() {
    // 匹配检查
    var reg = /^(\d{1,4})(-|\/)(\d{1,2})\2(\d{1,2}) (\d{1,2}):(\d{1,2}):(\d{1,2})([.]\d{1,3})?$/;
    var r = this.match(reg);
    if (r == null) return false;
    // 时间是否存在检查
    var d = new Date(r[1], r[3]-1, r[4], r[5], r[6], r[7]);
    return ((d.getFullYear()==r[1] || d.getYear()==r[1]) && (d.getMonth()+1)==r[3] && d.getDate()==r[4] &&
     d.getHours()==r[5] && d.getMinutes()==r[6] && d.getSeconds()==r[7]);
};

// 改写了
/**
 * 设置整个页面的元素都可用或者都不可用 (对frame,iframe里面的元素暂未处理)
 * @param canUse 是否可用,true为可用，false为不可用(默认不可用)
 * @param dom Dom对象，默认是 document
 * @param notChangeArr 不需要设置的元素的数组
 * @return c$ 对象本身，以支持连缀
 *
 * @example
 *  c$.setDomDisable();  // 设置整个页面所有的元素都不可用
 *  c$.setDomDisable(true);  // 恢复整个页面所有的元素都可用
 *  c$.setDomDisable(false, document, [document.getElementById('btn'), document.getElementById('btn2')]); // 除id为btn,btn2的两个元素外，设置整个页面不可用
 */
c$.setDomDisable = function(canUse, dom, notChangeArr) {
    dom = dom || window.document;
    notChangeArr = notChangeArr || [];
    var elements = dom.getElementsByTagName("*");
    // 逐个元素遍历修改
    out: for (var i = 0, length = elements.length; i < length; i++ ) {
        if (!elements[i] || !elements[i].tagName) continue;
		// 页面上不需更改的元素
		for (var j = 0, len = notChangeArr.length; j < len; j++) {
			// continue到外循环
			if (elements[i] === notChangeArr[j]) continue out;
		}
        c$.setElementDisable(elements[i], canUse);
    }
    return this;
};


// 改写了 cookie 操作
/**
 * 设置cookie
 * @param cookieName cookie名称(必须有)
 * @param cookieValue 对应这名称的值(必须有)
 * @param option 其它的 cookie 参数,包括: expires(过期时间,单位为天), path, domain, secure
 * @return c$ 对象本身，以支持连缀
 * @example
 *   c$.setCookie('counter', 1, {
 *      expires: 1,
 *      path: 'http://localhost:8080/index.htm',
 *      domain: 'localhost',
 *      secure:true
 *   });
 */
c$.setCookie = function(cookieName, cookieValue, option) {
    if (!navigator.cookieEnabled || !cookieName || !cookieValue) return this; // 不能写cookie,或者缺少必要参数
    var str = escape(cookieName) + '=' + escape(cookieValue);
    if (option && typeof(option) == 'object') {
        if (option.expires) {
	        var exdate = new Date();exdate.setDate(exdate.getDate() + option.expires); // 过期时间,单位为天
            str += ';expires=' + exdate.toGMTString();
        }
		str += (option.path ? ';path=' + option.path : '');
		str += (option.domain ? ';domain=' + option.domain : '');
		str += (option.secure ? ';secure' : '');
    }
	document.cookie = str;
    return this;
};
/**
 * 获取cookie里的值
 * @param cookieName cookie里面对应值的名称
 * @return 返回获取到的对应的值(string类型)
 */
c$.getCookie = function(cookieName) {
    if (!navigator.cookieEnabled || document.cookie.length <= 0 || !cookieName) return null;
    var theCookie = document.cookie.trim() + ";" ;
    cookieName = escape(cookieName);
    var c_start = (";" + theCookie).indexOf(";" + cookieName + "=");
    if (c_start != -1) {
        c_start += cookieName.length + 1;
        var c_end = theCookie.indexOf(";", c_start);
        if (c_end == -1) c_end = theCookie.length;
        return unescape(theCookie.substring(c_start,c_end));
    }
	return null;
};
/**
 * 删除cookie里的值
 * @param cookieName cookie里面对应值的名称
 * @return c$ 对象本身，以支持连缀
 */
c$.delCookie = function(cookieName) {
    var exp = new Date(); exp.setTime(exp.getTime() - 1);
    var cookieValue = c$.getCookie(cookieName);
    if (cookieValue != null) {
        document.cookie = escape(cookieName) + '=' + cookieValue + ";expires=" + exp.toGMTString();
    }
    return this;
};

// 改写了,为了提高效率
/**
 * 复制数组(浅拷贝)
 * @return {Array} 返回复制后的数组
 *
 * @example
 *  var arr = ['a', 'b', 'c', 'd', 'c'];
 *  var arr2 = arr.clone(); // 返回的是另一个数组,对 arr2 的操作不再影响 arr
 */
Array.prototype.clone = function() {
    return [].concat(this);
    return this.concat(); // 这方式比上面效率稍高,因为少创建了一次数组
    return this.slice(0); // 改用这种方式,效率最高
};

/**
 * 对Date的扩展，将 Date 转化为指定格式的String <br />
 * 月(M)、日(d)、12小时(h)、24小时(H)、分(m)、秒(s)、周(E)、季度(q) 可以用 1-2 个占位符<br />
 * 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字) <br />
 * eg: <br />
 * (new Date()).pattern("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423
 * <br />
 * (new Date()).pattern("yyyy-MM-dd E HH:mm:ss") ==> 2009-03-10 二 20:09:04
 * <br />
 * (new Date()).pattern("yyyy-MM-dd EE hh:mm:ss") ==> 2009-03-10 周二 08:09:04
 * <br />
 * (new Date()).pattern("yyyy-MM-dd EEE hh:mm:ss") ==> 2009-03-10 星期二 08:09:04
 * <br />
 * (new Date()).pattern("yyyy-M-d h:m:s.S") ==> 2006-7-2 8:9:4.18 <br />
 */
Date.prototype.pattern = function(fmt) {
	var o = {
		"M+" : this.getMonth() + 1, // 月份
		"d+" : this.getDate(), // 日
		"h+" : this.getHours() % 12 == 0 ? 12 : this.getHours() % 12, // 小时
		"H+" : this.getHours(), // 小时
		"m+" : this.getMinutes(), // 分
		"s+" : this.getSeconds(), // 秒
		"q+" : Math.floor((this.getMonth() + 3) / 3), // 季度
		"S" : this.getMilliseconds()
		// 毫秒
	};

	var week = {
		"0" : "/u65e5",
		"1" : "/u4e00",
		"2" : "/u4e8c",
		"3" : "/u4e09",
		"4" : "/u56db",
		"5" : "/u4e94",
		"6" : "/u516d"
	};

	if (/(y+)/.test(fmt))
		fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));

	if (/(E+)/.test(fmt))
		fmt = fmt.replace(RegExp.$1, ((RegExp.$1.length > 1) ? (RegExp.$1.length > 2 ? "/u661f/u671f" : "/u5468") : "") + week[this.getDay() + ""]);

	for (var k in o) {
		if (new RegExp("(" + k + ")").test(fmt))
			fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
	}

	return fmt;
};

/****************************************************************************/



// ------------------------------ Class -------------------------------------

/// 名称: 表单简单验证
/// 示例:
/// new Validate().validate(
/// {
/// 	txtUsername:{message:"用户名不能为空, 长度在 6~20 之间!"},
///
/// 	txtPassword:{min:6, max:20, message:"密码不能为空, 长度在 6~20 之间!" },
/// 	txtRePassword:{equals:"txtPassword", message:"内容不相同!" }
///
/// 	txtAge:{type:"Int", min:10, max:100, message:"年龄必须在 10~100 之间!" }
/// 	txtPrice:{type:"Float", min:10.5, max:11.7, message:"价格必须在 10.5~11.7 之间!" }
/// 	txtEmail:{type:"Email", message:"电子邮件格式错误!" }
/// 	txtUrl:{type:"Url", message:"链接格式错误!" }
/// 	txtDate:{type:"DateTime", message:"日期格式错误!" }
/// });
function Validate()
{
	var prototype = this.constructor.prototype;
	if (!prototype.hasOwnProperty("_init_"))
	{
		prototype._init_ = true;

		prototype.isInt = function(value, format)
		{
			if (!/^([\-\+]?)(\d+)$/.test(value)) return false;

			var i = parseInt(value);
			if (format.hasOwnProperty("min"))
			{
				if (i < format.min) return false;
			}

			if (format.hasOwnProperty("max"))
			{
				if (i > format.max) return false;
			}

			return true;
		};

		prototype.isFloat = function(value, format)
		{
			if (!/^([\+\-]?((([0-9]+(\.)?)|([0-9]*\.[0-9]+))([eE][+-]?[0-9]+)?))$/.test(value)) return false;

			var f = parseFloat(value);
			if (format.hasOwnProperty("min"))
			{
				if (f < format.min) return false;
			}

			if (format.hasOwnProperty("max"))
			{
				if (f > format.max) return false;
			}

			return true;
		};

		prototype.isEmail = function(value, format)
		{
			return /^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i.test(value);
		};

		prototype.isDateTime = function(value, format)
		{
			return /^(?=\d)(?:(?!(?:1582(?:\.|-|\/)10(?:\.|-|\/)(?:0?[5-9]|1[0-4]))|(?:1752(?:\.|-|\/)0?9(?:\.|-|\/)(?:0?[3-9]|1[0-3])))(?=(?:(?!000[04]|(?:(?:1[^0-6]|[2468][^048]|[3579][^26])00))(?:(?:\d\d)(?:[02468][048]|[13579][26]))\D0?2\D29)|(?:\d{4}\D(?!(?:0?[2469]|11)\D31)(?!0?2(?:\.|-|\/)(?:29|30))))(\d{4})([-\/.])(0?\d|1[012])\2((?!00)[012]?\d|3[01])(?:$|(?=\x20\d)\x20))?((?:(?:0?[1-9]|1[012])(?::[0-5]\d){0,2}(?:\x20[aApP][mM]))|(?:[01]\d|2[0-3])(?::[0-5]\d){1,2})?$/.test(value);
		};

		prototype.isUrl = function(value, format)
		{
			return /^(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/.test(value);
		}

		prototype.isString = function(value, format)
		{
			if (format.hasOwnProperty("min"))
			{
				if (value.length < format.min) return false;
			}

			if (format.hasOwnProperty("max"))
			{
				if (value.length > format.max) return false;
			}

			if (format.hasOwnProperty("equals"))
			{
				var sourceElement = document.getElementById(format.equals);
				if (sourceElement == null) return false;

				var value2 = trim(sourceElement.value);
				sourceElement.value = value2;

				if (isNullOrEmpty(value2)) return false;
				if (value != value2) return false;
			}

			return true;
		};

		prototype.validate = function(json)
		{
			for(var id in json)
			{
				var element = document.getElementById(id);
				if (element == null)
				{
					alert("Error: Id \"" + id + "\" not found!");
					return false;
				}

				var format = json[id];
				var value = trim(element.value);
				element.value = value;

				// ----

				var result = false;
				if (!isNullOrEmpty(value))
				{
					if (!format.hasOwnProperty("type")) format.type = "string";
					switch (format.type.toLowerCase())
					{
						case "url":
							result = this.isUrl(value); break;
						case "email":
							result = this.isEmail(value); break;
						case "datetime":
							result = this.isDateTime(value); break;
						case "int":
							result = this.isInt(value, format); break;
						case "float":
							result = this.isFloat(value, format); break;
						default:
							result = this.isString(value, format); break;
					}
				}
				if (!result)
				{
					element.focus();
					if (format.hasOwnProperty("message")) alert(format.message);
					return result;
				}
			}
			return true;
		};
	}
}


//=========================================================
//=========================================
// 语言模块 对原生对象进行扩展，实现全方位的链式操作
//==========================================
;;;(function(dom,window,undefined){
dom.provide("lang");

//相当于Array1.6的every与some,当every为true时要求arr的每一个元素都满足参数中提供的测试函数，则返回 true
//当every为true时要求数组中至少有一个元素满足参数函数的测试，则返回 true。
var everyOrSome = function(arr,fn,every,scope){
    for (var i=0,n = arr.length, result; i < n; i++) {
        result = !!fn.call(scope, arr[i], i, arr);
        // 异或(^), 当 every 为true时,只要有一个为 false 则返回false；当every 为false时,只要有一个为 true 则返回true
        if (every ^ result) {
            return result;
        }
    }
    return result;
};

//修正IE67下unshift不返回数组长度的问题
//http://www.cnblogs.com/rubylouvre/archive/2010/01/14/1647751.html
if([].unshift(1) !== 1){
    Array.prototype.unshift = function(){
    var args = [0,0];
    for(var i=0,n=arguments.length;i<n;i++){
    args[args.length] = arguments[i]
    }
    Array.prototype.splice.apply(this, args);
    return this.length; //返回新数组的长度
    }
}

dom.each({
indexOf: function (el, index) {
var n = this.length>>>0, i = ~~index;
if (i < 0) i += n;
for (; i < n; i++)
if (i in this && this[i] === el) return i;
return -1;
},
//判断数组是否包含此元素
contains: function (el) {
return this.indexOf(el) !== -1
},
//返回在数组中搜索到的与给定参数相等的元素的最后（最大）索引。
lastIndexOf: function (el, index) {
var n = this.length>>>0,
i = index == null ? n - 1 : index;
if (i < 0) i = Math.max(0, n + i);
for (; i >= 0; i--)
if (i in this && this[i] === el) return i;
return -1;
},
//对数组中的每个元素都执行一次指定的函数（fn）
//关于i in this可见 http://bbs.51js.com/viewthread.php?tid=86370&highlight=forEach
forEach: function (fn, scope) {
for(var i=0,n=this.length>>>0;i<n;i++){
i in this && fn.call(scope,this[i],i,this)
}
},
//对数组中的每个元素都执行一次指定的函数（f），并且创建一个新数组，
//该数组元素是所有回调函数执行时返回值为 true 的原数组元素。
filter: function (fn, scope) {
var result = [], array = this;
this.forEach(function(value, index, array) {
if (fn.call(scope, value, index, array))
result.push(value);
});
return result;
},
without:function(){//去掉与传入参数相同的元素
var args = dom.slice(arguments);
return this.filter(function (el) {
return !args.contains(el)
});
},
//对数组中的每个元素都执行一次指定的函数（f），将它们的返回值放到一个新数组
map: function (fn, scope) {
var result = [],array = this
this.forEach(function(value, index, array) {
result.push(fn.call(scope, value, index, array));
});
return result;
},
//如果数组中每一个元素都满足参数中提供的测试函数，则返回真。
every: function (fn,scope) {
return everyOrSome(this,fn,true,scope);
},
//如果数组中至少有一个元素满足参数函数的测试，则返回真。
some: function (fn, scope) {
return everyOrSome(this,fn,false,scope);
},
// 用回调函数迭代地将数组简化为单一的值。
reduce: function (fn, lastResult, scope) {
if (this.length == 0) return lastResult;
var i = lastResult !== undefined ? 0 : 1;
var result = lastResult !== undefined ? lastResult : this[0];
for (var n = this.length; i < n; i++)
result = fn.call(scope, result, this[i], i, this);
return result;
},
reduceRight: function (fn, lastResult, scope) {
var array = this.concat().reverse();
return array.reduce(fn, lastResult, scope);
},
flatten: function () {
return this.reduce(function(array, el) {
if (dom.isArray(el))
return array.concat(el.flatten());
array.push(el);
return array;
},[]);
},
first: function(fn, bind){
if(dom.isFunction(fn)){
for (var i=0, length = this.length; i < length; i++)
if (fn.call(bind, this[i], i, this))
return this[i];
return undefined;
}else{
return this[0];
}
},
last:function(fn, bind){
var array = this.concat().reverse();
return array.first(fn, bind);
},
//http://msdn.microsoft.com/zh-cn/library/bb383786.aspx
//移除 Array 对象中某个元素的第一个匹配项。
remove: function (item) {
var index = this.indexOf(item);
if (index !== -1) return this.removeAt(index);
return null;
},
//移除 Array 对象中指定位置的元素。
removeAt: function (index) {
return this.splice(index, 1)
},
//对原数组进行洗牌
shuffle: function () {
// Jonas Raoni Soares Silva
//http://jsfromhell.com/array/shuffle [v1.0]
for (var j, x, i = this.length; i;
j = parseInt(Math.random() * i), x = this[--i], this[i] = this[j], this[j] = x);
return this;
},
//从数组中随机抽选一个元素出来
random: function () {
return this.shuffle()[0]
},
ensure: function() { //只有原数组不存在才添加它
var args = dom.slice(arguments),array = this;
args.forEach(function(el){
if (!array.contains(el)) array.push(el);
});
return array;
},
//取得对象数组的每个元素的特定属性
pluck:function(name){
return this.map(function(el){
return el[name]
}).compact();
},

sortBy: function(fn, context) {
return this.map(function(el, index) {
return {
el: el,
re: fn.call(context, el, index)
};
}).sort(function(left, right) {
var a = left.re, b = right.re;
return a < b ? -1 : a > b ? 1 : 0;
}).pluck('el');
},

compact: function () {//以数组形式返回原数组中不为null与undefined的元素
return this.filter(function (el) {
return el != null;
});
},
unique: function () { //返回没有重复值的新数组
var result = [];
for(var i=0,l=this.length; i<l; i++) {
for(var j=i+1; j<l; j++) {
if (this[i] === this[j])
j = ++i;
}
result.push(this[i]);
}
return result
},

diff : function(array) {
var result = [],l = this.length,l2 = array.length,diff = true;
for(var i=0; i<l; i++) {
for(var j=0; j<l2; j++) {
if (this[i] === array[j]) {
diff = false;
break;
}
}
diff ? result.push(this[i]) : diff = true;
}
return result.unique();
}
},function(method,name){
if(!dom.isNative(Array.prototype[name])){
Array.prototype[name] = method;
}
});

Array.prototype.each = Array.prototype.forEach;
dom.each({
//javascript1.5 firefox已实现
//http://javascript.crockford.com/remedial.html
quote:function () {
var c, i, l = this.length, o = '"';
for (i = 0; i < l; i += 1) {
c = this.charAt(i);
if (c >= ' ') {
if (c === '\\' || c === '"') {
o += '\\';
}
o += c;
} else {
switch (c) {
case '\b':
o += '\\b';
break;
case '\f':
o += '\\f';
break;
case '\n':
o += '\\n';
break;
case '\r':
o += '\\r';
break;
case '\t':
o += '\\t';
break;
default:
c = c.charCodeAt();
o += '\\u00' + Math.floor(c / 16).toString(16) +
(c % 16).toString(16);
}
}
}
return o + '"';
},
//http://www.cnblogs.com/rubylouvre/archive/2009/09/18/1568794.html
trim: function(){
var str = this,ws = /\s/,i=str.length;
str = str.replace(/^\s\s*/, '');
while (ws.test(str.charAt(--i))) {}
return str.slice(0, i + 1);
},
contains: function(string, separator){
return (separator) ? (separator + this + separator).indexOf(separator + string + separator) > -1 : this.indexOf(string) > -1;
},
startsWith: function (pattern) {
return this.indexOf(pattern) === 0;
},
toArray:function(crash){
return !!crash ? this.split('') : this.split(/\s+/g);
},
endsWith: function (pattern) {
var d = this.length - pattern.length;
return d >= 0 && this.lastIndexOf(pattern) === d;
},
empty: function () {
return this.valueOf() === '';
},
blank: function () {
return /^\s*$/.test(this);
},
//length，新字符串长度，truncation，新字符串的结尾的字段
//返回新字符串
truncate :function(length, truncation) {
length = length || 30;
truncation = truncation === void(0) ? '...' : truncation;
return this.length > length ?
this.slice(0, length - truncation.length) + truncation :String(this);
},
camelize:function(){
return this.replace(/-([a-z])/g, function($1,$2){
return $2.toUpperCase()
});
},
capitalize: function(){
return this.replace(/\b[a-z]/g, function(s){
return s.toUpperCase();
});
},
underscore: function() {
return this.replace(/([a-z0-9])([A-Z]+)/g, function(match, first, second) {
return first+"_"+(second.length > 1 ? second : second.toLowerCase());
}).replace(/\-/g, '_');
},
toInt: function(radix) {
return parseInt(this, radix || 10);
},
toFloat: function() {
return parseFloat(this);
},
instead : function(object, regexp){
return this.replace(regexp || (/\\?\#{([^{}]+)\}/g), function(match, name){
if (match.charAt(0) == '\\') return match.slice(1);
return (object[name] != undefined) ? object[name] : '';
});
}
},function(method,name){
if(!dom.isNative(String.prototype[name])){
String.prototype[name] = method;
}
});
dom.each({
bind:function(context) {
if (arguments.length < 2 && context===void 0) return this;
var fn = this, args = dom.slice(arguments, 1);
return function() {
return fn.apply(context, dom.merge(args, arguments));
}
},
//http://www.cnblogs.com/rubylouvre/archive/2009/11/09/1598761.html
curry : function() {
var f = this;
if (f.length == 0) return f;
function iterate(args) {
if (args.length >=  f.length)
return f.apply(null, args);
return function () {
var a = dom.merge(args, arguments);
return iterate(a);
};
}
return iterate([]);
},
delay: function(timeout, bind,args){
return setTimeout(this.bind(bind, args || []), timeout);
}
},function(method,name){
if(!dom.isNative(Function.prototype[name])){
Function.prototype[name] = method;
}
});
dom.each({
times: function(fn, bind) {
for (var i=0; i < this; i++)
fn.call(bind, i);
return this;
},
upto: function(number, fn,  bind) {
for (var i=this+0; i <= number; i++)
fn.call(bind, i);
return this;
},
downto: function(number, fn, bind) {
for (var i=this+0; i >= number; i--)
fn.call(bind, i);
return this;
},
abs: function() {
return Math.abs(this);
},
round: function(base) {
if (base) {
base = Math.pow(10, base);
return Math.round(this * base) / base;
} else {
return Math.round(this);
}
},
ceil: function() {
return Math.ceil(this);
},
floor: function() {
return Math.floor(this);
}
}, function(method,name){
if(!dom.isNative(Number.prototype[name])){
Number.prototype[name] = method;
}
});
})(window[escape(document.URL.split("#")[0])],this);




var Common = {
    getEvent: function() {//ie/ff
        if (document.all) {
            return window.event;
        }
        func = getEvent.caller;
        while (func != null) {
            var arg0 = func.arguments[0];
            if (arg0) {
                if ((arg0.constructor == Event || arg0.constructor == MouseEvent) || (typeof (arg0) == "object" && arg0.preventDefault && arg0.stopPropagation)) {
                    return arg0;
                }
            }
            func = func.caller;
        }
        return null;
    },
    getViewportSize: {
        w: window.innerWidth || document.documentElement.clientWidth || document.body.offsetWidth || 0,
        h: window.innerHeight || document.documentElement.clientHeight || document.body.offsetHeight || 0
    },
    setOuterHtml: function(obj, html) {
        var Objrange = document.createRange();
        obj.innerHTML = html;
        Objrange.selectNodeContents(obj);
        var frag = Objrange.extractContents();
        obj.parentNode.insertBefore(frag, obj);
        obj.parentNode.removeChild(obj);
    },
    firstChild: function(parentObj, tagName) {
        if (Common.isIE) {
            return parentObj.firstChild;
        }
        else {
            var arr = parentObj.getElementsByTagName(tagName);
            return arr[0];
        }
    },
    lastChild: function(parentObj, tagName) {
        if (Common.isIE) {
            return parentObj.lastChild;
        }
        else {
            var arr = parentObj.getElementsByTagName(tagName);
            return arr[arr.length - 1];
        }
    }
}

