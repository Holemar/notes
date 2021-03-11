
漂亮的打印出JSON
    JSON是一种非常好的数据序列化的形式，被如今的各种API和web service大量的使用。
    使用python内置的 json 处理，可以使JSON串具有一定的可读性，但当遇到大型数据时，它表现成一个很长的、连续的一行时，人的肉眼就很难观看了。

    为了能让JSON数据表现的更友好，我们可以使用indent参数来输出漂亮的JSON。
    当在控制台交互式编程或做日志时，这尤其有用：

    import json

    data = {"status": "OK", "count": 2, "results": [{"age": 27, "name": "Oz", "lactose_intolerant": True}, {"age": 29, "name": "Joe", "lactose_intolerant": False}]}
    print(json.dumps(data))  # No indention, 打印:{"status": "OK", "count": 2, "results": [{"age": 27, "name": "Oz", "lactose_intolerant": true}, {"age": 29, "name": "Joe", "lactose_intolerant": false}]}

    print(json.dumps(data, indent=2))
    # With indention, 打印如下:
    '''
    {
      "status": "OK",
      "count": 2,
      "results": [
        {
          "age": 27,
          "name": "Oz",
          "lactose_intolerant": true
        },
        {
          "age": 29,
          "name": "Joe",
          "lactose_intolerant": false
        }
      ]
    }
    '''

    print(json.dumps(data, separators=(',',':')))  # 输出时去掉分隔符的空格, 打印如下:
    #{"status":"OK","count":2,"results":[{"age":27,"name":"Oz","lactose_intolerant":true},{"age":29,"name":"Joe","lactose_intolerant":false}]}

    同样，使用内置的pprint模块，也可以让其它任何东西打印输出的更漂亮。
    参考： http://docs.python.org/2/library/pprint.html



字符串 转成 json
    import json
    json_input = '{ "one": 1, "two": { "list": [ {"item":"A"},{"item":"B"} ] } }'
    try:
        decoded = json.loads(json_input)
        # pretty printing of json-formatted string
        print json.dumps(decoded, sort_keys=True, indent=2)
        print "JSON parsing example: ", decoded['one']
        print "Complex JSON parsing example: ", decoded['two']['list'][1]['item']
    except (ValueError, KeyError, TypeError):
        print "JSON format error"


