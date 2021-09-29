# lxml 的安装
参考: https://www.cnblogs.com/zhangxinqi/p/9210211.html


- lxml是python的一个解析库，支持HTML和XML的解析，支持XPath解析方式，而且解析效率非常高
- XPath，全称XML Path Language，即XML路径语言，它是一门在XML文档中查找信息的语言，它最初是用来搜寻XML文档的，但是它同样适用于HTML文档的搜索
- XPath的选择功能十分强大，它提供了非常简明的路径选择表达式，另外，它还提供了超过100个内建函数，用于字符串、数值、时间的匹配以及节点、序列的处理等，几乎所有我们想要定位的节点，都可以用XPath来选择
- XPath于1999年11月16日成为W3C标准，它被设计为供XSLT、XPointer以及其他XML解析软件使用，更多的文档可以访问其官方网站： <https://www.w3.org/TR/xpath/>

windows系统下的安装：

```shell
#pip安装
pip3 install lxml

#wheel安装
#下载对应系统版本的wheel文件:  http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
pip3 install lxml-4.2.1-cp36-cp36m-win_amd64.whl
```

linux下安装：

```shell
yum install -y epel-release libxslt-devel libxml2-devel openssl-devel

pip3 install lxml
```

验证安装：

```python
import lxml
```

# XPath常用规则

[参考 xpath 的选取节点规则](../../03.Web/xpath/2.选取节点.md)


### 读取文本解析节点

```python
from lxml import etree

text = '''
<div>
    <ul>
         <li name="link1" class="item-0"><a href="link1.html">第一个</a></li>
         <li name="link2" class="item-1"><a href="link2.html">second item</a></li>
         <li name="link5" class="item-0"><a href="link5.html">a属性</a>
     </ul>
 </div>
'''
# （1）读取文本
html = etree.HTML(text)  # 初始化生成一个XPath解析对象

# （2）解析HTML文件
# html = etree.parse('test.html', etree.HTMLParser()) #指定解析器HTMLParser会根据文件修复HTML文件中缺失的如声明信息

result = etree.tostring(html, encoding='utf-8')  # 解析对象输出代码
# result = etree.tostringlist(html) # 解析成列表
print(type(html))  # <class 'lxml.etree._Element'>
print(type(result))  # <class 'bytes'>
print(result.decode('utf-8'))  # etree会修复HTML文本节点,打印如下：
'''<html><body><div>
    <ul>
         <li class="item-0"><a href="link1.html">第一个</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0"><a href="link5.html">a属性</a>
     </li></ul>
 </div>
</body></html>
'''

# （3）获取所有节点
# 如要获取li节点，可以使用//后面加上节点名称，然后调用xpath()方法
print(html.xpath('//li'))  # 打印: [<Element li at 0x104b32c8>, <Element li at 0x10473308>, <Element li at 0x104b33c8>]

# （4）获取子节点
# 通过/或者//即可查找元素的子节点或者子孙节点，下面选择所有li节点的所有直接a节点
print(html.xpath('//li/a'))  # 打印: [<Element a at 0x103b32c8>, <Element a at 0x103bb3308>, <Element a at 0x103bb33c8>]

# （5）获取父节点
# 查找父节点可以使用 .. 来实现也可以使用 parent:: 来获取
print(html.xpath('//a[@href="link2.html"]/../@class'))  # 打印: ['item-1']
print(html.xpath('//a[@href="link1.html"]/parent::*/@class'))  # 打印: ['item-0']

# （6）属性匹配
# 在选取的时候，可以用@符号进行属性过滤
print(html.xpath('//li[@class="item-1"]'))  # 打印: [<Element li at 0x103db32c8>]

# （7）文本获取
# 用 text() 方法获取节点中的文本
print(html.xpath('//li/a/text()'))  # 获取a节点下的内容,打印: ['第一个', 'second item', 'a属性']
print(html.xpath('//li[@class="item-1"]//text()'))  # 获取li下所有子孙节点的内容,打印: ['second item']

# （8）属性获取
# 使用@符号即可获取节点的属性
print(html.xpath('//li/a/@href'))  # 获取a的href属性,打印: ['link1.html', 'link2.html', 'link5.html']
print(html.xpath('//li[@class="item-1"]//@href'))  # 获取所有li子孙节点的href属性,打印：['link2.html']

# （9）模糊匹配,contains()函数
# 如果某个属性的值有多个，或者需要截取其中一部分时，可以使用 contains() 函数来匹配包含的文本
print(html.xpath('//li[@class="item-0"]/a/text()'))  # 打印: ['第一个', 'a属性']
print(html.xpath('//li[contains(@class,"item")]/a/text()'))  # 打印: ['第一个', 'second item', 'a属性']

# （10）多属性匹配 and
# 如果需要根据多个属性确定一个节点，可以用 and 运算符来连接：
print(html.xpath('//li[@class="item-0" and @name="link1"]/a/text()'))  # 打印: ['第一个']
print(html.xpath('//li[contains(@class,"item") and @name="link1"]/a/text()'))  # 打印: ['第一个']
```


