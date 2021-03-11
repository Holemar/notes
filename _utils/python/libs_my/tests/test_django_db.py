#!python
# -*- coding:utf-8 -*-
"""
公用函数(数据库处理) django_db.py 的测试
Created on 2016/2/26
Updated on 2019/1/18
@author: Holemar
"""
import logging
import unittest
import datetime

from __init__ import *
from django.db import models
from django.conf import settings


# 定义数据库连接(使用 sqlite3 的内存数据库，避免外部依赖)
settings.DATABASES = {
        'default': {
            # sqlite3 测试
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:', # 内存处理

            # MySQL 测试
            #'ENGINE': 'django.db.backends.mysql',
            #'NAME': 'test', 'HOST': '127.0.0.1', 'USER': 'root', 'PASSWORD': 'root', 'PORT': 3306,
        }
    }

# 必须先设配置，再导入 django_db，不然会报错
from libs_my import django_db

# 用 Filter 类获取日志信息
NOW_LOG_RECORD = None
class TestFilter(logging.Filter):
    def filter(self, record):
        global NOW_LOG_RECORD
        if record.levelno in (logging.WARN, logging.ERROR):
            NOW_LOG_RECORD = record # 把 Filter 获取到的日志信息传递出去，供测试使用
        return True
django_db.logger.addFilter(TestFilter())

# 定义 model，以供测试用
class Person_DB(models.Model):
    class Meta:
        db_table = 't_persons'
        app_label = 'test_db'

    created_at = models.DateTimeField(u'添加时间', db_column='c_created_at', default=None, null=True, blank=True, auto_now_add = True)
    updated_at = models.DateTimeField(u'更新时间', db_column='c_updated_at', default=None, null=True, blank=True, auto_now = True)
    name = models.CharField(u'人名', db_column="c_name", max_length = 20, default=None, null=True, blank=True)
    age = models.IntegerField(u'年龄', db_column="c_age", default=None, null=True, blank=True)


