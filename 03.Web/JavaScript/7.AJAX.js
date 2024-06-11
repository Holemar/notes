
与服务器沟通：发送请求和处理回应
      XMLHttpRequest 提供两个存取 服务器回应的属性：
      1. responseText  将回应产生为字符串
      2. responseXML   将回应产生为一个 XML 对象
      如果后台返回的XML里包含有标签，可以先在后台把标签的"<"换成"&lt;"；而">"换成"&gt;"。这样就可以当成子元素接收。

Ajax概述：
    Ajax是由Jesse James Garrett创造的，是"Asynchronous JavaScript and XML"的缩写
    Adaptive Path公司的Jesse James Garrett如是说：
      Ajax不是一种新技术，它把几种成熟的技术以新的方式组合而成，形成强大的功能，包含：
      基于XHTML和CSS标准的表示；
      使用document Object Model进行动态显示和交互；
      使用XMLHttpRequest与服务器进行异步通信；
      使用JavaScript绑定一切。
    传统的Web应用是一个同步的交互过程。Ajax是异步的。
    AJAX是一个客户端动态网页思想；综合整合使用HTML，CSS，JavaScript，XML等页面技术完成客户端显示功能，同时以XMLHttpRequest为核心的异步对象与服务端后台通信。

Ajax的优势：
    减轻服务器的负担
      AJAX的原则是“按需取数据”，可以最大程度的减少冗余请求，和响应对服务器造成的负担。
    带来更好的用户体验
      无刷新更新页面，减少用户心理和实际的等待时间。
    利用客户端的处理能力
      可以把以前一些服务器负担的工作转嫁到客户端，利用客户端闲置的能力来处理，减轻服务器和带宽的负担
    基于标准化的并被广泛支持的技术，不需要下载插件或者小程序。
    进一步促进页面呈现和数据的分离。

XMLHttpRequest对象(AJAX引擎的核心)
1. 作用：实现AJAX的体验
       象桌面应用与server进行数据交换
       异步
       局部刷新
2. 目的：减轻server的压力，提高交互的速度
       局部刷新页面某个部份，不影响整个页面
3. 对象创建(XMLHttpRequest)：
  根据不同的浏览器，对XMLHttpRequest对象的初始化有所不同：
  <script language="javascript">
     var xmlreq = false;
     if ( window.ActiveXObject ) {
     //IE浏览器
     try { xmlreq = new ActiveXObject("Msxml2.XMLHTTP"); } catch(e){}
     //旧版本的IE
     try { xmlreq = new ActiveXObject("Microsoft.XMLHTTP"); } catch(e){}
     } else if ( window.XMLHttpRrquest ) {
     xmlreq = new XMLHttpRequest(); }   //Mozilla浏览器
  </script>

4. XMLHttpRequest对象是运行在browser的(Ajax引擎的核心)
状态：
    0=未初始化
    1=读取中
    2=已读取
    3=交互中
    4=完成


用 iframe 实现 Ajex ( 在 XMLHttpRequest 问世前 )

// ******* iframe.html 的内容 *******
<html>
<head>
<title>remote script in an IFRAME</title>
<script type="text/javascript">
<!--
   function handleResponse () {
       alert ( 'this function is called from server.html' );
   }
//-->
</script>
</head>
<body>
       <h1> Remote Scripting with an IFRAME </h1>
       <iframe id="beforexhr" name="beforexhr" src="blank.html"
        style="width:0px; height:0px; border:0px"> </iframe>
       <a href="server.html" target="beforexhr">call the server</a>
</body>
</html>

// ******* server.html 的内容 *******
<html>
<head>
<title>the erver</title>
</head>
<script type="text/javascript">
<!--
   window.parent.handleResponse();
//-->
</script>
<body>
</body>
</html>


