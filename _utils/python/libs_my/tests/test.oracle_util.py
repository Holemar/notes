#!python
# -*- coding:utf-8 -*-
"""
公用函数(数据库处理) oracle_util.py 的测试
Created on 2019/8/1
Updated on 2019/8/2
@author: Holemar
"""
import os
import logging
import unittest
import time, datetime

from __init__ import *
from libs_my import oracle_util


def test_init(DB_CONFIG):
    """测试前的初始化数据库表
    :param DB_CONFIG:数据库配置
    """
    oracle_util.set_conn(DB_CONFIG)
    assert oracle_util.ping()

    # 建表
    oracle_util.execute('drop table t_test_table')
    oracle_util.execute(u"""
        CREATE TABLE t_test_table(
            user_id int PRIMARY KEY NOT NULL,
            playlist_id NUMBER(10) default 0 NOT NULL,
            value NUMBER(10, 2) default 4 NOT NULL,
            circle_code VARCHAR2(18) default '-' NOT NULL,
            status VARCHAR2(10) default 'active' CHECK( status IN ('active','inactive') ),
            last_use_time DATE DEFAULT sysdate NOT NULL,
            update_date DATE default sysdate NOT NULL
        ) """)


def test_end():
    """测试结束后，删除测试表，避免遗留测试痕迹"""
    oracle_util.execute('drop table t_test_table')


