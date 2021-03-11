
mongoengine 提供对 MongoDB 的 ORM 操作

1. 连接数据库
   如果我们的 MongoDB 是直接在本地电脑上面运行的，可以使用以下代码来连接到电脑上的 MongoDB 数据库：

    from mongoengine import connect
    connect('数据库名')
    # 如果数据库需要身份验证
    connect('数据库名', username='webapp', password='pwd123')

   如果MongoDB不是运行在本地电脑上面的，就需要指定ip 地址和端口：

    from mongoengine import connect
    connect('数据库名', host='192.168.2.12', port=3456)

    # 如果数据库需要身份验证
    connect('数据库名', host='192.168.2.12', port=3456, username='webapp', password='pwd123')

    # 方式三：
    connect('数据库名', host='mongodb://localhost:27017/数据库名')
    connect('数据库名', host='mongodb://用户名:密码@10.0.0.90:27017/数据库名?authSource=admin')

    # 密码特殊符号的坑,由于连接字符串是拼接形式，所以特殊符号需要编码后拼接进去
    from urllib.parse import quote
    connect('数据库名', host=f'mongodb://{用户名}:{quote("密码")}@{quote("域名")}:27017/{数据库名}?authSource=admin')


2. 定义 model

    import datetime
    from mongoengine import *
    from bson import ObjectId

    SEX_CHOICES = (
        ('male','男'),
        ('female','女')
    )

    #成绩
    class Grade(EmbeddedDocument):
        name = StringField(required=True)
        score = FloatField(required=True)

    class People(Document):
        source_id = ObjectIdField(primary_key=True, default=ObjectId)  # 指定为主键。也可以指定 int 或者其它类型的主键。不指定则默认 _id 作为主键，且是 ObjectId类型
        name = StringField(required=True, unique=True)  # required=True 表示是必须填写的参数, unique=True 表示值唯一
        age = IntField()
        documentTTL = IntField(default=0) # 不指定默认值的话，默认空值而不是0
        keyword = StringField(index_type='keyword', unique_with=['title'])  # 创建索引，且指定索引类型。 unique_with指定联合唯一键
        sex = StringField(choices=SEX_CHOICES)  # 枚举类型
        status = StringField(default='pending', choices=['pending', 'running', 'error', 'deleted']) # 枚举 + 默认值
        score = FloatField()
        email = EmailField()
        is_tongzhao = BooleanField(db_field='is_tz') # 指定数据库对应字段名
        title = StringField(max_length=200)  # 指定最大字符串长度
        created = DateTimeField(default=datetime.datetime.utcnow)
        expires_at = DateTimeField(default=lambda: datetime.datetime.utcnow()+datetime.timedelta(seconds=30)) # 时间类型，且指定默认值
        # dict
        # 字典可以存储复杂的数据，其他字典，列表，对其他对象的引用，所以是最灵活的可用字段类型
        school_name_props = DictField(verbose_name='学校经历') # verbose_name指定名称
        options = DictField(default={})
        # list
        gaps = ListField(field=StringField())  # list 类型，且 list 里面是字符串
        tags = ListField(StringField(max_length=50))
        values = ListField(IntField(), default=list) # 默认空列表
        values2 = ListField(IntField(), default=lambda: [1,2,3]) # 指定默认列表内容
        # 外键
        user = LazyReferenceField(document_type='Manager', db_field='user_id') # 外键关联,document_type指向外键对应的model,db_field指定本类字段名
        messages = ReferenceField(document_type='Message', relation_type='has_many', target_field='account') # 一对多的外键
        grades = ListField(EmbeddedDocumentField(Grade))
        boss = ReferenceField('self')  # 引用文档自身，使用该字符串'self'代替文档类作为 ReferenceField 构造函数的参数。

        # 额外设置，不是必须的
        meta = {
            'db_alias': 'importer',  # db_alias用于指定model绑定的mongo连接，和connect函数中的alias对应，也可以说是 库名
            'collection': 'students', # 设置集合名称， 也可以说是 表名
            'ordering': ['-age'], # 设置默认排序方式
            'allow_inheritance': True,  # 可以继承
            'abstract': True,  # 抽象类
            'strict': False,  # 严格模式。当 strict 为 True 时, save 的时候传入多余字段会报错
            'indexes': [ # 设置索引
                'title',
                '$title',  # 文本索引
                '#title',  # 散列索引
                ('title', '-keyword'), # 联合索引
                #('age', '_cls'), # cls（默认值：True） 如果您有多态模型可以继承并 allow_inheritance打开，则可以配置索引是否应该将该_cls字段自动添加到索引的开头
                {
                    'fields': ['created'], # 要索引的字段。与上述相同的格式指定。
                    'expireAfterSeconds': 3600, # 允许您通过设置以秒为单位的时间过期来自动将某个字段中的数据过期
                },
                {'fields': ('mobile', 'name'), 'unique': True}  # 设置 唯一、联合唯一
            ],
            'max_documents': 1000,  # 限制文档的数量
            'max_size': 2000000,  # 限制文档的大小
        }

        # 文档调用 save()时，如果定义了clean，会先调用clean
        def clean(self):
            if self.status == 'Draft' and self.pub_date is not None:
                msg = 'Draft entries should not have a publication date.'
                raise ValidationError(msg)
            # Set the pub_date for published items if not set.
            if self.status == 'Published' and self.pub_date is None:
                self.pub_date = datetime.now()

    2.1 公共field字段选项
        db_field: 数据库中实际的字段名称， 如果未指定，取当前的变量名称。
        required: 是否必填
        default: 默认值
        null: 赋值是否可以为空
        max_length: 最大长度(字符串用到)
        unique: 字段在表中是否唯一
        unique_with: 联合唯一键可以参照下面name的定义，name = StringField(unique_with="mobile")，这样可以name和mobile可以成为联合唯一键
        choices: 可选值, 例如 name = StringField(unique_with="mobile", choices=["lisi", "wangwu"])
        primary_key: 是否定义为主键。默认False，如果为True, 则这个字段具备唯一性，如果插入两条同样的数据，则以后面的那条数据为准，会覆盖前一条字段一样的数据。


    2.2 可用的字段类型如下所示:
        BinaryField # 二进制数据字段
        BooleanField
        ComplexDateTimeField
        DateTimeField
        DecimalField
        DictField
        DynamicField
        EmailField
        EmbeddedDocumentField
        EmbeddedDocumentListField
        FileField GridFS存储字段
        FloatField
        GenericEmbeddedDocumentField
        GenericReferenceField # 允许引用任何类型的Document, 效率稍低于标准 ReferenceField
        GenericLazyReferenceField
        GeoPointField
        ImageField # 图像文件存储区域
        IntField
        ListField
        LineStringField
        MapField
        ObjectIdField
        ReferenceField  # 会自动加载
        LazyReferenceField  # ReferenceField 会导致性能的问题，推荐使用 LazyReferenceField
            # LazyReferenceField 的参数 passthrough: 如果在获取某个field的时候不想 fetch, 则需要将 passthrough 设置为 True
        SequenceField
        SortedListField
        StringField
        URLField
        UUIDField
        PointField
        PolygonField
        MultiPointField
        MultiLineStringField
        MultiPolygonField
   
    2.3 reverse_delete_rule 处理引用文档的删除
        mongoengine.DO_NOTHING = 0  # 默认值，没有任何动作。
        mongoengine.NULLIFY = 1  # 将外键置空
        mongoengine.CASCADE = 2  # 级联删除。引用字段被删除，则引用此字段的文档也会被删除
        mongoengine.DENY = 3  # 如果仍存在对被删除对象的引用，则拒绝删除。
        mongoengine.PULL = 4  # 从ListField（ReferenceField）的任何对象的字段中删除对该对象的引用（使用MongoDB的“拉”操作 ）。

        现在设置成除DO_NOTHING之外的其他值，保存的时候会报错：
        例如如果设置成 new_company = ReferenceField(document_type="Company", reverse_delete_rule=mongoengine.NULLIFY)
        则会报下面的错误
            mongoengine.errors.ValidationError: ValidationError (User:None) (A ReferenceField only accepts DBRef, LazyReference, ObjectId or documents: ['new_company'])

        可以选择注册的方式来实现：
        class Company(ResourceDocument):
            name = StringField()

        class User(ResourceDocument):
            name = StringField()
            mobile = StringField()
            new_company = ReferenceField(document_type="Company", db_field="new_company_id")

        # 在程序启动的时候注册级联删除规则
        Company.register_delete_rule(User, 'new_company', NULLIFY)


