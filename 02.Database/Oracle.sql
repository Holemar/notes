创建表(Create table)语法
1. ORACLE 常用的字段类型
    VARCHAR2(size) 可变长度的字符串, 必须规定长度
    CHAR(size) 固定长度的字符串, 不规定长度默认值为１
    NUMBER(p,s) 数字型p是位数总长度, s是小数的长度, 可存负数。最长38位. 不够位时会四舍五入.
    DATE 日期和时间类型
    LOB 超长字符, 最大可达4G
    CLOB 超长文本字符串
    BLOB 超长二进制字符串
    BFILE 超长二进制字符串, 保存在数据库外的文件里是只读的.

    范例：数字字段类型位数及其四舍五入的结果
        原始数值 1234567.89
        数字字段类型位数 存储的值
        Number 1234567.89
        Number(8) 1234568
        Number(6) 错
        Number(9,1) 1234567.9
        Number(9,3) 错
        Number(7,2) 错
        Number(5,-2) 1234600
        Number(5,-4) 1230000
        Number(*,1) 1234567.9

2. 创建表时给字段加默认值 和约束条件
    例如 : 日期字段 DEFAULT SYSDATE
    这样每次插入和修改时, 不用程序操作这个字段都能得到动作的时间

    创建表时可以给字段加上约束条件
    例如: 非空 NOT NULL
    不允许重复 UNIQUE
    主键 PRIMARY KEY
    按条件检查 CHECK (条件)
    外键 REFERENCES 表名(字段名)

3. 创建表的例子
    CREATE TABLE DEPT (
        EPTNO NUMBER(2) CONSTRAINT PK_DEPT PRIMARY KEY,
        DNAME VARCHAR2(14),
        LOC VARCHAR2(13)
    );
    CREATE TABLE region(
        ID number(2) NOT NULL PRIMARY KEY,
        postcode number(6) default '0' NOT NULL,
        areaname varchar2(30) default ' ' NOT NULL
    );

4. 创建表时的命名规则和注意事项
    1)表名和字段名的命名规则：必须以字母开头，可以含符号A-Z,a-z,0-9,_,$,#
    2)大小写不区分
    3)不用SQL里的保留字, 一定要用时可用双引号把字符串括起来．
    4)用和实体或属性相关的英文符号长度有一定的限制

    注意事项:
    1)建表时可以用中文的字段名, 但最好还是用英文的字段名
    2)创建表时要把较小的不为空的字段放在前面, 可能为空的字段放在后面
    3)建表时如果有唯一关键字或者唯一的约束条件，建表时自动建了索引
    4)一个表的最多字段个数也是有限制的，254个.

5. 约束名的命名规则和语法
    约束名的命名规则约束名如果在建表的时候没有指明，系统命名规则是SYS_Cn(n是数字)
    约束名字符串的命名规则同于表和字段名的命名规则

6. 使用约束时的注意事项
    约束里不能用系统函数,如SYSDATE和别的表的字段比较
    可以用本表内字段的比较
    想在事务处理后, 做约束的

    检查
    SQL> alter session set constraints deferred.

7. 由实体关系图到创建表的例子 s_dept
    前提条件:已有region表且含唯一关键字的字段id
    SQL> CREATE TABLE s_dept (
        id NUMBER(7) CONSTRAINT s_dept_id_pk PRIMARY KEY,
        name VARCHAR2(25) CONSTRAINT s_dept_name_nn NOT NULL,
        region_id NUMBER(7)
        CONSTRAINT s_dept_region_id_fk REFERENCES region (id),
        CONSTRAINT s_dept_name_region_id_uk UNIQUE(name, region_id)
    );

8. 较复杂的创建表例子
    SQL> CREATE TABLE s_emp (
        id NUMBER(7) CONSTRAINT s_emp_id_pk PRIMARY KEY,
        last_name VARCHAR2(25) CONSTRAINT s_emp_last_name_nn NOT NULL,
        first_name VARCHAR2(25),
        userid VARCHAR2(8) 
            CONSTRAINT s_emp_userid_nn NOT NULL
            CONSTRAINT s_emp_userid_uk UNIQUE,
        start_date DATE DEFAULT SYSDATE,
        comments VARCHAR2(25),
        manager_id NUMBER(7),
        title VARCHAR2(25),
        dept_id NUMBER(7) CONSTRAINT s_emp_dept_id_fk REFERENCES s_dept(id),
        salary NUMBER(11,2),
        commission_pct NUMBER(4,2) CONSTRAINT s_emp_commission_pct_ck CHECK (commission_pct IN(10,12.5,15,17.5,20))
    );

