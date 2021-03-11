
mongodb group分组
	和数据库一样 group 常常用于统计。
	MongoDB的 group 还有很多限制，如：返回结果集不能超过16M， group操作不会处理超过10000个唯一键，好像还不能利用索引[不很确定]。
 

group 大约需要一下几个参数:
	1.key：用来分组文档的字段。和keyf两者必须有一个
	2.keyf / $keyf：可以接受一个javascript函数。用来动态的确定分组文档的字段。和key两者必须有一个
	3.initial：reduce中使用变量的初始化
	4.reduce / $reduce：执行的reduce函数。函数需要返回值。(返回累计结果)
	5.cond / condition：执行过滤的条件。
	6.finallize：在reduce执行完成，结果集返回之前对结果集最终执行的函数。可选的。
	注意上面部分key值的不同写法:
		db.表名.group 语法中，使用 keyf、reduce、cond
		db.runCommand 语法中，使用 $keyf、$reduce、condition


下面介绍一个实例：

	for(var i=1; i<20; i++){
		var num = i%6; // 结果 0~5
		db.test.insert({_id:i,name:"user_"+i,age:num});
	}


1.普通分组查询
	// 写法1:
	db.test.group({
		key:{age:true}, // 字段
		initial:{num:0}, // 变量初始化
		reduce:function(doc,prev){prev.num++} // doc 是匹配到的原行数据, prev是计算结果集
	});
	// 查询结果：
	[{"age":1,"num":4},{"age":2,"num":3},{"age":3,"num":3},{"age":4,"num":3},{"age":5,"num":3},{"age":0,"num":3}]

	// 写法2:
	db.runCommand({group: {
		ns:"test", // collection/表 名称
		key:{age:true}, // 字段
		initial:{num:0}, // 变量初始化
		$reduce:function(doc,prev){prev.num++} // doc 是匹配到的原行数据, prev是计算结果集
	}});
	// 查询结果:
	{
		"retval":[{"age":1,"num":4},{"age":2,"num":3},{"age":3,"num":3},{"age":4,"num":3},{"age":5,"num":3},{"age":0,"num":3}],
		"count":NumberLong("19"), // 匹配到的行数
		"keys":NumberLong("6"),  // 分组数
		"ok":1
	}


2.筛选后再分组
	// 增加 cond/condition 参数来筛选

	// 写法1:
	db.test.group({
		key:{age:true},
		initial:{num:0},
		reduce:function(doc,prev){prev.num++},
		cond:{age:{$gt:2}} // 多了这个筛选条件
	});
	// 查询结果：
	[{"age":3,"num":3},{"age":4,"num":3},{"age":5,"num":3}]

	// 写法2:
	db.runCommand({group: {
		ns:"test",
		key:{age:true},
		initial:{num:0},
		$reduce:function(doc,prev){prev.num++},
		condition:{age:{$gt:2}} // 多了这个筛选条件
	}});
	// 查询结果：
	{
		"retval":[{"age":3,"num":3},{"age":4,"num":3},{"age":5,"num":3}],
		"count":NumberLong("9"),
		"keys":NumberLong("3"),
		"ok":1
	}


3.$where 查询
	// 普通的 $where 查询
	db.test.find({$where:function(){return this.age>2;}});

	// group 联合 $where 查询
	db.test.group({
		key:{age:true},
		initial:{num:0},
		reduce:function(doc,prev){prev.num++},
		cond:{$where:function() {return this.age>2;}}  // 这个筛选条件使用 $where
	});
	// 查询结果：
	[{"age":3,"num":3},{"age":4,"num":3},{"age":5,"num":3}]

	// 写法2:
	db.runCommand({group: {
		ns:"test",
		key:{age:true},
		initial:{num:0},
		$reduce:function(doc,prev){prev.num++},
		condition:{$where:function() {return this.age>2;}} // 这个筛选条件使用 $where
	}});
	// 查询结果：
	{
		"retval":[{"age":3,"num":3},{"age":4,"num":3},{"age":5,"num":3}],
		"count":NumberLong("9"),
		"keys":NumberLong("3"),
		"ok":1
	}


4.使用函数返回值分组
	//注意，$keyf 指定的函数一定要返回一个对象
	// 写法1:
	db.test.group({
		// key:{age:true},
		keyf:function(doc){return {age:doc.age};}, // 结果跟上面 key 的指定一样，但这个可以拼接及其它操作
		initial:{num:0},
		reduce:function(doc,prev){prev.num++}
	});
	// 查询结果：
	[{"age":1,"num":4},{"age":2,"num":3},{"age":3,"num":3},{"age":4,"num":3},{"age":5,"num":3},{"age":0,"num":3}]

	// 写法2:
	db.runCommand({group: {
		ns:"test",
		// key:{age:true},
		$keyf:function(doc){return {age:doc.age};}, // 结果跟上面 key 的指定一样
		initial:{num:0},
		$reduce:function(doc,prev){prev.num++}
	}});
	// 查询结果:
	{
		"retval":[{"age":1,"num":4},{"age":2,"num":3},{"age":3,"num":3},{"age":4,"num":3},{"age":5,"num":3},{"age":0,"num":3}],
		"count":NumberLong("19"),
		"keys":NumberLong("6"),
		"ok":1
	}


