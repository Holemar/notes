Requests 库

官方文档
requests官方文档中文版: http://cn.python-requests.org/en/latest/  
requests的具体安装过程请看：http://docs.python-requests.org/en/latest/user/install.html#install  
requests的官方指南文档：http://docs.python-requests.org/en/latest/user/quickstart.html  
requests的高级指南文档：http://docs.python-requests.org/en/latest/user/advanced.html#advanced  

# Requests 的简介及安装
参考: https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI2NTU4OTI1NQ==&action=getalbum&album_id=1787002840389894145

- Requests 是 Python HTTP 库。它是优秀的第三方的HTTP库，使用范围广，通常用于接口测试、爬虫、web后台服务调用外部服务等。

Requests 完全满足今日 web 的需求。
- Keep-Alive & 连接池
- 国际化域名和 URL
- 带持久 Cookie 的会话
- 浏览器式的 SSL 认证
- 自动内容解码
- 基本/摘要式的身份认证
- 优雅的 key/value Cookie
- 自动解压
- Unicode 响应体
- HTTP(S) 代理支持
- 文件分块上传
- 流下载
- 连接超时
- 分块请求
- 支持 .netrc

### 安装：

```shell
pip install requests
```

### 获取源码:

```shell
git clone git://github.com/kennethreitz/requests.git
```


# 发送请求
使用 Requests 发送网络请求非常简单。

```python
# 导入 Requests 模块
import requests

# 然后，尝试获取某个网页。GET网络请求：
r = requests.get('https://postman-echo.com/get')
#现在，我们有一个名为 r 的 Response 对象。我们可以从这个对象中获取所有我们想要的信息。

# 可以这样发送一个 HTTP POST 请求：
r = requests.post('https://postman-echo.com/post', data={'key': 'value'})

# 其他 HTTP 请求类型：PUT，DELETE，HEAD 以及 OPTIONS：
r = requests.put('https://postman-echo.com/put', data={'key': 'value'})
r = requests.delete('http://xxx.xxx.com/delete')
r = requests.head('http://xxx.xxx.com/get')
r = requests.options('http://xxx.xxx.com/get')
```
都很不错吧。其实 requests 进行网络请求很简单的。


# 传递 URL 参数
- 你也许经常想为 URL 的查询字符串(query string)传递某种数据。  
- 如果你是手工构建 URL，那么数据会以键/值对的形式置于 URL 中，跟在一个问号的后面。 例如， httpbin.org/get?key=val。
- Requests 允许你使用 params 关键字参数，以一个字符串字典来提供这些参数。  
- 举例来说，如果你想传递 key1=value1 和 key2=value2 到 httpbin.org/get ，那么你可以使用如下代码：

```python
import requests
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get("http://xxx.org/get", params=payload)

# 通过打印输出该 URL，你能看到 URL 已被正确编码(会将自动转码的内容打印出来)：
print(r.url)  # 打印: http://xxx.org/get?key2=value2&key1=value1
```
注意字典里值为 None 的键都不会被添加到 URL 的查询字符串里。

#### 你还可以将一个列表作为值传入：
```python
import requests
payload = {'key1': 'value1', 'key2': ['value2', 'value3'], 'wd': '张亚楠'}
r = requests.get('http://xxx.org/get', params=payload)
print(r.url)  # 打印: http://xxx.org/get?key1=value1&key2=value2&key2=value3
```

# 响应内容
我们能读取服务器响应的内容。我们可以找一个请求：

```python
import requests
r = requests.get('https://api.github.com/events')
print(r.text)  # 打印: '[{"repository":{"open_issues":0,"url":"https://github.com/...
```
- Requests 会自动解码来自服务器的内容。大多数 unicode 字符集都能被解码。
- 请求发出后，Requests 会基于 HTTP 头部对响应的编码作出有根据的推测。
- 当你访问 r.text 之时，Requests 会使用其推测的文本编码。

```python
import requests
r = requests.get('http://www.zhidaow.com')  # 发送请求
print(r.status_code)  # 状态码,打印: 200
print(r.headers['content-type'])  # 返回头部信息,打印:'text/html; charset=utf8'
print(r.headers) # 返回头部信息,打印:{'content-encoding': 'gzip', 'transfer-encoding': 'chunked', 'content-type': 'text/html; charset=utf-8';  ... }
print(r.encoding)  # 获取网页编码信息,打印:'utf-8'
print(r.text)  #内容部分（PS，由于编码问题，建议这里使用 r.content ）,打印:u'<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml"...'
print(r.content) #文档中说r.content是以字节的方式去显示，所以在IDLE中以b开头。但我在cygwin中用起来并没有，下载网页正好。所以就替代了urllib2的urllib2.urlopen(url).read()功能。
print(r.json()) # 如果返回内容是 json 格式,会自动转成 json 并返回
```

- 你可以找出 Requests 使用了什么编码，并且能够使用 r.encoding 属性来改变它：
```python
print(r.encoding)  # 打印: 'utf-8'

# 赋值，改变编码
r.encoding = 'ISO-8859-1'
```

- 如果你改变了编码，每当你访问 r.text ，Request 都将会使用 r.encoding 的新值。 
- 你可能希望在使用特殊逻辑计算出文本的编码的情况下来修改编码。 比如 HTTP 和 XML 自身可以指定编码。
- 这样的话，你应该使用 r.content 来找到编码，然后设置 r.encoding 为相应的编码。 这样就能使用正确的编码解析 r.text 了。


# 二进制响应内容
你也能以字节的方式访问请求响应体，对于非文本请求：

```python
print(r.content)  # 打印： b'[{"repository":{"open_issues":0,"url":"https://github.com/...
```

Requests 会自动为你解码 gzip 和 deflate 传输编码的响应数据。

例如，以请求返回的二进制数据创建一张图片，你可以使用如下代码：

```python
from PIL import Image
from io import BytesIO

i = Image.open(BytesIO(r.content))
```

# 设置超时时间
我们可以通过timeout属性设置超时时间，一旦超过这个时间还没获得响应内容，就会提示错误。
`requests.get('http://github.com', timeout=0.001)`


# 代理访问
采集时为避免被封IP，经常会使用代理。requests也有相应的proxies属性。

```python
import requests
proxies = {
  "http": "http://10.10.1.10:3128",
  "https": "http://10.10.1.10:1080",
}
requests.get("http://www.zhidaow.com", proxies=proxies)

#如果代理需要账户和密码，则需这样：
proxies = {
    "http": "http://user:pass@10.10.1.10:3128/",
}
```