3. 创建对象

    kingname = People(name='kingname', age=18, sex='male', score=99999) 
    kingname.save()

    # 当然，我们也可以这样写：
    kingname = People(name='kingname', age=18, sex='male')
    kingname.score = 99999
    kingname.save()

    # 也可以用 create 函数创建
    b = People.objects.create(name='User A', age= 40)

4. 读取对象

    # 读取所有的用户：
    for person in People.objects:
        print(person.name)

    # 按条件搜索也非常简单，在 objects 里面加参数即可，例如搜索所有年龄为22岁的人：
    for person in People.objects(age=22):
        print(person.name)

    # 查询第一条数据
    obj = People.objects.first()
    obj = People.objects.filter(name="xx").first()
    obj = People.objects(name="xx").first() # 进一步优化
    # get 也可以查询出一条数据，但需要注意它的报错。查询不到时报错 People.DoesNotExist
    obj = People.objects.get(name="xx")

    # 查询多条数据
    objects = People.objects.all()

    # 根据ID获取数据
    obj = People.objects.filter(pk=oid)

    # 排序
    # order_by 函数指定，+或者没符号表示升序，-表示降序
    first_post = People.objects.order_by("+created").first()

    # 查询结果个数限制
    # 跟传统的ORM一样，MongoEngine也可以限制查询结果的个数。一种方法是在QuerySet对象上调用limit和skip方法；另一种方法是使用数组的分片的语法。例如：
    users = User.objects[10:15]  # 下标从 0 开始
    users = User.objects.skip(10).limit(5)  # skip 下标从 0 开始