```python
from lxml import etree

text1 = '''
<div>
    <ul>
         <li class="aaa" name="item"><a href="link1.html">第一个</a></li>
         <li class="aaa" name="item"><a href="link1.html">第二个</a></li>
         <li class="aaa" name="item"><a href="link1.html">第三个</a></li>
         <li class="aaa" name="item"><a href="link1.html">第四个</a></li> 
     </ul>
 </div>
'''

html = etree.HTML(text1,etree.HTMLParser())

#（12）按序选择
# 如果同时匹配多个节点，但只想要其中的某个，如第二个节点或者最后一个节点，这时可以用索引获取特定次序的节点
# 索引从 1 开始。错误的索引值返回空数组(0 和 负数、小数 是错误值，超过最后一个的值也是错误值)。
print(html.xpath('//li[contains(@class,"aaa")]/a/text()'))  # 获取所有，打印: ['第一个', '第二个', '第三个', '第四个']
print(html.xpath('//li[1][contains(@class,"aaa")]/a/text()'))  # 获取第一个，打印: ['第一个']
print(html.xpath('//li[last()][contains(@class,"aaa")]/a/text()'))  # 获取最后一个，打印: ['第四个']
print(html.xpath('//li[position()>2 and position()<4][contains(@class,"aaa")]/a/text()'))  # 获取第三个，打印: ['第三个']
print(html.xpath('//li[last()-2][contains(@class,"aaa")]/a/text()'))  # 获取倒数第三个，打印: ['第二个']
print(html.xpath('//li[position()<2 or position()>3][contains(@class,"aaa")]/a/text()'))  # 打印: ['第一个', '第四个']

#（13）节点轴选择
# XPath提供了很多节点选择方法，包括获取子元素、兄弟元素、父元素、祖先元素等
print(html.xpath('//li[1]/ancestor::*'))  # 获取所有祖先节点，打印: [<Element html at 0x1043b4308>, <Element body at 0x1043b42c8>, <Element div at 0x1043b43c8>, <Element ul at 0x1043b4408>]
print(html.xpath('//li[1]/ancestor::div'))  # 获取div祖先节点，打印: [<Element div at 0x1043b42c8>]
print(html.xpath('//li[1]/attribute::*'))  # 获取所有属性值，打印: ['aaa', 'item']
print(html.xpath('//li[1]/child::*'))  # 获取所有直接子节点，打印: [<Element a at 0x1043b42c8>]
print(html.xpath('//li[1]/descendant::a'))  # 获取所有子孙节点的a节点，打印: [<Element a at 0x1043b42c8>]
print(html.xpath('//li[1]/following::*'))  # 获取当前子节之后的所有节点，打印: [<Element li at 0x1043b42c8>, <Element a at 0x1043b4408>, <Element li at 0x1043b43c8>, <Element a at 0x1043b4448>, <Element li at 0x1043b4488>, <Element a at 0x1043b4508>]
print(html.xpath('//li[1]/following-sibling::*'))  # 获取当前节点的所有同级节点，打印: [<Element li at 0x1043b42c8>, <Element li at 0x1043b4408>, <Element li at 0x1043b43c8>]

# Element 的部分属性
resutl = html.xpath('//li[1]')
print(resutl)  # 打印: [<Element li at 0x1035b32c8>]
e = resutl[0]
print(e.attrib)  # 打印: {'class': 'aaa', 'name': 'item'}
print(e.tag)  # 打印: li
print(e.text)  # 打印: None
print(e.sourceline)  # 打印: 4
print(e.keys())  # 打印: ['class', 'name']
print(e.items())  # 打印: [('class', 'aaa'), ('name', 'item')]
print(e.find('a'))  # 打印: <Element a at 0x1036eb408>
print(e.find('a').text)  # 打印: 第一个
print(e.findall('a'))  # 打印: [<Element a at 0x103eb4408>]
print(e.findtext('a'))  # 打印: 第一个
print(e.getparent())  # 打印: <Element ul at 0x103bb4408>
print(e.getchildren())  # 打印: [<Element a at 0x1033b4408>]
print(e.getnext())  # 打印: <Element li at 0x103bb4408>
print(e.getprevious())  # 打印: None
print(e.getroottree())  # 打印: <lxml.etree._ElementTree object at 0x103db3408>

```

- 上例（12）使用了 and、or、大于、小于 等运算符 [参考 xpath 的运算符](../../03.Web/xpath/5.运算符.md)
- 上例（12）使用了 last()、position() 函数，在XPath中，提供了100多个函数 [参考 xpath 的函数](../../03.Web/xpath/4.函数.md)
- 上例（13）使用了 轴， [参考 xpath 的轴](../../03.Web/xpath/3.轴.md)


