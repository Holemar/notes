
选取页面的对象:
    var obj = document.getElementById("elementID");
    var objs = document.getElementsByName("elementName"); //返回数组
    var objs = document.getElementsByTagName("TagName");  //返回数组
    var objs = document.getElementsByClassName("elementClass");  //返回数组

    var obj = document.forms["FormName"].elements["elementName"];
    var obj = document.forms[x].elements[y]; //x和y 是int类型，表示第几个表单，第几个元素
    var obj = document.FormName.elementName;
    var obj = document.all["elementName"];
    var obj = document.all["elementID"];

    var obj = document.querySelector("#elementID");  // 返回第一个符合条件的元素(里面的选择字符串参考CSS选择器)
    var objs = document.querySelectorAll(".elementClass");  // 返回所有符合条件的元素


Document对象
  属性
    all(elementID)	表示文档中所有<html>标记的集合(只适用与IE)
    alinkColor	设置一个被激活链接的颜色
    anchors	获取文档中<anchor>标记的集合(数组)
    bfColor	设置背景颜色
    fgColor	设置文档的前景色(文本)
    cookie	获取与文档相关的Cookie
    domain	用于指定文档的安全域
    embeds	代表文档中所有<embed>标记的数组
    forms	代表文档中所有<form>标记的数组
    getSelection()	返回选中的文本
    images	代表文档中所有<image>标记的数组
    lastModified	代表文档的最后修改时间
    linkColor	设置未访问过的链接的颜色
    links	代表文档中所有<a>标记的数组
    title	获得文档的标题
    URL	返回文档对应的URL
    vinkColor	设置以访问过链接的颜色
  方法
    open([mimetype])	未write()和writeln()语句准备一个流,它的参数mimetype可以时几个MIME类型(包括text/html,text/plain,image/x-bitmap和plugln(any Netscape plug-in MIMEtype))之一,默认值是text/html
    close()	关闭由open()方法打开的流
    focus()	让指定的文档获得焦点
    write()	向文档职工写入文本
    writeln()	向文档职工写入文本,并向文档的末尾追加一个换行符

遍历
    // dom 遍历推荐使用 for of
    // 而不推荐使用 for in, 因为 for in 返回的是 key 值，适合遍历固定枚举值
    for (let elem of document.getElementsByTagName('audio')) {
      elem.play();
    }


元素增减 class 样式
    现代浏览器
    // 现代浏览器 classList 优化过，它提供了一些方法，并且不依赖任何框架和插件。
    // 在IE10之前的版本不支持该 classList 属性，IE8和IE9可以通过第三方库来支持该方法。
    document.getElementById("MyElement").classList.add('MyClass');   // 添加 class
    document.getElementById("MyElement").classList.remove('MyClass');  // 移除 class
    if ( document.getElementById("MyElement").classList.contains('MyClass') )  // 判断是否存在 class
    document.getElementById("MyElement").classList.toggle('MyClass'); // 切换 class

    通用跨浏览器解决方案
    // 通过设置元素的 className 属性来实现的。 该属性是一个字符串，包含了所有 class 名的列表，用空格分隔。
    document.getElementById("MyElement").className = "MyClass";  //单个class
    document.getElementById("MyElement").className = "MyClass1 MyClass2";  //多个class
    // 下面是一些通用方法，可以用来添加、移除、判断和切换 class。
    function addClass(elem, className) {
      if (!elem.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'))) {
        elem.className += ' ' + className;
      }
    }
    function removeClass(elem, className) {
      elem.className = elem.className.replace(new RegExp('(\\s|^)' + className + '(\\s|$)'), '$2');
      // 或者写: elem.className = elem.className.replace(new RegExp('(\\s|^)' + className + '(\\s|$)'), ' ');
    }
    // 我们可以用以下代码来判断元素是否有某个 class
    function hasClass(elem, className) {
      return elem.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'));
    }
    // 切换 class
    function toggleClass(elem, className) {
      var classes = elem.className.split(' ');
      var existingIndex = classes.indexOf(className);
      if (existingIndex >= 0) {
        classes.splice(existingIndex, 1);
      } else {
        classes.push(className);
      }
      elem.className = classes.join(' ');
    }