class Test_Django_db(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """测试这个类前的初始化动作"""
        super(Test_Django_db, cls).setUpClass()

        django_db.execute_sql("DROP TABLE IF EXISTS t_persons")
        # 创建表，这也同时测试了 create_table 创建表函数
        django_db.create_table(Person_DB)

    @classmethod
    def tearDownClass(cls):
        """测试这个类所有函数后的结束动作"""
        super(Test_Django_db, cls).tearDownClass()

        # 还原配置信息
        # 定义数据库连接(使用 sqlite3 的内存数据库，避免外部依赖)
        settings.DATABASES = {
                'default': {
                    # 使用 sqlite3 的内存数据库，避免外部依赖
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:', # 内存处理
                }
            }
        # 删除表
        django_db.execute_sql("DROP TABLE t_persons")


    def setUp(self):
        """初始化"""
        super(Test_Django_db, self).setUp()
        django_db.execute_sql("DELETE FROM t_persons")


    def test_insert_select_get(self):
        """增删改查测试"""
        rows = 0 # 总行数

        # INSERT
        logging.info(u'execute_sql 测试')
        row = django_db.execute_sql("INSERT INTO t_persons(c_name, c_age) values('张三', 15)")
        assert row == 1
        rows += 1

        # SELECT
        logging.info(u'select_sql 查询结果集 测试')
        result = django_db.select_sql('select * from t_persons')
        assert len(result) == 1

        logging.info(u'select_sql 查询一条 测试')
        result = django_db.select_sql('select * from t_persons', fetchone=True)
        assert isinstance(result, dict)

        logging.info(u'execute_sql tuple/list 参数 测试')
        now = datetime.date.today()
        row = django_db.execute_sql(u"INSERT INTO t_persons(c_name, c_age, c_created_at) values(%s, %s, %s)", (u'李奇',1011,now))
        assert row == 1
        row = django_db.execute_sql(u"INSERT INTO t_persons(c_name, c_age, c_created_at) values(%s, %s, %s)", [u'李奇2',22,now])
        assert row == 1
        rows += 2

        # 获取新增 id
        rowid = django_db.execute_sql(u"INSERT INTO t_persons(c_name, c_age, c_created_at) values(%s, %s, %s)", [u'李奇3',33,now], rowid=True)
        assert rowid == 4
        rows += 1

        if 'mysql' in settings.DATABASES['default']['ENGINE']:
            logging.info(u'execute_sql dict 参数 测试') # dict 参数在 sqlite3 数据库插入失败，换 MySQL 则成功
            row = django_db.execute_sql(u"INSERT INTO t_persons(c_name, c_age) VALUES (%(c_name)s, %(c_age)s)", {'c_name':u'莫名', 'c_age':66})
            assert row == 1
            rows += 1

        # UPDATE
        row = django_db.execute_sql(u"UPDATE t_persons set c_name=%s, c_age=%s, c_created_at=%s WHERE c_name=%s AND c_age=%s", ['李奇2', 151, now, u'李奇2', 22])
        assert row == 1

        result2 = django_db.select_sql('select * from t_persons')
        assert len(result2) == rows


        # executemany
        logging.info(u'executemany tuple/list 参数 测试')
        now = datetime.date.today()
        row = django_db.executemany(u"INSERT INTO t_persons(c_name, c_age, c_created_at) values(%s, %s, %s)", [(u'李四',2011,now), (u'李四2',2012,now), (u'李四3',2013,now)])
        assert row == 3
        row = django_db.executemany(u"INSERT INTO t_persons(c_name, c_age, c_created_at) values(%s, %s, %s)", [[u'王五',301,now],[u'王五2',302,now]])
        assert row == 2
        rows += 5
        result = django_db.select_sql('select count(*) c from t_persons', fetchone=True)
        assert isinstance(result, dict)
        assert result.get('c', 0) == rows


    def test_time_warn(self):
        """SQL超时警告测试"""
        global NOW_LOG_RECORD
        logging.info(u'SQL超时警告测试')

        # 超时时间改成必然超时的，以便测试
        _orig_warn_time = django_db.SQL_WARN_TIME
        django_db.SQL_WARN_TIME = -1

        # ORM 操作
        Person_DB(name = u"张三", age = 13).save()
        record = NOW_LOG_RECORD
        assert record is not None
        assert record.levelno == logging.WARNING
        assert u'SQL执行超时' in record.msg

        # 原生 SQL 测试(上面是ORM生成的SQL测试)
        row = django_db.execute_sql(u"INSERT INTO t_persons(c_name, c_age) values('张三', 15)")
        assert row == 1
        record = NOW_LOG_RECORD
        assert record is not None
        assert record.levelno == logging.WARNING
        assert u'SQL执行超时' in record.msg

        # 超时时间改成原时间，避免太多日志
        django_db.SQL_WARN_TIME = _orig_warn_time

    def test_except(self):
        """SQL出错日志测试"""
        global NOW_LOG_RECORD
        logging.info(u'SQL出错日志测试')
        has_error = False
        try:
            row = django_db.execute_sql(u"INSERT INTO t_persons(c_name c_age) values('张三', 15)")
        except Exception as e:
            has_error = True # 上面程序要求必须报错
        assert has_error
        record = NOW_LOG_RECORD
        assert record is not None
        assert record.levelno in (logging.WARN, logging.ERROR)
        assert u'SQL执行失败' in record.msg

    def test_get_table_name(self):
        """获取SQL操作的表名测试"""
        logging.info(u'获取SQL操作的表名测试')

        # 简单 select
        sql = "SELECT c_item_id,c_item_name FROM t_common_base_data where c_type='company_scale';"
        assert django_db.get_table_name(sql) == 't_common_base_data'

        # 多行 select
        sql = """SELECT c_item_id,c_item_name
        FROM
        t_common_base_data
        where
        c_type='company_scale';"""
        assert django_db.get_table_name(sql) == 't_common_base_data'


        sql = "SELECT `django_session`.`session_data`, `django_session`.`expire_date` FROM `django_session` WHERE (`django_session`.`session_key` = 'j77gx6huc7igtom0yosgp0w73ktgrrjj' AND `django_session`.`expire_date` > '2016-11-15 11:32:34');"
        assert django_db.get_table_name(sql) == 'django_session'

        sql = "SELECT `auth_user_info`.`c_id`, `auth_user_info`.`c_user_id`, `auth_user_info`.`c_mobile` FROM `ehr-admin`.`auth_user_info` WHERE `auth_user_info`.`c_user_id` = 1;"
        assert django_db.get_table_name(sql) == 'ehr-admin.auth_user_info'

        sql = "SELECT `t_company`.`c_id`, `t_company`.`c_fullname`, `t_company_social_security`.`c_housing_fund_weal_package_id` FROM `ehr-ucenter`.`t_company` LEFT OUTER JOIN `ehr-ucenter`.`t_user` ON ( `ehr-ucenter`.`t_company`.`c_owner_id` = `ehr-ucenter`.`t_user`.`c_id` ) LEFT OUTER JOIN `ehr-social-security`.`t_company_social_security` ON ( `ehr-ucenter`.`t_company`.`c_id` = `ehr-social-security`.`t_company_social_security`.`c_company_id` ) WHERE (`t_company`.`c_is_enabled` = 1 AND `t_company`.`c_emp_count` >= 1 AND `t_company`.`c_emp_count` <= 10000) ORDER BY `t_company`.`c_add_dt` DESC LIMIT 20;"
        assert django_db.get_table_name(sql) == 'ehr-ucenter.t_company'

        # 增删改
        sql = "INSERT INTO   table_name(id,name,price,vend_name) VALUES(11,'TV',222,'US'),(22,'ss',12.22,'kk');"
        assert django_db.get_table_name(sql) == 'table_name'

        sql = "UPDATE   table1,table2 SET table2.column_name = expression,table1.prod_name = 'NEWCOMPUTER' [WHERE];"
        assert django_db.get_table_name(sql) == 'table1'

        sql = "UPDATE `ehr-op`.t_calendar_receive_record trr JOIN `ehr-op`.t_calendar_awards_record tar ON tar.c_id = trr.c_awards_record_id SET c_mch_billno = 'RP20170117103552211133138' WHERE c_open_id = 'o2qj_w_s85omz-9dRBNynm7m1TSk' AND tar.c_promotion_id ='05c730c996dc47fa8546bd75b84cc238';"
        assert django_db.get_table_name(sql) == 'ehr-op.t_calendar_receive_record'

        sql = "DELETE FROM `ehr-support`.t_action_message WHERE c_scene_code IN ('company_accredit_fail', 'company_accredit_success');"
        assert django_db.get_table_name(sql) == 'ehr-support.t_action_message'

        sql = "ALTER TABLE mytable Modify col_name varchar(100)"
        assert django_db.get_table_name(sql) == 'mytable'

        sql = "CREATE [UNIQUE] INDEX index_name ON   mytable(column [, column]…);"
        assert django_db.get_table_name(sql) == 'mytable'

        sql = "SELECT COUNT('*') FROM (SELECT DISTINCT `t_employee_attachment`.`c_company_id` AS Col1 FROM `t_employee_attachment` INNER JOIN `t_employee_info` ON ( `t_employee_attachment`.`c_employee_id` = `t_employee_info`.`c_id` ) WHERE (`t_employee_attachment`.`c_add_dt` <= '2017-06-26 23:59:59' AND `t_employee_info`.`c_is_delete` = 0 AND `t_employee_attachment`.`c_add_dt` >= '2017-06-26 00:00:00' AND NOT ((`t_employee_attachment`.`c_company_id`) IN (SELECT DISTINCT U0.`c_company_id` FROM `t_employee_attachment` U0 WHERE U0.`c_add_dt` <= '2017-06-26 00:00:00') AND `t_employee_attachment`.`c_company_id` IS NOT NULL))) subquery"
        assert django_db.get_table_name(sql) == 't_employee_attachment'


if __name__ == "__main__":
    unittest.main()

