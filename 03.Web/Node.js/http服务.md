
## 让HTTP服务器工作

```javascript
var http = require("http");
var url = require("url");

function onRequest(request, response) {
  var pathname = url.parse(request.url).pathname; // 获取访问路径，不包括域名和参数
  console.log("Request for " + pathname + " received.");
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.write("Hello World");
  response.end();
}

http.createServer(onRequest).listen(8888);
console.log("Server running at http://localhost:8888");
```

## 下面扩展一下请求路由
根据 event 绑定，直接将事件名定义成路径还是很不错的
```javascript
var http = require("http");
var url = require('url');
var events = require('events');
var util = require('util');

// 创建 eventEmitter 对象 
var eventEmitter = new events.EventEmitter();

// route 根路径 
eventEmitter.on('/', function(request, response){
    response.writeHead(200, {'Content-Type': 'text/plain'});

    // 解析 url 参数
    var params = url.parse(request.url, true).query;
    response.write("params.name: " + params.name);
    response.write("\n");
    response.write("params.url: " + params.url);
    response.end();
});

// 指定路径 
eventEmitter.on('/login', function(request, response){
    response.writeHead(200, {'Content-Type': 'text/plain'});
    // 读取所有的请求参数 
    response.end(util.inspect(url.parse(request.url, true)));
});

// route 404 
eventEmitter.on('404', function(url, request, response){
    response.writeHead(404, {'Content-Type': 'text/plain'});
    response.end('404 Not Found\n');
});

// 启动服务 
http.createServer(function (request, response) {
    var pathname = url.parse(request.url).pathname;
    console.log("Request for " + pathname + " received. ");
    console.log("Request url:" + request.url);

    // 分发 
    if (eventEmitter.listenerCount(pathname) > 0){
        eventEmitter.emit(pathname, request, response);
    }
    else {
        eventEmitter.emit('404', request.url, request, response);
    }

}).listen(8888);

console.log('Server running at http://127.0.0.1:8888/');
```


## 获取URL请求参数
```javascript
var http = require('http');
var url = require('url');
var util = require('util');
 
http.createServer(function(req, res){
    res.writeHead(200, {'Content-Type': 'text/plain'});
 
    // 解析 url 参数
    var params = url.parse(req.url, true).query;
    res.write("网站名：" + params.name);
    res.write("\n");
    res.write("网站 URL：" + params.url);
    res.end();
 
}).listen(3000);
```

## 获取POST请求参数
```javascript
var http = require('http');
var querystring = require('querystring');
 
var postHTML = 
  '<html><head><meta charset="utf-8"><title>菜鸟教程 Node.js 实例</title></head>' +
  '<body>' +
  '<form method="post">' +
  '网站名： <input name="name"><br>' +
  '网站 URL： <input name="url"><br>' +
  '<input type="submit">' +
  '</form>' +
  '</body></html>';
 
http.createServer(function (req, res) {
  var body = "";
  req.on('data', function (chunk) {
    body += chunk;
  });
  req.on('end', function () {
    // 解析参数
    body = querystring.parse(body);
    // 设置响应头部信息及编码
    res.writeHead(200, {'Content-Type': 'text/html; charset=utf8'});
 
    if(body.name && body.url) { // 输出提交的数据
        res.write("网站名：" + body.name);
        res.write("<br>");
        res.write("网站 URL：" + body.url);
    } else {  // 输出表单
        res.write(postHTML);
    }
    res.end();
  });
}).listen(8000);
```
