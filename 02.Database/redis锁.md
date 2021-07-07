
# SETNX 命令
命令格式: `SETNX key value`  
- 将 key 的值设为 value，当且仅当 key 不存在。  
- 若给定的 key 已经存在，则 SETNX 不做任何动作。  
- SETNX 是 SET if Not Exists的简写。  

- 目前通常所说的 Setnx 命令，并非单指 Redis 的 setnx key value 这条命令。
- 一般代指 Redis 中对 Set 命令加上 NX 参数进行使用，Set 这个命令，目前已经支持这么多参数可选：
命令格式:  `SET key value [EX seconds|PX milliseconds] [NX|XX] [KEEPTTL]`

### 因为 Redis 版本在 2.6.12 之前，Set 是不支持 NX 参数的，如果想要完成一个锁，那么需要两条命令：
1. `setnx Test uuid`
2. `expire Test 30`  
- 即放入 Key 和设置有效期，是分开的两步，理论上会出现 1 刚执行完，程序挂掉，无法保证原子性。
- 但是早在 2013 年，Redis 就发布了 2.6.12 版本，并且官网(Set 命令页)，也早早就说明了“SETNX，SETEX，PSETEX 可能在未来的版本中，会弃用并永久删除”。


### SETNX 命令返回值
返回整数，具体为
- 1，当 key 的值被设置(key不存在时)
- 0，当 key 的值没被设置(key已存在)

### 例子
```shell
redis> SETNX mykey “hello”
(integer) 1
redis> SETNX mykey “hello2”
(integer) 0
redis> GET mykey
“hello”
```

### 使用SETNX实现分布式锁
多个进程执行以下Redis命令：  
`SETNX lock.foo <current Unix time + lock timeout + 1>`

- 如果 SETNX 返回1，说明该进程获得锁，SETNX 将键 lock.foo 的值设置为锁的超时时间（当前时间 + 锁的有效时间）。  
- 如果 SETNX 返回0，说明其他进程已经获得了锁，进程不能进入临界区。进程可以在一个循环中不断地尝试 SETNX 操作，以获得锁。  

### 解决死锁1-设置超时
- 考虑一种情况，如果进程获得锁后，断开了与 Redis 的连接（可能是进程挂掉，或者网络中断），如果没有有效的释放锁的机制，那么其他进程都会处于一直等待的状态，即出现“死锁”。
- 上面在使用 SETNX 获得锁时，我们将键 lock.foo 的值设置为锁的有效时间，进程获得锁后，其他进程还会不断的检测锁是否已超时，如果超时，那么等待的进程也将有机会获得锁。

### 解决死锁2-删除锁
- 然而， SETNX + 超时 并不能保证万无一失。
- 如果进程 A 获取锁后，操作锁内资源超过前面设置的超时时间，那么就会导致其他进程拿到锁，等进程 A 操作完了，回手就是把其他进程的锁删了。
- 这时进程 B 在锁超时后 开开心心拿到锁不到一会，进程 A 操作完成，回手一个 Del，就把锁释放了。
- 如果是任务不允许重复执行的，锁时间需要足够长，或者定期再延迟一下锁时间。(比如扣款，不能重复扣)
- 如果是任务可以重复执行的，锁超时后允许其它进程取锁并操作。(比如统计，允许重复统计)

- - 下面介绍可以重复执行的任务，删除锁的操作
- 在用 Setnx 的时候，Key 虽然是主要作用，但是 Value 也不能闲着，可以设置一个唯一的进程 ID，或者用 UUID 这种随机数。
- 当解锁的时候，先获取 Value 判断是否是当前进程加的锁，再去删除。   
伪代码：
```java
String uuid = xxxx;
// 伪代码，具体实现看项目中用的连接工具
// 有的提供的方法名为set 有的叫setIfAbsent
set Test uuid NX PX 3000
try{
// biz handle....
} finally {
    // unlock
    if (uuid.equals(redisTool.get('Test')) {
        redisTool.del('Test');
    }
}
```
这回看起来是不是稳了？  
- 相反，这回的问题更明显了，在 `finally` 代码块中，`Get` 和 `Del` 并非原子操作，还是有进程安全问题。  
- 只是，现在出问题的概率大幅度降低，出问题的情况： 在 get 和 del 的间隙出现进程A的锁超时，并且其它进程又获取了锁，然后进程A删掉了其它进程的锁  


### 解决死锁2-删除锁的正确姿势
那么删除锁的正确姿势之一，就是可以使用 Lua 脚本，通过 Redis 的 eval/evalsha 命令来运行：
```lua
-- lua删除锁：
-- KEYS和ARGV分别是以集合方式传入的参数，对应上文的Test和uuid。
-- 如果对应的value等于传入的uuid。
 if redis.call('get', KEYS[1]) == ARGV[1]
    then
    -- 执行删除操作
        return redis.call('del', KEYS[1])
    else
    -- 不成功，返回0
        return 0
end
```
- 通过 Lua 脚本能保证原子性的原因说的通俗一点：
- 就算你在 Lua 里写出花，执行也是一个命令（eval/evalsha）去执行的，一条命令没执行完，其他客户端是看不到的。