9. 通过子查询建表
    通过子查询建表的例子
    SQL> CREATE TABLE emp_41 AS SELECT id, last_name, userid, start_date FROM s_emp WHERE dept_id = 41;
    SQL> CREATE TABLE A as select * from B where 1=2; -- 只建表，不插入数据，所以 where 条件为永恒的 false

10. 用子查询建表的注意事项
    1)可以关连多个表及用集合函数生成新表,注意选择出来的字段必须有合法的字段名称,且不能重复。
    2)用子查询方式建立的表，只有非空 NOT NULL 的约束条件能继承过来, 其它的约束条件和默认值都没有继承过来.
    3)根据需要，可以用 alter table add constraint ……再建立其它的约束条件，如 primary key 等.

11. Foreign Key 的可选参数 ON DELETE CASCADE
    在创建 Foreign Key 时可以加可选参数:
    ON DELETE CASCADE 它的含义是如果删除外键主表里的内容，子表里相关的内容将一起被删除.
    如果没有 ON DELETE CASCADE 参数，子表里有内容，父表里的主关键字记录不能被删除掉.

12. 如果数据库表里有不满足的记录存在，建立约束条件将不会成功.

13. 给表创建和删除同义词的例子
    SQL> CREATE SYNONYM d_sum
    2 FOR dept_sum_vu;
    SQL> CREATE PUBLIC SYNONYM s_dept
    2 FOR alice.s_dept;
    SQL> DROP SYNONYM s_dept;