5. 修改数据
    # 修改多条
    People.objects.filter(sex='male', age__gte=16).update(inc__age=10)  # 年龄大于等于16岁的女人，年龄加10

    # 修改一条数据, 只修改匹配到的第一条
    People.objects.filter(sex='male').update_one(inc__age=100)

    # save 修改
    obj = People.objects.filter(sex='male').first()
    obj.age = 20
    obj.save()  # 会产生一个 ValidationError 错误
    obj.save(validate=False) # 不会抛出 ValidationError


    # dict 和 list 类型修改的神坑
    obj = People.objects.filter(name="kingname").first()
    d = {}
    l = []
    obj.school_name_props = d
    obj.tags = l
    d['aa'] = 5555
    l.append('3333')
    print(obj.school_name_props)  # 打印：{'aa': 5555}
    print(obj.tags)  # 打印: ['3333']
    obj.save()
    obj.reload() # 重新读取并加载数据库的本行数据
    print(obj.school_name_props)  # 打印: {}
    print(obj.tags)  # 打印: []
    # 个人认为，是这个orm框架捕获了赋值事件，读取赋值时的值，而不是读取赋值的引用。
    # 所以保存时，其实还是取了刚赋值时的值，导致引用修改无效。需要在值修改后再赋值才生效。如下：
    obj = People.objects.filter(name="kingname").first()
    d = {}
    l = []
    d['aa'] = 5555
    l.append('3333')
    obj.school_name_props = d
    obj.tags = l
    obj.save()
    obj.reload()
    print(obj.school_name_props)  # 打印：{'aa': 5555}
    print(obj.tags)  # 打印: ['3333']


