import pymysql.cursors
import os
from util.read_env import EnvironmentLoaderSingleton

class SetUp:
    def __init__(self):
        pass

    def run(self):
        self.__pre_check_db()

    def __pre_check_db(self):
        try:
            connection = pymysql.connect(host=EnvironmentLoaderSingleton().get_env().db_ip,
                                user='root',
                                password=EnvironmentLoaderSingleton().get_env().db_password,
                                db='mysql',
                                port=EnvironmentLoaderSingleton().get_env().db_port,
                                cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            raise RuntimeError('ERROR: step1:db connect failed: ' + str(e))
        
        try:
            with connection.cursor() as cursor:
                # 执行SQL语句，查询所有数据库名
                sql = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA"
                cursor.execute(sql)
                
                # 获取所有数据库名
                databases = [row['SCHEMA_NAME'] for row in cursor.fetchall()]
                
                if EnvironmentLoaderSingleton().get_env().db_name not in databases:
                    sql = "CREATE DATABASE " + EnvironmentLoaderSingleton().get_env().db_name
                    cursor.execute(sql)
                    print('crate database successfully')

        finally:
            connection.close()

        try:
            connection = pymysql.connect(host=EnvironmentLoaderSingleton().get_env().db_ip,
                                user='root',
                                password=EnvironmentLoaderSingleton().get_env().db_password,
                                db=EnvironmentLoaderSingleton().get_env().db_name,
                                port=EnvironmentLoaderSingleton().get_env().db_port,
                                cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            raise RuntimeError('ERROR: step2: db connect failed: ' + str(e))
        
        try:
            with connection.cursor() as cursor:
                # 执行SQL语句，查询所有数据库名
                sql = "SHOW TABLES"
                cursor.execute(sql)
                
                # 获取所有数据库名
                tables = [row[0] for row in cursor.fetchall()]
                
                if len(tables) == 0:
                    os.system("python3 manage.py makemigrations")
                    os.system("python3 manage.py migrate")
                    os.system("python3 manage.py init_super_user")
                    print("database create successfully!")

        finally:
            connection.close()
                
if __name__ == '__main__':
    SetUp().run()