class OracleToolsTest(unittest.TestCase):
    db = oracle_util

    def setUp(self):
        """初始化"""
        super(OracleToolsTest, self).setUp()
        self.assertTrue(self.db.ping())

    def tearDown(self):
        """销毁"""
        logging.warning(u'%s 类清空数据表,避免影响别的测试用例。。。', self.class_name)
        self.assertTrue(self.db.ping())
        self.db.execute("TRUNCATE TABLE t_test_table")
        result = self.db.select('select * from t_test_table')
        self.assertEqual(len(result), 0)
        super(OracleToolsTest, self).tearDown()

    def test_insert_select_get(self):
        # 插入一条
        logging.warning('execute 测试')
        rows = self.db.execute("insert into t_test_table(user_id, playlist_id, status) values(1, 1, 'inactive')")
        self.assertEqual(rows, 1, 'execute 新增 返回值不合格')

        logging.warning('select 测试')
        result = self.db.select('select * from t_test_table')
        self.assertTrue(isinstance(result, (tuple, list)), 'select 返回类型不合格')
        self.assertEqual(len(result), 1)
        self.assertTrue(isinstance(result[0], dict))
        self.assertEqual(result[0].get('PLAYLIST_ID'), 1)
        self.assertEqual(result[0].get('STATUS'), 'inactive')

        logging.warning('get 测试')
        result = self.db.get('select * from t_test_table')
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(result.get('PLAYLIST_ID'), 1)
        self.assertEqual(result.get('STATUS'), 'inactive')

        logging.warning('execute 插入时间 测试')
        rows = self.db.execute(
            "INSERT INTO t_test_table(user_id, playlist_id,status,update_date) VALUES (2, :playlist_id, :status, :update_date)",
            {'status': 'active', 'playlist_id': 66, 'update_date': datetime.datetime.now()})
        self.assertEqual(rows, 1)

        # 不支持 time 类型及 字符串类型
        rows = self.db.execute(
            "INSERT INTO t_test_table(user_id, playlist_id,status,update_date) VALUES (3, :playlist_id, :status, :update_date)",
            {'status': 'inactive', 'playlist_id': 55, 'update_date': datetime.date.today()})
        self.assertEqual(rows, 1)

        logging.warning('execute 插入中文 测试')
        rows = self.db.execute(
            "INSERT INTO t_test_table(user_id, playlist_id, circle_code) VALUES (4, :playlist_id, :circle_code)",
            {'playlist_id': 24, 'circle_code': '中文字符'})
        self.assertEqual(rows, 1, 'execute 插入中文 返回值不合格')
        result = self.db.get('select * from t_test_table where user_id=:1', 4)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(result.get('CIRCLE_CODE'), '中文字符')

        logging.warning('select 测试')
        result = self.db.select('select * from t_test_table')
        self.assertTrue(isinstance(result, (tuple, list)))
        self.assertEqual(len(result), 4)
        self.assertTrue(isinstance(result[0], dict))

    def test_rowid_select(self):
        # 获取 rowid
        logging.warning('execute 获取 rowid 测试')
        now = datetime.datetime.now()
        rowid = self.db.execute(
            "insert into t_test_table(user_id, status, playlist_id, last_use_time) values(:1, :2, :3, :4)",
            (4, 'active', 1011, now))
        self.assertEqual(rowid, 1)

        rowid = self.db.execute(
            "insert into t_test_table(user_id, status, playlist_id, last_use_time) values(5, :status, :playlist_id, :last_use_time)",
            {'status': 'active', 'playlist_id': 1011, 'last_use_time': now})
        self.assertEqual(rowid, 1)

        rowid = self.db.execute(
            "insert into t_test_table(user_id, status, playlist_id, last_use_time) values(6, :1, :2, :3)",
            ('active', 1011, now))
        self.assertEqual(rowid, 1)

        rows = self.db.execute(
            "insert into t_test_table(user_id, playlist_id, status, last_use_time) values(7, 1, 'inactive', to_date('2019-07-28 13:54:11', 'yyyy-mm-dd hh24:mi:ss'))")
        self.assertEqual(rows, 1)

        result = self.db.select('select * from t_test_table')
        self.assertEqual(len(result), 4)

        # 查询参数
        logging.warning('select 参数测试')
        result = self.db.select('select * from t_test_table where playlist_id=:1', [1011])
        self.assertEqual(len(result), 3)

        result = self.db.select("SELECT * FROM t_test_table WHERE status=:status AND playlist_id=:playlist_id",
                                param={'status': 'active', 'playlist_id': 1})
        self.assertEqual(len(result), 0)

        result = self.db.select("SELECT * FROM t_test_table WHERE status=:1 AND playlist_id=:2", param=['active', 1011])
        self.assertEqual(len(result), 3)

        # fetchone 指定查询结果返回数量
        result = self.db.select("SELECT * FROM t_test_table ")
        self.assertEqual(len(result), 4)
        result = self.db.select("SELECT * FROM t_test_table ", fetchone=2)
        self.assertEqual(len(result), 2)
        # True 与 1 的区分
        result = self.db.select("SELECT * FROM t_test_table ", fetchone=True)
        self.assertTrue(isinstance(result, dict))
        result = self.db.select("SELECT * FROM t_test_table ", fetchone=1)
        self.assertTrue(isinstance(result, dict))
        # False 与 0 的区分
        result = self.db.select("SELECT * FROM t_test_table ", fetchone=0)
        self.assertEqual(len(result), 4)
        result = self.db.select("SELECT * FROM t_test_table ", fetchone=False)
        self.assertEqual(len(result), 4)

    def test_executemany(self):
        # executemany
        logging.warning('executemany 测试')
        rows = self.db.executemany("INSERT INTO t_test_table(user_id, circle_code,playlist_id) VALUES (:1, :2, :3)",
                                   [(21, u"a'e''呵呵", 11), (22, 'a', 12), (23, 'a', 13)])
        self.assertEqual(rows, 3, 'executemany返回值不合格')
        result = self.db.select('select * from t_test_table where circle_code=:1', 'a')
        self.assertEqual(len(result), 2)
        result = self.db.select('select * from t_test_table where circle_code=:1', '-')
        self.assertEqual(len(result), 0)

        rows = self.db.executemany(
            "INSERT INTO t_test_table(user_id, playlist_id,status,update_date) VALUES (:user_id, :playlist_id, :status, :update_date)",
            [{'user_id': 8, 'status': 'inactive', 'playlist_id': 55, 'update_date': datetime.date.today()},
             {'user_id': 9, 'status': 'active', 'playlist_id': 66, 'update_date': datetime.datetime.now()}])
        self.assertEqual(rows, 2)

        result = self.db.select('select * from t_test_table where circle_code=:1', '-')
        self.assertEqual(len(result), 2)

    def test_execute_list(self):
        # execute_list
        logging.warning('execute_list 测试')
        rows = self.db.execute_list([
            "insert into t_test_table(user_id, playlist_id, status) values(10, 33, 'inactive')",
            "insert into t_test_table(user_id, playlist_id, status) values(11, 44, 'inactive')"
        ], must_rows=True)
        self.assertEqual(rows, 2, 'execute_list 返回值不合格')

        rows = self.db.execute_list([
            ("insert into t_test_table(user_id, playlist_id, status) values(:1, :2, :3)", [20, 23, 'inactive']),
            ("insert into t_test_table(user_id, playlist_id, status) values(:user_id, :playlist_id, :status)",
             {'user_id': 29, 'status': 'active', 'playlist_id': 66})
        ], must_rows=True)
        self.assertEqual(rows, 2, 'execute_list 返回值不合格')

        result = self.db.select("SELECT * FROM t_test_table ")
        self.assertEqual(len(result), 4)

    def test_doc(self):
        # 每个变量都有文档
        logging.warning('函数文档 测试')
        functions = self.db.__all__
        # logging.warning(functions)
        for function in functions:
            if function.startswith('_'): continue
            self.assertTrue(bool(getattr(self.db, function).__doc__), '%s函数没有文档' % function)

    def test_format_sql(self):
        # 格式化字符串函数测试
        logging.warning('格式化字符串函数 测试')
        self.assertEqual(self.db.format_sql(',', None), '1=1')
        self.assertEqual(self.db.format_sql(',', {}), '1=1')
        self.assertEqual(self.db.format_sql(',', {'c': u"哈'哈"}), u'"C"=:c')
        self.assertTrue(self.db.format_sql(' AND ', {'a': u'a', 'b': 1, 'c': u"哈'哈"}) in (
            u'"A"=:a AND "C"=:c AND "B"=:b',  # py2 生成字符串的排序有点难理解
            u'"A"=:a AND "B"=:b AND "C"=:c',  # py3 生成字符串的排序经过优化
        ))
        self.assertTrue(self.db.add_sql('t_test_table', {'a': u'a', 'b': 1, 'c': u"哈'哈"}) in (
            'INSERT INTO "T_TEST_TABLE" ("A", "C", "B") VALUES (:a, :c, :b)',  # py2
            'INSERT INTO "T_TEST_TABLE" ("A", "B", "C") VALUES (:a, :b, :c)',  # py3
        ))

    def test_query_data(self):
        rows = self.db.execute("insert into t_test_table(user_id, playlist_id, status) values(30, 2233, 'inactive')")
        self.assertEqual(rows, 1)
        rows = self.db.execute("insert into t_test_table(user_id, playlist_id, status) values(31, 2233, 'inactive')")
        self.assertEqual(rows, 1)

        # query_data 测试
        logging.warning('query_data 测试')
        results = self.db.query_data('t_test_table', {"playlist_id": 2233})
        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].get('USER_ID') < results[1].get('USER_ID'))
        # 排序查询
        results2 = self.db.query_data('t_test_table', {"playlist_id": 2233}, 'user_id desc')
        self.assertEqual(len(results2), 2)
        self.assertTrue(results2[0].get('USER_ID') > results2[1].get('USER_ID'))

    def test_add_data(self):
        # add_data
        logging.warning('add_data 测试')
        # 添加单条
        rows = self.db.add_data('t_test_table', {'user_id': 40, "circle_code": "e'e''e", 'playlist_id': 331,
                                                 'last_use_time': datetime.datetime.now()})  # 参数含单引号
        self.assertEqual(rows, 1)
        result = self.db.query_data('t_test_table', {"circle_code": "e'e''e"})
        self.assertEqual(len(result), 1)

        # 添加多条
        rows = self.db.add_data('"t_test_table"', [
            {'user_id': 41, 'circle_code': "e'e''e", 'playlist_id': 332, 'last_use_time': datetime.datetime.now()},
            {'user_id': 42, 'circle_code': "e'e''e", 'playlist_id': 333, 'last_use_time': datetime.datetime.now()}])
        self.assertEqual(rows, 2)
        result = self.db.query_data('t_test_table', {"circle_code": "e'e''e"})
        self.assertEqual(len(result), 3)

    def test_add_datas(self):
        # add_datas (是 add_data 函数的多条执行模式)
        logging.warning('add_datas 测试')
        rows = self.db.add_datas(
            [('t_test_table', {'user_id': 51, "circle_code": "e'e''e", 'playlist_id': 221,
                               'update_date': datetime.datetime.now()}),
             ('t_test_table', {'user_id': 52, 'playlist_id': 443, 'circle_code': u"哎f'f''哈",
                               'update_date': datetime.datetime.now()})])
        self.assertEqual(rows, 2)

        result = self.db.query_data('t_test_table', {"circle_code": u"哎f'f''哈"})  # 中文参数+特殊符号
        self.assertEqual(len(result), 1)

    def test_update_data(self):
        rows = self.db.add_datas([
            ('t_test_table', {'user_id': 55, "circle_code": "e'e''e", 'playlist_id': 221,
                              'update_date': datetime.datetime.now()}),
            ('t_test_table', {'user_id': 56, 'playlist_id': 443, 'circle_code': u"哎f'f''哈",
                              'update_date': datetime.datetime.now()})
        ])
        self.assertEqual(rows, 2)
        result = self.db.query_data('t_test_table', {"playlist_id": 221})
        self.assertEqual(len(result), 1)
        data = result[0]
        self.assertEqual(data.get('STATUS'), 'active')
        self.assertEqual(data.get('CIRCLE_CODE'), "e'e''e")

        # update_data
        logging.warning('update_data 测试')
        rows = self.db.update_data('t_test_table', {'status': 'inactive', 'circle_code': "eee"}, {'playlist_id': 221})
        self.assertEqual(rows, 1)
        result = self.db.query_data('t_test_table', {"playlist_id": 221})
        self.assertEqual(len(result), 1)
        data = result[0]
        self.assertEqual(data.get('STATUS'), 'inactive')
        self.assertEqual(data.get('CIRCLE_CODE'), "eee")

        # update_data 条件与修改参数的字段名相同,区别度测试
        self.assertEqual(len(self.db.query_data('t_test_table', {"playlist_id": 1443})), 0)
        self.assertEqual(len(self.db.query_data('t_test_table', {"playlist_id": 443})), 1)
        rows = self.db.update_data('t_test_table', {'playlist_id': 1443}, {'playlist_id': 443})
        self.assertEqual(rows, 1)
        self.assertEqual(len(self.db.query_data('t_test_table', {"playlist_id": 1443})), 1)
        self.assertEqual(len(self.db.query_data('t_test_table', {"playlist_id": 443})), 0)

    def test_del_data(self):
        rows = self.db.add_data('t_test_table', {'user_id': 61, "circle_code": "e'e''e", 'playlist_id': 221,
                                                 'update_date': datetime.datetime.now()})
        self.assertEqual(rows, 1)
        result = self.db.query_data('t_test_table', {"playlist_id": 221})
        self.assertEqual(len(result), 1)
        # del_data
        logging.warning('del_data 测试')
        rows = self.db.del_data('t_test_table', {'playlist_id': 221})
        self.assertEqual(rows, 1)
        result = self.db.query_data('t_test_table', {"playlist_id": 221})
        self.assertEqual(len(result), 0)


