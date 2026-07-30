# project_name/__init__.py
import pymysql

# 告诉Django使用pymysql替代默认的MySQLdb
pymysql.install_as_MySQLdb()

