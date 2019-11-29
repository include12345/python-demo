import json
import os
import traceback

import pymysql.cursors

from utils import loggerutils

logger = loggerutils.logger


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def connect_mysql():
    try:
        config = find("db_config.json", os.path.abspath("."))
        with open(config, "r") as file:
            load_dict = json.load(file)
        # cursorclass = pymysql.cursors.DictCursor
        return pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **load_dict)
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error("cannot create mysql connect")


def simple_list(rows):
    # 结果只有一列的情况，直接使用数据返回
    # :param rows: [{'id': 1}, {'id': 2}, {'id': 3}]
    # :return: [1, 2, 3]
    if not rows:
        return rows
    if len(rows[0].keys()) == 1:
        simples = []
        key = list(rows[0].keys())[0]
        for row in rows:
            simples.append(row[key])
        return simples
    return rows


def simple_value(row):
    # 结果集只有一行，一列的情况，直接返回数据
    # :param row: {'count(*)': 3}
    # :return: 3
    if not row:
        return None
    if len(row.keys()) == 1:
        key = list(row.keys())[0]
        return row[key]
    return row


def queryone(sql, param=None):
    # 返回结果集的第一条数据
    # :param sql: sql语句
    # :param param: string|tuple|list
    # :return: 字典列表 [{}]

    con = connect_mysql()
    cur = con.cursor()

    row = None
    try:
        cur.execute(sql, param)
        row = cur.fetchone()
    except Exception as e:
        con.rollback()
        logger.error(traceback.format_exc())
        logger.error("[sql]:{} [param]:{}".format(sql, param))
    cur.close()
    con.close()
    return simple_value(row)

def queryall(sql, param=None):
    """
      返回所有查询到的内容 (分页要在sql里写好)
    :param sql: sql语句
    :param param: tuple|list
    :return: 字典列表 [{},{},{}...] or [,,,]
    """


    con = connect_mysql()
    cur =con.cursor()
    rows = None
    try:
        cur.execute(sql, param)
        rows = cur.fetchall()
    except Exception as e:
        con.rollback()
        logger.error(traceback.format_exc())
        logger.error("[sql]:{} [param]:{}".format(sql, param))
    cur.close()
    con.close()
    return simple_list(rows)

def insertmany(sql, arrays=None):
    """
    批量插入数据
    :param sql:  sql语句
    :param arrays:  list|tuple[(),(),()...]
    :return: 入库数量
    """



    con = connect_mysql()
    cur = con.cursor()

    cnt = 0
    try:
        cnt = cur.executemany(sql, arrays)
        con.commit()
    except Exception as e:
        con.rollback()
        logger.error(traceback.format_exc())
        logger.error("[sql]:{} [param]:{}".format(sql, arrays))

    cur.close()
    con.close()
    return cnt

def insertone(sql, param=None):
    # 插入一条数据
    # :param sql: sql语句
    # :param param:  string |tuple
    # :return: id

    con = connect_mysql()
    cur = con.cursor()
    lastrowid = 0
    try:
        cur.execute(sql, param)
        con.commit()
        lastrowid = cur.lastrowid
    except Exception as e:
        con.rollback()
        logger.error(traceback.format_exc())
        logger.error("[sql]:{} [param]:{}".format(sql, param))

    cur.close()
    con.close()
    return lastrowid

def execute(sql, param=None):
    """
     执行sql语句：修改或删除
    :param sql: sql语句
    :param param: string|list
    :return: 影响数量
    """


    con = connect_mysql()
    cur = con.cursor()
    cnt = 0
    try:
        cnt = cur.execute(sql, param)
        con.commit()
    except Exception as e:
        con.rollback()
        logger.error(traceback.format_exc())
        logger.error("[sql]:{} [param]:{}".format(sql, param))

    cur.close()
    con.close()
    return cnt


if __name__ == '__main__':
    # 删表
    print("删表:", execute('drop table test_users'))
    #

    # # 建表
    # sql = '''CREATE TABLE `test_users` (
    #             `id` int(11) NOT NULL AUTO_INCREMENT,
    #             `username` VARCHAR(255) NOT NULL,
    #             `password` VARCHAR(255) NOT NULL,
    #             PRIMARY KEY (`id`)
    #             ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT="测试";
    #       '''
    # print("建表:", execute(sql))
    #
    # insertSql = "insert into test_users(username, password) values (%s, %s)"
    # arrays = [
    #     ("test1", "test1"),
    #     ("test2", "test2")
    # ]
    # print("插入数据:", insertmany(insertSql, arrays))








