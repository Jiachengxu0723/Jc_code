from pymysql import Mysql

# 初始化数据库对象
mysql = Mysql('localhost', 'root', 'byb123456', 'mysql')

# 连接
mysql.connect()

#sql语句
sql = ''