14.范例
    CREATE TABLE banping (
        id NUMBER(5) CONSTRAINT banping_id_pk PRIMARY KEY,
        last_name VARCHAR2(10) CONSTRAINT banping_last_name_nn NOT NULL,
        first_name VARCHAR2(10) NOT NULL UNIQUE,
        userid VARCHAR2(8) CONSTRAINT banping_userid_uk UNIQUE,  
        start_date DATE DEFAULT SYSDATE,
        title VARCHAR2(10),
        dept_id NUMBER(7) CONSTRAINT banping_dept_id_fk REFERENCES dept(id),
        salary NUMBER(11,2),
        user_type VARCHAR2(4) CONSTRAINT banping_user_type_ck CHECK (user_type IN('IN','OUT')),
        CONSTRAINT banping_uk_title UNIQUE (title,salary)  
    )
    INITRANS 1 MAXTRANS 255
    PCTFREE 20 PCTUSED 50
    STORAGE(INITIAL 1024K NEXT 1024K PCTINCREASE 0 MINEXTENTS 1 MAXEXTENTS 5)
    TABLESPACE data;  

    语法说明如下：
        [sql]
        CREATE TABLE [schema.]table
        (column datatype [, column datatype] … )
        [TABLESPACE tablespace]
        [PCTFREE integer]
        [PCTUSED integer]
        [INITRANS integer]
        [MAXTRANS integer]
        [STORAGE storage-clause]
        [LOGGING | NOLOGGING]
        [CACHE | NOCACHE] ];

    Schema：表的所有者
    Table：表名
    Column：字段名
    Datatype：字段的数据类型
    Tablespace：表所在的表空间
    Pctfree：为了行长度增长而在每个块中保留的空间的量（以占整个空间减去块头部后所剩余空间的百分比形式表示），当剩余空间不足pctfree时，不再向该块中增加新行。
    Pctused：在块剩余空间不足pctfree后，块已使用空间百分比必须小于pctused后，才能向该块中增加新行。
    INITRANS：在块中预先分配的事务项数，缺省值为1
    MAXTRANS：限定可以分配给每个块的最大事务项数，缺省值为255
    STORAGE：标识决定如何将区分配给表的存储子句
    LOGGING：指定表的创建将记录到重做日志文件中。它还指定所有针对该表的后续操作都将被记录下来。这是缺省设置。
    NOLOGGING：指定表的创建将不被记录到重做日志文件中。
    CACHE：指定即使在执行全表扫描时，为该表检索的块也将放置在缓冲区高速缓存的LRU列表最近使用的一端。
    NOCACHE：指定在执行全表扫描时，为该表检索的块将放置在缓冲区高速缓存的LRU列表最近未使用的一端。
    STORAGE子句：
    INITIAL：初始区的大小
    NEXT：下一个区的大小
    PCTINCREASE：以后每个区空间增长的百分比
    MINEXTENTS：段中初始区的数量
    MAXEXTENTS：最大能扩展的区数
     如果已为表空间定义了MINIMUM EXTENT，则表的区大小将向上舍入为MINIMUM EXTENT值的下一个较高的倍数。
    外键关联的表dept的id列必须是唯一的或者是自身的主键，如不是可以用以下语句填加：
    [sql] 
    alter table dept  add constraint dept_id_pk primary key(id);  
    块空间使用参数可用来控制对数据段和索引段空间的使用：
    控制并发性参数：
    INITRANS和MAXTRANS指定初始的和最大的事务位置数，这些事务位置在索引块或者数据块内创建。事务位置用来存储在某一事件点上正在对块进行更改的事务的信息。一个事务只占用一个事务位置，即使它正在更改多行或者多个索引条目。 INITRANS对数据段的缺省值为1，对索引段的缺省值为2，以保证最低程度的并发。例如，如果INITRANS设为3，则保证至少3个事务可以同时对块进行更改。如果需要，也可以从块空闲空间内分配其它事务位置，以允许更多的事务并发修改块内的行。 MAXTRANS的缺省值为255，它设置可更改数据块或者索引块的并发事务数的限制。设置后，该值限制事务位置对空间的使用，从而保证块内有足够的空间供行或者索引数据使用。
    控制数据空间使用的参数：
    数据段的PCTFREE指定每个数据块中保留空间的百分比，用于因更新块内的行而导致的增长。PCTFREE的缺省值为10%。 数据段的PCTUSED代表Oracle服务器试图为表内的每个数据块维持的已用空间的最低百分比。如果一个块的已用空间低于PCTUSED，则将这块放回到空闲列表中。段的空闲列表示容纳将来所插入内容的可选择块的列表。根据缺省，每个段在创建时都有一个空闲列表。PCTUSED的缺省值为40%。 PCTFREE和PCTUSED都按可用数据空间百分比来计算，可用数据空间是从整个块大小减去块头空间后剩余的块空间。 块空间使用参数只能针对段指定，而不能在表空间级别设置。
    下面步骤介绍对PCTFREE=20且PCTUSED=40的数据段如何管理块内空间：
    1.向块中插入行，直到块内的空闲空间小等于20%。当行所占用的块内数据空间达到80%（100-PCTFREE）或者更多后，即无法再向该块进行插入。
    2.剩余的20%可在行大小增长时使用。例如，更新初始为NULL的列并分配一个值。这样，由于更新，块使用率可能超过80%。
    3.如果由于更新，删除了块内的行或者行大小减少，块使用率可能跌至80%以下。但是，仍然无法向块中插入，直到块使用率跌至PCTUSED以下，在本例中PCTUSED为40%。
    4.当块使用率跌至PCTUSED以下后，该块可用于插入。随着向块内插入行，块使用率增长，重复从步骤1开始的循环。