发送请求参数：(比较 GET 和 POST )
     //此方法仅为举例而写，下面的 GET 和 POST 都用到。
     function createQueryString() {
         var firstName = document.getElementById("firstName").value;
         var middleName = document.getElementById("middleName").value;
         var birthday = document.getElementById("birthday").value;
         var queryString = "firstName=" + firstName + "&middleName=" + middleName;
             queryString += "&birthday=" + birthday;
         return queryString;
     }

     function createXMLHttpRequest () {
        var xmlHttp = null;
        //Mozilla
        if ( window.XMLHttpRequest ) {
           xmlHttp = new XMLHttpRequest ();
           if ( xmlHttp.overrideMimeType ) {
               xmlHttp.overrideMimeType("text/xml");
           }
        }  //以下是 IE
        else if ( window.ActiveXObject ) {
           try {
                 xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
           } catch (e) {
                try {
                     xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
                } catch (e) { }
           }
        }
        return xmlHttp;
     }

     // GET 形式
     function doRequestUsingGET() {
         var xmlHttp = createXMLHttpRequest();  //此通用方法，省略。具体写法见前面的例子。
         // 注：GET传参时，URL里面不能有中文(中文须转码)，也不能传太长的参数字符串
         var queryString = "GetAndPostExample?";
             queryString += createQueryString() + "&timeStamp=" + new Date().getTime();
         xmlHttp.onreadystatechange = handleStateChange;  // handleStateChange方法同样省略。不是本节重点。
         // 第3个参数： flase为同步，true为异步
         xmlHttp.open("GET", queryString, true);
         xmlHttp.send(null);
     }

     // POST 形式
     function doRequestUsingPOST() {
         var xmlHttp = createXMLHttpRequest();  //此通用方法，省略。具体写法见前面的例子。
         var url = "GetAndPostExample?&timeStamp=" + new Date().getTime(); //此句不同。
         var queryString = createQueryString();
         xmlHttp.open("POST", url, true);
         xmlHttp.onreadystatechange = handleStateChange;  // handleStateChange方法省略。
         xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;"); //此句不同。
         xmlHttp.send(queryString); //此句不同。
     }

    说明：这例子为什么把时间戳记加到URL中？
         有些浏览器会把多个XMLHttpRequest请求的结果快取到同一个URL。附加时间戳记，确保URL的唯一性。
    使用 POST 还可以把请求参数作为XML发送。写法一样，POST的最后一行：xmlHttp.send(xmlName);

    // 回调函数,举例写法
    function handleStateChange() {
       /*
       readyState 表示 XMLHttpRequest 对象的处理状态：
         0 － （未初始化）还没有调用send()方法
         1 － （载入）已调用send()方法，正在发送请求
         2 － （载入完成）send()方法执行完成，已经接收到全部响应内容，但是当前的状态及http头未知
         3 － （交互）正在解析响应内容 (因为响应及http头不全，这时通过responseBody和responseText获取部分数据会出现错误)
         4 － （完成）响应内容解析完成，可以在客户端调用了
       */
       if ( xmlHttp.readyState == 4 ) {
           // xmlHttp.status 的状态请看下面详细解析
           if ( xmlHttp.status == 200 ) {
               // ... 成功返回的代码
           } else {
               // ... 错误返回的代码
           }
       }
    }

另：在IE(即Internet Explorer)浏览器中可以不区分大小写，但在其他浏览器中将严格区分大小写。所以为了保证更好的跨浏览器效果，建议采用严格区分大小写的形式。

    建立XML如：
    function createXML() {
         var xmlName = "<pets>";
         var options = document.getElementById("petTypes").childNodes;
         var option = null;
         for ( var i = 0; i < options.length; i++ ) {
             option = options[i];
             if ( option.selected ) {
                 xmlName += "<type>" + option.value + "<\/type>";
             }
         }
         xmlName += "<\/pets>";
         return xmlName;
    }

    说明：上述方法为什么结束标签的斜线前有一个反斜线？ 如："<\/pets>"
    SGML规约(HTML就是SGML发展来的)。使用反斜线可以避免把字符串解析为标签，大多数浏览器上不使用也可以，但严格上应该用。



/*********** xmlHttp.status 状态解析 start ****************************/

0 : 0并不是一个状态值(最小是100)，它是没有被初始化。在本地通过文件方式访问时出现，因为根本就没使用HTTP协议，所以也不会有http的状态代码。

1xx: 信息响应类，表示接收到请求并且继续处理
100——客户必须继续发出请求
101——客户要求服务器根据请求转换HTTP协议版本

2xx: 处理成功响应类，表示动作被成功接收、理解和接受
200——交易成功
201——提示知道新文件的URL
202——接受和处理、但处理未完成
203——返回信息不确定或不完整
204——请求收到，但返回信息为空
205——服务器完成了请求，用户代理必须复位当前已经浏览过的文件
206——服务器已经完成了部分用户的GET请求

