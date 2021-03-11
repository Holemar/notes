
1.用 LEFT JOIN 取代 NOT IN

    强烈要求不要太多使用 NOT IN 查询，最好用表连接来取代它。如：

    SELECT ID,name FROM Table_A WHERE ID NOT IN (SELECT ID FROM Table_B);

    这句是最经典的 NOT IN 查询了。
    改为表连接代码如下：

    SELECT Table_A.ID,Table_A.name FROM Table_A LEFT JOIN Table_B ON Table_A.ID=Table_B.ID AND Table_B.ID IS NULL; -- 经测试， MySQL上查询结果不正确。
    或者：
    SELECT Table_A.ID,Table_A.name FROM Table_A LEFT JOIN Table_B ON Table_A.ID=Table_B.ID WHERE Table_B.ID IS NULL;

    经试用，效果立竿见影。


2. 用 EXISTS 代替 IN
    select num from a where num in(select num from b)

　　用下面的语句替换：

　　select num from a where exists(select 1 from b where num=a.num)


3.避免死锁
  insert / update / delete 都会锁表，需要避免表级锁，改成行级锁操作。
  根据主键操作，会是行级锁，而其它字段作为条件则会是表级锁。

  delete from 表a a left join (select 主键 from 表a where 条件)b using(主键)

  更新语句可以考虑使用 update low_priority [table]，另外更新语句 减少 更新字段（如果没有必要不要全部更新）
  添加语句可以考虑使用 insert delayed [table] into ， 延迟插入，不适用于要求即时查询的。