15.注释
    建表语句:
    CREATE table "TABLE_COUNT" (
       "TABLE_NAME"     varchar2(40 char) not null enable,
       "COUNT"          varchar2(40 char) not null enable,
       "DESCRIPTION"    varchar2(40 char) not null enable,
       "FLAG"           varchar2(40 char) not null enable,
       "CREATE_DATE"    varchar2(40 char) not null enable,
       PRIMARY KEY ("TABLE_NAME","CREATE_DATE")
    );
    comment on table "ZX_COUNT" is '每天产生的业务条数';
    comment on column  "ZX_COUNT"."TABLE_NAME"  is '表名';
    comment on column  "ZX_COUNT"."COUNT"       is '发生条数';
    comment on column  "ZX_COUNT"."DESCRIPTION" is '说明';
    comment on column  "ZX_COUNT"."FLAG"        is '类型标记';
    comment on column  "ZX_COUNT"."CREATE_DATE" is '业务发生日期';
    commit;

    查询语句：
    select *from user_tab_comments where table_name='TABLE_COUNT'; -- 表注释
    select *from user_col_comments where table_name='TABLE_COUNT'; -- 字段注释

    -- 反查建表语句
    SELECT DBMS_METADATA.GET_DDL('TABLE','T_TEST_TABLE') FROM DUAL;

    -- 获取T_POL_CUSTOMER_NEW表的字段名、字段类型、默认值、是否允许为空、字段说明
    select t1.column_name,data_type,data_default,nullable,comments from (
        select table_name,column_name,data_type,data_default,nullable from user_tab_cols where Table_Name='HW_TALENT_RESUME_T'
        ) t1 RIGHT JOIN (
                select column_name,comments from user_col_comments where Table_Name='HW_TALENT_RESUME_T'
        ) t2 on t1.column_name=t2.column_name;

    select t.column_name,t.data_type,t.data_length,t.nullable,t.column_id,c.comments, 
         (SELECT CASE WHEN t.column_name=m.column_name THEN 1 ELSE 0 END FROM DUAL) iskey
         FROM user_tab_cols t, user_col_comments c, (select m.column_name from user_constraints s, user_cons_columns m 
                     where lower(m.table_name)=lower('HW_TALENT_RESUME_T') and m.table_name=s.table_name
                     and m.constraint_name=s.constraint_name and s.constraint_type='P') m
         WHERE lower(t.table_name)=lower('HW_TALENT_RESUME_T')
                     and c.table_name=t.table_name and c.column_name=t.column_name and t.hidden_column='NO' 
     order by t.column_id;


日期转换
    to_date ( '2007-12-20 18:31:34' , 'YYYY-MM-DD HH24:MI:SS' )
    to_date ( '2007-11-15' , 'YYYY-MM-DD' )