5.1. 自动更新 
    你而已对一个QuerySet()使用update_one()或update()来实现自动更新，有一些可以与这两个方法结合使用的操作符

    set – 设置成一个指定的值强调内容
    unset – 删除一个指定的值
    inc – 将值加上一个给定的数
    dec – 将值减去一个给定的数
    pop – 将 list 里面的 最前/最后 一项移除。 传参 1 是移除最后一项，传参 -1 是移除最前一项，只能传这两个参数
    push – 在 list 最后添加一个值
    push_all – 在 list 里面添加好几个值， 要求传参是 list 。
    pull – 将一个值从 list 里面移除, 参数不存在不会报错。
    pull_all – 将好几个值从 list 里面移除， 要求传参是 list, 参数不存在不会报错。
    add_to_set – 如果list里面没有这个值，则添加这个值自动更新的语法与查询的语法基本相同，区别在于操作符写在字段之前：*

    # 下面这两句效果完全一样
    People.objects.filter(sex='male').update_one(set__age=10)
    People.objects.filter(sex='male').update(age=10)

    # age 值被设成 null，这里写的 10 并不起任何作用
    People.objects.filter(sex='male').update_one(unset__age=10)
    # age 为null时也可以减，当作 0 来看待
    People.objects.filter(sex='male').update_one(dec__age=10)

    # pop 只能传值 1 和 -1， 1是移除最后一项， -1是移除最前一项
    People.objects.filter(sex='male').update_one(pop__values2=1)
    People.objects.filter(sex='male').update_one(pop__values2=-1)
    # push 把值添加到 list 的最后面，相当于 list.append 操作
    People.objects.filter(sex='male').update_one(push__values2=-3)
    # push_all 要求传参是 list，且并非每个版本都支持，我的 pymongo 3.5.0 就运行不了，报错： pymongo.errors.WriteError: Unknown modifier: $pushAll
    People.objects.filter(sex='male').update_one(push_all__values2=[5,6,7])

    # 查询出来的 object 实例也可以执行 自动更新。
    obj = People.objects.filter(sex='male').first()
    print(obj.values2)
    # pull 删除参数在 list 里面的值，参数不存在则没有影响，不报错。
    obj.update(pull__values2=3)
    # pull_all 要求传参是 list, 参数不存在不会报错。
    obj.update(pull_all__values2=[3,1])
    # add_to_set 值不存在则添加到最后一项，已存在则不再添加。
    obj.update(add_to_set__values2=55)
    obj.reload()
    print(obj.values2)

6. 删除记录
    如果你想删除记录，那就先把记录找出来，然后调用 delete() 方法吧：

    # 删除一条数据
    People.objects.filter(sex='male').first().delete()

    # 删除多条数据
    People.objects.filter(sex='female').delete()

7. with_id使用
    # mongo默认id类型为ObjectId，所以使用id查询时，需将str转换为 ObjectId
    from bson import ObjectId
    obj = People.objects.get(pk=ObjectId(user_id))
    # 实测发现，直接写字符串也是支持的，会自动转换成 ObjectId
    obj = People.objects.get(pk='5d70f47bd8941f0e2733c6c2')
    # 优化
    obj = People.objects.with_id(user_id)

