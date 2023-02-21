"""
    python操作mysql进行增删查改
    1. 增删改，代码类似
    2. 查询

    代码分析
    (1)获取连接对象
    (2)sql语句不同，参数不同
    (3)获取执行对象
        增删改
        查询
            a.fetchone
            b.fetchall
    (4)处理结果
    (5)关闭
"""

import pymysql


class Mysql:
    """python操作MySQL的增删改查的封装"""

    def __init__(self, host, user, password, database, port=3306, charset='utf8'):
        """
        初始化参数
        Args:
            host:          主机
            user:          用户名
            password:      密码
            database:      数据库
            port:          端口号，默认为3306
            charset:       编码，默认是utf8
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset

    def connect(self):
        """
        获取连接对象和执行对象
        Returns:
        """
        self.conn = pymysql.connect(host=self.host, user=self.user,
                                    password=self.password, database=self.database,
                                    port=self.port, charset=self.charset)
        self.cur = self.conn.cursor()

    def fetchone(self, sql, params=None):
        """
        根据sql和params获取一行数据
        Args:
            sql:       sql语句
            params:    sql语句对象的参数元组，默认值为None

        Returns:       查询的一行数据
        """
        dataOne = None
        try:
            count = self.cur.execute(sql, params)
            if count != 0:
                dataOne = self.cur.fetchone()
        except Exception as ex:
            print(ex)
        finally:
            self.close()
        return dataOne

    def fetchall(self, sql, params=None):
        """
        根据sql和params获取符合条件的数据
        Args:
            sql:        sql语句
            params:     sql语句对象的参数列表，默认值为None

        Returns:        查询的符合条件的数据
        """
        dataAll = None
        try:
            count = self.cur.execute(sql, params)
            if count != 0:
                dataAll = self.cur.fetchall()
        except Exception as ex:
            print(ex)
        finally:
            self.close()
        return dataAll

    def __item(self, sql, params=None):
        """
        执行增删改
        Args:
            sql:        sql语句
            params:     sql语句对象的参数列表，默认值为None

        Returns:        受影响的行数
        """
        count = 0
        try:
            count = self.cur.execute(sql, params)
            self.conn.commit()  # 涉及写操作需要提交，且在连接对象上提交
        except Exception as ex:
            print(ex)
        finally:
            self.close()
        return count

    def update(self, sql, params=None):
        """
        修改操作
        Args:
            sql:      sql语句
            params:   sql语句对象的参数列表，默认值为None

        Returns:      受影响的行数
        """
        return self.__item(sql, params)

    def insert(self, sql, params=None):
        """
        新增操作
        Args:
            sql:      sql语句
            params:   sql语句对象的参数列表，默认值为None

        Returns:      受影响的行数
        """
        return self.__item(sql, params)

    def delete(self, sql, params=None):
        """
        删除操作
        Args:
            sql:      sql语句
            params:   sql语句对象的参数列表，默认值为None

        Returns:      受影响的行数
        """
        return self.__item(sql, params)

    def close(self):
        """
        关闭执行工具和连接对象
        Returns:
        """
        if self.cur != None:
            self.cur.close()
        if self.conn != None:
            self.conn.close()
