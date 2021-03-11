#python
# -*- coding:utf-8 -*-
'''
本模块是 django model 所需的枚举专用
Created on 2015/12/11
Updated on 2019/7/15
@author: Holemar


使用说明：
    0.定义说明
        class Platform(Const):
            属性 = (值, 说明)
            属性 = {'value':值, 'label':说明}
            属性 = 说明 # 值 与 属性 相同的情况下(值与属性都定义为字符串)

    1.定义枚举类， 直接继承此文件的 Const 类即可， 如：

        # 属性 = (值, 说明)  的定义模式,且值是整形
        class Platform(Const):
            ios = (1, 'IOS')
            android = (2, 'ANDROID')
            wp = (3, 'WP')

        # 属性 = (值, 说明)  的定义模式,且值是字符串
        class LocationType(Const):
            asia = ('Asia', u'亚洲')
            europe = ('Europe', u'欧洲')
            america = ('America', u'美洲')
            australia = ('Australia', u'澳洲')

        # 属性 = {'value':值, 'label':说明}  的定义模式,值是整形或者字符串都允许
        class LocationType2(Const):
            asia = {'value':'Asia', 'label':'亚洲'}
            europe = {'value':'Europe', 'label':'欧洲'}
            america = {'value':'America', 'label':'美洲'}
            australia = {'value':'Australia', 'label':'澳洲'}

        # 属性 = 说明  的定义模式,且值跟属性一样
        class LocationType3(Const):
            asia = u'亚洲'
            europe = u'欧洲'
            america = '美洲'
            australia = '澳洲'


    2.在 model 中定义字段时， 可直接 new 枚举类， 如：

        from django.db import models
        class TestModel(models.Model):
            platform = models.PositiveSmallIntegerField('平台', choices=Platform(), db_index=True, default=Platform.android)
            location = models.CharField('用户所属地区', choices=LocationType(), max_length=20, blank=True, null=True)


    3.用来判断时， 直接点出枚举类对应的值即可：

        mo = TestModel()
        if mo.platform == Platform.android: print '这是安卓用户'


    4.获取对应的说明时， 用类的“get_FEILD_display”即可：

        mo = TestModel()
        plat_name = mo.get_platform_display()

        页面展示时：
        {{ object.get_platform_display }}


    5.获取对应的说明， 也可以由枚举类直接获取(用 _attrs, _values, _labels, _labels_to_values, _items 五个属性)：

        print( Platform.ios == 1 and Platform.android == 2 ) # 打印: True

        print( Platform._attrs[2] == 'ANDROID' ) # 打印: True
        print( Platform._attrs ) # 打印: {1: 'IOS', 2: 'ANDROID', 3: 'WP'}
        # 枚举类._attrs 返回 {值:说明}

        print( Platform._labels_to_values['ANDROID'] == 2 ) # 打印: True
        print( Platform._labels_to_values ) # 打印: {'ANDROID': 2, 'IOS': 1, 'WP': 3}
        # 枚举类._labels_to_values 返回 {说明:值} 。 与 _attrs 正好相反

        print( Platform._values['ios'] == 1 ) # 打印: True
        print( Platform._values ) # 打印: {'android': 2, 'ios': 1, 'wp': 3}
        # 枚举类._values 返回 {属性:值}

        print( Platform._labels['ios'] == 'IOS' ) # 打印: True
        print( Platform._labels ) # 打印: {'android': 'ANDROID', 'ios': 'IOS', 'wp': 'WP'}
        # 枚举类._labels 返回 {属性:说明}

        print( Platform() ) # 打印: [(1, 'IOS'), (2, 'ANDROID'), (3, 'WP')]
        print( Platform._items ) # 打印: [(1, 'IOS'), (2, 'ANDROID'), (3, 'WP')]
        # 枚举类._items 返回 [(值,说明), (值,说明)]

'''
import sys
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    basestring = unicode = str


class ConstType(type):
    def __new__(cls, name, bases, attrs):
        _values = {} # {属性:值}
        _labels = {} # {属性:说明}
        _attrs = {}  # {值:说明}
        _labels_to_values = {} # {说明:值}

        for k, v in attrs.items():
            if k.startswith('__'):
                continue
            if isinstance(v, (tuple, list)) and len(v) == 2:
                _values[k] = v[0]
                _labels[k] = v[1]
                _attrs[v[0]] = v[1]
                _labels_to_values[v[1]] = v[0]
            elif isinstance(v, dict) and 'label' in v and 'value' in v:
                _values[k] = v['value']
                _labels[k] = v['label']
                _attrs[v['value']] = v['label']
                _labels_to_values[v['label']] = v['value']
            elif isinstance(v, basestring):
                _values[k] = k
                _labels[k] = v
                _attrs[k] = v
                _labels_to_values[v] = k
            else:
                _values[k] = v
                _labels[k] = v

        obj = type.__new__(cls, name, bases, _values)
        obj._values = _values
        obj._labels = _labels
        obj._labels_to_values = _labels_to_values
        obj._attrs = _attrs
        obj._items = sorted(_attrs.items(), key=lambda k: k[0])
        return obj

    def __call__(cls, *args, **kw):
        return cls._items

"""
# 由于py2及py3的使用元类写法不一致，这里为了兼容且不引起编译报错，改用统一写法
if PY2:
    class Const(object):
        __metaclass__ = ConstType
elif PY3:
    class Const(object, metaclass=ConstType):  # 这样写，py2编译时会报错。
        pass
"""
Const = ConstType('Const', (object,), {})


# 布尔值是最常用的枚举，所以这里先写一个
class Boolean(Const):
    no = (0, '否')
    yes = (1, '是')


def get_enum_value(EnumModel, value):
    """
    获取枚举类里对应的值
    :param EnumModel: 枚举类，只支持上面Const类继承的枚举类
    :param value: 输入值，可以是枚举值，也可以是枚举说明或者枚举的属性
    :return: 对应的枚举值
    """
    enum_values = EnumModel._attrs.keys()
    if value in enum_values:
        return value
    if value in EnumModel._labels_to_values:
        return EnumModel._labels_to_values.get(value)
    if value in EnumModel._values:
        return EnumModel._values.get(value)
    # 上述方式都没法取到枚举值，说明不在正常选项范围内。下面是特例情况

    if isinstance(value, basestring):
        # 特例一： 说明，允许unicode和str两种类型
        _labels_to_values = {}
        for k, v in EnumModel._labels_to_values.items():
            if isinstance(k, str):
                _labels_to_values[unicode(k)] = v
            elif isinstance(k, unicode):
                _labels_to_values[str(k)] = v
        if value in _labels_to_values:
            return _labels_to_values.get(value)

        # 特例二： 属性，允许unicode和str两种类型
        _values = {}
        for k, v in EnumModel._values.items():
            if isinstance(k, str):
                _values[unicode(k)] = v
            elif isinstance(k, unicode):
                _values[str(k)] = v
        if value in _values:
            return _values.get(value)

    # 特例三： 所有值都是整形，且输入值也是整形的字符串时，强行将输入值转成整形。
    if isinstance(value, basestring) and value.isdigit():
        tem_value = int(value)
        if tem_value in enum_values:
            return tem_value
    # 实在无法获取时，返回None
    return None
