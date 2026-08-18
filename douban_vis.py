from SQL_helper import MySQLHelper
import pandas as pd

data_sql = MySQLHelper(database='douban')
connection = data_sql.connect()
df = pd.read_sql('select * from douban_films', con=connection)
print(df.head())
print(df["title"])
print(df[["title", "rating"]])

# EDA 1.完整性 2.分布 3.关联 4.异常值
print('===数据形状===\n', df.shape)
print('===数据信息===\n', df.info())
print('===数据描述===\n', df.describe())
print('===缺失值===\n', df.isnull().sum())