8. 复杂条件
    # contains 包含，icontains 包含(忽略大小写), 不包含 not__contains
    # 模糊检索时对象属性包含所查询字符,如name为abc,输入ab
    user = User.objects.filter(name__contains=search_str)
    user = User.objects.filter(name__not__contains="aa")

    # in 查询
    set_role = Role.objects.filter(pk__in=[i.pk for i in role_list if i])

    # 列举出各函数
    __exact  # 精确等于 like 'aaa'
    __iexact  # 精确等于 忽略大小写 ilike 'aaa'
    __contains  # 包含 like '%aaa%'
    __icontains  # 包含 忽略大小写 ilike '%aaa%'，但是对于sqlite来说，contains的作用效果等同于icontains。
    __gt  # 大于
    __gte  # 大于等于
    __lt  # 小于
    __lte  # 小于等于
    __in  # 存在于一个list范围内
    __nin  # 值不在列表中(索引不会生效，全表扫描)
    __startswith  # 以…开头
    __istartswith  # 以…开头 忽略大小写
    __endswith  # 以…结尾
    __iendswith  # 以…结尾，忽略大小写
    __ne  # 不相等
    __not  # 取反
    __all  # 与列表的值相同
    __mod  # 取模
    __size  # 数组的大小
    __exists  # 字段的值存在
    __match  # 使你可以使用一整个document与数组进行匹配查询list
    #对于大多数字段，这种语法会查询出那些字段与给出的值相匹配的document，但是当一个字段引用 ListField 的时候，而只会提供一条数据，那么包含这条数据的就会被匹配上：

    # 上面没有判断是否为空的函数，所以改成下面的判断
    __ne=None

    # 多条件组合的 Q
    # 它可以将多个查询条件进行 &(与) 和 |(或) 操作。
    from mongoengine.queryset.visitor import Q
    # 例如下面的语句是查询所有年龄大于等于18岁的英国用户，或者所有年龄大于等于20岁的用户。
    User.objects((Q(country='uk') & Q(age__gte=18)) | Q(age__gte=20))


    class Page(Document):  
        tags = ListField(StringField())  

    # 普通查询
    Page.objects(tags='coding')

    # 可以通过list的位置来进行查询，你可以使用一个数字来作为查询操作符，例子如下
    Page.objects(tags__0='db')

    #如果你只是想取出list中的一部分，例子如下：
    # comments - skip 5, limit 10  
    Page.objects.fields(slice__comments=[5, 10])

    # 更新document的时候，如果你不知道在list中的位置，你可以使用 $ 这个位置操作符
    Post.objects(comments__by="joe").update(**{'inc__comments__$__votes': 1})

    # 可是，如果这种映射不能正常工作的时候可以使用大写 S 来代替：
    Post.objects(comments__by="joe").update(inc__comments__S__votes=1)


8.1. 聚合
    # 统计结果个数即可以使用QuerySet的count方法，也可以使用Python风格的方法：
    num_users = len(User.objects)
    num_users = User.objects.count()

    # 求和
    yearly_expense = Employee.objects.sum('salary')
    # 求平均数
    mean_age = User.objects.average('age')

    # item_frequencies 的使用
    # 文档是这么写的:返回整个查询文档集中字段存在的所有项的字典及其对应的频率，即某字段所有值的集合(去重)和结果出现次数，简单来说就是group_by
    objects = People.objects.all()
    objects.item_frequencies('status')
    # 结果如： {'pending':50, 'running':1, 'error':33}

    # scalar 获取所查询的字段值的列表
    People.objects.scalar('name')
    # 结果如： ["kitty", "lily", "john"]

    # in_bulk 通过索引列表获取queryset
    result = Role.objects(pk__in=ids) # 不使用in_bulk
    # 使用in_bulk
    ids = [ObjectId(i) for i in ids]
    documents = Role.objects.in_bulk(ids)
    results = [documents.get(obj_id) for obj_id in ids]
    # 注意： 列表生成式会导致list类型发生变化，无法继续filter

9. model转dict
    user = User.objects.get(name="xxx")
    # 需注意的是，若将此功能作为结果集的serializer使用，不应该包含外键关联字段
    # 用fields方法过滤指定字段也不起作用
    user_dict = user.to_mongo().to_dict()

    # Serializer 处理
    # todo: 外键、list和dict、嵌套model等 情况还需要考虑
    def mongo_to_dict(obj, fields=None, exclude=None):
        """mongo的model转成dict
        :param exclude: 要排除的字段列表
        :param fields: 只返回指定的字段列表
        """
        model_dict = obj.to_mongo().to_dict()
        if fields:
            exclude = list(exclude) if exclude else []
            exclude.extend(list(set(model_dict.keys()) - set(fields)))
        if exclude:
            assert isinstance(exclude, (list, tuple, set))
            list(map(model_dict.pop, exclude))
        if "_id" in model_dict.keys():
            model_dict["_id"] = str(model_dict["_id"])
        return model_dict