5.使用终结器
	// 写法1:
	db.test.group({
		key:{age:true},
		initial:{num:0},
		reduce:function(doc,prev){prev.num++},
		finalize: function(doc){ doc.count=doc.num;delete doc.num; } // 将结果的 num 改名为 count
	});
	// 查询结果：
	[{"age":1,"count":4},{"age":2,"count":3},{"age":3,"count":3},{"age":4,"count":3},{"age":5,"count":3},{"age":0,"count":3}]

	// 写法2:
	db.runCommand({group: {
		ns:"test",
		key:{age:true},
		initial:{num:0},
		$reduce:function(doc,prev){prev.num++},
		finalize: function(doc){ doc.count=doc.num;delete doc.num; } // 将结果的 num 改名为 count
	}});
	// 查询结果:
	{
		"retval":[{"age":1,"count":4},{"age":2,"count":3},{"age":3,"count":3},{"age":4,"count":3},{"age":5,"count":3},{"age":0,"count":3}],
		"count":NumberLong("19"),
		"keys":NumberLong("6"),
		"ok":1
	}


6. 使用 Map/Reduce
	注意：
	1.Map/Reduce 是根据 map 函数里调用的 emit 函数的第一个参数来进行分组的
	2.仅当根据分组键分组后一个键匹配多个文档，才会将 key 和文档集合交由reduce函数处理。

    执行函数：
    db.runCommand(
    {
        mapreduce : <collection>,
        map : <mapfunction>,
        reduce : <reducefunction>
        [, query : <query filter object>]
        [, sort : <sort the query.  useful   optimization>] for
        [, limit : <number of objects to   from collection>] return
        [, out : <output-collection name>]
        [, keeptemp: < | >] true false
        [, finalize : <finalizefunction>]
        [, scope : <object where fields go into javascript global scope >]
        [, verbose :  ] true
    });

    参数说明:
    mapreduce: 要操作的目标集合。
    map: 映射函数 (生成键值对序列，作为 reduce 函数参数)。
    reduce: 统计函数。
    query: 目标记录过滤。
    sort: 目标记录排序。
    limit: 限制目标记录数量。
    out: 统计结果存放集合 (不指定则使用临时集合，在客户端断开后自动删除)。
    keeptemp: 是否保留临时集合。
    finalize: 最终处理函数 (对 reduce 返回结果进行最终整理后存入结果集合)。
    scope: 向 map、reduce、finalize 导入外部变量。
    verbose: 显示详细的时间统计信息。


	// 按 name 前6个字符分组，且统计各组的数量
	db.runCommand(
	{
		mapreduce:'test',  // 操作的 collection/表 名称
		map:function(){emit(this.name.substr(0,6), this);}, // emit 第一个参数是分组的key，第二个参数是传给 reduce 的 doc 内容
		reduce:function(key, docs){return docs.length;}, //注意：docs不是一个Object对象而是数组
		out:'wq' // 输出结果的 collection/表 名称，如果此表已存在则覆盖
	});
	// 执行结果：
	{
		"result": "wq",
		"timeMillis": NumberInt("137"),
		"counts": {
			"input": NumberInt("19"),
			"emit": NumberInt("19"),
			"reduce": NumberInt("1"),
			"output": NumberInt("9")
		},
		"ok": 1
	}
	// 生成结果：
	// 即 db.getCollection("wq").find() 的查询结果:
	{"_id":"user_1","value":11} // 仅 user_1 有多个，所以仅这一项取了 reduce 结果，下面都是直接取 map 里面 emit 的第二个参数值
	{"_id":"user_2","value":{"_id":2,"name":"user_2","age":2}}
	{"_id":"user_3","value":{"_id":3,"name":"user_3","age":3}}
	{"_id":"user_4","value":{"_id":4,"name":"user_4","age":4}}
	{"_id":"user_5","value":{"_id":5,"name":"user_5","age":5}}
	{"_id":"user_6","value":{"_id":6,"name":"user_6","age":0}}
	{"_id":"user_7","value":{"_id":7,"name":"user_7","age":1}}
	{"_id":"user_8","value":{"_id":8,"name":"user_8","age":2}}
	{"_id":"user_9","value":{"_id":9,"name":"user_9","age":3}}


	// 统计各 age 的数量
	db.runCommand(
	{
		mapreduce:'test',  // 操作的 collection/表 名称
		map:function(){emit(this.age, this);}, // emit 第一个参数是分组的key，第二个参数是传给 reduce 的 doc 内容
		reduce:function(key, docs){return docs.length;}, //注意：docs不是一个Object对象而是数组
		out:'wq' // 输出结果的 collection/表 名称，如果此表已存在则覆盖
	});
	// 执行结果：
	{
		"result": "wq",
		"timeMillis": NumberInt("153"),
		"counts": {
			"input": NumberInt("19"),
			"emit": NumberInt("19"),
			"reduce": NumberInt("6"),
			"output": NumberInt("6")
		},
		"ok": 1
	}
	// 生成结果：
	// 即 db.getCollection("wq").find() 的查询结果:
	{"_id":0,"value":3}
	{"_id":1,"value":4}
	{"_id":2,"value":3}
	{"_id":3,"value":3}
	{"_id":4,"value":3}
	{"_id":5,"value":3}


