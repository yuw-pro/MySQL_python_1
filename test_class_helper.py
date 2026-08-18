from SQL_helper import MySQLHelper
import os
from dotenv import load_dotenv
load_dotenv()

db_test = MySQLHelper()
db_test_connection = db_test.connect()
assert db_test_connection.is_connected(), "Failed to connect"
rows = db_test.query_all("students")
assert isinstance(rows, list), "query_all should return a list"
db_test.close_connection()
