import pymysql
from dbutils.pooled_db import PooledDB
from pymysql.cursors import DictCursor
from threading import Lock


class DBPool:
    """
    带参数的sql语句，需要使用占位符(%s, %d, ...)占位，param参数应是列表或者元组
    """
    _instance_dict = dict()
    lock = Lock()

    def __new__(cls, *args, **kwargs):
        """利用__new__实现单例"""
        key = ''
        for item in args:
            key += str(item)
        for item in kwargs.values():
            key += str(item)

        with cls.lock:
            if key in cls._instance_dict:
                return cls._instance_dict[key]
            cls._instance_dict[key] = super(DBPool, cls).__new__(cls)

            return cls._instance_dict[key]

    def __init__(self, host, port, user, password, db=None, mincached=5, maxcached=50):
        # 如果有 pool 属性，表示当前对象是之前实例化好的，就不需要在进行初始化了
        if not hasattr(self, "pool"):
            self.pool = PooledDB(creator=pymysql,  # 指明创建链接的模块
                                 mincached=mincached,  # 池中最小保持的连接数
                                 maxcached=maxcached,  # 池中最多存在的连接数
                                 ping=0,  # 不主动 ping
                                 host=host,
                                 port=port,
                                 user=user,
                                 passwd=password,
                                 db=db,
                                 use_unicode=False,
                                 charset="utf8",
                                 cursorclass=DictCursor  # fetch的结果 由默认的元组，改成字典形式
                                 )

    def get_cursor(self):
        conn = self.pool.connection()
        cursor = conn.cursor()
        return conn, cursor

    def close_cursor(self, conn, cursor):
        cursor.close()
        conn.close()

    def query_many(self, sql, param=None, size=None):
        """
        执行查询，并取出多条结果集
        @param sql:查询SQL，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @param size: 查询条数
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        conn, cursor = self.get_cursor()
        if param:
            count = cursor.execute(sql, param)
        else:
            count = cursor.execute(sql)

        if count > 0:
            if size:
                result = cursor.fetchmany(size)
            else:
                result = cursor.fetchall()
        else:
            result = False

        self.close_cursor(conn, cursor)
        return result

    def query_one(self, sql, param=None):
        """
        执行查询，并取出第一条
        @param sql:查询SQL，如果有查询条件，请指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        conn, cursor = self.get_cursor()
        if param:
            count = cursor.execute(sql, param)
        else:
            count = cursor.execute(sql)

        if count > 0:
            result = cursor.fetchone()
        else:
            result = False

        self.close_cursor(conn, cursor)
        return result

    def execute_many(self, sql, values):
        """
        增删改操作多条数据
        @param sql:要插入的SQL格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        conn, cursor = self.get_cursor()
        try:
            count = cursor.executemany(sql, values)
            conn.commit()
        except Exception:
            conn.rollback()
            count = False

        self.close_cursor(conn, cursor)
        return count

    def execute_one(self, sql, param=None):
        """
        增删改操作单条数据
        @param sql:要插入的SQL格式
        @param param:要插入的记录数据tuple/list
        @return: count 受影响的行数
        """
        conn, cursor = self.get_cursor()

        try:
            if param:
                count = cursor.execute(sql, param)
            else:
                count = cursor.execute(sql)
            conn.commit()
        except Exception:
            conn.rollback()
            count = False

        self.close_cursor(conn, cursor)
        return count