3xx: 重定向响应类，为了完成指定的动作，必须接受进一步处理
300——请求的资源可在多处得到
301——删除请求数据
302——在其他地址发现了请求数据
303——建议客户访问其他URL或访问方式
304——客户端已经执行了GET，但文件未变化
305——请求的资源必须从服务器指定的地址得到
306——前一版本HTTP中使用的代码，现行版本中不再使用
307——申明请求的资源临时性删除

4xx: 客户端错误，客户请求包含语法错误或者是不能正确执行
400——错误请求，如语法错误
401——请求授权失败
402——保留有效ChargeTo头响应
403——请求不允许
404——没有发现文件、查询或URl
405——用户在Request-Line字段定义的方法不允许
406——根据用户发送的Accept拖，请求资源不可访问
407——类似401，用户必须首先在代理服务器上得到授权
408——客户端没有在用户指定的饿时间内完成请求
409——对当前资源状态，请求不能完成
410——服务器上不再有此资源且无进一步的参考地址
411——服务器拒绝用户定义的Content-Length属性请求
412——一个或多个请求头字段在当前请求中错误
413——请求的资源大于服务器允许的大小
414——请求的资源URL长于服务器允许的长度
415——请求资源不支持请求项目格式
416——请求中包含Range请求头字段，在当前请求资源范围内没有range指示值，请求也不包含If-Range请求头字段
417——服务器不满足请求Expect头字段指定的期望值，如果是代理服务器，可能是下一级服务器不能满足请求

5xx:服务端错误，服务器不能正确执行一个正确的请求
500——服务器产生内部错误
501——服务器不支持请求的函数
502——服务器暂时不可用，有时是为了防止发生系统过载
503——服务器过载或暂停维修
504——关口过载，服务器使用另一个关口或服务来响应用户，等待时间设定值较长
505——服务器不支持或拒绝支请求头中指定的HTTP版本

/*********** xmlHttp.status 状态解析 end ****************************/


给XMLHttpRequests设置timeouts
　　如果一个XHR需要花费太长时间，你可以终止链接（例如网络问题），通过给XHR使用setTimeout()解决。

    var xhr = new XMLHttpRequest ();
    xhr.onreadystatechange = function () {
        if (this.readyState == 4) {
            clearTimeout(timeout);
            // do something with response data
        }
    }
    var timeout = setTimeout(function () {
        xhr.abort(); // call error callback
    }, 60*1000 /* timeout after a minute */ );
    xhr.open('GET', url, true);

    xhr.send();
　　此外，通常你应该完全避免同步Ajax调用。


// *************** 常用Ajax工具 开始 ***************

/**
 * Ajax类
 */
var Ajax = new Object();


/**
 * 生成 XMLHttpRequest
 * @return XMLHttpRequest
 */
Ajax.createXMLHttpRequest = function() {
    var fns = [
        function () { return new XMLHttpRequest(); }, // w3c, IE7+
        function () { return new ActiveXObject('Msxml2.XMLHTTP'); }, // IE6
        function () { return new ActiveXObject('Microsoft.XMLHTTP'); }, // IE5
        function () { return false; } // 无法使用Ajax
    ];
    var xmlHttp = false;
    for (var i=0, n=fns.length; i < n; i++) {
        try {
            xmlHttp = fns[i]();
            Ajax.createXMLHttpRequest = fns[i]; // 重置函数, 不用每次调用都重复判断
            break;
        }catch(e){}
    }
    return (xmlHttp || false);
};

/**
 * 发送 Ajax 请求
 * 需改变的参数则需写上，使用默认的不用写，所有的参数都可以不写
 *
 * Ajax.send({
 *    url : "submit.html",                         // 需要发送的地址(默认: 当前页地址)
 *    param : "a=1&b=2",                           // 需要发送的传参字符串
 *    async : true,                                // 异步或者同步请求(默认: true, 异步请求)。如果需要发送同步请求，请将此选项设置为 false
 *    cache : true,                                // 是否允许缓存请求(默认: true, 允许缓存)
 *    method : "GET",                              // 请求方式(默认: "GET"),也可用"POST"
 *    success : function(xmlHttp){....},           // 请求成功返回的动作
 *    error : function(xmlHttp, status){....},     // 请求失败时的动作
 *    complete : function(xmlHttp, status){....}   // 请求返回后的动作(不管成败,且在 success 和 error 之后运行)
 * });
 */