class TestOracleAtom1(OracleToolsTest):
    db = None

    def setUp(self):
        u"""初始化"""
        self.class_name = self.__class__.__name__
        logging.info(u'%s 类的 %s 函数测试开始...', self.class_name, self._testMethodName)
        self.db = oracle_util.Atom()
        assert self.db.ping()

    def tearDown(self):
        u"""销毁"""
        logging.info(u'%s 类清空数据表,避免影响别的测试用例。。。', self.class_name)
        assert self.db.ping()
        self.db.execute("TRUNCATE TABLE t_test_table")
        result = self.db.select('select * from t_test_table')
        assert len(result) == 0

        self.db.dispose()
        self.db = None
        logging.info(u'%s 类的 %s 函数测试完毕。。。\r\n', self.class_name, self._testMethodName)

    def test_doc(self):
        # 每个变量都有文档
        logging.warning('Atom 文档 测试')
        functions = dir(oracle_util.Atom)
        # logging.warning(functions)
        for function in functions:
            if function.startswith('_'): continue
            # logging.warning("%s.__doc__: %s" % (function, getattr(oracle_util.Atom, function).__doc__))
            assert bool(getattr(oracle_util.Atom, function).__doc__)

    def test_threads(self):
        # 异步 测试
        logging.warning('Atom 异步测试, 此功能已去掉, 故无法测试')

    def test_rollback(self):
        logging.warning('Atom rollback 测试')
        # 插入一条
        rows = self.db.execute("insert into t_test_table(user_id, playlist_id, status) values(1101, 1, 'inactive')")
        assert rows == 1
        # 类内查询
        result = self.db.select('select * from t_test_table')
        assert len(result) == 1
        # 类外查询
        result = oracle_util.select('select * from t_test_table')
        assert len(result) == 0
        # 回滚
        self.db.rollback(dispose=False)
        # 类外查询
        result = oracle_util.select('select * from t_test_table')
        assert len(result) == 0

    def test_commit(self):
        logging.warning('Atom commit 测试')
        # 插入一条
        rows = self.db.execute("insert into t_test_table(user_id, playlist_id, status) values(:1, :2, :3)",
                               (1102, 1, 'inactive'))
        assert rows == 1
        # 类内查询
        result = self.db.select('select * from t_test_table where playlist_id=:1', 1)
        assert len(result) == 1
        # 类外查询
        result = oracle_util.select('select * from t_test_table where playlist_id=:playlist_id', {'playlist_id': 1})
        assert len(result) == 0
        # 提交
        self.db.commit(dispose=False)
        # 类外查询
        result = oracle_util.select('select * from t_test_table')
        assert len(result) == 1


class TestOracleAtom2(unittest.TestCase):
    # 原子操作类 Atom 的测试2:连接多个数据库
    def test_Atom2(self):
        fail = False
        try:
            mydb = oracle_util.Atom(**{
                'host': '127.1.1.3',
                'port': '1521',
                'user': 'root',
                'password': 'keepc@2014..',
                'sid': 'test',
            })
            assert mydb.ping()
        except:
            fail = True
            logging.warning('Atom连接不上,测试通过, 上面报错是必须的。。。')
        assert fail


if __name__ == "__main__":
    # 数据库配置
    DB_CONFIG = {
        'host': '127.0.0.1',
        'port': '1521',
        'user': 'system',
        'password': 'oracle',
        'sid': 'xe',  # 使用默认数据库空间 SYSTEM
    }

    test_init(DB_CONFIG)  # 数据库初始化连接、建表
    unittest.main()
    test_end()  # 删除表，避免遗留测试痕迹
