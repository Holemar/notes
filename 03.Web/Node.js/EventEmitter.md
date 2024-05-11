
# `EventEmitter` 类
`events` 模块只提供了一个对象： `events.EventEmitter`。  
`EventEmitter` 的核心就是事件触发与事件监听器功能的封装。

你可以通过`require("events");`来访问该模块。

## 方法
方法 | 描述
--- | ---
`addListener(event, listener)` | 为指定事件添加一个监听器到监听器数组的尾部。
`on(event, listener)` | 为指定事件注册一个监听器，接受一个字符串 event 和一个回调函数。
`once(event, listener)` | 为指定事件注册一个单次监听器，即 监听器最多只会触发一次，触发后立刻解除该监听器。
`removeListener(event, listener)` | 移除指定事件的某个监听器，监听器必须是该事件已经注册过的监听器。<br/>它接受两个参数，第一个是事件名称，第二个是回调函数名称。
`removeAllListeners([event])` | 移除所有事件的所有监听器， 如果指定事件，则移除指定事件的所有监听器。
`setMaxListeners(n)` | 默认情况下， `EventEmitters` 如果你添加的监听器超过 10 个就会输出警告信息。<br/>`setMaxListeners` 函数用于改变监听器的默认限制的数量。
`listeners(event)` |返回指定事件的监听器数组。
`emit(event, [arg1], [arg2], [...])` | 按监听器的顺序执行每个监听器，如果事件有注册监听返回 true，否则返回 false。
`listenerCount(emitter, event)` | (`类方法`)返回指定事件的监听器数量。

```javascript
events.EventEmitter.listenerCount(emitter, eventName) //已废弃，不推荐
events.emitter.listenerCount(eventName) //推荐
```

## 事件
事件 | 描述
--- | ---
`newListener` <br/>&nbsp;&nbsp; `event` - 字符串，事件名称<br/>&nbsp;&nbsp; `listener` - 处理事件函数 | 该事件在添加新监听器时被触发。
`removeListener` <br/>&nbsp;&nbsp; `event` - 字符串，事件名称<br/>&nbsp;&nbsp; `listener` - 处理事件函数 | 从指定监听器数组中删除一个监听器。<br/>需要注意的是，此操作将会改变处于被删监听器之后的那些监听器的索引。


```javascript
var events = require('events');
var eventEmitter = new events.EventEmitter();

// 监听器 #1
var listener1 = function listener1() {
   console.log('监听器 listener1 执行。');
}

// 监听器 #2
var listener2 = function listener2() {
  console.log('监听器 listener2 执行。');
}

// 绑定 removeListener 事件
eventEmitter.on('removeListener', function (event) {
  console.log('removeListener 事件被触发，之前有 ' + eventEmitter.listenerCount('connection') + " 个监听器监听连接事件。");
});

// 绑定 newListener 事件
eventEmitter.on('newListener', function (event) {
  console.log('newListener 事件被触发，之前有 ' + eventEmitter.listenerCount('connection') + " 个监听器监听连接事件。");
});

// 绑定 connection 事件，处理函数为 listener1 
eventEmitter.addListener('connection', listener1);

// 绑定 connection 事件，处理函数为 listener2
eventEmitter.on('connection', listener2);

// 获取指定事件的监听器数量
var eventListeners = eventEmitter.listenerCount('connection');
console.log(eventListeners + " 个监听器监听连接事件。");

// 触发 connection 事件 
eventEmitter.emit('connection');

// 移除监绑定的 listener1 函数
eventEmitter.removeListener('connection', listener1);
console.log("listener1 不再受监听。");

// 触发连接事件
eventEmitter.emit('connection');

eventListeners = eventEmitter.listenerCount('connection');
console.log(eventListeners + " 个监听器监听连接事件。");

console.log("程序执行完毕。");
```