10. 使用pymongo语法
    使用名称 Model 作为您在实例中为连接定义的实际类的占位符：

    Model._get_collection().aggregate([
        { '$group' : 
            { '_id' : { 'carrier' : '$carrierA', 'category' : '$category' }, 
              'count' : { '$sum' : 1 }
            }
        }
    ])

    所以你可以随时访问 pymongo 对象而不建立单独的连接. Mongoengine 本身建立在 pymongo 上.
    # 示例

    # 标签数量大于3的学生
    class Tag(documents):
      name = StringField()

    class Student(documents):
      name = StringField()
      tag = ListField(ReferenceField(Tag))

    # 使用原生查询
    db.student.find({ "tag.3" : { "$exists" : 1 } })
    # ORM查询
    Student.objects(__raw__={ "tag.3":{ "$exists":1}})

    # 姓名相同的学生数量
    # 原生mongo
    db.getCollection("student").aggregate([
        {"$match":{"status":0}},
        {"$sortByCount":"$name"},
        {"$match":{"count":{"$gt":1}}}
    ]).itcount()

    # ORM
    a = Student._get_collection().aggregate([
        {"$match":{"status":0}},
        {"$sortByCount":"$name"},
        {"$match":{"count":{"$gt":1}}}
    ])
    l = list(a)


    # 实例1:
    from bson import ObjectId
    class Message(documents):
        account = LazyReferenceField(document_type='Account', db_field='account_id') # 外键关联，注意数据库字段是 account_id
        filter_status = StringField(default='pending', choices=['pending', 'filtered', 'un_filtered'])  # 邮件是否被过滤掉
        # 其它字段...

    collection = Message._get_collection()
    account_ids = [ObjectId('5df2153ede3ffb0001dd70f8'), ObjectId('5df1b3b961414d0001afa9fd'), ObjectId('5def1e34d8941f08fdf932b0')]
    # 按 account_id 分组,得注意下面写的是 account_id 而不是字段名 account
    sync_counts = collection.aggregate([
        {"$match": {"account_id": {"$in": account_ids}}},
        {'$group': {"_id": "$account_id", "count": {"$sum": 1}}},
    ], allowDiskUse=True)
    # 由于没法把两个不同条件的分组合并，只好分开两次查询
    unfiltered_counts = collection.aggregate([
        {"$match": {"account_id": {"$in": account_ids}, "filter_status": 'un_filtered'}},
        {'$group': {"_id": "$account_id", "count": {"$sum": 1}}},
    ], allowDiskUse=True)
    # 遍历结果
    result = {}  # 格式为: {'account_id': {'sync_count':值1, 'unfiltered_count':值2}}
    for item in sync_counts:
        # 返回结果的 item.get('_id') 是 ObjectId 类型，好在 dict 支持它做key
        result.setdefault(item.get('_id'), {})['sync_count'] = item.get('count')
    for item in unfiltered_counts:
        result.setdefault(item.get('_id'), {})['unfiltered_count'] = item.get('count')


    # 实例2(以不同方式实现实例1的功能,共用实例1的Model):
    collection = Message._get_collection()
    reduce = 'function(doc,prev){prev.sync_count++;if(doc.filter_status=="un_filtered")prev.unfiltered_count++;}'
    counts = collection.group(key={"account_id": 1},
                              condition={"account_id": {"$in": account_ids}},
                              initial={'sync_count': 0, 'unfiltered_count': 0},
                              reduce=reduce)
    result = {}  # 格式为: {'account_id': {'sync_count':值1, 'unfiltered_count':值2}}
    for item in counts:
        account_id = item.pop('account_id')
        # 计算后结果会有小数，这里改回 int 类型
        for k, v in item.items():
            item[k] = int(v)
        result[account_id] = item


11. 在服务器端执行javascript代码
    # 通过MongoEngine QuerySet对象的 exec_js 方法可以将javascript代码作为字符串发送给服务器端执行，然后返回执行的结果。
    User.objects.exec_js("db.getCollectionNames()")  # 查询该数据库都有那些集合

