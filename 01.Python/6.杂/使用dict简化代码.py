# -*- coding:utf-8 -*-
"""示例2： 使用 dict 减少遍历，简化代码"""

category_map = [
    {
        "major": "技术",
        "minor": "后端开发",
        "detail": "python工程师",
        "channels": [
            {
                "name": "ciwei",
                "info": [
                    {
                        "key": "jobtype",
                        "value": "1"
                    },
                    {
                        "key": "sub_jobtype",
                        "value": "17"
                    },
                    {
                        "key": "mini_jobtype",
                        "value": "81"
                    }
                ]
            },
            {
                "name": "lagou",
                "info": [
                    {
                        "key": "firstType",
                        "value": "开发|测试|运维类"
                    },
                    {
                        "key": "positionType",
                        "value": "后端开发"
                    },
                    {
                        "key": "positionThirdType",
                        "value": "Python"
                    }
                ]
            }
        ]}
]


def get_category(major, minor, detail, channel):
    """获取职能分类值"""
    result = dict()
    for category in category_map:
        if major != category['major']:
            continue
        if minor != category['minor']:
            continue
        if detail != category['detail']:
            continue
        channels = category.get('channels', [])
        channel = next(filter(lambda x: x['name'] == channel, channels), {})
        info = channel.get('info', [])
        for key_value in info:
            result[key_value['key']] = key_value['value']
    return result


# 使用 dict 减少遍历，简化代码
category_map2 = {  # 对比上面的 category_map
    ("技术", "后端开发", "python工程师"):
        {"ciwei": {"jobtype": "1", "sub_jobtype": "17", "mini_jobtype": "81"},
         "lagou": {"firstType": "开发|测试|运维类", "positionType": "后端开发", "positionThirdType": "Python"}
         },
    ("高级管理", "高级管理", "CEO/总裁/总经理"):
        {"lagou": {"firstType": "综合职能|高级管理", "positionType": "高级管理职位", "positionThirdType": "CEO|总裁|总经理"},
         "zhipin": {"position": 150407, "positionCategory": "总裁/总经理/CEO"}
         },
}


# 对比上面的 get_category 函数
def get_category2(major, minor, detail, channel):
    """获取职能分类值"""
    return category_map2.get((major, minor, detail), {}).get(channel, {})


if __name__ == '__main__':
    print(get_category("技术", "后端开发", "python工程师", 'lagou'))
    print(get_category2("技术", "后端开发", "python工程师", 'lagou'))
