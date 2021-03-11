# -*- coding:utf-8 -*-
"""示例1: 使用 dict 减少数据库消耗"""

from bello_adam import ResourceDocument
from bello_adam.io.fields import IntField, ListField, StringField, DateTimeField, ObjectIdField
from bello_adam.models.user import User
from bello_adam.models.company import Company


class Account(ResourceDocument):
    user_id = ObjectIdField()
    company_id = ObjectIdField()
    level = IntField()
    name = StringField()


if __name__ == '__main__':
    # 直接查询对应的user和company，数据库消耗很大
    for account in Account.objects(level=1).all():
        user = User.objects(id=account.user_id).first()
        company = Company.objects(id=account.company_id).first()
        print(account.name, user.name, company.name)

    # 改用dict缓存，减少数据库消耗
    accounts = [a for a in Account.objects(level=1).all()]
    users = {str(u.id): u for u in User.objects(id__in=[a.user_id for a in accounts]).all()}
    companies = {str(c.id): c for c in Company.objects(id__in=[a.company_id for a in accounts]).all()}
    for account in accounts:
        user = users.get(str(account.user_id))
        company = companies.get(str(account.company_id))
        print(account.name, user.name, company.name)