Ajax.send = function(paramObj) {
    // 创建 XMLHttpRequest
    var xmlHttp = Ajax.createXMLHttpRequest();
    // 如果不支缓 Ajax，提示信息
    if (!xmlHttp) {
        alert("您的浏览器不支持 Ajax，部分功能无法使用！");
        return;
    }

    // 需要发送的地址(默认: 当前页地址)
    paramObj.url = paramObj.url || "#";
    // 异步或者同步请求(默认: true, 异步请求)
    if (typeof paramObj.async == 'undefined') {
        paramObj.async = true;
    }
    //请求方式(默认: "GET")
    paramObj.method = paramObj.method || "GET";
    // get形式，将参数放到URL上
    if ("GET" == ("" + paramObj.method).toUpperCase() && paramObj.param) {
        paramObj.url += (paramObj.url.indexOf("?") > 0) ? "&" : "?";
        paramObj.url += paramObj.param;
        paramObj.param = null;
    }
    //发送请求
    xmlHttp.open(paramObj.method, paramObj.url, paramObj.async);
    //执行回调方法
    xmlHttp.onreadystatechange = function() {
        // XMLHttpRequest对象响应内容解析完成
        if (4 !== xmlHttp.readyState) return;
        var status = xmlHttp.status;
        // 2XX表示有效响应，304表示从缓存读取, 0是本地直接打开文件(没有使用服务器时)
        if (status >= 200 && status < 300 || status == 304 || status == 0) {
            // 请求成功时的动作
            if (paramObj.success) paramObj.success(xmlHttp);
        }
        else {
            // 请求失败时的动作
            if (paramObj.error)  paramObj.error(xmlHttp, status);
            // 默认的出错处理
            else alert("页面发生Ajax错误，请联系管理人员! \n错误类型：" + status + ": “" + location.pathname + "”");
        }
        // 请求返回后的动作(不管成败,且在 success 和 error 之后运行)
        if (paramObj.complete) paramObj.complete(xmlHttp, status);
    };
    // 缓存策略(默认: 缓存)
    if (false === paramObj.cache) {
        xmlHttp.setRequestHeader("If-Modified-Since","0");
        xmlHttp.setRequestHeader("Cache-Control","no-cache");
    }
    //请求方式("POST")
    if (paramObj.method.toUpperCase() === "POST") xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;charset=utf-8");
    xmlHttp.setRequestHeader("Charset", "UTF-8");
    //发送参数
    xmlHttp.send(paramObj.param);
};

/**
 * 获取xmlHttp里符合的资料
 * @param  xmlHttp XMLHttpRequest
 * @param  tagName 资料的 TagName
 * @param  init    默认值
 * @param  index   第几个子元素
 * @return 符合的数据的字符串
 */
Ajax.getAjaxValue = function(xmlHttp, tagName, init, index) {
    init = init || "";
    index = index || 0;
    // 没法继续执行
    if (!xmlHttp || !tagName) return init;

    try {
        //获取xmlHttp里对应的值
        var element1 = xmlHttp.responseXML.getElementsByTagName(tagName)[index].firstChild;
        var value = element1.nodeValue || element1.data;
        //如果能获取值
        if (value) return value;
    }
    catch (e) {}
    // 异常或者没能取到值时,返回默认值
    return init;
};


/**
 * 探测 url 是否存在(注意不能跨域, js的限制)
 * @param url 要探测的网址,可以绝对地址，也可以相对地址。(注意：只能探测域名相同的)
 * @return 网址存在则返回true，否则返回false。
 */
Ajax.checkUrl = function (url) {
    // 创建 XMLHttpRequest
    var xmlHttp = Ajax.createXMLHttpRequest();
    // XMLHTTP的Head方法是不用全部返回的,这样就可以快速获取状态,不必等页面内容全部返回。注意不能跨域
    xmlHttp.open("HEAD",url,false);
    xmlHttp.send();
    return xmlHttp.status==200 || xmlHttp.status==0;
};
// *************** 常用Ajax工具 结束 ***************