ORACLE 分页查询 SQL 语法

    提升效率的关键，是尽可能减少最底层查询的数据量。
    第一种写法将 ROWNUM 写到最底层查询条件中，效率最高。
    有 ORDER BY 之后没法再将 ROWNUM 写到最底层查询条件里面，使用 HAVING 也不行，所以得多包一层，降低了查询效率。
    注意： ROWNUM 从 1 开始递增。

    1:无 ORDER BY 排序的写法。(效率最高)
      -- (经过测试，此方法成本最低，只嵌套一层，速度最快！即使查询的数据量再大，也几乎不受影响，速度依然！)
        SELECT *
          FROM (SELECT ROWNUM AS rowno, t.* FROM emp t
                WHERE hire_date BETWEEN TO_DATE ('20060501', 'yyyymmdd') AND TO_DATE ('20060731', 'yyyymmdd')
                AND ROWNUM <= 20) table_alias
         WHERE table_alias.rowno >= 11;

    2:有 ORDER BY 排序的写法。(效率最高)
        -- (经过测试，此方法随着查询范围的扩大，速度也会越来越慢哦！)
        SELECT *
          FROM (SELECT tt.*, ROWNUM AS rowno
                  FROM (  SELECT t.* FROM emp t
                          WHERE hire_date BETWEEN TO_DATE ('20060501', 'yyyymmdd') AND TO_DATE ('20060731', 'yyyymmdd')
                          ORDER BY create_time DESC, emp_no) tt
                 WHERE ROWNUM <= 20) table_alias
         WHERE table_alias.rowno >= 11;

        -- (经过测试，此方法也可行，但速度未经测试！嵌套只有一层，估计不会慢)
        SELECT *
            FROM (SELECT ROWNUM AS rowno, t.* FROM HW_TALENT_RESUME_T t
                 WHERE LAST_UPDATE_DATE >= TO_DATE ('2019-08-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                 ORDER BY LAST_UPDATE_DATE) table_alias
         WHERE table_alias.rowno between 11 and 20;

    =================================================================================
    =======================垃圾但又似乎很常用的分页写法==========================
    =================================================================================
    3:无 ORDER BY 排序的写法。(建议使用方法1代替)
        -- (此方法随着查询数据量的扩张，速度会越来越慢哦！)
        SELECT *
          FROM (SELECT ROWNUM AS rowno, t.* FROM k_task t
                 WHERE flight_date BETWEEN TO_DATE ('20060501', 'yyyymmdd') AND TO_DATE ('20060731', 'yyyymmdd')) table_alias
         WHERE table_alias.rowno <= 20 AND table_alias.rowno >= 11;
         -- WHERE TABLE_ALIAS.ROWNO  between 10 and 100;

    4:有 ORDER BY 排序的写法.(建议使用方法2代替)
        -- (此方法随着查询范围的扩大，速度会越来越慢哦！)
        SELECT *
          FROM (SELECT tt.*, ROWNUM AS rowno
                  FROM (  SELECT * FROM k_task t
                           WHERE flight_date BETWEEN TO_DATE ('20060501', 'yyyymmdd') AND TO_DATE ('20060531', 'yyyymmdd')
                        ORDER BY fact_up_time, flight_no) tt) table_alias
         WHERE table_alias.rowno BETWEEN 11 AND 20;


    5:另类语法。(有 ORDER BY 写法）
        -- (语法风格与传统的SQL语法不同，不方便阅读与理解，为规范与统一标准，不推荐使用。)
        WITH partdata AS
             ( SELECT ROWNUM AS rowno, tt.*
                  FROM (  SELECT * FROM k_task t
                           WHERE flight_date BETWEEN TO_DATE ('20060501', 'yyyymmdd') AND TO_DATE ('20060531', 'yyyymmdd')
                        ORDER BY fact_up_time, flight_no) tt
                 WHERE ROWNUM <= 20)
        SELECT *
          FROM partdata
         WHERE rowno >= 11;

    6:另类语法。(无 ORDER BY 写法）
        WITH partdata AS
             ( SELECT ROWNUM AS rowno, t.*
                  FROM k_task t
                 WHERE flight_date BETWEEN TO_DATE ('20060501', 'yyyymmdd') AND TO_DATE ('20060531', 'yyyymmdd')
                   AND ROWNUM <= 20)
        SELECT *
          FROM partdata
         WHERE rowno >= 11;
 

oracle 自增主键
    -- 建表 (主键不会自动自增)
    CREATE TABLE t_test_table(
        user_id int PRIMARY KEY NOT NULL, -- 主键
        playlist_id NUMBER(10) default 0 NOT NULL,
        value NUMBER(10, 2) default 4 NOT NULL,
        circle_code VARCHAR2(8) default '-' NOT NULL,
        status VARCHAR2(10) default 'active' CHECK( status IN ('active','inactive') ),
        last_use_time DATE DEFAULT sysdate NOT NULL,
        update_date DATE default sysdate NOT NULL
    );
    -- 自增主键 = SEQUENCE + 触发器

    -- 建 sequence
    create sequence s_test_table increment by 1 start with 1 nomaxvalue nocycle cache 20;

    -- 建 触发器
    CREATE OR REPLACE TRIGGER TRIGGER_test_table_ID
     BEFORE INSERT ON t_test_table
     FOR EACH ROW --对表的每一行触发器执行一次
     DECLARE NEXT_ID NUMBER;
    BEGIN
     SELECT s_test_table.NEXTVAL INTO NEXT_ID FROM DUAL;
     :NEW.user_id := NEXT_ID; --:NEW表示新插入的那条记录
    END;

    -- 插入数据
    insert into t_test_table(value,circle_code) VALUES (55.32, 'aaaa');
    insert into t_test_table(value,circle_code) VALUES (22.1, 'bbb');
    -- 看看效果
    SELECT * from t_test_table;

    -- 删除测试表及SEQUENCE、触发器
    drop trigger TRIGGER_test_table_ID;
    drop SEQUENCE s_test_table;
    drop table t_test_table;

